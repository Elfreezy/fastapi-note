
from app.repositories.note_repository import note_repository
from app.models.note_model import NoteModel
from app.schemas.note_schema import NoteSchema

class NoteService():
    def __init__(self, repository):
        self.repositoty = repository
    
    def get_note_all(self):
        return self.repositoty.get_note_all()
    
    def add_note(self, note_schema):
        note = NoteModel(title=note_schema.title, note_description=note_schema.note_description)
        note_repository.add_note(note)

    def delete_note(self, id: int):
        note_repository.delete_note(id)

    def update_note(self, id: int, update_data: NoteSchema):
        note_repository.update_note(id, update_data)

    def get_note_by_id(self, id: int) -> NoteModel:
        return note_repository.get_note_by_id(id)

note_service = NoteService(note_repository)