from app.models.user_model import UserModel
from app.database import Session

class UserRepository():
    def add_user(self, user):
        with Session() as session:
            session.add(user)
            session.commit()
    
    def get_user_by_id(self, id: int) -> None | UserModel:
        user = None
        with Session() as session:
            user = session.query(UserModel).filter(UserModel.id == id).one_or_none()
        return user
    
    def get_user_by_username(self, username: str) -> None | UserModel:
        user = None
        with Session() as session:
            user = session.query(UserModel).filter(UserModel.username == username).one_or_none()
        return user
    
    def get_user_all(self) -> None | list:
        users = None
        with Session() as session:
            users = session.query(UserModel).all()
        return users


user_repository = UserRepository()