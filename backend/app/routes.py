from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name:  str = Field(..., max_length=100)
    email: EmailStr
    phone: str = Field(..., max_length=20)

class FirebaseUserCreate(BaseModel):
    phone: str = Field(..., max_length=20)
