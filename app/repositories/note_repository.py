from sqlalchemy import select, delete, update
from app.database import Session
from app.models.note_model import NoteModel
from app.schemas.note_schema import NoteSchema



class NoteRepository():
    
    def get_note_all(self):
        with Session() as session:
            statement = select(NoteModel).order_by(NoteModel.id)
            notes = session.scalars(statement).all()
            return notes

    def add_note(self, note: NoteModel) -> None:
        with Session() as session:
            session.add(note)
            session.commit()
    
    def get_note_by_id(self, id: int) -> NoteModel:
        note = None
        with Session() as session:
            statement = select(NoteModel).where(NoteModel.id == id)
            note = session.scalars(statement=statement).one_or_none()
        
        return note
    
    def delete_note(self, id: int) -> None:
        with Session() as session:
            statement = delete(NoteModel).where(NoteModel.id == id)
            session.execute(statement)
            session.commit()
    
    def update_note(self, id: int, update_data: NoteSchema):
        with Session() as session:
            statement = update(NoteModel).where(NoteModel.id == id).values(**update_data.dict())
            session.execute(statement=statement)
            session.commit()
    


note_repository = NoteRepository()