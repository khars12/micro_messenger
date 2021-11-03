from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('app.config')

socketio = SocketIO(app, cors_allowed_origins='*')

db = SQLAlchemy(app)

migrate = Migrate()
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'welcome'
login_manager.login_message = ''
login_manager.login_message_category = None

from app import views, models