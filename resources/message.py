from flask import request, jsonify
from flask_restful import Resource
from models import db, Message
from flask_jwt_extended import jwt_required

class MessageResource(Resource):
    @jwt_required()
    def get(self, message_id):
        message = Message.query.get(message_id)
        if not message:
            return {'message': 'Message not found'}, 404
        
        return jsonify(message.to_dict())

    @jwt_required()
    def delete(self, message_id):
        message = Message.query.get(message_id)
        if not message:
            return {'message': 'Message not found'}, 404
        
        db.session.delete(message)
        db.session.commit()
        
        return {'message': 'Message deleted successfully'}, 200
