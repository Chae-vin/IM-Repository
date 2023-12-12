from database import fetchone, fetchall


def create_transaction(user_id, cat_id, amount, description, trans_date):
    query = "CALL create_transaction(%s, %s, %s, %s, %s)"
    params = (user_id, cat_id, amount, description, trans_date)
    result = fetchone(query, params)
    return result["trans_id"]


def get_transactions():
    query = "SELECT * FROM get_transactions"
    result = fetchall(query)
    return result


def get_transaction(trans_id):
    query = "SELECT * FROM get_transactions WHERE trans_id = %s"
    params = (trans_id,)
    result = fetchone(query, params)
    return result


def update_transaction(trans_id, user_id, cat_id, amount, description, trans_date):
    query = "CALL update_transaction(%s, %s, %s, %s, %s, %s)"
    params = (trans_id, user_id, cat_id, amount, description, trans_date)
    result = fetchone(query, params)
    return result["trans_id"]


def delete_transaction(trans_id):
    query = "CALL delete_transaction(%s)"
    params = (trans_id,)
    result = fetchone(query, params)
    return result["trans_id"]


# USERS

def get_user(user_id):
    query = "SELECT * FROM get_users WHERE user_id = %s"
    params = (user_id,)
    result = fetchone(query, params)
    return result


def create_user(username, password, email):
    query = "CALL create_user(%s, %s, %s)"
    params = (username, password, email)
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


# CATEGORIES

def create_category(cat_username):
    query = "CALL create_category(%s)"
    params = (cat_username,)
    result = fetchone(query, params)
    return result["cat_id"]


def get_categories():
    query = "SELECT * FROM get_categories"
    result = fetchall(query)
    return result


def get_category(cat_id):
    query = "SELECT * FROM get_categories WHERE cat_id = %s"
    params = (cat_id,)
    result = fetchone(query, params)
    return result


def update_category(cat_id, cat_username):
    query = "CALL update_category(%s, %s)"
    params = (cat_id, cat_username)
    result = fetchone(query, params)
    return result["cat_id"]


def delete_category(cat_id):
    query = "CALL delete_category(%s)"
    params = (cat_id,)
    result = fetchone(query, params)
    return result["cat_id"]
