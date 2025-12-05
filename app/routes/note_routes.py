import starlette.status as status
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.note_service import note_service
from app.schemas.note_schema import NoteSchema

note_routes = APIRouter(prefix="/notes")
templates = Jinja2Templates(directory="app/templates/notes")



@note_routes.get('/')
def get_all_notes(request: Request):
    context = {"request": request}
    notes = note_service.get_note_all()
    if notes:
        context["notes"] = notes
        
    response = templates.TemplateResponse("notes.html", context=context)
    return response

@note_routes.get('/add_note')
def add_note(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("note_create.html", context=context)
    return response


@note_routes.post('/add_note')
def add_note(request: Request, title: str = Form(...), note_description: str = Form(...)):
    try:
        note_schema = NoteSchema(title=title, note_description=note_description)
        note_service.add_note(note_schema)

        return RedirectResponse("/notes", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)

    return RedirectResponse("/notes", status_code=status.HTTP_304_NOT_MODIFIED)

@note_routes.get('/update_note/{id}')
def update_note(request: Request, id:int):
    context = {"request": request}
    update_note = note_service.get_note_by_id(id)
    if update_note:
        context["note"] = update_note
    response = templates.TemplateResponse("note_update.html", context=context)
    return response

@note_routes.post('/update_note/{id}')
def update_note(id: int, title: str = Form(...), note_description: str = Form(...), is_archive: bool = Form(None)):
    try:
        note = NoteSchema(title=title, note_description=note_description)
        if is_archive:
            note.is_archive = is_archive

        note_service.update_note(id, note)

        return RedirectResponse("/notes", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)

    return RedirectResponse("/notes", status_code=status.HTTP_304_NOT_MODIFIED)


@note_routes.get('/delete_note/{id}')
def delete_note(id: int):
    note_service.delete_note(id)
    return RedirectResponse("/notes", status_code=status.HTTP_303_SEE_OTHER)