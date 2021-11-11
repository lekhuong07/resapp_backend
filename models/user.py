import json
import uuid

from argon2.exceptions import VerifyMismatchError
from flask import session
from database import Database
from argon2 import PasswordHasher
from datetime import date
from datetime import datetime

from models.helpers import valid_datetime, generate_random_password
from models.mailgun import Mailgun

ph = PasswordHasher()


class User(object):
    def __init__(self, email, password, name=None, dob=None, application=None, ps=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.email = email
        self.password = password
        self.name = email if name is None else name
        self.dob = date.today().strftime("%m/%d/%Y") if dob is None else dob
        self.statement = "Change your personal statement here" if ps is None else ps
        self.application = [] if application is None else application

    def get_user_id(self):
        return self._id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {'email': email})
        if data is not None:
            return cls(**data)  # default is None

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        # User.login_valid(...., .....) check if user's email matches the password
        user = User.get_by_email(email)
        if user is not None:
            #  check the password
            try:
                return ph.verify(user.password, password)
            except VerifyMismatchError:
                return False
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:  # user doesn't exist
            password = ph.hash(password)
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            flag, sample_application = new_user.add_application("Position name", "Sample company")
            if not flag:
                return False, "Session is not created"
            return True, "Registered"
        else:
            return False, "Email exists"

    @classmethod
    def reset_password(cls, email):
        user = cls.get_by_email(email)
        if user is None:  # user doesn't exist
            return False, "Email does not exist"
        else:
            new_password = generate_random_password()
            subject = "Reset password"
            text = f"Your new password is: {new_password}"
            flag1, message1 = Mailgun.send_mail(email, subject, text, html=None)
            if flag1 is False:
                return message1
            flag2, message2 = user.change_password(email, new_password)
            if flag2 is False:
                return message2
            return message2

    @classmethod
    def change_password(cls, email, new_password):  # this function is called when user exists.
        user = cls.get_by_email(email)
        query = {'email': user.email}, {"$set": {"password": ph.hash(new_password)}}
        Database.update_one(
            "users",
            *query
        )
        return True, "Password changed"

    @staticmethod
    def login(user_email):
        #  login_valid has called been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "dob": self.dob,
            "ps": self.statement,
            "application": self.application
        }

    @classmethod
    def get_profile(cls):
        if 'email' in session:
            email = session['email']
        else:
            return False, 'Need to login to do it'

        user_data = cls.get_by_email(email)
        if user_data is None:
            return False, 'There is no email'
        return True, user_data.json()

    @classmethod
    def edit_profile(cls, name, dob, statement):
        if name == '':
            return False, 'Name cannot be empty'

        flag_date = valid_datetime(dob)
        if not flag_date:
            return False, "Date format is invalid"

        if statement == '':
            return False, 'Name cannot be empty'

        if 'email' in session:
            email = session['email']
        else:
            return False, 'Need to login to do it'

        query = {'email': email}, {"$set": {"name": name, "dob": dob, "ps": statement}}
        Database.update_many(
            "users",
            *query
        )
        return True, "Profile changed"

    @classmethod
    def add_application(cls, company, position):
        daytime = date.today().strftime("%m/%d/%Y")
        status = "initialized"  # 4 states: initialized, interviewed, accepted, denied
        if 'email' in session:
            email = session['email']
        else:
            return False, 'Need to login to do this function'

        apply = {
            "_id": uuid.uuid4().hex,
            "details": [company, position, daytime, status]
         }
        query = {'email': email}, {'$push': {'application': apply}}
        Database.update_one(
            "users",
            *query
        )
        return True, "Application added"

    @classmethod
    def get_application(cls, _id=None):
        if 'email' in session:
            email = session['email']
        else:
            return False, 'Need to login to do this function'
        user = cls.get_by_email(email)
        if not _id:
            return True, user.application

        for ua in user.application:
            if ua['_id'] == _id:
                return True, ua

        return False, "No application found"

    @classmethod
    def update_application(cls, _id, status):
        # 4 states: initialized, interviewed, accepted, denied
        # status == failed -> go straight to denied
        # status == success -> initialized -> interviewed -> accepted
        daytime = date.today().strftime("%m/%d/%Y")
        flag, curr = cls.get_application(_id)
        if not flag:
            return curr  # curr is a message
        curr_data = curr['details']

        if 'email' in session:
            email = session['email']
        else:
            return False, "Need to login to do this"
        curr_status = curr_data[-1]
        if curr_status == 'denied' or curr_status == 'accepted':
            return False, "Reach the end of the process"

        if status == "success":
            new_status = "interviewed" if curr_status == 'initialized' else 'accepted'
            message = "Congratulations"
        else:
            new_status = 'denied'
            message = "Unfortunately"

        query = {'email': email, 'application._id': _id}, \
                {'$set': {'application.$.details': [curr_data[0], curr_data[1], daytime, new_status]}}
        Database.update_many(
            "users",
            *query
        )
        return True, message

    @classmethod
    def delete_application(cls, _id):
        if 'email' in session:
            email = session['email']
        else:
            return False, 'Need to login to do this function'

        query = {'email': email}, {'$pull': {'application': {'_id': _id}}}
        Database.update_one(
            "users",
            *query
        )
        return True, "Application is deleted"

    def save_to_mongo(self):
        Database.insert("users", self.json())
