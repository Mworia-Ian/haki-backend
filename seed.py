from app import app
from models import db, User, LawyerDetails, Payment, Subscription, Case, CaseHistory, Review, Message
from datetime import datetime, timedelta


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
            password='password123',
            area_of_residence='Nairobi',
            role='client'
        )

        user2 = User(
            firstname='Jane',
            lastname='Smith',
            id_no=87654321,
            phone='0709876543',
            email='jane.smith@example.com',
            password='password456',
            area_of_residence='Mombasa',
            role='lawyer'
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create Lawyer Details
        lawyer_details1 = LawyerDetails(
            user_id=user2.id,
            years_of_experience=10,
            specialization='Criminal Law',
            rate_per_hour=150,
            image='path/to/lawyer_image.jpg',
            qualification_certificate=b'certificate_data'
        )

        db.session.add(lawyer_details1)
        db.session.commit()

        # Create Subscriptions
        subscription1 = Subscription(
            user_id=user1.id,
            payment_status='paid',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30)
        )

        db.session.add(subscription1)
        db.session.commit()

        # Create Payments
        payment1 = Payment(
            user_id=user1.id,
            subscription_id=subscription1.id,
            amount=100.0,
            transaction_id='txn_123456789',
            status='completed'
        )

        db.session.add(payment1)
        db.session.commit()

        # Create Cases
        case1 = Case(
            user_id=user1.id,
            lawyer_id=lawyer_details1.id,
            description='Case description example.',
            court_date=datetime.utcnow() + timedelta(days=15),
            status='open'
        )

        db.session.add(case1)
        db.session.commit()

        # Create Case History
        case_history1 = CaseHistory(
            case_id=case1.id,
            details='Initial case details.',
            timestamp=datetime.utcnow()
        )

        db.session.add(case_history1)
        db.session.commit()

        # Create Reviews
        review1 = Review(
            user_id=user1.id,
            lawyer_id=lawyer_details1.id,
            review='Great lawyer!',
            rating=5
        )

        db.session.add(review1)
        db.session.commit()

        # Create Messages
        message1 = Message(
            user_id=user1.id,
            message='Hello, I need your help.',
            date=datetime.utcnow(),
            sender_id=user1.id,
            receiver_id=user2.id
        )

        db.session.add(message1)
        db.session.commit()

        print("Seed data added successfully!")

if __name__ == '__main__':
    seed_data()

    seed_data()