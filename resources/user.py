from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User

class SignupResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', required=True, help='First name is required')
    parser.add_argument('lastname', required=True, help='Last name is required')
    parser.add_argument('id_no', required=True, help='ID number is required')
    parser.add_argument('phone', required=True, help='Phone number is required')
    parser.add_argument('email', required=True, help='Email is required')
    parser.add_argument('password', required=True, help='Password is required')
    parser.add_argument('area_of_residence', required=True, help='Area of residence is required')
    parser.add_argument('role', required=True, help='Role is required (must be either lawyer or client)')

    def post(self):
        data = self.parser.parse_args()
        
        # Hash the password
        data['password'] = generate_password_hash(data['password']).decode('utf-8')
        
        # Validate the role
        role = data['role'].lower()
        if role not in ['lawyer', 'client']:
            return {'message': 'Invalid role. Must be either lawyer or client', 'status': 'fail'}, 422
        
        # Check if the email already exists
        email = User.query.filter_by(email=data['email']).first()
        if email:
            return {'message': 'Email already exists', 'status': 'fail'}, 422
        
        # Create a new user instance
        user = User(**data)
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Something went wrong', 'status': 'fail', 'error': str(e)}, 500
        
        return {
            "message": "User registered successfully",
            "status": "success",
            "user": user.to_dict()
        }, 201

