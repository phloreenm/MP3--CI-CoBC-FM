import os

from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import (
    Flask, flash, render_template, request, redirect, url_for, session)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import logging

if os.path.exists('env.py'):
    import env

load_dotenv()

NAV_ITEMS = {
    'index': 'home',
    'procedures': 'procedures',
    'tasks': 'tasks',
    'login': 'login',
    'dashboard_admin': 'dashboard',
    'dashboard_employee': 'dashboard',
    'dashboard_manager': 'dashboard',
    'users': 'users',
    'register': 'register',
}

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
SECRET_KEY = os.getenv('SECRET_KEY')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

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
roles_coll = db['roles']


@app.route('/')
@app.route('/index')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Check if username or email have been used
        user = users_coll.find_one(
            {'un': request.form.get('un').lower()}
            )
        email = users_coll.find_one(
            {'email': request.form.get('email1').lower()}
            )
        if user or email:
            if user:
                flash(f'Username {user["un"]} already exists. Please choose a different username.', 'info')
            elif email:
                flash(f'Email {email["email"]} already used. Please choose a different email.', 'info')
            return redirect(url_for('register'))
        new_user = {
            'role': request.form.get('role'),
            'un': request.form.get('un').lower(),
            'pw': generate_password_hash(request.form.get('password1')),
            'fname': request.form.get('first_name').lower(),
            'lname': request.form.get('last_name').lower(),
            'email': request.form.get('email1').lower(),
            'company': request.form.get('company').lower()
        }
        # If new user, add it to the database:
        users_coll.insert_one(new_user)
        # Add user to session cookie
        # session['user'] = request.form.get('un').lower()
        # print(f"session['user'] in register route: {session['user']}")
        # Add role to session cookie
        # session['role'] = request.form.get('role').lower()
        # print(f"session['role'] in register route: {session['role']}")
        role = session['role']
        flash(f'\nUser {session["user"]} successfully registered and logged in!', 'success')
        return redirect(url_for('users', role=role))
    db_roles = list(roles_coll.find())
    db_user_comp = users_coll.find_one(
        {'un': session['user']}
        )
    restaurant = db_user_comp['company']
    return render_template(
        'register_user.html', db_roles=db_roles, restaurant=restaurant)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in and redirect him to first page:
    # may be removed, as id user is session it's redirected to index and the login link is not shown anymore
    if 'user' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Check if username is already registered
        user = users_coll.find_one(
            {'un': request.form.get('un').lower()}
            )
        if user:
            # Check if password is correct
            if check_password_hash(user['pw'], request.form.get('password')):
                session['user'] = request.form.get('un').lower()
                print(f"session['user'] in register route: {session['user']}")
                session['role'] = user['role'].lower()
                print(f"session['role'] in register route: {session['role']}")
                flash(f'\nUser {session["user"]} logged in!', 'success')
                # return to the dashboard specific to user's role:
                role = user['role']
                return redirect(url_for('dashboard', role=role))
            else:
                flash('Incorrect Username and/or Password', 'danger')
                return redirect(url_for('login'))
        else:
            # Username not registered
            flash('Incorrect Username and/or Password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/edit_user')
def edit_user():
    return render_template('edit_user.html')


# @app.route('/edit_user/<string:un>', methods=['GET', 'POST'])
# def edit_user(un):
#     # query the database for the user to be edited:
#     user = users_coll.find_one(
#             {'un': un}
#             )
#     if request.method == 'POST':
#         # user can not edit username and role
#         # check if old password is correct:
#         if check_password_hash(user['pw'], request.form.get('password')):
#             # check if fields password1 matches password2:
#             if request.form.get('password1') == request.form.get('password2'):
#                 # update user's password:
#                 users_coll.update_one(
#                     {'un': un},
#                     {'$set': {'pw': generate_password_hash(
#                         request.form.get('password1'))}}
#                     )
#                 # update user's first name:
#                 users_coll.update_one(
#                     {'un': un},
#                     {'$set': {'fname': request.form.get('first_name').lower()}}
#                     )
#                 # update user's last name:
#                 users_coll.update_one(
#                     {'un': un},
#                     {'$set': {'lname': request.form.get('last_name').lower()}}
#                     )
#                 # update user's email:
#                 users_coll.update_one(
#                     {'un': un},
#                     {'$set': {'email': request.form.get('email1').lower()}}
#                     )
#                 flash(f'\nUser {session["user"]} successfully updated!', 'success')
#                 return redirect(url_for('users', role=session['role']))
#             else:
#                 # flash('New Passwords do not match!', 'danger')
#                 return redirect(url_for('edit_user', user=user))
#     return render_template('edit_user.html', user=user)


@app.route('/logout')
def logout():
    # Remove user from session cookies
    flash(f'\nUser {session["user"]} logged out!', 'success')
    # session.pop('user')
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard/<role>')
def dashboard(role):
    # username = session['user']
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
    # set user's role in session:
    session['user_role'] = role
    # Check user's role and redirect if not logged in:
    if role not in ['admin', 'manager', 'employee']:
        flash('You\'re not authorized to acces this page', 'danger')
        return redirect(url_for('login'))
    # Render dashboard template based on users's role:
    if role == 'admin':
        return render_template('dashboard_admin.html')
    elif role == 'manager':
        return render_template('dashboard_manager.html')
    else:
        return render_template('dashboard_employee.html')


@app.route('/users')
def users():
    try:
        users = list(users_coll.find().sort('role', 1))
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


def get_current_page_name():
    return request.path.lstrip('/')


if __name__ == '__main__':
    app.run(
        host=app.config['IP'],
        port=int(app.config['PORT']),
        debug=True
    )
