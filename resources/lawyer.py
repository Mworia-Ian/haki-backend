from flask_restful import Resource, reqparse
from models import db, LawyerDetails
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import request
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'path/to/upload/folder'
ALLOWED_EXTENSIONS = {'jpeg', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class LawyerDetailsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('years_of_experience', required=True,  help='Years of experience')
    parser.add_argument('specialization', required=True, help='Specialization')
    parser.add_argument('rate_per_hour', required=True, help='Rate per hour')
    parser.add_argument('image', required=True, help='Image URL')
    
    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        user_id = get_jwt_identity()
        
        if jwt['role'] in ['client', 'lawyer']:
            if id is None:
                lawyers = LawyerDetails.query.all()
                results = [lawyer.to_dict() for lawyer in lawyers]
                return results
            else:
                lawyer = LawyerDetails.query.filter_by(id=id).first()
                if lawyer is None:
                    return {'message': 'Lawyer not found'}, 404
                return lawyer.to_dict()
        else:
            return {'message': 'You are not authorized to access this resource'}, 401

    @jwt_required()
    def patch(self, id):
        jwt = get_jwt()
        
        if jwt['role'] == 'lawyer':
            data = self.parser.parse_args()
            lawyer = LawyerDetails.query.filter_by(id=id).first()
            if lawyer is None:
                return {'message': 'Lawyer not found'}, 404
            
            if 'years_of_experience' in data and data['years_of_experience'] is not None:
                lawyer.years_of_experience = data['years_of_experience']
            if 'specialization' in data and data['specialization'] is not None:
                lawyer.specialization = data['specialization']
            if 'rate_per_hour' in data and data['rate_per_hour'] is not None:
                lawyer.rate_per_hour = data['rate_per_hour']
            if 'image' in data and data['image'] is not None:
                lawyer.image = data['image']
            
            # Handle file upload for qualification_certificate
            if 'qualification_certificate' in request.files:
                file = request.files['qualification_certificate']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    lawyer.qualification_certificate = filepath
                else:
                    return {'message': 'Invalid file type. Only JPEG images are allowed.'}, 400

            db.session.commit()
            return lawyer.to_dict(), 200
        else:
            return {'message': 'You are not authorized to access this resource'}, 401

    @jwt_required()
    def post(self):
        jwt = get_jwt()

        if jwt['role'] == 'lawyer':
            data = self.parser.parse_args()

            if 'qualification_certificate' not in request.files:
                return {'message': 'Qualification certificate is required'}, 400

            file = request.files['qualification_certificate']
            if file.filename == '':
                return {'message': 'No selected file'}, 400

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                new_lawyer_details = LawyerDetails(
                    user_id=jwt['user_id'],
                    years_of_experience=data['years_of_experience'],
                    specialization=data['specialization'],
                    rate_per_hour=data['rate_per_hour'],
                    image=data['image'],
                    qualification_certificate=filepath
                )

                db.session.add(new_lawyer_details)
                db.session.commit()
                return new_lawyer_details.to_dict(), 201
            else:
                return {'message': 'Invalid file type. Only JPEG images are allowed.'}, 400
        else:
            return {'message': 'You are not authorized to access this resource'}, 401