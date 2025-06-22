from sqlalchemy import  Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship
from app.entity import Base


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    street = Column(String)
    city = Column(String)
    zipcode = Column(String)