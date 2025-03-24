# A model class for Product items
# See https://docs.pydantic.dev/latest/concepts/models/

from pydantic import BaseModel, ValidationError, ValidationInfo, field_validator
from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from uuid import UUID
import re

class User(BaseModel):
    email: str
    password: str

# Pydantic model for user registration
class RegisterUser(BaseModel):
    
    first_name: str
    last_name: str
    email: EmailStr
    password: constr(min_length=8)
    phone: Optional[str] = None
    address: Optional[str] = None

    # Add a validator for the password field
    @validator('password')
    def validate_password(cls, v):
        # You can add a custom validation here
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v