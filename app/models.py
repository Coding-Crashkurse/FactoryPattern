"""Pydantic models for User API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """User creation request schema."""

    username: str
    email: EmailStr


class User(BaseModel):
    """User response model."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime
