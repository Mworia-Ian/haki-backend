import os
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt, check_password_hash
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
import re

# Import models
from models import db, User, LawyerDetails, Review, Case, CaseHistory, Payment, Message, Subscription

app = Flask(__name__)
api = Api(app)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = os.urandom(24)  

# Initialize extensions
CORS(app)
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return 'Hello from Flask'

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    required_fields = ['firstname', 'lastname', 'id_no', 'phone', 'email', 'password', 'area_of_residence', 'role']

    # Check for missing fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        # Validate email and phone
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        if not re.match(r"^0[0-9]{9}$", data['phone']):
            return jsonify({"error": "Phone number must be a 10-digit number starting with 0"}), 400

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            id_no=data['id_no'],
            phone=data['phone'],
            email=data['email'],
            password=hashed_password,
            area_of_residence=data['area_of_residence'],
            role=data['role']
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "role": user.role}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this email or phone already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role
        return jsonify({'message': 'Login successful', 'role': user.role}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/lawyers', methods=['GET'])
def get_lawyers():
    lawyers = LawyerDetails.query.all()
    lawyer_list = [{"id": lawyer.id, "specialization": lawyer.specialization, "rate_per_hour": lawyer.rate_per_hour} for lawyer in lawyers]
    return jsonify(lawyer_list), 200

@app.route('/lawyer_details', methods=['POST'])
def update_lawyer_details():
    data = request.json
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403

    user = User.query.get(user_id)
    if user and user.role == 'lawyer':
        lawyer_details = LawyerDetails.query.filter_by(user_id=user_id).first()
        if lawyer_details:
            lawyer_details.years_of_experience = data.get('years_of_experience', lawyer_details.years_of_experience)
            lawyer_details.specialization = data.get('specialization', lawyer_details.specialization)
            lawyer_details.rate_per_hour = data.get('rate_per_hour', lawyer_details.rate_per_hour)
            db.session.commit()
            return jsonify({"message": "Lawyer details updated successfully"}), 200
        else:
            return jsonify({"error": "Lawyer details not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 403

@app.route('/messages', methods=['GET'])
def get_messages():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403
    messages = Message.query.filter_by(user_id=user_id).all()
    return jsonify([message.serialize() for message in messages]), 200

@app.route('/reviews', methods=['GET'])
def get_reviews():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify([review.serialize() for review in reviews]), 200

@app.route('/cases', methods=['GET'])
def get_cases():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403
    cases = Case.query.filter_by(user_id=user_id).all()
    return jsonify([case.serialize() for case in cases]), 200

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403
    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    return jsonify([subscription.serialize() for subscription in subscriptions]), 200

@app.route('/review_lawyer', methods=['POST'])
def review_lawyer():
    data = request.json
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 403

    try:
        review = Review(
            user_id=user_id,
            lawyer_id=data['lawyer_id'],
            review=data['review'],
            rating=data['rating']
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
