from flask import Flask, jsonify, render_template, request, session, redirect, url_for
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
    create_user,
    get_user_by_username,
    get_users,
    get_userById,
    update_user,
    delete_user,
    authenticate_user,
)
from database import set_mysql
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "piogensan"  # replace 'your_secret_key' with your actual secret key
CORS(app)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "112402"
app.config["MYSQL_DB"] = "im2"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True
mysql = MySQL(app)
set_mysql(mysql)


@app.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        user = authenticate_user(username, password)
        if user:
            session["username"] = username
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))

@app.route("/index")
def home():
    if "username" not in session:
        return redirect(url_for("login_page"))
    else:
        content_type_header = request.headers.get("Content-Type")
        if content_type_header and "application/json" in content_type_header:
            return jsonify(
                financial_data=get_transactions(),
                budgets=get_budgets(),
                user=get_user_by_username(session["username"]),
            )
        else:
            return render_template(
                "index.html",
                financial_data=get_transactions(),
                budgets=get_budgets(),
                user=get_user_by_username(session["username"]),
            )


@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        email = data["email"]
        user_id = create_user(username, password, email)
        return jsonify({"created user": user_id})
    else:
        users = get_users()
        return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def user(user_id):
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
        user = get_userById(user_id)
        return jsonify(user)


@app.route("/transactions", methods=["GET", "POST"])
def transactions():
    if request.method == "POST":
        data = request.get_json()
        budget_id = data["budget_id"]
        amount = data["amount"]
        description = data["description"]
        trans_date = data["trans_date"]
        user_id = data["user_id"]
        trans_id = create_transaction(budget_id, amount, description, trans_date, user_id)
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
        user_id = data["user_id"]
        budget_id = create_budget(category, amount, user_id)
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


if __name__ == "__main__":
    app.run(debug=True)
