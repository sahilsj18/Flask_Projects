import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'efcd620756f3bda78f406bca22517ac546f42333d70e417bed9bfb8d41317288')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql%4024@localhost/football_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
