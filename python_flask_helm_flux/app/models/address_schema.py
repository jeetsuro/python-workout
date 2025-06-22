from app.models import MyBaseModel

# Pydantic Schemas
class AddressSchema(MyBaseModel):
    street: str
    city: str
    zipcode: str