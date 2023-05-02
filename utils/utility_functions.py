from pymongo.errors import ConnectionFailure

# if default admin user is not in the DB, then set variable to False
default_admin_user_created = False


# function to create and later check if 
# there is a default admin user in the database
def check_sysadmin_user():
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
            'company': 'None'
        }
        users_coll.insert_one(new_user)
        default_admin_user_created = True
    except (ConnectionFailure, Exception) as e:
        flash(
            'Unable to connect to the database: ' + str(e), 'error')
