# Script to model the databases

from quiz import db, login_manager
from flask_login import UserMixin

#Login manager to manage users logged in

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

#db to manage users

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    score = db.Column(db.Integer)

#print user details
    def __repr__(self):
        return f"User('{self.username}', '{self.score}')"


#db to manage codes
class Active(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    code = db.Column(db.String(5), unique=True, nullable=False)

    def __repr__(self):
        return f"Code('{self.username}, {self.code}')"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movietitle = db.Column(db.String(50), nullable=False)
    movieyear = db.Column(db.String(4))
    movielength = db.Column(db.String(10))
    movierating = db.Column(db.Float)
    moviegenre = db.Column(db.String(50))
    moviedirector = db.Column(db.String(100))
    moviestars = db.Column(db.String(500))

    def __repr__(self):
        return f"Movie('{self.movietitle}, {self.movieyear},{self.movielength}, {self.movierating}, " \
               f"{self.moviegenre},{self.moviedirector}, {self.moviestars}')"

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(50), nullable=False)
    option1 = db.Column(db.String(50), nullable=False)
    option2 = db.Column(db.String(50), nullable=False)
    option3 = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Questions('{self.question}, {self.answer}, {self.option1}, {self.option2}, {self.option3}')"