from typing import Optional 
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    note_description: Mapped[Optional[str]]
    is_archive: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f"id:{self.id}, title:{self.title}, note_description:{self.note_description}, is_archive:{self.is_archive}"