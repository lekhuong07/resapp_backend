from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from rake_nltk import Rake
import nltk
#import boto3
import os

load_dotenv()


app = Flask(__name__)
app._static_folder = os.path.abspath("static/")
app.secret_key = os.environ.get("SECRET_KEY")
client = MongoClient(os.environ.get("MONGODB_URI"))
"""
s3_client = boto3.client('s3',
                         region_name=os.environ.get("S3_REGION"),
                         aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"))
"""

app.db = client.resapp
nltk.download('stopwords')
nltk.download('punkt')
rake = Rake()
entries = []
