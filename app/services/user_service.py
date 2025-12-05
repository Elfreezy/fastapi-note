import jwt
from config import settings

from fastapi import HTTPException, status, Request
from app.schemas.user_schema import UserSchema, UserLoginSchema
from app.models.user_model import UserModel
from app.repositories.user_repository import user_repository



class UserService():

    def __init__(self, repository):
        self.repository = repository

    def create_user(self, user_form_data: UserSchema, password_repeat: str) -> None:
        if not user_form_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Данные отсутствуют")
        
        if user_form_data.password != password_repeat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароль не совпадает")
        
        if self.repository.get_user_by_username(user_form_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким именем уже зарегистрирован")
        
        user = UserModel(username=user_form_data.username)
        user.create_password_hash(password=user_form_data.password)
        self.repository.add_user(user)
    
    def login_user(self, user_form_data: UserLoginSchema) -> None | UserModel:
        user = self.repository.get_user_by_username(user_form_data.username)

        if not user or not user.verify_password(user_form_data.password):
            raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail="Некорректное имя или пароль")

        return user

    def get_user_by_id(self, id: int) -> None | UserModel:
        return self.repository.get_user_by_id(id)
    
    def get_user_by_username(self, username: str) -> None | UserModel:
        return self.repository.get_user_by_username(username)
    
    def get_user_all(self) -> None | list:
        return self.repository.get_user_all()
    
    def get_current_user(self, request: Request) -> None | UserModel:
        token = request.cookies.get("access_token")
        user = None

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не авторизован")
        
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username = payload.get("sub")
        if username:
            user = user_service.get_user_by_username(username=username)

            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
            
        return user


user_service = UserService(user_repository)