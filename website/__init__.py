from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# import flask_whooshalchemy as wa
# import flask.ext.sqlalchemy as flask_sqlalchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    app.config['WHOOSH_BASE']='whoosh'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# def create_database(app):
#     if not path.exists("website/" + DB_NAME):
#         db.create_all(app=app)
#         print("Created database!")

# SQLAlchemy.create_all()
def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!")