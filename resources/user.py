from flask_restful import Resource, reqparse
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User,LawyerDetails

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

    # Additional arguments for lawyer
    parser.add_argument('years_of_experience', type=int, help='Years of experience is required for lawyers')
    parser.add_argument('specialization', help='Specialization is required for lawyers')
    parser.add_argument('rate_per_hour', type=int, help='Rate per hour is required for lawyers')
    parser.add_argument('image', help='Image URL is required for lawyers')
    parser.add_argument('qualification_certificate', help='Qualification certificate is required for lawyers')

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
        user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            id_no=data['id_no'],
            phone=data['phone'],
            email=data['email'],
            password=data['password'],
            area_of_residence=data['area_of_residence'],
            role=role
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            
            if role == 'lawyer':
                # Create a LawyerDetails instance
                if not all(field in data for field in ['years_of_experience', 'specialization', 'rate_per_hour', 'image', 'qualification_certificate']):
                    return {'message': 'Missing lawyer details fields', 'status': 'fail'}, 422

                lawyer_details = LawyerDetails(
                    user_id=user.id,
                    years_of_experience=data['years_of_experience'],
                    specialization=data['specialization'],
                    rate_per_hour=data['rate_per_hour'],
                    image=data['image'],
                    qualification_certificate=data['qualification_certificate']
                )
                db.session.add(lawyer_details)
                db.session.commit()

        except Exception as e:
            db.session.rollback()
            # Log the exception
            import logging
            logging.error(f"Error occurred: {str(e)}")
            return {'message': 'Something went wrong', 'status': 'fail', 'error': str(e)}, 500
        
        return {
            "message": "User registered successfully",
            "status": "success",
            "user": user.to_dict()
        }, 201 
        
class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True,
                        help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        # 1. Try to retrieve user with provided email
        user = User.query.filter_by(email=data['email']).first()

        # 2. check if user exists
        if user:
            # 3. password verification
            is_password_match = user.check_password(data['password'])

            if is_password_match:
                user_dict = user.to_dict(only=('id','firstname','role', 'email',))
                additional_claims = { "role": user_dict['role'] }
                access_token = create_access_token(identity=user_dict['id'],
                                                   additional_claims=additional_claims)

                return {"message": "Login successful",
                        "status": "success",
                        "user": user_dict,
                        "access_token": access_token}
            else:
                return {"message": "Invalid email/password", "status": "fail"}, 403
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 403
        
        
        
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # JWT handles logout by removing the token from the client-side.
        return {"message": "Logged out successfully"}, 200