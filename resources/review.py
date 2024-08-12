from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models import db, Review, User, LawyerDetails

class ReviewResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=int, required=True, help='User ID is required and must be an integer')
        self.parser.add_argument('lawyer_id', type=int, required=True, help='Lawyer ID is required and must be an integer')
        self.parser.add_argument('review', type=str, required=True, help='Review content is required')
        self.parser.add_argument('rating', type=int, required=True, help='Rating is required and must be an integer')
    
    @jwt_required()
    def get(self, id=None):
        if id:
            # Retrieve a single review by ID
            review = Review.query.get(id)
            if not review:
                return {'message': 'Review not found'}, 404
            return review.to_dict()
        else:
            # Retrieve all reviews
            reviews = Review.query.all()
            return [review.to_dict() for review in reviews]
    
    @jwt_required()
    def post(self):
        # Parse the incoming request data
        args = self.parser.parse_args()
        
        user_id = args['user_id']
        lawyer_id = args['lawyer_id']
        review_text = args['review']
        rating = args['rating']

        # Validate user and lawyer existence
        user = User.query.get(user_id)
        lawyer = LawyerDetails.query.get(lawyer_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if not lawyer:
            return {'message': 'Lawyer not found'}, 404

        # Create the review
        review = Review(
            user_id=user_id,
            lawyer_id=lawyer_id,
            review=review_text,
            rating=rating
        )

        try:
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error creating review: {str(e)}'}, 500

        return jsonify(review.to_dict()), 201
    
    @jwt_required()
    def delete(self, review_id):
        # Delete a review by ID
        review = Review.query.get(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        try:
            db.session.delete(review)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error deleting review: {str(e)}'}, 500
        
        return {'message': 'Review deleted successfully'}, 200
