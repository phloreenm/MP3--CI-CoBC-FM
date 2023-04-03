import os
from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session
import logging

if os.path.exists('env.py'):
    import env

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
# print(f"os.getenv(MONGO_URI): {os.getenv('MONGO_URI')}")
CERT_FILE_PATH = os.getenv('CERT_FILE_PATH')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
SECRET_KEY = os.getenv('SECRET_KEY')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['CERT_FILE_PATH'] = CERT_FILE_PATH
app.config['IP'] = IP
app.config['PORT'] = PORT


if os.path.exists('env.py'):
    import env

# print(f'IP: {IP}')
# print(f'PORT: {PORT}')
# print(f'MONGO_URI: {MONGO_URI}')
# print(f'CERT_FILE_PATH: {CERT_FILE_PATH}')
# print(f'MONGO_DBNAME: {MONGO_DBNAME}')
# print(f'SECRET_KEY: {SECRET_KEY}')

client = MongoClient(
    app.config['MONGO_URI'],
    tls=True,
    tlsCertificateKeyFile=app.config['CERT_FILE_PATH'],
    appname=app.name
)

# print(f'client: {client}')
# print(f'MONGO_DBNAME: {MONGO_DBNAME}')
db = client.get_database(app.config['MONGO_DBNAME'])
# print(f'db: {db}')
users_coll = db['users']
procedures_coll = db['procedures']
daily_tasks_coll = db['daily_tasks']


@app.route('/')
@app.route('/index')
def index():
    try:
        users = list(users_coll.find())
        for user in users:
            print(f'User: {user}')
        return render_template('index.html', users=users)
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/procedures')
def procedures():
    try:
        procedures = list(procedures_coll.find())
        for procedure in procedures:
            print(f'Procedure: {procedure}')
        return render_template('procedures.html', procedures=procedures)
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/tasks')
def tasks():
    tasks = list(daily_tasks_coll.find())
    for task in tasks:
        print(f'Task: {task}')
    return render_template('tasks.html', tasks=tasks)


if __name__ == '__main__':
    app.run(
        host=app.config['IP'],
        port=int(app.config['PORT']),
        debug=True
    )
