from flask import request, jsonify
from flask_restful import Resource, Api
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required
from models import db, Review, User, LawyerDetails

class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id=None):
        if review_id:
            # Retrieve a single review by ID
            reviews = Review.query.filter_by(lawyer_id = review_id).all()
            if not reviews:
                return {'message': 'Review not found', 'status': 'fail'}, 404
            return jsonify([review.to_dict(only=("review", "rating", "id", "user.firstname", "user.lastname")) for review in reviews])
        
        
    
    @jwt_required()
    def post(self):
        # Create a new review
        data = request.get_json()
        user_id = data.get('user_id')
        lawyer_id = data.get('lawyer_id')
        
        # Validate user and lawyer existence
<<<<<<< HEAD
        user = User.query.get(user_id)
=======
        user = User.query.filter_by(id=user_id).first()
>>>>>>> c1f9da0ba33cbb85751e98f2dce33c57a9d70206
        lawyer = LawyerDetails.query.filter_by(user_id=lawyer_id).first()
        
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

        return review.to_dict(only=("review", "rating", "id",)), 201

<<<<<<< HEAD
        

=======
>>>>>>> c1f9da0ba33cbb85751e98f2dce33c57a9d70206
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