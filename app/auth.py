#helper modul za autentikaciju i autorizaciju.
#Ovdje se nalaze sve pomoćne funkcije za hashiranje lozinki i rad s JWT tokenima
#Brine se o sigurnosti korisnika; Hashira i provjerava lozinke (ne spremaju se kao običan tekst u bazi); 
# Generira i dekodira JWT tokene za login i autorizaciju

#!Servisi i funkcije za auth! ; u mapi routers su api endpointi
from __future__ import annotations
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from .database import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
