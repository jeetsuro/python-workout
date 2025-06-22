from typing import List 
from typing import Optional
from pydantic import field_validator

from app.models import MyBaseModel
from app.models.address_schema import AddressSchema

# Pydantic Schemas
class UserWithAddressesSchema(MyBaseModel):
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