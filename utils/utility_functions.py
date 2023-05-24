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
            # 'company'] == company and user['role'] == 'employee']
            'company'] == company]

