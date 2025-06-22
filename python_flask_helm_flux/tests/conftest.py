import os
import pytest
from unittest.mock import MagicMock

from app import create_app
from app.entity.user import User
from app.entity.address import Address

# - 'pytest.fixture' : decorator to set up common resources (Flask test client, database connection, temp file) once, 
#    and share it across multiple tests.
# - 'pytest' automatically calls the fixture and passes the return value to calle method under test_app.py
@pytest.fixture(scope='module')
def test_client():
    fapp=create_app() # treat app as object
    fapp.config['TESTING'] = True
    with fapp.test_client() as client:
        with fapp.app_context() :
            yield client, fapp

@pytest.fixture
def sample_user_data():
    return {
        "id": 1,
        "name": "Kimberly Scott",
        "email": "rperkins@yahoo.com",
        "age": 11,
        "addresses": [
            {
                "street": "15830 Spencer Park Suite 051",
                "city": "South Davidhaven",
                "zipcode": "93010"
            }
        ]
    }

@pytest.fixture
def sample_mock_users_data():
    return [
        {
            "id": 1,
            "name": "Kimberly Scott",
            "email": "rperkins@yahoo.com",
            "age": 11,
            "addresses": [
                {
                    "street": "15830 Spencer Park Suite 051",
                    "city": "South Davidhaven",
                    "zipcode": "93010"
                }
            ]
        },
        {
            "id": 2,
            "name": "SURAJIT PAUL",
            "email": "surajit@gmail.com",
            "age": 41,
            "addresses": [
                {
                    "street": "36 central road",
                    "city": "kolkata",
                    "zipcode": "743127"
                }
            ]
        }
    ]


@pytest.fixture
def mock_db_session():
    return MagicMock()
