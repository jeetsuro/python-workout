
from sqlalchemy import Column, Integer, String
from typing import List 
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

Base = declarative_base()

class Orders(Base): # TODO
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    code= Column(String)
    name = Column(String)
    manufacturer = Column(String)
    category = Column(String)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    street = Column(String)
    city = Column(String)
    zipcode = Column(String)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    age  = Column(Integer)
    addresses = relationship('Address', backref='user', cascade='all, delete-orphan')
    # backref='user': This adds a property user to the Address class, allowing you to access the User object associated with an Address. 
    # So, for each address, you can access the User it belongs to by simply referencing address.user
    
    # cascade='all, delete-orphan': This ensures that:
       # If a User is deleted, all associated Address objects are also deleted (all cascade).
       # If an Address is removed from the addresses collection of a User and becomes orphaned (not associated with any user), 
       # it is also deleted (delete-orphan).

# Pydantic Schemas
class AddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    street: str
    city: str
    zipcode: str

class UserWithAddressesSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    age:  Optional[int] = None
    @field_validator('age')
    def check_age(cls, value):
        if value < 10:
            raise ValueError('Age must be at least 10')
        return value
    addresses: List[AddressSchema] = []
