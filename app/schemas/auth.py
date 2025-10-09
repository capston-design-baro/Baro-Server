from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str
    address: str
    phone_number: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('비밀번호는 최소 8자 이상이어야 합니다')
        if len(v) > 72:
            raise ValueError('비밀번호는 최대 72자까지 가능합니다')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    address: str
    phone_number: str
    created_at: datetime

    class Config:
        from_attributes = True