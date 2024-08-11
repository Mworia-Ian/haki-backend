from flask_restful import Resource, reqparse
from models import db, CaseHistory
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity


class CaseHistoryResource(Resource):
    # Create a new instance of reqparse
    parser = reqparse.RequestParser()
    parser.add_argument('details', required=True, help="Details are required")
    parser.add_argument('timestamp', required=True, help="Timestamp is required")
    parser.add_argument('case_id', required=True, help="Case ID is required")

    @jwt_required()
    def get(self, case_id=None):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        # If a specific case_id is provided, fetch histories for that case
        if case_id:
            case_histories = CaseHistory.query.filter_by(case_id=case_id).all()
        else:
            # Otherwise, fetch all case histories for the authenticated user
            case_histories = CaseHistory.query.filter_by(user_id=user_id).all()

        results = [history.to_dict() for history in case_histories]
        return results, 200

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        user_id = get_jwt_identity()

        # Parse the request data
        data = self.parser.parse_args()
        try:
            timestamp = datetime.fromisoformat(data['timestamp'])
        except ValueError:
            return {"message": "Invalid timestamp format."}, 400

        # Create a new case history record
        new_case_history = CaseHistory(
            details=data['details'],
            timestamp=timestamp,
            case_id=data['case_id'],
            user_id=user_id  # Associate the case history with the authenticated user
        )

        # Add and commit the new record to the database
        db.session.add(new_case_history)
        db.session.commit()

        return new_case_history.to_dict(), 201