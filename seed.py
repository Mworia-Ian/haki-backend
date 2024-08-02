from app import app
from models import db,User

with app.app_context():
     print('Seeding dummy data')
     User.query.delete()
     
     user1 = User(firstname='Charles',lastname='Biegon',id_no=12345678,phone='0712345678',email='charles@gmail.com',password='1234',area_of_residence='Nairobi')
     
     db.session.add(user1)
     db.session.commit()