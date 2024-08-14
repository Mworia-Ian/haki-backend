from app import app
from models import db, User, LawyerDetails, Payment, Subscription, Case, CaseHistory, Review, Message
from datetime import datetime, timedelta
from flask_bcrypt import generate_password_hash


# Seed data

def seed_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create Users
        user1 = User(
            firstname='John',
            lastname='Doe',
            id_no=12345678,
            phone='0701234567',
            email='john.doe@example.com',
            password=generate_password_hash('password123').decode('utf-8'),
            area_of_residence='Nairobi',
            role='client'
        )

       

        db.session.add(user1)
      
        db.session.commit()

       

 

        print("Seed data added successfully!")

if __name__ == '__main__':
    seed_data()