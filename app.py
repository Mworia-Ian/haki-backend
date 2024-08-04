#Views
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api


#Import models
from models import db, User, LawyerDetails

app = Flask(__name__)
api = Api(app)

## app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.ubtabihyrjnwkxhztihb:123!hakiapp@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

CORS(app)


migrate = Migrate(app, db, render_as_batch=True)
db.init_app(app)

bcrypt =Bcrypt(app)

@app.route('/')
def home():
    return 'Hello from flask'

@app.route('/users',methods=['GET'])
def users():
    user = User.query.all()
    print(user)
    return []
