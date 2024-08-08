from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Review, User, LawyerDetails

class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        # Retrieve a single review by ID
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        
        return jsonify(review.to_dict())
    
    @jwt_required()
    def post(self):
        # Create a new review
        data = request.get_json()
        user_id = data.get('user_id')
        lawyer_id = data.get('lawyer_id')
        
        # Validate user and lawyer existence
        user = User.query.get(user_id)
        lawyer = LawyerDetails.query.get(lawyer_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if not lawyer:
            return {'message': 'Lawyer not found'}, 404

        review = Review(
            user_id=user_id,
            lawyer_id=lawyer_id,
            review=data.get('review'),
            rating=data.get('rating')
        )

        db.session.add(review)
        db.session.commit()

        return jsonify(review.to_dict()), 201
    @jwt_required()
    def delete(self):
        # Delete a review by ID
        data = request.get_json()
        review_id = data.get('review_id')
        
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        
        db.session.delete(review)
        db.session.commit()
        
        return {'message': 'Review deleted successfully'}, 200
