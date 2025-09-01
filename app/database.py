from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    SECRET_KEY: str = "change_me_please"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "library"
    MYSQL_USER: str = "library_user"
    MYSQL_PASSWORD: str = "library_pass"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_CACHE_TTL_SECONDS: int = 30

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()

def get_db_url() -> str:
    s = get_settings()
    return f"mysql+pymysql://{s.MYSQL_USER}:{s.MYSQL_PASSWORD}@{s.MYSQL_HOST}:{s.MYSQL_PORT}/{s.MYSQL_DB}"

engine = create_engine(
    get_db_url(),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
