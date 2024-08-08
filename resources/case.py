from flask_restful import Resource,reqparse
from flask import request, make_response
from datetime import datetime
from models import db, Case
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

class CaseResource(Resource):
    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        user_id = get_jwt_identity()
        
        if jwt['role'] == 'lawyer': 
            if id is None:
                cases = Case.query.filter_by(lawyer_id=user_id).all()
                results = [case.to_dict() for case in cases]
                return results
            else:
                case = Case.query.filter_by(id=id).first()
                if case is None:
                    return {"message": "Case not found", "status": "fail"}, 404
                return case.to_dict()
        else:
            return {"message": "You are not authorized to access this resource", "status": "fail"}, 401
        
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        
        if jwt['role'] == 'lawyer':
            try:
                data = request.get_json()
                court_date = datetime.fromisoformat(data['court_date'])  # Ensure correct date format
                new_case = Case(
                    description=data['description'],
                    court_date=court_date,
                    status=data['status'],
                    user_id=data['user_id'],
                    lawyer_id=jwt['sub']
                )
                db.session.add(new_case)
                db.session.commit()
                response_dict = new_case.to_dict()
                return make_response(response_dict, 201)
            except Exception as e:
                db.session.rollback()
                return {"message": f"An error occurred: {str(e)}", "status": "fail"}, 500
        else:
            return {"message": "You are not authorized to access this resource", "status": "fail"}, 401

    @jwt_required()
    def patch(self, id):
        jwt = get_jwt()
        
        if jwt['role'] == 'lawyer':
            data = request.get_json()  # Use request.get_json() to handle JSON input
            case = Case.query.filter_by(id=id).first()

            if case is None:
                return {"message": "Case not found"}, 404

            # Check for existing case with the same court_date
            if 'court_date' in data:
                existing_case = Case.query.filter(
                    and_(Case.court_date == datetime.fromisoformat(data['court_date']), not_(Case.id == id))
                ).first()

                if existing_case:
                    return {"message": "Case already exists for this court_date"}, 422

            # Update the case with new data
            for key, value in data.items():
                if value is not None:  # Ensure we only update fields with new data
                    setattr(case, key, value)

            db.session.commit()
            return {"message": "Case updated successfully"}, 200
        else:
            return {"message": "Unauthorized request"}, 401
