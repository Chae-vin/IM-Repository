from database import fetchone, fetchall

def create_transaction(budget_id, amount, description, trans_date):
    query = "CALL create_transaction(%s, %s, %s, %s)"
    params = (budget_id, amount, description, trans_date)
    result = fetchone(query, params)
    return result

def get_transactions():
    query = "SELECT * FROM get_transactions"
    result = fetchall(query)
    return result


def get_transaction(trans_id):
    query = "SELECT * FROM get_transactions WHERE trans_id = %s"
    params = (trans_id,)
    result = fetchone(query, params)
    return result

def update_transaction(trans_id, budget_id, amount, description, trans_date):
    query = "CALL update_transaction(%s, %s, %s, %s, %s)"
    params = (trans_id, budget_id, amount, description, trans_date)
    result = fetchone(query, params)
    return result

def delete_transaction(trans_id):
    query = "CALL delete_transaction(%s)"
    params = (trans_id,)
    result = fetchone(query, params)
    return result