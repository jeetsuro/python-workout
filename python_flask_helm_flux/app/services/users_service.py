
from typing import List, Optional
from functools import lru_cache
from pydantic import ValidationError

import logging
from app.logging_config import setup_logging
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import scoped_session
from app.services.base_service import BaseService
from app.models.users_schema import UserWithAddressesSchema
from app.models.address_schema import AddressSchema
from app.entity.address import Address
from app.entity.user import User

logger = setup_logging().getLogger(__name__) # Get the logger for this module
if logger is None:
    print ('Logger not created for logging_config..')
logger = logging.getLogger(__name__)

@lru_cache
def get_users_service():
    return UsersService()

class UsersService(BaseService):

    def __init__(self):
        super().__init__()

    def insert_users(self,users_data: List[dict]) -> List[User]:

        users_final_list=[]
        print(logger)
        print(type(logger))

        session=None
        try:
            session=scoped_session(self.db.Session)
        except:
            logger.error('Issue in creating session..')
            return None

        #if self.db.session is None:
        #    return users_final_list

        if session() is None:
            return users_final_list
                
        # Raw data validation by Pydantic
        logger.info ('About to validate raw data by Pydantic..')
        print ('About to validate raw data by Pydantic..')

        for user_data in users_data:
            try:
                validated_user_data = UserWithAddressesSchema.model_validate(user_data)
                user = User(
                    id=validated_user_data.id,
                    name=validated_user_data.name,
                    email=validated_user_data.email,
                    age=validated_user_data.age
                )
                for addr in validated_user_data.addresses:
                    user.addresses.append(Address(**addr.model_dump()))
                users_final_list.append(user)
            except ValidationError as ve:
                logger.warning (f"❌ Validation Error: {ve.title}")
                print ('f"❌ Validation Error: {ve.title}')
            except Exception as e:
                logger.error (f"❌ Unexpected Error: {e.__str__}")
                print (f"❌ Unexpected Error: {e.__str__}")
           
        try :
            # Add all users to the session at once
            
            #self.db.session.add_all(users_final_list)
            #self.db.session.commit() # commit
            session().add_all(users_final_list)
            session().commit() # commit

            for u in users_final_list:
                logger.info  ("----------------------------")
                logger.info (f"Successfully inserted user : ID - {u.id} , name - '{u.name}' age - {str(u.age)}")
            logger.info ("✅ All Validated Users inserted successfully..")
        except IntegrityError as ie:
            #self.db.session.rollback()
            session().rollback()
            logger.error (f"❌ Integrity Error: {ie._message}")
        except SQLAlchemyError as se:
            #self.db.session.rollback()
            session().rollback()
            logger.error (f"❌ Database Error: {se._message}")
        except Exception as e:
            #self.db.session.rollback()
            session().rollback()
            logger.error (f"❌ Unexpected Error: {e.__cause__}")
        finally:
            #self.db.session.close()
            session().close()
            return users_final_list

    # Fetch one
    def get_user(self, user_id: int) -> UserWithAddressesSchema:
        res_user =None
        try:
            stmt = select(User).where(User.id == user_id)
            session=scoped_session(self.db.Session)
            # user = self.db.session.execute(stmt).scalars().one()
            user = session().execute(stmt).scalars().one()
            logger.info(f"SUCCESS: User found with id : {str(user_id)}")
            print(f"SUCCESS: User found with id : {str(user_id)}")
            print (repr(user))
            res_user = UserWithAddressesSchema.model_validate(user)
        except Exception:
            logger.info(f"❌ User with ID {user_id} not found.")
            print("❌ User with ID {user_id} not found.")
        finally:
            session().close()
            return res_user

    # delete user
    def delete_user(self, user_id: int) -> str:
        print (f"About to delete user_id : {user_id}")
        logger.info(f"About to delete user_id : {user_id}")
        MSG=""
        try:    
            session=scoped_session(self.db.Session)
            stmt = select(User).where(User.id == user_id)
            #user = self.db.session.execute(stmt).scalars().first()
            user = session().execute(stmt).scalars().first()
            if user:
                #self.db.session.delete(user)
                #self.db.session.commit()
                session().delete(user)
                session().commit()
                MSG=f"User with ID {user_id} has been deleted."
                logger.info(f"User with ID {user_id} has been deleted..")
                print(f"User with ID {user_id} has been deleted..")
            else:
                MSG="No user found with ID {user_id} to delete."
                logger.warning(f"User with ID {user_id} has been deleted..")
                print(f"No user found with ID {user_id} to delete..")
        except Exception:
            MSG=f"ERROR: User with ID {user_id} not deleted."
            print(f"❌ERROR: User with ID {user_id} not deleted...")
            #self.db.session.rollback()
            session().rollback()
        finally:
            #self.db.session.close()
            session().close()
            return MSG
            
    # Delete_address
    def delete_address(self, zipcode: str) -> str:
        
        print(f"About to delete all addresses with zipcode: {zipcode}")
        logger.info(f"About to delete all addresses with zipcode: {zipcode}")
        MSG=""
        try:
            session=scoped_session(self.db.Session) # Thread local
            stmt = select(Address).where(Address.zipcode == zipcode)
            #addresses = self.db.session.execute(stmt).scalars().all()
            addresses = session().execute(stmt).scalars().all()
            if addresses:
                for addr in addresses:
                    #self.db.session.delete(addr)
                    session().delete(addr)
                #self.db.session.commit() # commit
                session().commit() # commit
                print(f"✅ Deleted {len(addresses)} address(es) with zipcode {zipcode}.")
                MSG=f"Deleted {len(addresses)} address(es) with zipcode {zipcode}."
            else:
                MSG=f"No addresses found with zipcode {zipcode} to delete."
                print(f"ℹ️ No addresses found with zipcode {zipcode} to delete.")
                logger.info(f"ℹ️ No addresses found with zipcode {zipcode} to delete.")
        except Exception as e:
            #self.db.session.rollback()
            session().rollback()
            MSG=f"ERROR deleting addresses with zipcode {zipcode}"
            logger.warning(f"❌ Error deleting addresses with zipcode {zipcode}: {e}")
            print(f"❌ Error deleting addresses with zipcode {zipcode}: {e}")
        finally:
            #self.db.session.close()
            session().close()
            return MSG

    # Fetch all users
    def get_all_users(self) -> List[UserWithAddressesSchema]:

        logger.info(f"About to fetch all users..")
        print("About to fetch all users..")
        validated_users = []
        session = None
        try:
            session=scoped_session(self.db.Session)
            stmt = select(User)
            #users = self.db.session.execute(stmt).scalars().all()
            users=session().execute(stmt).scalars().all()
            for u in users:
                try: 
                    if u.id is not None and u.name and u.email:
                        validated_users.append(UserWithAddressesSchema.model_validate(u))
                        logger.info(f"Successfully fetched user_id: {str(u.id)} , name : {u.name}")
                        print(f"Successfully fetched user_id: {str(u.id)} , name : {u.name}")
                    else:
                        logger.info(f"Skipping user with incomplete data: {u}")
                        print(f"Skipping user with incomplete data: {u}")
                except Exception as e:
                    logger.warning(f"❌ Failed to fetch user_id: {u.id}")
                    print(f"❌ Failed to fetch user_id: {u.id}")
        except Exception as e:
            logger.info(f"❌ Failed to fetch all users: {e}")
            print(f"❌ Failed to fetch all users: {e}")
        finally:
            #self.db.session.close()
            session().close()
            return validated_users            
        
    def get_all_addresses_from_table(self) -> List[AddressSchema]:

        logger.info(f"About to fetch all address..")
        print("About to fetch all address..")
        res=[]
        session = None
        try:
            session=scoped_session(self.db.Session)
            stmt = select(Address)
            adds = session().execute(stmt).scalars().all()
            res =[AddressSchema.model_validate(u) for u in adds]
        except Exception as e:
            print(f"❌ Failed to fetch adds: {e}")
            logger.warning(f"❌ Failed to fetch adds: {e}")
        finally:
            #self.db.session.close()
            return res
        
    def get_headers(self) -> List[str]:

        user_fields = list(UserWithAddressesSchema.model_fields.keys())

        # Remove 'address'
        ll=[ u for u in user_fields if u != 'addresses' ]
        addr_fields = list(AddressSchema.model_fields.keys())
        #return ['Id', 'Name', 'email', 'Age', 'street', 'city', 'zip']  
        return ll + addr_fields    
          