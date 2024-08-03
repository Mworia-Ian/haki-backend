from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import check_password_hash, generate_password_hash
from datetime import datetime
import re

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

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    id_no = db.Column(db.Integer, nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    area_of_residence = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    serialize_rules = ('-password',)

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not re.match(r"^0[0-9]{9}$", phone):
            raise ValueError("Phone number must be a 10-digit number starting with 0")
        return phone

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return generate_password_hash(password).decode('utf8')

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['lawyer', 'client']:
            raise ValueError("Role must be either 'lawyer' or 'client'")
        return role

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    # Relationships
    payments = db.relationship('Payment', back_populates='user')
    subscriptions = db.relationship('Subscription', back_populates='user')
    lawyer_details = db.relationship('LawyerDetails', back_populates='user', uselist=False)
    reviews = db.relationship('Review', back_populates='user')
    messages = db.relationship('Message', back_populates='user')
    cases = db.relationship('Case', back_populates='user')


class LawyerDetails(db.Model, SerializerMixin):

    __tablename__ = 'lawyers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    years_of_experience = db.Column(db.Integer, nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    rate_per_hour = db.Column(db.Integer)
    qualification_certificate = db.Column(db.LargeBinary)

    user = db.relationship('User', back_populates='lawyer_details')
    cases = db.relationship('Case', back_populates='lawyer')
    reviews = db.relationship('Review', back_populates='lawyer')


class Payment(db.Model, SerializerMixin):

    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))
    amount = db.Column(db.Float, nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='payments')
    subscription = db.relationship('Subscription', back_populates='payments')


class Subscription(db.Model, SerializerMixin):

    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payment_status = db.Column(db.String(20), nullable=False, default='unpaid')
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # Relationships
    user = db.relationship('User', back_populates='subscriptions')
    payments = db.relationship('Payment', back_populates='subscription')


class Case(db.Model, SerializerMixin):

    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.id'))
    description = db.Column(db.String(500), nullable=False)
    court_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')

    # Relationships
    user = db.relationship('User', back_populates='cases')
    lawyer = db.relationship('LawyerDetails', back_populates='cases')
    case_histories = db.relationship('CaseHistory', back_populates='case')


class CaseHistory(db.Model, SerializerMixin):

    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    details = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    case = db.relationship('Case', back_populates='case_histories')


class Review(db.Model, SerializerMixin):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Integer, db.ForeignKey('lawyers.id'))
    review = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='reviews')
    lawyer = db.relationship('LawyerDetails', back_populates='reviews')


class Message(db.Model, SerializerMixin):

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    sender_id = db.Column(db.String(50), nullable=False)
    receiver_id = db.Column(db.String(50), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='messages')
