import os
from datetime import timedelta
from flask import Flask,redirect,url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import datetime


# Import models
from models import db,Subscription
from resources.user import SignupResource, LoginResource, LogoutResource
from resources.case import CaseResource
from resources.history import CaseHistoryResource
from resources.lawyer import LawyerDetailsResource, LawyerResource
from resources.mpesa import StkPush
from resources.subscription import SubscriptionResource
from resources.payment import PaymentResource
# from resources.reviews import ReviewResource

app = Flask(__name__)
api = Api(app)


# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Middleware for subscription check
def subscription_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()

        # Check for active subscription
        active_subscription = Subscription.query.filter_by(user_id=user_id, payment_status='Paid').order_by(Subscription.end_date.desc()).first()

        if not active_subscription or active_subscription.end_date < datetime.now():
            
            return redirect(url_for('paymentresource'))

        return fn(*args, **kwargs)
    
    return wrapper

# HelloWorld resource
class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello Haki"}


class ProtectedResource(Resource):
    @subscription_required
    def get(self):
        return {"message": "You have access to this protected resource because you have an active subscription!"}

api.add_resource(HelloWorld, '/')
# Add resources
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CaseResource, '/cases', '/cases/<int:id>')
api.add_resource(LawyerDetailsResource, '/lawyer_details', '/lawyer_details/<int:id>')
api.add_resource(CaseHistoryResource, '/case_histories', '/case_histories/<int:case_id>')
api.add_resource(LawyerResource, '/lawyers', '/lawyers/<int:id>')

api.add_resource(StkPush, '/stk_push')
api.add_resource(SubscriptionResource, '/subscription')
api.add_resource(PaymentResource, '/payment', endpoint='paymentresource')
# api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
api.add_resource(ProtectedResource, '/protected')  

if __name__ == '__main__':
    app.run(debug=True)
