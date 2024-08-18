from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import Message, User, db
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime
import redis
from redis_client import redis_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()

        receiver_id = data.get('receiver_id')
        message_text = data.get('message')
        reply_to = data.get('reply_to')  # Get reply_to from request data

        # Check if receiver_id and message_text are provided
        if not receiver_id or not message_text:
            logger.warning(f"Missing fields - receiver_id: {receiver_id}, message: {message_text}")
            return {'message': 'Receiver ID and message are required'}, 400

        # Retrieve sender and receiver from database
        sender = User.query.get(current_user_id)
        receiver = User.query.get(receiver_id)

        # Log details for debugging
        logger.info(f"Sender ID: {current_user_id}, Receiver ID: {receiver_id}")

        if not sender:
            return {'message': 'Sender does not exist'}, 404
        if not receiver:
            return {'message': 'Receiver does not exist'}, 404

        # Create new message
        new_message = Message(
            user_id=current_user_id,
            message=message_text,
            sender_id=current_user_id,
            receiver_id=receiver_id,
            date=datetime.utcnow(),
            reply_to=reply_to  # Set reply_to
        )

        try:
            self.save_message_to_db(new_message)
            self.save_message_to_redis(current_user_id, receiver_id, message_text, new_message.date)
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database error: {e}")
            return {'message': 'Database error occurred'}, 500
        except Exception as e:
            logger.error(f"Internal server error: {e}")
            return {'message': 'Internal server error'}, 500

        return {'message': 'Message sent successfully'}, 201

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        messages = Message.query.filter(
            (Message.sender_id == current_user_id) | (Message.receiver_id == current_user_id)
        ).all()

        return [{'id': msg.id, 'message': msg.message, 'date': msg.date.isoformat(), 'reply_to': msg.reply_to} for msg in messages], 200

    @jwt_required()
    def delete(self, message_id):
        current_user_id = get_jwt_identity()
        message = Message.query.get(message_id)

        if not message:
            return {'message': 'Message not found'}, 404
        if message.sender_id != current_user_id and message.receiver_id != current_user_id:
            return {'message': 'Not authorized to delete this message'}, 403

        try:
            db.session.delete(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Internal server error while deleting message: {e}")
            return {'message': 'Internal server error'}, 500

        logger.info(f"Message with ID {message_id} deleted by user {current_user_id}")
        return {'message': 'Message deleted successfully'}, 200

    def save_message_to_db(self, message):
        try:
            db.session.add(message)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Database IntegrityError: {e}")
            raise

    def save_message_to_redis(self, sender_id, receiver_id, message_text, date):
        message_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'date': date.isoformat()  
        }
        try:
            redis_client.xadd('messages', message_data)
        except Exception as e:
            logger.error(f"Redis error: {e}")
