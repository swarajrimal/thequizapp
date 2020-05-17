# Script to randomly generate questions, answer and options from the Movie database

from quiz import db
from quiz.models import Movie, Questions
from sqlalchemy.sql.expression import func

count = db.session.query(Movie).count()

def qnset1(ids):
    qn = "Which year did the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " release? "
    ans = Movie.query.filter_by(id=ids).first().movieyear
    while True:
        o1 = Movie.query.order_by(func.random()).first().movieyear
        o2 = Movie.query.order_by(func.random()).first().movieyear
        o3 = Movie.query.order_by(func.random()).first().movieyear
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):   # check if the set of options are unique to avoid duplicate choices
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

def qnset2(ids):
    qn = "Who directed the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " ? "
    ans = Movie.query.filter_by(id=ids).first().moviedirector
    while True:
        o1 = Movie.query.order_by(func.random()).first().moviedirector
        o2 = Movie.query.order_by(func.random()).first().moviedirector
        o3 = Movie.query.order_by(func.random()).first().moviedirector
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

def qnset3(ids):
    qn = "How long is the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " in mins.? "
    ans = Movie.query.filter_by(id=ids).first().movielength
    while True:
        o1 = Movie.query.order_by(func.random()).first().movielength
        o2 = Movie.query.order_by(func.random()).first().movielength
        o3 = Movie.query.order_by(func.random()).first().movielength
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

def qnset4(ids):
    qn = "What rating does the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " has in IMDB? "
    ans = Movie.query.filter_by(id=ids).first().movierating
    while True:
        o1 = Movie.query.order_by(func.random()).first().movierating
        o2 = Movie.query.order_by(func.random()).first().movierating
        o3 = Movie.query.order_by(func.random()).first().movierating
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

def qnset5(ids):
    qn = "Name actors in the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " ."
    ans = Movie.query.filter_by(id=ids).first().moviestars
    while True:
        o1 = Movie.query.order_by(func.random()).first().moviestars
        o2 = Movie.query.order_by(func.random()).first().moviestars
        o3 = Movie.query.order_by(func.random()).first().moviestars
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

def qnset6(ids):
    qn = "What genre does the movie "+ Movie.query.filter_by(id=ids).first().movietitle + " belong?"
    ans = Movie.query.filter_by(id=ids).first().moviegenre
    while True:
        o1 = Movie.query.order_by(func.random()).first().moviegenre
        o2 = Movie.query.order_by(func.random()).first().moviegenre
        o3 = Movie.query.order_by(func.random()).first().moviegenre
        optchk = [ans, o1, o2, o3]
        if len(optchk) == len(set(optchk)):
            break
    quest = Questions(question=qn, answer=ans, option1=o1, option2=o2, option3=o3)
    db.session.add(quest)

for i in range(1, count+1):
    qnset1(i)
    qnset2(i)
    qnset3(i)
    qnset4(i)
    qnset5(i)
    qnset6(i)

db.session.commit()