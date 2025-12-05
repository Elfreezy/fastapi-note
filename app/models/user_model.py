import jwt
from pwdlib import PasswordHash
from datetime import timedelta, datetime, timezone
from sqlalchemy import String, Integer, Boolean
from typing import List
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi import HTTPException, status

from config import settings
from app.models.base_model import BaseModel

PasswordHashObject = PasswordHash.recommended()

class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    password_hash: Mapped[str] = mapped_column(String(300))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    notes: Mapped[List["NoteModel"]] = relationship(back_populates="user")

    def create_password_hash(self, password) -> None:
        self.password_hash = PasswordHashObject.hash(password=password)
    
    def verify_password(self, plain_password) -> bool:
        return PasswordHashObject.verify(plain_password, self.password_hash)
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()

        if settings.ACCESS_TOKEN_EXPIRE_MINUTES:
            expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, algorithm=settings.ALGORITHM, key=settings.SECRET_KEY)
        return encode_jwt


    def __repr__(self):
        return f"id:{self.id}, username:{self.username}, is_admin:{self.is_admin}"



            