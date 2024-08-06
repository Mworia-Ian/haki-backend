from datetime import datetime, timedelta
from models import db, User, LawyerDetails, Payment, Subscription, Case, Review, Message
from flask_bcrypt import generate_password_hash

# Sample data
def seed_data():
    # Create users
    user1 = User(
        firstname="Charles",
        lastname="Kibet",
        id_no=12345679,
        phone="0722222222",
        email="charlesdoe@example.com",
        password=generate_password_hash("password123").decode('utf-8'),
        area_of_residence="Nairobi",
        role="client"
    )
    user2 = User(
        firstname="Lema",
        lastname="Sam",
        id_no=23456789,
        phone="0723456788",
        email="lemasmith@example.com",
        password=generate_password_hash("password123").decode('utf-8'),
        area_of_residence="Mombasa",
        role="lawyer"
    )

    # Create lawyer details
    lawyer_details = LawyerDetails(
        user_id=user2.id,
        years_of_experience=5,
        specialization="Criminal Law",
        rate_per_hour=1500,
        qualification_certificate=None
    )

    # Create subscription
    subscription1 = Subscription(
        user_id=user1.id,
        payment_status="paid",
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=30)
    )

    # Create payments
    payment1 = Payment(
        user_id=user1.id,
        subscription_id=subscription1.id,
        amount=1000,
        transaction_id="txn_123456",
        status="completed"
    )

    # Create cases
    case1 = Case(
        user_id=user1.id,
        lawyer_id=lawyer_details.id,
        description="Case description here.",
        court_date=datetime.utcnow() + timedelta(days=15),
        status="active"
    )

    # Create reviews
    review1 = Review(
        user_id=user1.id,
        lawyer_id=lawyer_details.id,
        review="Excellent service!",
        rating=5
    )

    # Create messages
    message1 = Message(
        user_id=user1.id,
        message="Hello, I need assistance with my case.",
        date=datetime.utcnow(),
        sender_id=user1.id,
        receiver_id=user2.id
    )

    # Add records to the database
    db.session.add_all([user1, user2, lawyer_details, subscription1, payment1, case1, review1, message1])
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_data()
        print("Database seeded successfully!")
