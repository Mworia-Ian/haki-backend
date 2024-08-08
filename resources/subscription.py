from flask import request, jsonify,make_response
from flask_restful import Resource
from models import db, Subscription
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

class SubscriptionResource(Resource):
    @jwt_required()
    def get(self, subscription_id):
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404
        
        return jsonify(subscription.to_dict())

    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()

        # Check if the user already has an active subscription
        active_subscription = Subscription.query.filter_by(user_id=user_id, payment_status='Paid').first()
        if active_subscription:
            return {'message': 'User already has an active subscription'}, 400

        # Verify payment status
        if data.get('payment_status') != 'Paid':
            return {'message': 'Payment not verified'}, 400

        # Create a new subscription
        new_subscription = Subscription(
            user_id=user_id,
            payment_status=data['payment_status'],
            start_date=datetime.now(),
            end_date=datetime.now()
        )

        db.session.add(new_subscription)
        db.session.commit()

        return make_response(jsonify(new_subscription.to_dict()), 201)

    @jwt_required()
    def put(self, subscription_id):
        data = request.get_json()
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404

        # Update fields
        subscription.payment_status = data.get('payment_status', subscription.payment_status)
        subscription.start_date = data.get('start_date', subscription.start_date)
        subscription.end_date = data.get('end_date', subscription.end_date)

        db.session.commit()

        return jsonify(subscription.to_dict())

    @jwt_required()
    def delete(self, subscription_id):
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404
        
        db.session.delete(subscription)
        db.session.commit()
        
        return {'message': 'Subscription deleted successfully'}, 200