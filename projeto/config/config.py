from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG')

    BASE_DIR = Path(__file__).resolve().parent.parent

    UPLOAD_USER = os.path.join(BASE_DIR, 'static', 'uploads', 'user')
    UPLOAD_PONTOS = os.path.join(BASE_DIR, 'static', 'uploads', 'pontos')

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    MYSQL_PORT = os.getenv('MYSQL_PORT')

    SUPERADMIN_EMAIL = os.getenv('SUPERADMIN_EMAIL')
    SUPERADMIN_PASSWORD = os.getenv('SUPERADMIN_PASSWORD')
    SUPERADMIN_USERNAME = os.getenv('SUPERADMIN_USERNAME')