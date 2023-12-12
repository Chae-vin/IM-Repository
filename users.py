from database import fetchone, fetchall

def create_user(username, password, email):
    query = "CALL create_user(%s, %s, %s)"
    params = (username, password, email)
    result = fetchone(query, params)
    return result

def get_users():
    query = "SELECT * FROM get_users"
    result = fetchall(query)
    return result

def get_userById(user_id):
    query = "SELECT * FROM get_users WHERE user_id = %s"
    params = (user_id,)
    result = fetchone(query, params)
    return result

def update_user(user_id, new_username, new_password, new_email):
    query = "CALL update_user(%s, %s, %s, %s)"
    params = (user_id, new_username, new_password, new_email)
    result = fetchone(query, params)
    return result

def delete_user(user_id):
    query = "CALL delete_user(%s)"
    params = (user_id,)
    result = fetchone(query, params)
    return result

def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and user["password"] == password:
        return user
    else:
        return None

def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    params = (username,)
    result = fetchone(query, params)
    return result

