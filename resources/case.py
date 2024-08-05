from flask_restful import Resource, reqparse
from models import db, Case
from sqlalchemy import and_, not_
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

class CaseResource(Resource):
    # create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('description', required=True, help="Description is required")
    parser.add_argument('court_date', required=True, help="Court_date is required in ISO 8601 format")
    parser.add_argument('status', required=True, help="Status is required")
     
    @jwt_required()
    def get(self, id=None):
        jwt = get_jwt()
        user_identity = get_jwt_identity()
        
        if jwt['role'] == 'lawyer':
            if id is None:
                cases = Case.query.all()
                results = [case.to_dict() for case in cases]
                return results
            else:
                case = Case.query.filter_by(id=id).first()
                if case is None:
                    return {"message": "Case not found"}, 404
                return case.to_dict()
        else:
            return {"message": "Unauthorized request"}, 401

    @jwt_required()
    def patch(self, id):
        jwt = get_jwt()
        if jwt['role'] == 'lawyer':
            data = self.parser.parse_args()
            case = Case.query.filter_by(id=id).first()
            
            if case is None:
                return {"message": "Case not found"}, 404
            
            existing_case = Case.query.filter(and_(Case.court_date == data['court_date'], not_(Case.id == id))).first()
            
            if existing_case:
                return {"message": "Case already exists for this court_date"}, 422

            for key in data.keys():
                setattr(case, key, data[key])
            
            db.session.commit()
            return {"message": "Case updated successfully"}
        else:
            return {"message": "Unauthorized request"}, 401
            
    @jwt_required()
    def delete(self, id):
        jwt = get_jwt()
        if jwt['role'] != 'lawyer':
            return {"message": "Unauthorized request"}, 401
         
        case = Case.query.filter_by(id=id).first()
        if case is None:
            return {"message": "Case not found"}, 404
         
        db.session.delete(case)
        db.session.commit()
        return {"message": "Case deleted successfully"}, 200

         
            
        
        
         
