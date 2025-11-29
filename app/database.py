
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base_model import BaseModel

engine = create_engine("postgresql+psycopg2://postgres:root@127.0.0.20:5432/test_db")
Session = sessionmaker(engine)

def create_db_and_tables():
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)