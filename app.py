# Views
import os
from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager



from models import db,User
from resources.user import SignupResource, LoginResource, LogoutResource
from resources.case import CaseResource

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
app.config['SQLALCHEMY_ECHO'] = True

app.config['JWT_SECRET_KEY'] = "haki_secret_key"

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

# initialize bcrypt
bcrypt = Bcrypt(app)

# setup jwt
jwt = JWTManager(app)


  
@app.route('/users',methods=['GET'])
def users():
     user = User.query.all()
     print(user)
     return []
 
 
 

class HelloWorld(Resource):
    def get(self):
        return { "message": "Hello Haki" }
    
api.add_resource(HelloWorld, '/')
api.add_resource(SignupResource, '/signup')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')
api.add_resource(CaseResource, '/cases', '/cases/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)