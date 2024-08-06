from flask import request, jsonify
from flask_restful import Resource
from models import db, Subscription
from flask_jwt_extended import jwt_required

class SubscriptionResource(Resource):
    @jwt_required()
    def get(self, subscription_id):
        subscription = Subscription.query.get(subscription_id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404
        
        return jsonify(subscription.to_dict())

    @jwt_required()
    def post(self, subscription_id):
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
