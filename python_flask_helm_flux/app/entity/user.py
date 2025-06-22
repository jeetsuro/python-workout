from sqlalchemy import  Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship
from app.entity import Base

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