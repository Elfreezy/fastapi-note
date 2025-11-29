from fastapi import FastAPI, Request
from app.services.note_service import note_service
from app.database import create_db_and_tables
from app.schemas.note_schema import NoteSchema

app = FastAPI()
create_db_and_tables()


@app.get('/notes')
def get_all_notes():
    return note_service.get_note_all()

@app.post('/add_note')
def add_note(title: str, full_name: str):
    note_service.add_note(title, full_name)
    return {"result": "success added"}

@app.post('/update_note')
def update_note(id: int, update_note: NoteSchema):
    note_service.update_note(id, update_note)
    return {"result": "success updated"}

@app.post('/delete_note')
def delete_note(id: int):
    note_service.delete_note(id)
    return {"result": "success deleted"}