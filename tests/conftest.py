import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the database module BEFORE importing app
with patch.dict('sys.modules', {
    'app.database': MagicMock(),
    'app.database.mongodb': MagicMock()
}):
    # Now import your app
    from app.api import app

""" Test """

@pytest.fixture(autouse=True)
def mock_mongodb():
    """Mock MongoDB for all tests"""
    with patch('app.database.mongodb.MongoDBConnection.get_database') as mock_db:
        # Create mock database
        mock_database = MagicMock()
        mock_collection = MagicMock()
        
        # Mock user operations
        mock_collection.find_one.return_value = {
            "_id": "69",
            "userID": 1,
            "name": "test user",
            "email": "test@example.com",
            "phone": "+1 234 56789012",
            "birthday": "14.04.2004"
        }

        mock_collection.insert_one.return_value = MagicMock("69")
        mock_collection.delete_one.return_value = MagicMock({"n": 1})

        mock_database.__getitem__.return_value = mock_collection
        mock_database.users = mock_collection
        mock_db.return_value = mock_database
        
        yield TestClient(app)
