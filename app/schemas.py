#shema ulaznih i izlaznih podataka; koristi pydantic modele da bi fastapi automatski validirao podatke i 
# generirao openapi/swagger dokumentaciju; most između baze i api-ja
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field  #baza za Pydantic modele; specijalizirani tip koji provjerava je li string valjana email adresa; omogućava dodatna pravila validacije (npr. minimalna duljina stringa)
from typing import Optional

# Auth (registracija)
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

#update - naslov i autor također opcionalni jer ne moramo nužno ažurirati sve podatke
class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None

class BookOut(BookBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
