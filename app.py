import os
from flask import Flask, render_template, redirect, request, url_for, request
import dns
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

chars_sheets = []
chars = mongo.db.char_sheets.find()

for i in chars:
    characters.append(i)


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/characters")
def characters():
    return render_template("characters.html", characters=chars_sheets)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=5000,
            debug=True)
