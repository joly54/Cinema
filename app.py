import json
import random
import string
import re
import ssl
import smtplib
import config
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from email.message import EmailMessage

app = Flask(__name__)
api = Api(app)

users = {}
try:
    with open('users.json') as f:
        users = json.load(f)
except:
    pass


def send_email(username, code):
    sender_email = config.sender_email
    password = config.password
    receiver_email = username
    subject = "Secret code"
    body = "Your secret code is " + code
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = sender_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)


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
    message = 'Internal server error' + str(e)
    if hasattr(e, 'code'):
        code = e.code
        message = e.description

    return make_response(jsonify({'message': message}), code)


class Login(Resource):
    def post(self):
        #
        username = request.args.get('username')
        password = request.args.get('password')
        if username not in users or users[username]['password'] != password:
            return {'error': 'Wrong username or password'}, 400
        return {'message': 'Logged in successfully', 'token': users[username]['token']}, 200


class Register(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        print(password)
        if username is None or password is None or not is_email(username):
            return {'error': 'Bad request'}, 400
        if username not in users:
            token = get_random_string(32)
            users[username] = {'password': password, 'token': token, "secretCode": get_random_string(8)}
            return {'message': 'User registered successfully', 'token': token}, 201
        return {'error': 'User already exists'}, 409


class FogotPassword(Resource):
    def post(self):
        username = request.args.get('username')
        if username not in users:
            return {'message': 'User not found'}, 404
        else:
            users[username]['secretCode'] = get_random_string(8)
            send_email(username, users[username]['secretCode'])
            return {'message': 'Secret code sent to your email'}, 200


class ResetPassword(Resource):
    def post(self):
        username = request.args.get('username')
        secretCode = request.args.get('secretCode')
        newPassword = request.args.get('newPassword')
        if username not in users:
            return {'message': 'User not found'}, 404
        elif users[username]['secretCode'] != secretCode:
            return {'message': 'Wrong secret code'}, 400
        else:
            users[username]['password'] = newPassword
            users[username]['secretCode'] = get_random_string(8)
            return {'message': 'Password changed successfully'}, 200


api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(FogotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password')

if __name__ == '__main__':
    app.run(debug=True)
