# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = ""

class UserRead(BaseModel):
    uid: str
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = ""
    created_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None

class PostCreate(BaseModel):
    author_uid: str = Field(..., description="User uid who creates the post")
    content: str
    media: Optional[dict] = None

class PostRead(BaseModel):
    uid: str
    content: str
    media: Optional[dict]
    created_at: datetime
    author_uid: Optional[str] = None
