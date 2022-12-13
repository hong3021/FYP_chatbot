from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)

    app.secret_key = 'cvbkjdh asdjksahdlj'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .view import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    from .model import User
    from .model import Chatlog

    with app.app_context():
        db.create_all()
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



