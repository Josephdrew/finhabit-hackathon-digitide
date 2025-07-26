from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    phone: str

class UserCreate(UserBase):
    pass