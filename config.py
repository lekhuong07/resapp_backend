import os

from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app._static_folder = os.path.abspath("static/")
app.secret_key = os.environ.get("SECRET_KEY")
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.resapp
entries = []