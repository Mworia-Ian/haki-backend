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

