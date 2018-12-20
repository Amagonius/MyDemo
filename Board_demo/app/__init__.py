from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'


from app import views, models
