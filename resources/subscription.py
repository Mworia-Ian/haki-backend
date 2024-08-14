from flask import request, jsonify, make_response
from flask_restful import Resource
from models import db, Subscription, Payment
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

class SubscriptionResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        subscription = Subscription.query.filter_by(user_id=user_id, active=False).first()
        
        # Debugging: Log the fetched subscription
        print(f"Fetched subscription: {subscription}")

        if subscription:
            print(subscription)
            return {
                'id': subscription.id,
                'user_id': subscription.user_id,
                'payment_status': subscription.payment_status,
                'start_date': subscription.start_date.isoformat(),
                'end_date': subscription.end_date.isoformat(),
                'active': subscription.active
            }, 200
        else:
            return {'message': 'No active subscription found.'}, 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()

        # Debugging: Log incoming data
        print(f"Post data received: {data}")

        # Check if the user already has an active subscription
        active_subscription = Subscription.query.filter_by(user_id=user_id, active=True).first()
        if active_subscription:
            return {'message': 'User already has an active subscription'}, 400

        # Verify payment status
        payment_status = data.get('payment_status')
        if payment_status != 'Paid':
            return {'message': 'Payment not verified'}, 400

        # Calculate end_date (e.g., 1 month from now)
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=30)

        # Create a new subscription
        new_subscription = Subscription(
            user_id=user_id,
            payment_status=payment_status,
            start_date=start_date,
            end_date=end_date,
            amount=data.get('amount', 0),
            active=True
        )

        db.session.add(new_subscription)
        db.session.commit()

        # Debugging: Log new subscription
        print(f"New subscription created: {new_subscription.to_dict()}")

        return make_response(jsonify(new_subscription.to_dict()), 201)

    @jwt_required()
    def put(self, subscription_id):
        data = request.get_json()
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404

        # Debugging: Log the existing subscription and data
        print(f"Updating subscription {subscription_id} with data: {data}")

        # Update fields
        subscription.payment_status = data.get('payment_status', subscription.payment_status)
        subscription.start_date = data.get('start_date', subscription.start_date)
        subscription.end_date = data.get('end_date', subscription.end_date)
        subscription.amount = data.get('amount', subscription.amount)
        subscription.active = data.get('active', subscription.active)

        db.session.commit()

        # Debugging: Log updated subscription
        print(f"Updated subscription: {subscription.to_dict()}")

        return jsonify(subscription.to_dict())
