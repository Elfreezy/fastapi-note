from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str 
    note_description: str
    is_archive: bool = False