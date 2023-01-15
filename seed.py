from models import db, User, connect_db
from app import app

def seed_data():
    """Seeds data and is accessible for testing purposes"""
    connect_db(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        User.query.delete()



    johnny = User(first_name = "Johnny", last_name = "Depp", image_url = "https://m.media-amazon.com/images/M/MV5BOTBhMTI1NDQtYmU4Mi00MjYyLTk5MjEtZjllMDkxOWY3ZGRhXkEyXkFqcGdeQXVyNzI1NzMxNzM@._V1_UY209_CR1,0,140,209_AL_.jpg")
    brad = User(first_name = "Brad", last_name = "Pitt")
    angelina = User(first_name = "Angelina", last_name = "Jolie", image_url = "https://m.media-amazon.com/images/M/MV5BODg3MzYwMjE4N15BMl5BanBnXkFtZTcwMjU5NzAzNw@@._V1_UY209_CR15,0,140,209_AL_.jpg")

    with app.app_context():
        db.session.add(johnny)
        db.session.add(brad)
        db.session.add(angelina)
        db.session.commit()
    print("Seed data complete")
    
seed_data()