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

    # Linking up relationships
    roles = db.relationship('Role', back_populates='user')
    payments = db.relationship('Payment', back_populates='user')


class Role(db.Model, SerializerMixin):

    # Table to keep track of our users roles
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False)

    # Relationship
    user = db.relationship('User', back_populates='roles')


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


class Payment(db.Model, SerializerMixin):

    # Table to store payment of the users
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    
    #Relationship
    user = db.relationship('User',back_populates='payments')


class Subscription(db.Model, SerializerMixin):

    # Table to keep track of whether the users have payed
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


class Case(db.Model, SerializerMixin):

    # Table to store the cases of our users
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lawyer_id = db.Column(db.Integer)
    description = db.Column(db.String)
    court_date = db.Column(db.TIMESTAMP)
    status = db.Column(db.Text)


class CaseHistorY(db.Model, SerializerMixin):

    # Table to keep track of the our users cases
    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer)
    details = db.Column(db.String)


class Review(db.Model, SerializerMixin):

    # Table to store the reviews
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    lawyer_id = db.Column(db.Integer)
    review = db.Column(db.String)


class Message(db.Model, SerializerMixin):

    # Table to store the messages
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    message = db.Column(db.String)
    date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    sender_id = db.Column(db.Text)
    receiver_id = db.Column(db.Text)
