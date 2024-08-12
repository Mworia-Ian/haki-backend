from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import Message, User, db
from sqlalchemy.exc import IntegrityError
import firebase_admin
from firebase_admin import firestore, credentials

# Initialize Firestore
cred = credentials.Certificate('assets/haki-ed7c8-firebase-adminsdk-p5g92-aaf3880795.json')
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

class MessageResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # Validate input data
        if not all(k in data for k in ('receiver_id', 'message')):
            return {'message': 'Missing fields'}, 400

        receiver_id = data['receiver_id']
        message_text = data['message']

        # Check if the current user and receiver exist in the users table
        sender = User.query.get(current_user_id)
        receiver = User.query.get(receiver_id)

        if not sender:
            return {'message': 'Sender does not exist'}, 404
        if not receiver:
            return {'message': 'Receiver does not exist'}, 404

        # Create a new message instance
        new_message = Message(
            user_id=current_user_id,
            message=message_text,
            sender_id=current_user_id,
            receiver_id=receiver_id
        )

        try:
            self.save_message_to_db(new_message)
            self.save_message_to_firestore(current_user_id, receiver_id, message_text, new_message.date)
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Database error occurred'}, 500
        except Exception as e:
            return {'message': 'Internal server error'}, 500

        return {'message': 'Message sent successfully'}, 201

    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        messages = Message.query.filter(
            (Message.sender_id == current_user_id) | (Message.receiver_id == current_user_id)
        ).all()

        return [{'id': msg.id, 'message': msg.message, 'date': msg.date} for msg in messages], 200

    @jwt_required()
    def delete(self, message_id):
        current_user_id = get_jwt_identity()
        message = Message.query.get(message_id)

        if message is None or (message.sender_id != current_user_id and message.receiver_id != current_user_id):
            return {'message': 'Message not found or not authorized to delete'}, 404

        try:
            db.session.delete(message)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Internal server error'}, 500

        return {'message': 'Message deleted successfully'}, 200

    def save_message_to_db(self, message):
        db.session.add(message)
        db.session.commit()

    def save_message_to_firestore(self, sender_id, receiver_id, message_text, date):
        message_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'date': date
        }
        db_firestore.collection('messages').add(message_data)