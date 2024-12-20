from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Updated for Pydantic V2


class Token(BaseModel):
    access_token: str
    token_type: str
