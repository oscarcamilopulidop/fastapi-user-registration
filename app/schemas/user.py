from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional


class EmailUser(BaseModel):
    email: EmailStr = Field(..., example="johndoe@example.com")


class BaseUser(EmailUser):
    password: str = Field(..., min_length=8, example="yourpassword")


class VerificationUser(BaseModel):
    email: str = Field(..., example="johndoe@example.com")
    verification_code: Optional[str] = Field(..., example="0240")

    @validator("verification_code")
    def validate_verification_code(cls, v):
        if not v.isdigit():
            raise ValueError("verification_code must be a digit")
        if len(v) != 4:
            raise ValueError("verification_code must be 4 digits long")
        return v


class User(BaseUser):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    verification_code: Optional[str] = Field(
        ..., example="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
    )
    verification_code_expiry: Optional[datetime] = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(minutes=1)
    )
    is_verified: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "yourpassword",
                "created_at": "2022-01-01T00:00:00",
                "verification_code": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "verification_code_expiry": "2022-01-01T00:01:00",
                "is_verified": False,
            }
        }
