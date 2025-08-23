import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/nama_database")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secure-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 

settings = Settings()
