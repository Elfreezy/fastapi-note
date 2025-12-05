from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import create_db_and_tables
from app.routes.user_routes import user_routes
from app.routes.note_routes import note_routes

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()
app.include_router(user_routes)
app.include_router(note_routes)

create_db_and_tables()


@app.get("/")
def root(request: Request):
    return RedirectResponse("/users/login", status_code=status.HTTP_302_FOUND)

