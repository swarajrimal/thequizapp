# The Quiz App
A movie-based quiz app for friends to play built using Flask/Python and SQLite

This project is my first try on building a full application using Flask/Python. It is a movie quiz based game that is to be played among friends and compare the scores. The application incorporates a lot of packages and modules, mostly based on Flask. It also includes building HTML pages that are rendered into various views. The SQLAlchemy toolkit for Flask is useful and very simple to work with Flask-SQLite interface.

## Approach
The approach in building this project was to first learn about using Flask and incorporate it with the database. The first component that I built was a user management system. It includes creating database models to store user details and creating forms to accept registration and login details. Since an activation method is also incorporated, a separate form to accept username and generate a unique code is also created. To generate the code and write to a file, a read/write system of Python is used. User sessions are managed by the LoginManager component of flask_login module.

Second part of the project was to create a script that would scrape the website data from IMDB and store the movie details to a database. Tons of resources are available online on how to do a scrape from website using Python. The movie details are stored first in separate containers and then pushed into the database after some cleaning. This way, the database is populated with the movie details such as movie name, length, release year and so on.

Next, sets of questions needed to be generated using the movie information that was stored in the database. I wrote a separate script to do the same. 6 sets of questions are generated for each entry in the movie database. These 6 questions are based on the movie name, and asks various information about that movie. For e.g., 'What year was the movie released?' and so on. Each question generated is stored in a separate row on a new database table. The corresponding columns store the answer for the question, and 3 randomly selected unique options from the movie database. This way, each row of the questions database contains a question, the answer and 3 random choices.

The final step was to incorporate the questions and answeres from the question database into a form that would display the questions randomly. The form also displays the choices in form of radio buttons, one of them being the correct answer. This incorporation is done using Flask and the logic is such that once the user submits the form, a new form is generated with another random question-choices set. Correct entries are recorded as scores. The form generation is done 10 times form 10 questions, and after answering the final question, the score is updated in the user database. Re-taking the quiz and logging out of the session resets the user score.

Lastly, paginated tables are also used in certain views to list and display the user scores in descending order.

## Setup
Application setup is fairly simple and can be invoked using the terminal command line. 

#### Repository Structure
The repository contains the application package **quiz**, a run file **quizapp.py** and a dependency management file **requirements.txt**. The main application package **quiz** is a directory that contains all the scripts and templates required to run the application. The package structure is as follows:
```
├── __init__.py
├── code.txt
├── forms.py
├── models.py
├── questions.py
├── routes.py
├── scrape.py
├── site.db
└── templates
    	├── account.html
    	├── activate.html
    	├── home.html
    	├── layout.html
    	├── login.html
    	├── questions.html
    	├── register.html
    	├── replay.html
    	└── result.html
```
The **templates** directory contains all the HTML templates correspoinding to different views on the application that are rendered within the **route.py** script. The script **scrape.py** scrapes IMDB website for movie details and stores them in the *Movie* database. Similarly, **questions.py** reads the *Movie* database, generates questions and the options, and stores them in *Questions* database. Scripts **models.py** and **forms.py** defines the database models and form structures respectively. Routing information and main logic is defined in **routes.py**. The application, database and other packages are invoked in **\_\_init.py\_\_**, which is run first by the main application script. Files such as **code.txt** and **site.db** are created during the first run of the application.


#### Prerequisites
The environment needs to be setup before running the application. The application is built using Python 3.8.3rc1. Clone the repository on a virtual environment created using Python3. All the packages needed for the application to run is mentioned in **requirements.txt** file. Environment can be setup by installing all the components mentioned in the file. It can be done in a single command line expression.
```bash
$ pip install -m requirements.txt
```
This will install all the required packages to the environment suitable to run the application.

#### Running the application
The application run script is located in the repository and is named **quizapp.py**. To run the application, do the following in command line.
```bash
$ python quizapp.py
```
Running this script will initialize the application, initialize the database, scrape the IMDB website, stores them in database, generate questions using that data and store the questions and other options in the database. After all the initializations, it starts the application server and returns a URL, which is typically the localhost:5000. Copy the URL from the terminal and access it using any web browsers (I used Chrome) as front-end.

All this happens during the first run of the application. For subsequent runs, the database tables related to Movie and Questions needs to be dropped. 

## Using the Application
Once the application server is up and running, and the URL is accessed using the web browser, The first view is that of home screen. On this view, first time users can either activate their username, or returning users can login. 

#### User Activation
Upon clicking the *Activate Here* button on the homepage, the user is directed to the activation view. New users need to activate their username to get a code generated in the backend. This is done to make sure the application is used by a selected group of users only. Once the user enters a username and submits the form in the activation view, the code is generated against that username and is stored in **code.txt** file within the **quiz** directory. This code needs to be explicitly and manually provided the user for further registration. The user is redirected to the registration view.

#### User Registration
The registration view contains the form that enables the user to register themselves using the chosen username, the received code and a password. The username-code combination is unique to the activated user and they can register only using the same combination. After filling out and submitting the form, the user details is recorded in the *User* database and the registration is complete. The user is redirected to the login view where they can log into their session.

#### User Login
On the login view, the user can enter the username and password they registered with and submit the form. Their session is now active. A text containing the username and a *Logout* button is displayed in each page the user accesses. User login management is done via the **LoginManager** module of **Flask**. The user is redirected to the accounts view that contains a link to access the quiz, and a paginated table showing the high scores of all the users. Upon accessing the link to take the quiz, the user is redirected to the quiz view.

#### Taking the Quiz
The quiz view consists of a multiple choice question-answer form field with a randomly generated question, and 4 radio button choices. The questions and choices are generated randomly from the Quiz table each time the user answers a question. Every time the choice is correct, the score is incremented by 1 and a success message is flashed.

#### Logging Out
Users who are logged in can logout anytime from any view on the application. The logout action resets the user score to 0 and updates the table. The paginated tables are updated accordingly.

## Re-Running the Application
Once the application has been run for the first time, it initializes and creates all the required database tables using the models defined. Terminating the appliacation and re-running the same will try to populate the same values into those database. It is therefore needed to drop those tables before trying to re-run the application server. On the Python environment, use the SQLite instance to do the same.
```python
from quiz import db
from quiz.models import Movie, Questions
db.drop_all()
```
After the tables are dropped, the application can be re-run from the command line.
```bash
$ python quizapp.py
```

## Build
The application is built using the following:
* [Python](https://www.python.org/) - Platform
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Application Server
* [SQLite](https://www.sqlite.org/index.html) - Database 
* [SQLAlchemy](https://www.sqlalchemy.org/) - Flask-based database toolkit
* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE
