from flask import request, jsonify
from flask_restful import Resource
from models import db, Payment
from flask_jwt_extended import jwt_required

class PaymentResource(Resource):
    @jwt_required()
    def get(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        return jsonify(payment.to_dict())

    @jwt_required()
    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return {'message': 'Payment not found'}, 404
        
        db.session.delete(payment)
        db.session.commit()
        
        return {'message': 'Payment deleted successfully'}, 200
