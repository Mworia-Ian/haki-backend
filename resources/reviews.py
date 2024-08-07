from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import db, Review, User, LawyerDetails

class ReviewResource(Resource):
