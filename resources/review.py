from flask import request, jsonify
from flask_restful import Resource
from models import db, Review
from flask_jwt_extended import jwt_required

class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        
        return jsonify(review.to_dict())

    @jwt_required()
    def post(self, review_id):
        data = request.get_json()
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        # Update fields
        review.review = data.get('review', review.review)
        review.rating = data.get('rating', review.rating)

        db.session.commit()

        return jsonify(review.to_dict())

    @jwt_required()
    def delete(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        
        db.session.delete(review)
        db.session.commit()
        
        return {'message': 'Review deleted successfully'}, 200
