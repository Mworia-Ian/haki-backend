from flask_restful import Resource, reqparse 
from models import db, Case
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity


class CaseResource(Resource):
     # create a new instance of reqparse
     parser = reqparse.RequestParser()
     parser.add_argument('description', required=True, 
                         help="Description is required")
     parser.add_argument('court_date', required=True, 
                         help="Court_date is required in ISO 8601 format")
     parser.add_argument('status', required=True, 
                         help="Status is required")
     
 
         
