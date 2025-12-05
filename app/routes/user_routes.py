from fastapi import APIRouter, Form, Request, status, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.schemas.user_schema import UserSchema, UserLoginSchema
from app.models.user_model import UserModel
from app.services.user_service import user_service

user_routes = APIRouter(prefix="/users")
templates = Jinja2Templates(directory="app/templates")

@user_routes.get("/")
async def root():
    return {"users": user_service.get_user_all()}

@user_routes.get("/add_user/")
async def add_user(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("users/register_user.html", context=context)
    return response


@user_routes.post("/add_user/")
async def add_user(request: Request):
    form_data = await request.form()
    if form_data:
        user_form_data = UserSchema(username=form_data.get("username"), password=form_data.get("password"))
        user_service.create_user(user_form_data=user_form_data, password_repeat=form_data.get("password_repeat"))

    redirect_url = request.url_for("get_user_all")
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@user_routes.get('/login')
async def login_user(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("users/login_user.html", context=context)
    return response

@user_routes.post('/login')
async def login_user(request: Request):
    context = {"request": request}
    response = RedirectResponse(request.url_for("get_me"), status_code=status.HTTP_302_FOUND)
    form_data = await request.form()

    if form_data:
        user_form_data = UserLoginSchema(username=form_data.get("username"), password=form_data.get("password"))
        user = user_service.login_user(user_form_data)
        if user:
            context["user"] = user
            access_token = user.create_access_token({"sub": user.username})
            response.set_cookie(key="access_token", value=access_token)

    return response

@user_routes.get("/all_users/")
async def get_user_all(request: Request):
    context = {"request": request}

    users = user_service.get_user_all()
    if users:
        context["users"] = users

    response = templates.TemplateResponse("users/users.html", context=context)
    return response

@user_routes.get("/me/")
async def get_me(request: Request, current_user: UserModel = Depends(user_service.get_current_user)):
    context = {"request": request, "user": current_user}
    response = templates.TemplateResponse("users/user.html", context=context)
    return response

@user_routes.get("/logout/")
async def logout_user(request: Request):
    response = RedirectResponse(request.url_for("login_user"), status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    print(response)
    return response

