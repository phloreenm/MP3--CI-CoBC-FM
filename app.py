import os

from flask_pymongo import PyMongo
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import (
    Flask, flash, render_template, request, redirect, url_for, session)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from datetime import datetime
# from flask_login import login_required
# from flask_login import LoginManager

if os.path.exists('env.py'):
    import env

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
SECRET_KEY = os.getenv('SECRET_KEY')
IP = os.getenv('IP')
PORT = os.getenv('PORT')

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = SECRET_KEY
app.config['MONGO_URI'] = MONGO_URI
app.config['MONGO_DBNAME'] = MONGO_DBNAME
app.config['IP'] = IP
app.config['PORT'] = PORT

# Create MongoDB client instance:
client = MongoClient(
    app.config['MONGO_URI'],
    appname=app.name
)

# Access MongoDB database and collections with Python client instance:
db = client.get_database(app.config['MONGO_DBNAME'])
# Access collections:
users_coll = db['users']
procedures_coll = db['procedures']
daily_tasks_coll = db['daily_tasks']
roles_coll = db['roles']
temps_coll = db['daily_tasks_temps']
dt_reps_coll = db['daily_tasks_reports']


@app.route('/')
@app.route('/index')
def index():
    try:
        if 'user' in session:
            return redirect(url_for('dashboard', role=session['role']))
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
        role = session['role']
        flash(f'\nUser {new_user["un"]} successfully registered!', 'success')
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
                session['role'] = user['role'].lower()
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


@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # query the database for the user to be edited
    # and populate form with user's info:
    user = users_coll.find_one(
            {'_id': ObjectId(user_id)}
            )
    roles = list(roles_coll.find())
    if request.method == "POST":
        if request.form.get('password'):
            # if password is NOT empty:
            if request.form.get('password1'):
                # update user's info:
                users_coll.update_one(
                    {'_id': ObjectId(user_id)},
                    {
                        '$set': {
                            'role': request.form.get('role').lower(),
                            'company': request.form.get('company').lower(),
                            'un': request.form.get('un').lower(),
                            'fname': request.form.get('first_name').lower(),
                            'lname': request.form.get('last_name').lower(),
                            'email': request.form.get('email1').lower(),
                            'pw': generate_password_hash(
                                request.form.get('password1'))
                            }
                    }
                )
        # if password field IS empty:
        else:
            # update user's info:
            users_coll.update_one(
                {'_id': ObjectId(user_id)},
                {
                    '$set': {
                        'role': request.form.get('role').lower(),
                        'company': request.form.get('company').lower(),
                        'un': request.form.get('un').lower(),
                        'fname': request.form.get('first_name').lower(),
                        'lname': request.form.get('last_name').lower(),
                        'email': request.form.get('email1').lower()
                        }
                }
            )
            flash('User updated successfully!', 'success')
            return redirect(url_for('users', role=session['role']))
        # if password field is not empty:
        # elif request.form.get('password') != '':

        print("POST edit_user template\n")
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template(
        'edit_user.html', user=user, roles=roles,
        restaurant=user['company'])


@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    if (users_coll.find({'un': 'sysadmin'})):
        flash('Can not delete System Administrator', 'danger')
        return redirect(url_for('users', role=session['role']))
    # delete user from the database:
    users_coll.delete_one({'_id': ObjectId(user_id)})
    # query the database if the user was deleted
    user = users_coll.find_one(
            {'_id': ObjectId(user_id)}
            )
    if user:
        flash('User not deleted!', 'danger')
    else:
        flash('User deleted successfully!', 'success')
    return redirect(url_for('users', role=session['role']))


