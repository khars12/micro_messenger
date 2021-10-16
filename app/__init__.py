from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'welcome'
login_manager.login_message = ''
login_manager.login_message_category = None

from app import views, models