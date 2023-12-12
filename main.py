from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from database import fetchone, fetchall
from transactions import (
    create_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    get_transaction,
)
from budgets import (
    create_budget,
    get_budgets,
    update_budget,
    delete_budget,
    get_budget,
)
from users import (
    update_user,
    delete_user,
    create_user as create_user_function,
)
from database import set_mysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "112402"
app.config["MYSQL_DB"] = "im2"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True
mysql = MySQL(app)
set_mysql(mysql)


@app.route("/")
def home():
    content_type_header = request.headers.get("Content-Type")
    if content_type_header and "application/json" in content_type_header:
        return jsonify(financial_data=get_transactions(), budgets=get_budgets())
    else:
        return render_template(
            "index.html", financial_data=get_transactions(), budgets=get_budgets()
        )


@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        data = request.get_json()
        budget_id = data["budget_id"]
        amount = data["amount"]
        description = data["description"]
        trans_date = data["trans_date"]
        trans_id = create_transaction(
            budget_id, amount, description, trans_date)
        return jsonify({"created transaction": trans_id})
    else:
        transactions = get_transactions()
        return jsonify(transactions)


@app.route("/transactions/<int:trans_id>", methods=["GET", "PUT", "DELETE"])
def transaction(trans_id):
    if request.method == "PUT":
        data = request.get_json()
        budget_id = data["budget_id"]
        amount = data["amount"]
        description = data["description"]
        trans_date = data["trans_date"]
        trans_id = update_transaction(
            trans_id, budget_id, amount, description, trans_date
        )
        return jsonify({"updated transaction": trans_id})
    elif request.method == "DELETE":
        trans_id = delete_transaction(trans_id)
        return jsonify({"deleted transaction": trans_id})
    else:
        transaction = get_transaction(trans_id)
        return jsonify(transaction)


@app.route("/budgets", methods=["GET", "POST"])
def budgets():
    if request.method == "POST":
        data = request.get_json()
        category = data["category"]
        amount = data["amount"]
        budget_id = create_budget(category, amount)
        return jsonify({"created budget: ": budget_id})
    else:
        budgets = get_budgets()
        return jsonify(budgets)


@app.route("/budgets/<int:budget_id>", methods=["GET", "PUT", "DELETE"])
def budget(budget_id):
    if request.method == "PUT":
        data = request.get_json()
        category = data["category"]
        amount = data["amount"]
        budget_id = update_budget(budget_id, category, amount)
        return jsonify({"updated_budget: ": budget_id})
    elif request.method == "DELETE":
        budget_id = delete_budget(budget_id)
        return jsonify({"deleted budget: ": budget_id})
    else:
        budget = get_budget(budget_id)
        return jsonify(budget)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # Add your login logic here
    return jsonify({"message": "Login successful"})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    email = data["email"]
    user_id = create_user_function(username, password, email)
    return jsonify({"created user": user_id})


@app.route("/users/<int:user_id>", methods=["GET"])
def get_single_user(user_id):
    try:
        user = get_user(user_id)
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404  # Not Found
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error


def get_user(user_id):
    query = "SELECT * FROM get_users WHERE user_id = %s"
    params = (user_id,)
    result = fetchone(query, params)
    return result


@app.route("/users", methods=["GET"])
def get_users():
    users = fetchall("SELECT * FROM get_users")
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["PUT", "DELETE"])
def modify_user(user_id):
    if request.method == "PUT":
        data = request.get_json()
        new_username = data["new_username"]
        new_password = data["new_password"]
        new_email = data["new_email"]
        user_id = update_user(user_id, new_username, new_password, new_email)
        return jsonify({"updated user": user_id})
    elif request.method == "DELETE":
        user_id = delete_user(user_id)
        return jsonify({"deleted user": user_id})
    else:
        return jsonify({"error": "Invalid method"}), 400  # Bad Request


if __name__ == "__main__":
    app.run(debug=True)
