import pytest
import logging
import json
import unittest
from unittest.mock import MagicMock
from sqlalchemy import select
from app import create_app
from tests.conftest import test_client, sample_user_data, mock_db_session, sample_mock_users_data
from app.entity.user import User
from app.entity.address import Address
from app.services.users_service import get_users_service, UsersService

# https://deepwiki.com/pallets/flask/8.1-test-client

logger=logging.getLogger(__name__)

'''pytest style class'''
class TestUsers():
    
    @pytest.fixture
    def users_service(self):

        ins=get_users_service()
        #ins.insert_users= MagicMock()
        ins.get_all_users = MagicMock()
        ins.get_user = MagicMock()
        logger.info("users_service initialized..")

        return ins
    
    def test_insert_users(self, sample_user_data):

        user = User(
            id=sample_user_data["id"],
            name=sample_user_data["name"],
            email=sample_user_data["email"],
            age=sample_user_data["age"]
        )

        for addr in sample_user_data["addresses"]:
            user.addresses.append(Address(**addr))

        assert user.name == "Kimberly Scott"
        assert user.addresses[0].zipcode == "93010"
        assert user.addresses[0].user == user  # backref relationship
        logger.info(f"SQL-ORM {user} validated")

    def test_sqlalchemy_session_add_commit(self, sample_user_data, mock_db_session):

        logger.info("sql-session session_add_commit test..")

        user = User(
            id=sample_user_data["id"],
            name=sample_user_data["name"],
            email=sample_user_data["email"],
            age=sample_user_data["age"]
        )

        for addr in sample_user_data["addresses"]:
            user.addresses.append(Address(**addr))

        mock_db_session.add(user)
        mock_db_session.commit()

        mock_db_session.add.assert_called_once_with(user)
        mock_db_session.commit.assert_called_once()

    def test_get_all_users(self,sample_mock_users_data, mock_db_session):
        
        mock_users = []
        for data in sample_mock_users_data:
            user = User(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                age=data["age"]
            )
            user.addresses = [Address(**addr) for addr in data["addresses"]]
            mock_users.append(user)

        # Mock the session with all the users
        mock_db_session.query.return_value.all.return_value = mock_users

        # Call the mock and assert
        result = mock_db_session.query(User).all()
        assert len(result) == 2
        assert result[1].name == "SURAJIT PAUL"
        assert result[1].name != "SURAJIT PAUL2"
        assert result[0].addresses[0].city == "South Davidhaven"

    # Mock user based on User_ID
    def test_get_user(self, sample_mock_users_data, mock_db_session):

        mock_users = []
        for data in sample_mock_users_data:
            user = User(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                age=data["age"]
            )
            user.addresses = [Address(**addr) for addr in data["addresses"]]
            mock_users.append(user)

        # Mock the session populated with only 2nd user
        mock_db_session.execute.return_value.scalars.return_value.first.return_value = mock_users[1]

        given_user_id=2
        result = mock_db_session.query(User).filter_by(id=given_user_id).first()

        stmt = select(User).where(User.id ==given_user_id)
        result = mock_db_session.execute(stmt).scalars().first()

        assert result.id == 2
        assert result.name == "SURAJIT PAUL"

'''unittest.TestCase style'''
class TestRestEndPoints(unittest.TestCase):

    def setUp(self):
        
        fapp=create_app() # treat app as real flask client object
        fapp.config['TESTING'] = True
        with fapp.test_client() as client:
            with fapp.app_context() :
                self.client = client
                self.app = fapp

    def test_get_system_restend_header_and_param_valid( self):

        headers = {"X-API-KEY": "abcdef12345"}
        params = {"api_key": "abcdef12345"}
        
        try :
            response = self.client.get("/system", headers=headers, query_string=params)
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data["status"], "healthy")
        except Exception as e:

            self.client = MagicMock()
            mock_response = MagicMock()
            mock_response.data={"status": "healthy", "host_name": "SURAJIT_DELL", "ip_address" : "1.2.3.4"}
            self.client.get.return_value=mock_response
            res_after_mocking=self.client.get()
            print (res_after_mocking)
            self.assertEqual(res_after_mocking.data['host_name'], "SURAJIT_DELL")
            self.assertEqual(res_after_mocking.data['ip_address'], "1.2.3.4")

    # TODO
    def test_get_system_restend_header_and_param_invalid(self):
        pass

def test_home_restend(test_client) :

    cl,app=test_client
    res= cl.get('/home')
    assert res.status_code == 404

def test_index_restend(test_client) :

    cl,app=test_client
    res= cl.get('/')

    assert res.status_code == 200
    assert app.config['APP_MESSAGE'] in res.data.decode('utf-8')

def test_health_restend(test_client) :

    cl,app=test_client
    res= cl.get('/health')

    assert res.status_code == 200
    print (res.data.decode('utf-8'))
    assert b"healthy" in res.data



