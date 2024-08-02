# Views
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api


from models import db,User

app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
# "postgresql://postgres:123456@localhost/bookmate"
app.config['SQLALCHEMY_ECHO'] = True

CORS(app)

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)


@app.route('/')
def home():
    return 'Hello from flask'
  
@app.route('/users',methods=['GET'])
def users():
     user = User.query.all()
     print(user)
     return []
