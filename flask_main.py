import uuid
import flask
from flask import Flask, render_template, request, session, url_for, request,jsonify
from Users import User
from db_config import local_session
from werkzeug.security import generate_password_hash, check_password_hash
from DbRepo import DbRepo
from Customers import Customer
from flask_cors import CORS,cross_origin



repo = DbRepo(local_session)
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'secret'  # Change this!
CORS(app)

def convert_to_json(_list):  # cleaning & jsoning data recieved from SQLACLCHEMY
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


def add_customer_user(_input):
    repo.add(User(username=_input['username'],
                   password=_input['password'],
                   email=_input['email'],
                   user_role=2))
    user = repo.get_by_column_value(User, User.username, _input['username'])
    customer = repo.add(Customer(first_name=_input['first_name'],
                        last_name=_input['last_name'],
                        address=_input['address'],
                        phone_number=_input['phone_number'],
                        credit_card_number=_input['credit_card_number'],
                        user_id=user[0].id))
    return jsonify(customer)


def update_customer(_input, id):
    customers_json = convert_to_json(repo.get_all(Customers))
    for c in customers_json:
        if c["id"] == id:
            c["id"] = _input["id"] if "id" in _input.keys() else None
            c["first_name"] = _input["first_name"] if "first_name" in _input.keys() else None
            c["last_name"] = _input["last_name"] if "last_name" in _input.keys() else None
            c["address"] = _input["address"] if "address" in _input.keys() else None
            c["phone_number"] = _input["phone_number"] if "phone_number" in _input.keys(
            ) else None
            c["credit_card_number"] = _input["credit_card_number"] if "credit_card_number" in _input.keys() else None
            repo.update_by_id(Customers, Customers.id, id, c)
    return jsonify(c)



# localhost:5000/
@app.route("/")
def home():
    try:
        if session['remember'] == 'on':
            return flask.redirect(url_for('login_success'))
    except:
        pass
    return flask.redirect(url_for('login'))

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', try_again=False, registered_success=False)

@app.route('/my_app', methods=['GET'])
def login_success():
    try:
        user = repo.get_by_column_value(
            User, User.username, session['uname'])
        if user[0] != None:
            return render_template('my_app.html')
    except:
        pass
    return render_template('login.html', try_again=True, registered_success=False)

@app.route('/login_process', methods=['POST'])
def hanle_login():
    form_data = request.form
    username = form_data.get('uname')
    password = form_data.get('psw')
    print(request)
    print(form_data)
    try:
        user = repo.get_by_column_value(User, User.username, username)
        if username == user[0].username and check_password_hash(user[0].password, password):
            session['remember'] = request.form.get('remember')
            session['uname'] = username
            session['pwd'] = password if session['remember'] == 'on' else None
            return flask.redirect(url_for('login_success'))
    except:
        pass
    return render_template('login.html', try_again=True)

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=False, short_password=False)

@app.route('/signup_process', methods=['POST'])
def handle_signup():
    if request.form['psw'] != request.form['psw-repeat']:
        return render_template('signup.html', bad_repeat=True)
    form_data = request.form
    # gets username, email and password
    username = form_data.get('uname')
    password = form_data.get('psw')
    email = form_data.get('email')
    # check if user exists
    user_username = repo.get_by_column_value(User, User.username, username)
    user_email = repo.get_by_column_value(User, User.email, email)
    if user_username:
        return render_template('signup.html', bad_repeat=False, user_exists=True, email_exists=False, short_password=False, status=202, mimetype='application/json')
    elif user_email:
        return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=True, short_password=False, status=202, mimetype='application/json')
    elif len(password) < 6:
        return render_template('signup.html', bad_repeat=False, user_exists=False, email_exists=False, short_password=True, status=202, mimetype='application/json')
    else:
        repo.add(User(username=username, password=generate_password_hash(
            password), email=email,  user_role=2))
        return render_template('login.html', try_again=False, registered_success=True, status=201, mimetype='application/json')


@app.route('/logout', methods=['GET'])
def logging_out():
    session['remember'], session['uname'], session['pwd'] = None, None, None
    return flask.redirect(url_for('login'))


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customer():
    customers = convert_to_json(repo.get_all(Customer))
    if request.method == 'GET':
        print(request.args.to_dict())
        search_args = request.args.to_dict()
        if len(search_args) == 0:
            jsonify(customers)
        results = []
        for c in customers:
            if "first_name" in search_args.keys() and c["first_name"].find(search_args["first_name"]) < 0:
                continue
            if "last_name" in search_args.keys() and c["last_name"].find(search_args["last_name"]) < 0:
                continue
            if "address" in search_args.keys() and c["address"].find(search_args["address"]) < 0:
                continue
            if "phone_number" in search_args.keys() and c["phone_number"].find(search_args["phone_number"]) < 0:
                continue
            if "credit_card_number" in search_args.keys() and c["credit_card_number"].find(search_args["credit_card_number"]) < 0:
                continue
            results.append(c)
        if len(results) == 0:
            return '{}'
        return jsonify(results)
    if request.method == 'POST':
        new_customer = request.get_json()
        print(new_customer)
        return add_customer_user(new_customer)


@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@cross_origin()
def get_customer_by_id(id):
    customers = convert_to_json(repo.get_all(Customer))
    if request.method == 'GET':
        for c in customers:
            if c["id"] == id:
                return jsonify(c)
        return "{}"
    if request.method == 'PUT':
        updated_new_customer = request.get_json()
        if repo.get_by_id(Customer, id) != None:
            return update_customer(updated_new_customer, id)
        return add_customer_user(updated_new_customer)
    if request.method == 'PATCH':
        updated_customer = request.get_json()
        if repo.get_by_id(Customer, id) != None:
            return update_customer(updated_customer, id)
        return '{}'
    if request.method == 'DELETE':
        deleted_customer = request.get_json()
        for c in customers:
            if c["id"] == id:
                repo.delete_by_id(Customer, Customer.id, id)
                repo.delete_by_id(User, User.id, c["user_id"])
                return f'{jsonify(deleted_customer)} deleted'
        return '{}'

if __name__ == "__main__":
    app.run(debug=True, port=5002)
