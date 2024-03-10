import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from models.models import CreateUser, Base  # Replace "your_module_name" with the actual module name

# Define your database URL here
DATABASE_URL = "sqlite:///:memory:"

class TestCreateUser(unittest.TestCase):

    def setUp(self):
        # Create an in-memory SQLite database for testing
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = Session()

    def tearDown(self):
        # Close the database session
        self.db.close()

    def test_create_user(self):
        # Define test data
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword",
            "user_role": "user",
            # Add other required fields based on your model definition
        }

        # Create a new user instance
        user = CreateUser(**user_data)

        # Add the user to the database session
        self.db.add(user)
        self.db.commit()

        # Query the database to retrieve the user by username
        saved_user = self.db.query(CreateUser).filter_by(username="testuser").first()

        # Assert that the user is not None (i.e., it was successfully saved)
        self.assertIsNotNone(saved_user)

        # Add additional assertions based on your requirements
        self.assertEqual(saved_user.email, "testuser@example.com")
        self.assertEqual(saved_user.user_role, "user")

if __name__ == '__main__':
    unittest.main()
