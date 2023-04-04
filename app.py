import json
import random
import string
import re

from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = {}
try:
    with open('users.json') as f:
        users = json.load(f)
except:
    pass

def is_email(username):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, username))
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
@app.after_request
def after_request(response):
    try:
        with open('users.json', 'w') as f:
            json.dump(users, f)
    except Exception as e:
        print(e)
    return response

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    message = 'Internal server error'
    if hasattr(e, 'code'):
        code = e.code
        message = e.description

    return make_response(jsonify({'error': message}), code)

class Login(Resource):
    def post(self):
        #
        username = request.args.get('username')
        password = request.args.get('password')
        f=open(username+".txt","w")
        f.close()
        if username not in users or users[username]['password'] != password:
            return {'error': 'Wrong username or password'}, 400
        return {'message': 'Logged in successfully', 'token': users[username]['token']}, 200

class Register(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        #check is username email or not

        if username == '' or password == '' or not is_email(username):
            return {'error': 'Bad request'}, 400
        if username not in users:
            token = get_random_string(32)
            users[username] = {'password': password, 'token': token}
            return {'message': 'User registered successfully', 'token': token}, 201
        return {'error': 'User already exists'}, 409

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    app.run(debug=True)