@app.route('/logout')
def logout():
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
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
# @login_required
def procedures():
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
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
    t_reports = list(temps_coll.find(
            {}).sort('timestamp', -1).limit(20))
    return render_template('tasks.html', tasks=tasks, t_reports=t_reports)


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    tasks = list(daily_tasks_coll.find())
    if request.method == "POST":
        task = {
            'task': request.form.get('task'),
            'description': request.form.get('description'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'user': request.form.get('user'),
            'status': request.form.get('status')
        }
        daily_tasks_coll.insert_one(task)
        flash('Task added successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('add_task.html', tasks=tasks)


@app.route('/temps_form', methods=['GET', 'POST'])
def temps_form():
    if request.method == "POST":
        ts_str = request.form['timestamp_tf']
        ts_obj = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M')
        iso_date = ts_obj.isoformat()
        user = users_coll.find_one(
            {'un': session['user'].lower()}
            )
        # get the form data:
        temp_measurement = {
            'dish_name': request.form.get('dish_name').lower(),
            'probe_used': request.form.get('probe_used').lower(),
            'temperature': request.form.get('temperature'),
            'unit': request.form.get('unit').lower(),
            'timestamp': iso_date,
            'user': user['un'].lower(),
            'company': user['company'].lower(),
            'comments': request.form.get('comments').lower()
        }
        temps_coll.insert_one(temp_measurement)
        flash('Temperature added successfully!', 'success')
        return redirect(url_for('temps'))
    return render_template('temps_form.html')


@app.route('/shift_form/<form_type>', methods=['GET', 'POST'])
def shift_form(form_type):
    if form_type == 'begin':
        dt = list(daily_tasks_coll.find({'t_type': 'begin'.lower()}).limit(1))
    elif form_type == 'finish':
        dt = list(daily_tasks_coll.find({'t_type': 'finish'.lower()}).limit(1))
    if request.method == "POST":
        tasks = []
        task_list_db = []
        task_responses = {}
        # get the form data:
        ts_str = request.form['timestamp_tf']
        ts_obj = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M')
        iso_date = ts_obj.isoformat()
        # get tasks index and user's choices and pair them in a dict:
        for key in request.form.keys():
            if key.startswith('task_'):
                task_number = int(key.split('_')[-1])
                tasks.append(request.form[f'task_{task_number}'])
                task_responses[task_number] = request.form[key]
        # get tasks values from DB and append them to the task_list_db list
        for d in dt:
            for t in d['tasks']:
                task_list_db.append(t)
        # create a dict with list containg the tasks and the user's choices
        tasks_answers_pairs = {
            str(key): [task_list_db[key-1], task_responses[key]]
            for key in task_responses.keys()}
        # get the form data:
        observations = request.form.get('obs')
        if observations is None:
            observations = ''
        c_shift_rep = {
            't_type': dt[0]['t_type'],
            't_ts_submit': iso_date,
            't_rp_un': session['user'].lower(),
            'answers': tasks_answers_pairs,
            't_obs': observations.lower(),
        }
        # insert the report into the DB
        dt_reps_coll.insert_one(c_shift_rep)
        flash('Commencing Shift Report added successfully!', 'success')
        return redirect(url_for('tasks'))
    return render_template('shift_form.html', dt=dt)


@app.route('/reports/<report_type>')
def reports(report_type):
    user = users_coll.find_one(
            {'un': session['user'].lower()}
            )
    if report_type == 'begin':
        reports = list(dt_reps_coll.find(
            {'t_type': 'begin'}).sort('timestamp', -1).limit(20))
        for report in reports:
            report['t_ts_submit'] = format_date(report['t_ts_submit'])
        return render_template(
            'reports_list.html', reports=reports)
    elif report_type == 'finish':
        reports = list(dt_reps_coll.find(
            {'t_type': 'finish'}).sort('timestamp', -1).limit(20))
        for report in reports:
            report['t_ts_submit'] = format_date(report['t_ts_submit'])
        return render_template('reports_list.html', reports=reports)
    elif report_type == 'temperatures':
        reports = list(temps_coll.find(
            {'company': user['company']}).sort('timestamp', -1).limit(40))
        for r in reports:
            dt = r['timestamp']
            r['timestamp'] = format_date(dt)
        return render_template('temps_report.html', reports=reports)
    else:
        # handle invalid report type
        return "Invalid report type"


@app.route('/report/<report_id>')
def report(report_id):
    report = dt_reps_coll.find_one({'_id': ObjectId(report_id)})
    answers = report['answers']
    date = format_date(report['t_ts_submit'])
    return render_template(
        'report_details.html', report=report, answers=answers, date=date)


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    app.run(
        host=app.config['IP'],
        port=int(app.config['PORT']),
        debug=True
    )
