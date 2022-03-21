import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'main_blueprint.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('main/settings.py')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate()



    from server.transfer.routes import post
    from server.main.routes import main
    from server.additional_pages.routes import additional
    app.register_blueprint(main)
    app.register_blueprint(post)
    app.register_blueprint(additional)

    migrate.init_app(app, db, render_as_batch=True)
    return app


appctx = create_app()


def resset_db():
    with appctx.app_context():
        from server.models import User
        from server.models import Head
        from server.models import Tag
        db.drop_all()
        db.create_all()
        hashed_password = bcrypt.generate_password_hash('1234').decode('utf-8')
        admin_pass = bcrypt.generate_password_hash('1234').decode('utf-8')
        user = User(username='Mike', email='1234@gmail.com', password=hashed_password, role=True)
        head = Head(username = '01', password = admin_pass)
        tag = Tag(name='123456789', price=1500)
        db.session.add(user)
        db.session.add(head)
        db.session.add(tag)
        db.session.commit()


def create_user():
    with appctx.app_context():
        if os.path.exists(f'{os.path.abspath(os.path.dirname(__file__))}\\server.db'):
            resset_db()
        else:
            db.create_all()