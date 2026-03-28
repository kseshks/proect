from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str

class TokenData(BaseModel):
    username: str
    user_id: str
    user_type: str