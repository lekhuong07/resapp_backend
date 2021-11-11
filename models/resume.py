import uuid

from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from flask import session
from database import Database
from argon2 import PasswordHasher
import datetime
from datetime import datetime

from models.helpers import valid_datetime
from models.user import User

ph = PasswordHasher()


class Resume(object):
    def __init__(self, title, user_id, _id=None, section=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.user_id = user_id
        self.title = title
        self.section = [] if section is None else section

    @classmethod
    def get_resume_from_session(cls, _id=None):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"
        user_id = user_data['_id']

        if _id is None:
            data = Database.find("resumes", {'user_id': user_id})
            if data is None:
                return False, "No resumes found"
            result = [cls(**d).json() for d in data]
        else:
            data = Database.find_one("resumes", {'user_id': user_id, '_id': _id})
            if data is None:
                return False, "No resumes found"
            result = cls(**data).json()

        return True, result

    @classmethod
    def add_resume(cls, title):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"
        user_id = user_data['_id']

        flag, data = cls.get_resume_from_session()
        if flag is False:
            return False, "No profile found"
        if len(data) == 4:
            return False, "Reach limit number of resumes"
        new_resume = cls(title, user_id)
        new_resume.save_to_mongo()
        return True, "Resume added"

    @classmethod
    def change_title(cls, resume_id, title):  # this function is called when user exists.
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']

        query = {'_id': resume_id, 'user_id': user_id}, {"$set": {"title": title}}
        Database.update_one(
            "resumes",
            *query
        )
        return True, "Title changed to " + title

    @classmethod
    def delete_resume(cls, resume_id):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        query = {'_id': resume_id, 'user_id': user_id}, {}
        Database.delete_one(
            "resumes",
            *query
        )
        return True, "Resume is deleted"

    def save_to_mongo(self):
        Database.insert("resumes", self.json())

    def json(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "title": self.title,
            "section": self.section,
        }


class Section(object):
    def __init__(self, name, experiences=None, skills=None, _id=None, **kwargs):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.name = name
        self.experiences = [] if experiences is None else experiences
        self.skills = [] if skills is None else skills

    @classmethod
    def get_section_from_session(cls, resume_id, section_id=None):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"
        user_id = user_data['_id']
        data = Database.find_one("resumes", {'user_id': user_id, '_id': resume_id})
        if data is None:
            return False, "No sections found"
        result = None
        if section_id is None:
            result = data['section']
        else:
            for d in data['section']:
                if d['_id'] == section_id:
                    result = d
                    break
            if result is None:
                return False, "No sections found"
        return True, result

    @classmethod
    def add_section(cls, resume_id, name):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        if flag is False:
            return False, "No profile found"

        new_section = cls(name).json()
        query = {'_id': resume_id, 'user_id': user_id}, {'$push': {'section': new_section}}
        Database.update_one(
            "resumes",
            *query
        )
        return True, "Section added"

    @classmethod
    def edit_section_name(cls, resume_id, section_id, new_name):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        query = {'_id': resume_id, 'section._id': section_id, 'user_id': user_id}, \
                {'$set': {'section.$.name': new_name}}
        Database.update_many(
            "resumes",
            *query
        )
        return True, "Section name changed"

    @classmethod
    def delete_section(cls, resume_id, section_id):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        query = {'_id': resume_id, 'user_id': user_id}, {'$pull': {'section': {'_id': section_id}}}
        Database.update_one(
            "resumes",
            *query
        )
        return True, "Section is deleted"

    def save_to_mongo(self):
        Database.insert("resumes", self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "experiences": self.experiences,
            "skills": self.skills,
        }


class Experience(object):
    def __init__(self, data, _id=None, **kwargs):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.exp_data = data  # dictionary store all the input

    def json(self):
        if 'description' in self.exp_data:
            self.exp_data['description'] = self.exp_data['description'].split("\n")
        return {
            '_id': self._id,
            'exp_data': self.exp_data
        }

    @classmethod
    def add_experience(cls, resume_id, section_id, input_data):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']

        title = input_data['title']
        place = input_data['place']
        city_state = input_data['city_state']
        country = input_data['country']
        start_date = input_data['start_date']
        end_date = input_data['end_date']
        if title == "" or place == "" or city_state == "" or country == "":
            return False, "All values cannot be empty"

        if not valid_datetime(start_date) or not valid_datetime(end_date):
            return False, "Date format is invalid"

        flag, existed_session = Section.get_section_from_session(resume_id, section_id)
        if flag is False or len(existed_session['skills']) > 0:
            return False, "Add only skills in this section for consistence"

        new_experience = cls(input_data).json()
        query = {'_id': resume_id, 'section._id': section_id, 'user_id': user_id}, \
                {'$push': {'section.$.experiences': new_experience}}
        Database.update_one(
            "resumes",
            *query
        )
        return True, "Experience added"

    @classmethod
    def edit_experience(cls, resume_id, section_id, experience_id, input_data):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']

        new_experience = cls(input_data, experience_id).json()
        Database.DATABASE['resumes'].update_one(
            {'_id': resume_id, 'user_id': user_id},
            {'$set': {'section.$[sid].experiences.$[eid]': new_experience}},
            upsert=True,
            array_filters=[{'sid._id': section_id}, {'eid._id': experience_id}]
        )
        return True, "Experience is changed"

    @classmethod
    def delete_experience(cls, resume_id, section_id, experience_id):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        Database.DATABASE['resumes'].update_one(
            {'_id': resume_id, 'section._id': section_id, 'user_id': user_id},
            {'$pull': {'section.$[sid].experiences': {'_id': experience_id}}},
            upsert=True,
            array_filters=[{'sid._id': section_id}]
        )

        return True, "Experience is deleted"


class Skill(object):
    def __init__(self, data, _id=None, **kwargs):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.skill_data = data  # dictionary store all the input

    @classmethod
    def add_skill(cls, resume_id, section_id, input_data):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        flag, existed_session = Section.get_section_from_session(resume_id, section_id)
        if flag is False or len(existed_session['experiences']) > 0:
            return False, "Add only experiences in this section for consistence"

        user_id = user_data['_id']
        new_skills = cls(input_data).json()
        query = {'_id': resume_id, 'section._id': section_id, 'user_id': user_id}, \
                {'$push': {'section.$.skills': new_skills}}
        Database.update_one(
            "resumes",
            *query
        )
        return True, "Skill added"

    def json(self):
        if 'description' in self.skill_data:
            self.skill_data['description'] = self.skill_data['description'].split("\n")
        return {
            '_id': self._id,
            'exp_data': self.skill_data
        }

    @classmethod
    def edit_skill(cls, resume_id, section_id, skill_id, input_data):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']
        new_skill = cls(input_data, skill_id).json()
        Database.DATABASE['resumes'].update_one(
            {'_id': resume_id, 'user_id': user_id},
            {'$set': {'section.$[sid].skills.$[eid]': new_skill}},
            upsert=True,
            array_filters=[{'sid._id': section_id}, {'eid._id': skill_id}]
        )

        return True, "Skill is changed"

    @classmethod
    def delete_skill(cls, resume_id, section_id, skill_id):
        flag, user_data = User.get_profile()
        if flag is False:
            return False, "No profile found"

        user_id = user_data['_id']

        Database.DATABASE['resumes'].update_one(
            {'_id': resume_id, 'section._id': section_id, 'user_id': user_id},
            {'$pull': {'section.$[sid].skills': {'_id': skill_id}}},
            upsert=True,
            array_filters=[{'sid._id': section_id}]
        )

        return True, "Skill is deleted"
