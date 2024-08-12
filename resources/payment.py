from flask import jsonify
from flask_restful import Resource
from models import Payment
from flask_jwt_extended import jwt_required

class PaymentStatusResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        payment = Payment.query.filter_by(transaction_id=transaction_id).first()
        if not payment:
            return jsonify({'error': 'Transaction not found'}), 404

        return jsonify({'status': payment.status})
