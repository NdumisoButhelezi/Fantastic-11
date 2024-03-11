from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdfghjkloiuytrdcvbnm'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth.routes import auth
    app.register_blueprint(auth)

    from app.student.routes import student
    app.register_blueprint(student, url_prefix='/student')

    # Register other blueprints...

    return app

