from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str 
    full_name: str