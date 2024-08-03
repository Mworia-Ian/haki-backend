# Views
from flask import Flask, request, jsonify, render_template,redirect,url_for
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api


from models import db, User, LawyerDetails

app = Flask(__name__)
api = Api(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.ubtabihyrjnwkxhztihb:123!hakiapp@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haki.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

CORS(app)

migrate = Migrate(app, db, render_as_batch=True)

db.init_app(app)


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    id_no = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    area_of_residence = data.get('area_of_residence')
    password = data.get('password')
    role = data.get('role')

    new_user = User(firstname=firstname, lastname=lastname, id_no=id_no, phone=phone,
                    email=email, area_of_residence=area_of_residence, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    if role not in ['lawyer', 'client']:
        return jsonify({'message': 'Invalid role'}), 400

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/lawyer-details', methods=['GET', 'POST'])
def lawyer_details():
    if request.method == 'GET':
        return render_template('lawyer_details.html')

    user_id = request.args.get('user_id')
    data = request.form

    lawyer_id = data.get('lawyer_id')
    years_of_experience = data.get('years_of_experience')
    specialization = data.get('specialization')
    rate_per_hour = data.get('rate_per_hour')
    qualification_certificate = request.files['qualification_certificate'].read(
    )

    new_lawyer_detail = LawyerDetails(
        user_id=user_id,
        lawyer_id=lawyer_id,
        years_of_experience=years_of_experience,
        specialization=specialization,
        rate_per_hour=rate_per_hour,
        qualification_certificate=qualification_certificate
    )
    db.session.add(new_lawyer_detail)
    db.session.commit()

    return jsonify({"message": "Lawyer details submitted successfully"}), 201

@app.route('/available-lawyer',methods=['GET'])
def available_lawyers():
    user_id = request.args.get('user')