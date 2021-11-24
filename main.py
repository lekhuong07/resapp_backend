from datetime import timedelta

from dotenv import load_dotenv
from flask import session, render_template

import api.authenticate
import api.profile
import api.resume
import os

from config import app
from database import Database
from models.mailgun import Mailgun
from models.user import User

load_dotenv()


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


'''
@app.route("/", methods=["GET", "POST"])
def hello_world():
    print([e for e in app.db.entries.find({})])
    # app.db.entries.delete_many({"content": "resume-app"})
    return "Hello"
'''


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/profile')  # profile page that return 'profile'
def profile():
    prof = User.get_profile()
    return render_template('profile.html', name=prof[1]['name'])
