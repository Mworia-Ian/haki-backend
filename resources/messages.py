from firebase_admin import firestore

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize Firestore
db_firestore = firestore.client()

class MessageResource(Resource):
    @jwt_required()
    def post(self):
        pass

    @jwt_required()
    def get(self):
        pass

    @jwt_required()
    def delete(self, message_id):
        pass