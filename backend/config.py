import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DB_URL')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('HS256')

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY')
