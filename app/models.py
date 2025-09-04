#schemas kako izgleda prema api-ju; models kako pohranjeni podaci u bazi
from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) #primarni ključ
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False) #nullable=false znači da je obavezno polje
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    books: Mapped[list['Book']] = relationship(back_populates="owner") #veza 1:N (1..*)

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String(64), unique=False, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False) #strani ključ
    owner: Mapped[User] = relationship(back_populates="books") #veza prema user-u
