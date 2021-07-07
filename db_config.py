import os
from datetime import timedelta


class Config:
    APPLICATION_DIR = os.getcwd()
    UPLOAD_FOLDER = os.path.abspath('./uploads')

    #Conexão com o SQLite
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{APPLICATION_DIR}/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.urandom(16)
    SESSION_TYPE = 'sqlalchemy'
    PERMANENT_SESSION_LIFETIME = timedelta(hours = 6)