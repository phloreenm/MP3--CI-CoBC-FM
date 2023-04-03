import os
from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask import (
    Flask, flask, render_template, request, redirect, url_for, session)
from bson.objectid import ObjectId
import logging

if os.path.exists('env.py'):
    import env

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
SECRET_KEY = os.getenv('SECRET_KEY')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['IP'] = IP
app.config['PORT'] = PORT

client = MongoClient(
    app.config['MONGO_URI'],
    appname=app.name
)

db = client.get_database(app.config['MONGO_DBNAME'])
users_coll = db['users']
procedures_coll = db['procedures']
daily_tasks_coll = db['daily_tasks']


@app.route('/')
@app.route('/index')
def index():
    try:
        
        return render_template('index.html')
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/users')
def users():
    try:
        users = list(users_coll.find())
        return render_template('users.html', users=users)
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/procedures')
def procedures():
    try:
        procedures = list(procedures_coll.find())
        return render_template('procedures.html', procedures=procedures)
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/tasks')
def tasks():
    tasks = list(daily_tasks_coll.find())
    return render_template('tasks.html', tasks=tasks)


if __name__ == '__main__':
    app.run(
        host=app.config['IP'],
        port=int(app.config['PORT']),
        debug=True
    )
