from database import fetchone, fetchall


def create_budget(category, amount):
    query = "CALL create_budget(%s, %s)"
    params = (category, amount)
    result = fetchone(query, params)
    return result


def get_budgets():
    query = "SELECT * FROM budgets"
    result = fetchall(query)
    return result


def get_budget(budget_id):
    query = "SELECT * FROM budgets WHERE budget_id = %s"
    params = (budget_id,)
    result = fetchone(query, params)
    return result


def update_budget(budget_id, category, anount):
    query = "CALL update_budget(%s, %s, %s)"
    params = (budget_id, category, anount)
    result = fetchone(query, params)
    return result


def delete_budget(budget_id):
    query = "CALL delete_budget(%s)"
    params = (budget_id,)
    result = fetchone(query, params)
    return result
