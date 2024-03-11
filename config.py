import os

class Config:
    SECRET_KEY = 'your_secret_key_here'  # Replace 'your_secret_key_here' with a real secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///yourdatabase.db'  # Replace 'yourdatabase.db' with your database path
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To avoid SQLAlchemy warning, you can disable track modifications
