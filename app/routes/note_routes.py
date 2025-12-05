import starlette.status as status
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas.note_schema import NoteSchema
from app.models.user_model import UserModel
from app.services.note_service import note_service
from app.services.user_service import user_service

note_routes = APIRouter(prefix="/notes")
templates = Jinja2Templates(directory="app/templates")



@note_routes.get('/')
async def get_all_notes(request: Request, current_user: UserModel = Depends(user_service.get_current_user)):
    context = {"request": request}
    notes = note_service.get_note_by_user(current_user)
    if notes:
        context["notes"] = notes
        
    response = templates.TemplateResponse("notes/notes.html", context=context)
    return response

@note_routes.get('/add_note')
async def add_note(request: Request, current_user: UserModel = Depends(user_service.get_current_user)):
    context = {"request": request}
    response = templates.TemplateResponse("notes/note_create.html", context=context)
    return response


@note_routes.post('/add_note')
async def add_note(request: Request, title: str = Form(...), note_description: str = Form(...), current_user: UserModel = Depends(user_service.get_current_user)):
    try:
        note_schema = NoteSchema(title=title, note_description=note_description)
        note_service.add_note(note_schema, current_user)

        return RedirectResponse("/notes", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        print(e)

    return RedirectResponse("/notes", status_code=status.HTTP_304_NOT_MODIFIED)

@note_routes.get('/update_note/{id}')
async def update_note(request: Request, id:int, current_user: UserModel = Depends(user_service.get_current_user)):
    context = {"request": request}
    update_note = note_service.get_note_by_id(id)
    if update_note:
        context["note"] = update_note
    response = templates.TemplateResponse("notes/note_update.html", context=context)
    return response

@note_routes.post('/update_note/{id}')
async def update_note(id: int, title: str = Form(...), note_description: str = Form(...), is_archive: bool = Form(None), current_user: UserModel = Depends(user_service.get_current_user)):
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
async def delete_note(id: int, current_user: UserModel = Depends(user_service.get_current_user)):
    note_service.delete_note(id)
    return RedirectResponse("/notes", status_code=status.HTTP_303_SEE_OTHER)