from flask import request, jsonify
from flask_restful import Resource
from models import db, Case
from flask_jwt_extended import jwt_required

class CaseResource(Resource):
    @jwt_required()
    def get(self, case_id):
        case = Case.query.get(case_id)
        if not case:
            return {'message': 'Case not found'}, 404
        
        return jsonify(case.to_dict())

    @jwt_required()
    def post(self, case_id):
        data = request.get_json()
        case = Case.query.get(case_id)
        if not case:
            return {'message': 'Case not found'}, 404

        # Update fields
        case.description = data.get('description', case.description)
        case.court_date = data.get('court_date', case.court_date)
        case.status = data.get('status', case.status)

        db.session.commit()

        return jsonify(case.to_dict())

    @jwt_required()
    def delete(self, case_id):
        case = Case.query.get(case_id)
        if not case:
            return {'message': 'Case not found'}, 404
        
        db.session.delete(case)
        db.session.commit()
        
        return {'message': 'Case deleted successfully'}, 200
