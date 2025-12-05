from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str 
    password: str
    is_admin: bool = False


class UserLoginSchema(BaseModel):
    username: str
    password: str