# Modeling  the database
from flask_sqlachemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


# Models
class User(db.Model, SerializerMixin):

    # Table to store our users information
    __tablename__ = 'users'

    # Columns in the database
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    id_no = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.Text, nullable=False)
    area_of_residence = db.Column(db.Text, nullable=False)


class Role(db.Model, SerializerMixin):

    # Table to keep track of our users roles
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False)


class LawyerDetails(db.Model, SerializerMixin):

    # Table to hold lawyers details
    __tablename__ = 'lawyers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lawyer_id = db.Column(db.Text)
    years_of_experience = db.Column(db.Text, nullable=False)
    specialization = db.Column(db.Text, nullable=False)
    rate_per_hour = db.Column(db.Integer)
    qualification_certificate = db.Column(db.LargeBinary, nullable=False)
    

class Payment(db.Model,SerializerMixin):
      
      #Table to store payment of the users
      __tablename__= 'payments'
      
      id =db.Column(db.Integer,primary_key=True)
      user_id = db.Column(db.Integer)
      
