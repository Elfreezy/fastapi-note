import os 
from dotenv import load_dotenv

load_dotenv()
class Settings():
    DATABASE_URI = os.getenv("POSTGRES_URI")

settings = Settings()