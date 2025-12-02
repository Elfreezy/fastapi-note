import starlette.status as status
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Optional


from app.services.note_service import note_service
from app.database import create_db_and_tables
from app.schemas.note_schema import NoteSchema

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
create_db_and_tables()


@app.get('/')
def get_all_notes(request: Request):
    context = {"request": request}
    notes = note_service.get_note_all()
    if notes:
        context["notes"] = notes
        
    response = templates.TemplateResponse("base.html", context=context)
    return response

@app.get('/add_note')
def add_note(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("note_create.html", context=context)
    return response


@app.post('/add_note')
def add_note(request: Request, title: str = Form(...), note_description: str = Form(...)):
    try:
        note_schema = NoteSchema(title=title, note_description=note_description)
        note_service.add_note(note_schema)

        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)

    return RedirectResponse("/", status_code=status.HTTP_304_NOT_MODIFIED)

@app.get('/update_note/{id}')
def update_note(request: Request, id:int):
    context = {"request": request}
    update_note = note_service.get_note_by_id(id)
    if update_note:
        context["note"] = update_note
    response = templates.TemplateResponse("note_update.html", context=context)
    return response

@app.post('/update_note/{id}')
def update_note(id: int, title: str = Form(...), note_description: str = Form(...), is_archive: bool = Form(None)):
    try:
        note = NoteSchema(title=title, note_description=note_description)
        if is_archive:
            note.is_archive = is_archive

        note_service.update_note(id, note)

        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)

    return RedirectResponse("/", status_code=status.HTTP_304_NOT_MODIFIED)


@app.get('/delete_note/{id}')
def delete_note(id: int):
    note_service.delete_note(id)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)