from app import app
from datetime import datetime
from models import db, User, LawyerDetails, Review, Payment, Subscription, Case, CaseHistory, Message, Role

with app.app_context():
    print('Seeding dummy data')
    User.query.delete()
    LawyerDetails.query.delete()
    Review.query.delete()
    Payment.query.delete()
    Subscription.query.delete()
    Case.query.delete()
    Message.query.delete()
    Role.query.delete()
    CaseHistory.query.delete()

    # Users data
    user1 = User(firstname='Charles', lastname='Biegon', id_no=12345678, phone='0712345678',
                 email='charles@gmail.com', password='1234', area_of_residence='Nairobi')
    user2 = User(
        firstname='Jane', lastname='Doe', id_no=000000,
        phone=1234567890, email='jane@gmail.com',
        area_of_residence='Kenya', password='1234'
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    print("user added successfully")

    # lawyers data
    lawyer1 = LawyerDetails(user_id=user1.id,
                            lawyer_id='LAW123', years_of_experience='5',
                            specialization='Criminal Law', rate_per_hour=150,
                            qualification_certificate=None
                            )
    db.session.add(lawyer1)
    db.session.commit()
    print("lawyer added successfully")

    # Reviews data
    review1 = Review(user_id=user2.id, lawyer_id=lawyer1.id,
                     review='Excellent service.')
    db.session.add(review1)
    db.session.commit()
    print("Reviews for lawyer 1 added ")

    # Payments data
    payment1 = Payment(user_id=user1.id)
    db.session.add(payment1)
    db.session.commit()
    print("payment added")

    # Subscriptions data
    subscription1 = Subscription(user_id=user1.id, payment_id=1)
    db.session.add(subscription1)
    db.session.commit()
    print('Subscription added successfully')

    # Cases data
    case1 = Case(user_id=user1.id, lawyer_id=lawyer1.id, description='Case 1 description',
                 court_date=datetime.now(), status='Open')
    db.session.add(case1)
    db.session.commit()
    print('Cases added')

    # Case history added
    case_history1 = CaseHistory(
        case_id=case1.id, details='Case history details.')
    db.session.add(case_history1)
    db.session.commit()
    print('Case history')

    # message data
    message1 = Message(user_id=user1.id, date=datetime.now(), message='Message details',
                       sender_id='Charles Biegon', receiver_id='Jane Doe')
    db.session.add(message1)
    db.session.commit()
    print('messages added')

    # Role data
    role1 = Role(user_id=user1.id, firstname='Charles',
                 lastname='Biegon', email='charles@gmail.com')
    db.session.add(role1)
    db.session.commit()
    print('Roles created')
