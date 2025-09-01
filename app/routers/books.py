from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user
from ..cache import cache_get, cache_set, cache_del

router = APIRouter(prefix="/books", tags=["books"])

LIST_CACHE_KEY = "books:list"

@router.post("/", response_model=schemas.BookOut, status_code=201)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    book = models.Book(**payload.model_dump(), owner_id=user.id)
    db.add(book)
    db.commit()
    db.refresh(book)
    # Invalidate list cache
    cache_del(f"{LIST_CACHE_KEY}*")
    return book

@router.get("/", response_model=List[schemas.BookOut])
def list_books(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Check cache first
    cache_key = f"{LIST_CACHE_KEY}:user:{user.id}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached
    books = db.query(models.Book).filter(models.Book.owner_id == user.id).order_by(models.Book.id.desc()).all()
    data = [schemas.BookOut.model_validate(b).model_dump() for b in books]
    cache_set(cache_key, data)
    return data

@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.owner_id == user.id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.owner_id == user.id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    cache_del(f"{LIST_CACHE_KEY}*")
    return book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == book_id, models.Book.owner_id == user.id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    db.delete(book)
    db.commit()
    cache_del(f"{LIST_CACHE_KEY}*")
    return None
