import os 
from dotenv import load_dotenv

load_dotenv()
class Settings():
    DATABASE_URI = os.getenv("POSTGRES_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()