from unittest import TestCase
from app import app
from models import db, User, connect_db
from seed import seed_data

class UserDetail(TestCase):

    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
        seed_data()
        
    def test_user_detail(self):
        with self.client:
            response = self.client.get("/users/1")
            html = response.get_data(as_text=True)
            
            self.assertIn('Johnny Depp', html)
            self.assertIn('<img src="https://m.media-amazon.com/images/M/MV5BOTBhMTI1NDQtYmU4Mi00MjYyLTk5MjEtZjllMDkxOWY3ZGRhXkEyXkFqcGdeQXVyNzI1NzMxNzM@._V1_UY209_CR1,0,140,209_AL_.jpg" alt="profile photo" height="200">', html)