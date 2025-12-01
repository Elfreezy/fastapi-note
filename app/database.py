
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base_model import BaseModel
from config import settings

engine = create_engine(settings.DATABASE_URI)
Session = sessionmaker(engine)

def create_db_and_tables():
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)