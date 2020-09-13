# This file contains setup of the User class for the flask-login extension.

from flask_mongoengine import MongoEngine, Document
from flask_login import UserMixin

db = MongoEngine()

# While UserMixin does allow us to inherit the required class attributes, I decided to implement them for clarity of code.


class User(UserMixin, db.Document):
    meta = {'collection': 'User'}
    email = db.StringField(max_length=50)
    password = db.StringField()
    # A required attribute from flask-login to ensure the login.required decorators operate functionally. As auth here is very simple, all users are considered authenticated if they pass login.
    is_authenticated = True
    # As required by flask-login. For our purposes, all users are active users.
    is_active = True
    # As required by flask-login. For our purposes, there are no anonymous users.
    is_anonymous = False
    # A requirement of flask-logins authentication process is to return a unicode string for user_loader() callback.
