from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


app = Flask(__name__)

CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456@localhost/bookmate"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
