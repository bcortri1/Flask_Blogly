from unittest import TestCase
from app import app
from models import db, User, connect_db
from seed import seed_data

class UserCreate(TestCase):

    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
        seed_data()
        
    def test_create_new_user(self):
        with self.client:
            response = self.client.post("/users/new",json = {"first-name": "Patrick","last-name":"Stewart"})
            patrick = User.query.get(4)
            self.assertEqual(patrick.first_name, "Patrick")
            self.assertEqual(patrick.last_name, "Stewart")
            self.assertEqual(patrick.full_name, "Patrick Stewart")
            self.assertEqual(patrick.image_url, "https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png")