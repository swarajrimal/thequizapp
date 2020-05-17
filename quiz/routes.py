# Script to define routes for server

from flask import render_template, url_for, flash, redirect, request
from quiz import app, db, bcrypt
from quiz.forms import UserForm, RegistrationForm, LoginForm, QuestionForm
from quiz.models import Active, User, Questions
from flask_login import login_user, current_user, logout_user, login_required
import random, string, os
from sqlalchemy.sql.expression import func

cwd = os.getcwd()

@app.route("/")
@app.route("/home")  #Homepage
def home():
    if current_user.is_authenticated:       #If user is logged in then it redirects to accounts page
        return redirect(url_for('account'))
    return render_template('home.html')


@app.route("/activate", methods=['GET', 'POST'])
def activate():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    #if user is logged in then the login button will return to homepage
    form = UserForm()
    if form.validate_on_submit():
        codes = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(5)])
        with open(cwd+"/quiz/code.txt", "a") as fo:
            fo.write("%s: %s\n" % (form.username.data, str(codes)))
        active = Active(username=form.username.data, code=codes)
        db.session.add(active)  # add user to db
        db.session.commit()
        flash(f'Code sent for {form.username.data}!', 'success')
        return redirect(url_for('register'))
    return render_template('activate.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if Active.query.filter_by(username=form.username.data).first():
            dbcode = Active.query.filter_by(username=form.username.data).first().code
            if dbcode == form.code.data:
                hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #hash the password for db storage
                user = User(username=form.username.data, code=form.code.data, password=hash_pw)  #create an instance of the user
                db.session.add(user)   #add user to db
                db.session.commit()
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('login'))
            else:
                flash(f'Registration Unsuccessful. Please check code!', 'danger')
        else:
            flash(f'User not activated. Please activate first!', 'danger')
            return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    global count
    count=0
    if current_user.is_authenticated:
        return redirect(url_for('home'))    #if user is logged in then the login button will return to homepage
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()  # check if username exist in db
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # check if username and password match
            login_user(user, remember=form.remember.data)  # login the user
            return redirect(url_for('account'))
        else:
            flash(f'Login Unsuccessful. Please try again!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    score = User.query.filter_by(username=current_user.username).first().score
    page = request.args.get('page', 1, type=int)
    info = User.query.order_by(User.score.desc()).paginate(page, 5, False)
    next_url = url_for('account', page=info.next_num) if info.has_next else None
    prev_url = url_for('account', page=info.prev_num) if info.has_prev else None
    return render_template('account.html', title='Account', score=score, info=info.items, next_url=next_url, prev_url=prev_url)


count=0  #count for correct responses. A global variable to accumulate scores for current user
limit = 0   #counts the number of times a page is rendered. Limits to 10


@app.route("/quiz", methods=['GET', 'POST'])
@login_required
def quiz():
    if current_user.is_authenticated:
        global limit, count

        form = QuestionForm()

        id = Questions.query.order_by(func.random()).first().id
        question = Questions.query.filter_by(id=id).first().question
        answer = Questions.query.filter_by(id=id).first().answer
        option1 = Questions.query.filter_by(id=id).first().option1
        option2 = Questions.query.filter_by(id=id).first().option2
        option3 = Questions.query.filter_by(id=id).first().option3

        choice = [('answer',answer), ('option1',option1), ('option2',option2), ('option3',option3)]
        random.shuffle(choice)
        form.options.choices = choice

        if form.validate_on_submit():

            dat = form.options.data
            if dat == 'answer':
                flash(f'Correct!', 'success')
                count=count+1
            else:
                flash(f'Incorrect!', 'danger')

            if limit >= 10:
                limit=0

                score_user = current_user.username
                user = User.query.filter_by(username=score_user).first()
                user.score = count
                db.session.commit()
                return redirect(url_for('result'))

            return redirect(url_for('quiz'))
        limit = limit + 1

        return render_template('questions.html', title='Quiz', form=form, question=question, limit=str(limit))
    else:
        return redirect(url_for('login'))


@app.route("/result")
@login_required
def result():
    if current_user.is_authenticated:
        score = User.query.filter_by(username=current_user.username).first().score
        page = request.args.get('page', 1, type=int)
        info = User.query.order_by(User.score.desc()).paginate(page, 5 , False)
        next_url = url_for('result', page=info.next_num) if info.has_next else None
        prev_url = url_for('result', page=info.prev_num) if info.has_prev else None
        return render_template('result.html', title='Result', score=score, info=info.items, next_url=next_url, prev_url=prev_url)
    else:
        return redirect(url_for('login'))


@app.route("/replay", methods=['POST', 'GET'])   #If a user wants to play again, then clear the score from db and start again.
@login_required
def replay():
    global count
    user = User.query.filter_by(username=current_user.username).first()
    user.score = 0
    db.session.commit()
    count=0
    return redirect(url_for('quiz'))