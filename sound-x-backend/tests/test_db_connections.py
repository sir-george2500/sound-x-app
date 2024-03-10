# tests/test_db_connections.py
import unittest
from unittest.mock import patch, MagicMock
from config.db import db_connection
from sqlalchemy.orm import Session

class TestDBConnections(unittest.TestCase):
    def test_db_connection_exists(self):
        """
        Test that the db_connection function exists.
        """
        self.assertTrue(hasattr(db_connection, '__call__'), "db_connection function does not exist")

    @patch('config.db.create_engine')
    @patch('config.db.sessionmaker')
    def test_db_connection_successful(self, mock_sessionmaker, mock_create_engine):
        """
        Test that the db_connection function successfully establishes a database connection using SQLAlchemy.
        """
        # Set up mock objects
        mock_engine = mock_create_engine.return_value
        mock_session = MagicMock(spec=Session)  # Ensure that the mock is a Session instance
        mock_sessionmaker.return_value = mock_session

        # Call the function to connect to the database
        result = db_connection()

        # Assert that the function returned a session object
        self.assertIsInstance(result, MagicMock, "Failed to establish a database connection")

        # Assert that create_engine was called with the correct parameters
        mock_create_engine.assert_called_once_with(
            "postgresql://postgres:admin@localhost:5432/auth_services"
        )

        # Perform additional database-related tests or queries if needed

if __name__ == '__main__':
    unittest.main()

