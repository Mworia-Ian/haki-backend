# Modelling the database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import check_password_hash
from datetime import datetime

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
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    area_of_residence = db.Column(db.Text, nullable=False)
    role = db.Column(db.String, nullable=False)

    serialize_rules = ('-password',)

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    # Linking up relationships
    payments = db.relationship('Payment', back_populates='user')
    subscriptions = db.relationship('Subscription', back_populates='user')
    lawyer_details = db.relationship(
        'LawyerDetails', back_populates='user', uselist=False)
    reviews = db.relationship('Review', back_populates='user')
    messages = db.relationship('Message', back_populates='user')
    cases = db.relationship('Case', back_populates='user')

    # Validating the role of the user who just registers
    @validates('role')
    def validate_role(self, key, role):
        if role not in ['lawyer', 'client']:
            raise ValueError("Role must be either 'lawyer' or 'client'")
        return role


class LawyerDetails(db.Model, SerializerMixin):

    # Table to hold the lawyers details
    __tablename__ = 'lawyers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Text)
    years_of_experience = db.Column(db.Text, nullable=False)
    specialization = db.Column(db.Text, nullable=False)
    rate_per_hour = db.Column(db.Integer)
    qualification_certificate = db.Column(db.LargeBinary)

    user = db.relationship('User', back_populates='lawyer_details')
    cases = db.relationship('Case', back_populates='lawyer')
    reviews = db.relationship('Review', back_populates='lawyer')


class Payment(db.Model, SerializerMixin):

    # Table to store the payments of our users
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    user = db.relationship('User', back_populates='payments')
    subscriptions = db.relationship('Subscription', back_populates='payment')


class Subscription(db.Model, SerializerMixin):

    # Table to keep track of whether our users have payed or not
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    user = db.relationship('User', back_populates='subscriptions')
    payment = db.relationship('Payment', back_populates='subscriptions')


class Case(db.Model, SerializerMixin):

    # Table to store the cases of our users
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.id'))
    description = db.Column(db.String)
    court_date = db.Column(db.TIMESTAMP)
    status = db.Column(db.Text)

    # Relationships
    user = db.relationship('User', back_populates='cases')
    lawyer = db.relationship('LawyerDetails', back_populates='cases')
    case_histories = db.relationship('CaseHistory', back_populates='case')


class CaseHistory(db.Model, SerializerMixin):
    # Users case history
    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    details = db.Column(db.String)

    # Relationships
    case = db.relationship('Case', back_populates='case_histories')


class Review(db.Model, SerializerMixin):

    # Table to store the reviews
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.id'))
    review = db.Column(db.String)

    # Relationship
    user = db.relationship('User', back_populates='reviews')
    lawyer = db.relationship('LawyerDetails', back_populates='reviews')


class Message(db.Model, SerializerMixin):

    # Table to store the messages
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String)
    date = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    sender_id = db.Column(db.Text)
    receiver_id = db.Column(db.Text)

    # Relationship
    user = db.relationship('User', back_populates='messages')
