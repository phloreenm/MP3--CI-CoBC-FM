from pymongo.errors import ConnectionFailure
from datetime import datetime

# if default admin user is not in the DB, then set variable to False
default_admin_user_created = False


def check_sysadmin_user():
    """
    This function is called from the app.py file.
    It checks if the default admin user is in the database.
    If it is not, then it creates it. This is to ensure that has a default 'sysadmin' user,
    which is the starting point of the application.
    """
    global default_admin_user_created
    if default_admin_user_created:
        return
    from app import users_coll
    try:
        # Check if 'sysadmin' user already exists in the database
        sysadmin = users_coll.find_one({'un': 'sysadmin'})
        if sysadmin is not None:
            return
        # If 'sysadmin' user does not exist, create it with default password
        hashed_password = generate_password_hash('1111')
        new_user = {
            'role': 'admin',
            'un': 'sysadmin',
            'pw': hashed_password,
            'fname': 'System',
            'lname': 'Admin',
            'email': 'sysadmin@example.com',
            'company': 'eManager'
        }
        users_coll.insert_one(new_user)
        default_admin_user_created = True
    except (ConnectionFailure, Exception) as e:
        flash(
            'Unable to connect to the database: ' + str(e), 'error')


def format_date(date_str):
    """
    This functions is called each time there is a need to convert a date string from the database to a more readable format.
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    return date_obj.strftime('%Y-%m-%d %H:%M:%S')


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


def should_edit_role(
        restaurant_manager_count: int,
        session_role: str, user_role: str) -> bool:
    """
    Determines whether the user can edit the role of another user based on their session role,
    the number of managers in the same restaurant, and the role of the user being edited.
    Returns a boolean value.
    """
    if session_role == 'manager':
        if restaurant_manager_count <= 1 and user_role == 'manager':
            can_edit = False
        else:
            can_edit = True
    elif session_role == 'admin':
        can_edit = True
    else:
        can_edit = False
    return can_edit


def filter_admin_users(users):
    """
    function to filter users displayed to the admin
    """
    return [user for user in users if user['role'] in ['admin', 'manager']]


def filter_manager_users(users, company):
    """
    function to filter users displayed to the admin
    """
    return [user for user in users if user['company'] == company]


def filter_employee_users(users, company):
    """
    function to filter users displayed to the admin
    """
    return [
        user for user in users if user[
            'company'] == company and user['role'] == 'employee']
