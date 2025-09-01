from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Books
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None

class BookOut(BookBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
