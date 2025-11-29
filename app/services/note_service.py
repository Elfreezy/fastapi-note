
from app.repositories.note_repository import note_repository
from app.models.note_model import NoteModel
from app.schemas.note_schema import NoteSchema

class NoteService():
    def __init__(self, repository):
        self.repositoty = repository
    
    def get_note_all(self):
        return self.repositoty.get_note_all()
    
    def add_note(self, title: str, full_name: str):
        note = NoteModel(title=title, full_name=full_name)
        note_repository.add_note(note)

    def delete_note(self, id: int):
        note_repository.delete_note(id)

    def update_note(self, id: int, update_data: NoteSchema):
        note_repository.update_note(id, update_data)

note_service = NoteService(note_repository)