from flask_restful import Resource, reqparse
from flask import request, make_response
from datetime import datetime
from models import db, Case, User
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity



class CaseResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description', required=True, help='Description of the case is required')
    parser.add_argument('court_date', required=True, help='Court date is required')
    parser.add_argument('status',  required=True, help='Status of the case is required')
    parser.add_argument('user_id', required=True, help='User ID is required')

    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        if jwt['role'] == 'lawyer':
            if id is None:
                cases = Case.query.filter_by(lawyer_id=user_id).all()
                results = [case.to_dict(only=("description", "court_date", "status","user.firstname", "user.lastname",)) for case in cases]
                return results
            else:
                case = Case.query.filter_by(id=id, lawyer_id=user_id).first()
                if case is None:
                    return {"message": "Case not found", "status": "fail"}, 404
                return case.to_dict()
        else:
            return {"message": "You are not authorized to access this resource", "status": "fail"}, 401

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        if jwt['role'] == 'lawyer':
            data = CaseResource.parser.parse_args()
            try:
                court_date = datetime.strptime(data['court_date'], '%Y-%m-%d %H:%M:%S')  # Adjust format as needed

                new_case = Case(
                    description=data['description'],
                    court_date=court_date,
                    status=data['status'],
                    user_id=data['user_id'],
                    lawyer_id=user_id
                )

                db.session.add(new_case)
                db.session.commit()
                response_dict = new_case.to_dict(only=("description", "court_date", "status", "user_id", "lawyer_id",))
                return make_response(response_dict, 201)
            except ValueError as ve:
                return {"message": f"Invalid date format: {str(ve)}", "status": "fail"}, 400
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}", "status": "fail"}, 500
        else:
            return {"message": "You are not authorized to access this resource", "status": "fail"}, 401

    @jwt_required()
    def patch(self, id):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        if jwt['role'] == 'lawyer':
            data = request.get_json()
            case = Case.query.filter_by(id=id, lawyer_id=user_id).first()

            if case is None:
                return {"message": "Case not found"}, 404

            if 'court_date' in data:
                try:
                    # Convert court_date to a datetime object
                    court_date = datetime.strptime(data['court_date'], '%Y-%m-%d %H:%M:%S')
                    existing_case = Case.query.filter(
                        and_(Case.court_date == court_date, not_(Case.id == id))
                    ).first()
                    if existing_case:
                        return {"message": "Case already exists for this court date"}, 422
                except ValueError:
                    return {"message": "Invalid date format"}, 400

                # Update court_date in the case
                case.court_date = court_date

            for key, value in data.items():
                if value is not None and key != 'court_date':
                    setattr(case, key, value)

            db.session.commit()
            return {"message": "Case updated successfully"}, 200
        else:
            return {"message": "Unauthorized request"}, 401
