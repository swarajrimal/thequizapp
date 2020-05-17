from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '8e8c0af3aac4d7677a8089a5e5865b63'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)   #for database
bcrypt = Bcrypt(app)  #for password hash
login_manager = LoginManager(app)   #to manage login
login_manager.login_view = 'login'

from quiz.models import Movie, Questions
db.create_all()
from quiz import scrape
from quiz import questions
from quiz import routes

