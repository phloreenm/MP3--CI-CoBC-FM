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
from utils.utility_functions import (
    check_sysadmin_user,
    format_date,
    should_edit_role,
    filter_admin_users,
    filter_manager_users,
    filter_employee_users)

if os.path.exists('env.py'):
    import env

load_dotenv()

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

# function to create/check if 'sysadmin' users exists in the database
check_sysadmin_user()


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
        form_un = request.form.get('un').lower()
        form_email = request.form.get('email1').lower()
        user = users_coll.find_one({'un': form_un})
        email = users_coll.find_one({'email': form_email})
        if (
            user == form_un.lower()) or (
                email == form_email.lower()):
            if user:
                flash(f'Username {user["un"]} already exists. '
                      f'Choose a different username.', 'info')
            elif email:
                flash(f'Email {email["email"]} already exists. '
                      f'Choose a different email.', 'info')
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
    '''
    Check if user is already logged in and redirect him to first page:
    may be removed, as id user is session it's redirected to index
    and the login link is not shown anymore
    '''
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
                flash(
                    f'\nUser {session["user"].title()} logged in!', 'success')
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
    company = user['company']
    restaurant_manager_count = users_coll.count_documents({
        'company': company,
        'role': 'manager',
    })
    can_edit_role = should_edit_role(
        restaurant_manager_count, session['role'], user['role'])
    # print("can_edit_role", can_edit_role)
    if request.method == "POST":
        if request.form.get('password'):
            # if password is NOT empty:
            if request.form.get('password1'):
                # update user's info:
                print("get_role_lower: ", request.form.get('role').lower())
                print("get_role: ", request.form.get('role'))
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
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))
    return render_template(
        'edit_user.html', user=user, roles=roles, can_edit_role=can_edit_role,
        restaurant=user['company'],
        restaurant_manager_count=restaurant_manager_count)


@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    # Prevent deleting System Administrator:
    sys_admin_user = users_coll.find_one(
        {'_id': ObjectId(user_id), 'un': 'sysadmin'})
    if sys_admin_user is not None:
        flash('Can not delete System Administrator', 'danger')
        return redirect(url_for('users', role=session['role']))
    # Delete user from the database:
    users_coll.delete_one({'_id': ObjectId(user_id)})
    # Query the database if the user was deleted
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


def statistics_count():
    """
    Count the number of registered companies, users and reports
    to be displayed on Admins dashboard
    """
    reg_companies = len(set(users_coll.distinct('company')))
    reg_users = len(set(users_coll.distinct('un')))
    reg_reports = len(set(dt_reps_coll.distinct('t_ts_submit')))

    today_date = datetime.now().strftime("%Y-%m-%d")
    start_of_day = today_date + "T00:00:00Z"
    end_of_day = today_date + "T23:59:59Z"
    reps_agg = [
        {
            "$match": {
                "t_ts_submit": {
                    "$gte": start_of_day,
                    "$lt": end_of_day
                }
            }
        },
        {
            "$count": "total_documents"
        }
            ]

    reps = dt_reps_coll.aggregate(reps_agg)
    count_result = next(reps, None)

    if count_result is not None:
        reps_count = count_result["total_documents"]
    else:
        reps_count = 0

    stats_results = {
        "registered_companies": reg_companies,
        "registered_users": reg_users,
        "registered_reports": reg_reports,
        "today_reports": reps_count
    }
    return stats_results


def show_user_reports(user):
    reports = list(dt_reps_coll.find(
        {'t_rp_un': user, }).sort('timestamp', -1))
    for report in reports:
        report['t_ts_submit'] = format_date(report['t_ts_submit'])
    return reports


def show_user_t_reports(user):
    reports = list(temps_coll.find(
        {'user': user, }).sort('timestamp', -1))
    for report in reports:
        print("report['timestamp']", report['timestamp'])
        report['timestamp'] = format_date(report['timestamp'])
    return reports


@app.route('/dashboard/<role>')
def dashboard(role):
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
    # Set user's role in session:
    session['user_role'] = role
    # Check user's role and redirect if not logged in:
    if role not in ['admin', 'manager', 'employee']:
        flash('You\'re not authorized to access this page', 'danger')
        return redirect(url_for('login'))
    # Get list of all users:
    users_list = list(users_coll.find().sort('role', 1))
    logged_in_user = session['user']
    logged_user_company = users_coll.find_one(
        {'un': logged_in_user})['company']
    # Filter users list based on role:
    if role == 'admin':
        filtered_users = filter_admin_users(users_list)
        stats_results = statistics_count()
        return render_template(
            'dashboard_admin.html', users=list(
                filtered_users), stats=stats_results)
    elif role == 'manager':
        filtered_users = filter_manager_users(users_list, logged_user_company)
        stats_results = statistics_count()
        return render_template(
            'dashboard_manager.html', users=list(filtered_users),
            stats=stats_results)
    else:
        filtered_users = filter_employee_users(
            users_list, logged_user_company)
        my_reports = show_user_reports(logged_in_user)
        my_temp = show_user_t_reports(logged_in_user)
        return render_template(
            'dashboard_employee.html',
            users=list(filtered_users),
            my_reports=my_reports,
            my_temps=my_temp)


