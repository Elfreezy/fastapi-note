from typing import Optional 
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    full_name: Mapped[Optional[str]]

    def __repr__(self):
        return f"id:{self.id}, title:{self.title}, full_name:{self.full_name}"