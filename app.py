import os
from datetime import timedelta
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager




# Import models
from models import db
from resources.user import SignupResource, LoginResource, LogoutResource
from resources.mpesa import StkPush
from resources.payment import PaymentResource
from resources.subscription import SubscriptionResource
from resources.case import CaseResource
from resources.review import ReviewResource
from resources.message import MessageResource


app = Flask(__name__)
api = Api(app)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.ubtabihyrjnwkxhztihb:123!hakiapp@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['JWT_SECRET_KEY'] = "haki_secret_key"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)

# setup jwt
jwt = JWTManager(app)
@app.route('/')

def home():
    return 'Hello from Flask'


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello Haki"}
    


api.add_resource(HelloWorld, '/')
# Add resources
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(StkPush, '/stk_push')
api.add_resource(PaymentResource, '/payment/<int:payment_id>')
api.add_resource(SubscriptionResource, '/subscription/<int:subscription_id>')
api.add_resource(CaseResource, '/case/<int:case_id>')
api.add_resource(ReviewResource, '/review/<int:review_id>')
api.add_resource(MessageResource, '/message/<int:message_id>')
if __name__ == '__main__':
    app.run(debug=True)
