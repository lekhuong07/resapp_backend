from datetime import timedelta
from flask import session, render_template


from config import app
from database import Database
from models.user import User

from api import authenticate
from api import profile
from api import resume
from api import helpers


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/profile')  # profile page that return 'profile'
def profile():
    prof = User.get_profile()
    return render_template('profile.html', name=prof[1]['name'])


if __name__ == '__main__':
    app.run()