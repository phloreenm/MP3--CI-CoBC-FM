from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, render_template
import os
from env import *
import logging

load_dotenv()

app = Flask(__name__)

if os.path.exists("env.py"):
    import env

client = MongoClient(MONGODB_URI, tls=True, tlsCertificateKeyFile=CERT_FILE_PATH)

db = client[MONGO_DBNAME]
users_coll = db['users']
procedures_coll = db['procedures']
daily_tasks_coll = db['daily_tasks']


@app.route("/")
@app.route("/index")
def index():
    try:
        users = list(users_coll.find())
        for user in users:
            print(f"User: {user}")
        return render_template("index.html", users=users)
    except Exception as e:
        logging.error(f"Error accessing MongoDB: {e}", exc_info=True)
        error_message = e
        return render_template("error.html", error_message=error_message)


@app.route("/procedures")
def procedures():
    try:
        procedures = list(procedures_coll.find())
        for procedure in procedures:
            print(f"Procedure: {procedure}")
        return render_template("procedures.html", procedures=procedures)
    except Exception as e:
        logging.error(f"Error accessing MongoDB: {e}", exc_info=True)
        error_message = e
        return render_template("error.html", error_message=error_message)


@app.route("/tasks")
def tasks():
    tasks = list(daily_tasks_coll.find())
    for task in tasks:
        print(f"Task: {task}")
    return render_template("tasks.html", tasks=tasks)


if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
