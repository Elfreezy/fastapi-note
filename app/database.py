
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base_model import BaseModel
from app.models.user_model import UserModel
from app.models.note_model import NoteModel
from config import settings

engine = create_engine(settings.DATABASE_URI)
Session = sessionmaker(engine)

def create_db_and_tables():
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    
    with Session() as session:
        user = UserModel(username="root")
        user.create_password_hash("root")

        note = NoteModel(title="title of note", note_description="desc of note")
        note.user = user 

        session.add(user)
        session.add(note)
        session.commit()