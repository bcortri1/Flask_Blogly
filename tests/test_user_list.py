from unittest import TestCase
from app import app
from models import db, User, connect_db
from seed import seed_data

class UserList(TestCase):

    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
        seed_data()
        
        
    def test_user_list(self):
        with self.client:
            response = self.client.get("/users")
            html = response.get_data(as_text=True)
            self.assertIn('Johnny Depp', html)
            self.assertIn('Brad Pitt', html)
            self.assertIn('Angelina Jolie', html)