@app.route('/users')
def users():
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
    try:
        logged_in_user = session['user']
        user_role = session['role']
        if user_role == 'admin':
            users = list(users_coll.find().sort('role', 1))
        else:
            company = users_coll.find_one({'un': logged_in_user})['company']
            users = list(users_coll.find({'company': company}).sort('role', 1))
        return render_template('users.html', users=users)
    except Exception as e:
        logging.error(f'Error accessing MongoDB: {e}', exc_info=True)
        error_message = e
        return render_template('error.html', error_message=error_message)


@app.route('/tasks')
def tasks():
    # Check if user is logged in:
    if 'user' not in session:
        return redirect(url_for('login'))
    tasks = list(daily_tasks_coll.find())
    t_reports = list(temps_coll.find(
            {}).sort('timestamp', -1).limit(20))
    return render_template('tasks.html', tasks=tasks, t_reports=t_reports)


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
        return redirect(url_for('reports', report_type='temperatures'))
    return render_template('temps_form.html')


def process_form_data(form_data, dt, session_user):
    """
    This function is called from the app.py file
    when processing the reports form data submitted by the user.
    """
    tasks = []
    task_list_db = []
    task_responses = {}
    # get the form data:
    ts_str = form_data['timestamp_tf']
    ts_obj = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M')
    iso_date = ts_obj.isoformat()
    # get tasks index and user's choices and pair them in a dict:
    for key in form_data.keys():
        if key.startswith('task_'):
            task_number = int(key.split('_')[-1])
            tasks.append(form_data[f'task_{task_number}'])
            task_responses[task_number] = form_data[key]
    # get tasks values from DB and append them to the task_list_db list
    for d in dt:
        for t in d['tasks']:
            task_list_db.append(t)
    # create a dict with list containg the tasks and the user's choices
    tasks_answers_pairs = {
        str(key): [task_list_db[key-1], task_responses[key]]
        for key in task_responses.keys()}
    # get the form data:
    observations = form_data.get('obs')
    if observations is None:
        observations = ''
    c_shift_rep = {
        't_type': dt[0]['t_type'],
        't_ts_submit': iso_date,
        't_rp_un': session_user.lower(),
        'answers': tasks_answers_pairs,
        't_obs': observations.lower(),
    }
    dt_reps_coll.insert_one(c_shift_rep)
    return c_shift_rep


@app.route('/shift_form/<form_type>', methods=['GET', 'POST'])
def shift_form(form_type):
    dt = list(daily_tasks_coll.find({'t_type': form_type.lower()}).limit(1))
    if request.method == "POST":
        process_form_data(request.form, dt, session['user'])
        if (form_type == 'begin'):
            flash('Commencing Shift Report added successfully!', 'success')
        elif (form_type == 'finish'):
            flash('Finishing Shift Report added successfully!', 'success')
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
        flash('Invalid report type.', 'success')
        return render_template('error.html')


@app.route('/report/<report_id>')
def report(report_id):
    report = dt_reps_coll.find_one({'_id': ObjectId(report_id)})
    answers = report['answers']
    date = format_date(report['t_ts_submit'])
    return render_template(
        'report_details.html', report=report, answers=answers, date=date)


@app.route('/delete_report/<report_id>')
def delete_report(report_id):
    report = dt_reps_coll.find_one({'_id': ObjectId(report_id)})
    # delete report from the database:
    try:
        dt_reps_coll.delete_one({'_id': ObjectId(report_id)})
        # query the database if the report was deleted
        deleted_report = users_coll.find_one(
                {'_id': ObjectId(report_id)}
                )
    except Exception as e:
        print(e)
        deleted_report = False
    if deleted_report:
        flash('Report not deleted!', 'danger')
    else:
        flash('Report deleted successfully!', 'success')
    print(report['t_type'])
    return redirect(url_for('reports', report_type=report['t_type']))


@app.route('/delete_temp/<temp_id>')
def delete_temp(temp_id):
    # delete report from the database:
    try:
        temps_coll.delete_one({'_id': ObjectId(temp_id)})
        # query the database if the report was deleted
        deleted_report = temps_coll.find_one(
                {'_id': ObjectId(temp_id)}
                )
    except Exception as e:
        print(e)
        deleted_report = False
    if deleted_report:
        flash('Temperature Report  not deleted!', 'danger')
    else:
        flash('Temperature Report deleted successfully!', 'success')
    return redirect(url_for('reports', report_type='temperatures'))


@app.route('/tos')
def tos():
    return render_template('tos.html')


@app.route('/pp')
def pp():
    return render_template('pp.html')


@app.route('/project')
def project():
    return render_template('project.html')


if __name__ == '__main__':
    app.run(
        host=app.config['IP'],
        port=int(app.config['PORT']),
        debug=True
    )
