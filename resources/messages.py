from firebase_admin import firestore

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import Message, db
# Initialize Firestore
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

        # Create a new message instance
        new_message = Message(
            user_id=current_user_id,
            message=message_text,
            sender_id=current_user_id,
            receiver_id=receiver_id
        )

        # Save to SQL database
        db.session.add(new_message)
        db.session.commit()

        # Save to Firestore for real-time messaging
        message_data = {
            'sender_id': current_user_id,
            'receiver_id': receiver_id,
            'message': message_text,
            'date': new_message.date
        }

        db_firestore.collection('messages').add(message_data)

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
        pass