from flask import jsonify,make_response
from flask_restful import Resource
from models import Payment
from flask_jwt_extended import jwt_required

class PaymentStatusResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        payment = Payment.query.filter_by(transaction_id=transaction_id).first()
        if payment:
            return make_response(jsonify({'status': payment.status}), 200)
        else:
            return make_response(jsonify({'error': 'Payment not found'}), 404)
