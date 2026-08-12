from pydantic import BaseModel, Field, model_validator, EmailStr
from typing_extensions import Self
from datetime import datetime

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., max_length=100, description="username of user")
    password: str = Field(..., min_length=8, max_length=250, description="password of user")

class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., max_length=100, description="username of user")
    password: str = Field(..., min_length=8, max_length=250, description="password of user")
    password_confirm: str = Field(..., min_length=8, max_length=250, description="confirm password of user")

    @model_validator(mode='after')
    def check_password_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Password & Confirm password doesn't match")
        return self



