from datetime import timedelta

from dotenv import load_dotenv
from flask import session

import api.authenticate
import api.profile
import api.resume
import os

from config import app
from database import Database
from models.mailgun import Mailgun

load_dotenv()


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.route("/", methods=["GET", "POST"])
def hello_world():
    print([e for e in app.db.entries.find({})])
    # app.db.entries.delete_many({"content": "resume-app"})
    return "Hello"


@app.route("/fancy")
def hello_fancy():
    return """
    <html>
    <body>
    
    <h1> Greetings! </h1>
    <p> Hello, world! <\p>
    
    </body>
    </html>
    """
