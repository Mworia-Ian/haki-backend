import os
from datetime import timedelta, datetime
from flask import Flask, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request

# Import models
from models import db, Subscription
from resources.user import SignupResource, LoginResource, LogoutResource
from resources.case import CaseResource
from resources.mpesa import StkPush
from resources.subscription import SubscriptionResource
from resources.payment import PaymentResource

app = Flask(__name__)
api = Api(app)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
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

# Add resources
api.add_resource(HelloWorld, '/')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CaseResource, '/cases', '/cases/<int:id>')
api.add_resource(StkPush, '/stk_push')
api.add_resource(SubscriptionResource, '/subscription')
api.add_resource(PaymentResource, '/payment', endpoint='paymentresource')
api.add_resource(ProtectedResource, '/protected')  

if __name__ == '__main__':
    app.run(debug=True)
