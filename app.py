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
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
try:
    with open('days.json') as f:
        days = json.load(f)
except:
    pass


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    secret_code = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}', token='{self.token}', secret_code='{self.secret_code}')"


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
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    return response





class Login(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return {'error': 'Wrong username or password'}, 400
        return {'message': 'Logged in successfully', 'token': user.token}, 200


class Register(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        print(password)
        if username is None or password is None or not is_email(username):
            return {'error': 'Bad request'}, 400
        user = User.query.filter_by(username=username).first()
        if user is None:
            token = get_random_string(32)
            secret_code = get_random_string(8)
            user = User(username=username, password=password, token=token, secret_code=secret_code)
            db.session.add(user)
            db.session.commit()
            return {'message': 'User registered successfully', 'token': token}, 201
        return {'error': 'User already exists'}, 409


class FogotPassword(Resource):
    def post(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'error': 'User not found'}, 404
        send_email(username, user.secret_code)
        return {'message': 'Email sent successfully'}, 200


class ResetPassword(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        secret_code = request.args.get('secret_code')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'error': 'User not found'}, 404
        if user.secret_code != secret_code:
            return {'error': 'Wrong secret code'}, 400
        user.password = password
        db.session.commit()
        return {'message': 'Password reset successfully'}, 200


class Display(Resource):
    def get(self):
        users = User.query.all()
        for user in users:
            print(
                f"Username: {user.username} Password: {user.password} Token: {user.token} Secret code: {user.secret_code}")
        return {'message': 'Data displayed successfully'}, 200
class getDay(Resource):
    def get(self):
        date = request.args.get('date')
        print(days)
        if date in days:
            return {"message": "succes", "day": days[date]}, 200
        else:
            return {'message': 'Date not found'}, 404
class fullSchedule(Resource):
    def get(self):
        return days, 200

class buyTicket(Resource):
    def post(self):
        #get arguments from header
        token = request.headers.get('token')
        date = request.headers.get('date')
        title = request.headers.get('title')
        time = request.headers.get('time')
        number = int(request.headers.get('number'))
        print(type(number))
        print(f"token: {token} date: {date} title: {title} time: {time} number: {number}")
        user = User.query.filter_by(token=token).first()
        if user is None:
            return {'error': 'User not found'}, 404
        if token != user.token:
            return {'error': 'Wrong token'}, 400
        if date in days:
            for film in days[date]['films']:
                if title == film['title']:
                    if time ==film["beginTime"]:
                        if number in film["aviableTikets"]:
                            film["aviableTikets"].remove(number)
                            with open('days.json', 'w') as f:
                                json.dump(days, f)
                            return {'message': 'Ticket bought successfully'}, 200
                        else:
                            return {'message': 'Seat not found'}, 404
                    else:
                        return {'message': 'Time not found'}, 404
            else:
                return {'message': 'Title not found'}, 404
        else:
            return {'message': 'Date not found'}, 404




api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(FogotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(Display, '/display')
api.add_resource(getDay, '/getDay')
api.add_resource(fullSchedule, '/fullSchedule')
api.add_resource(buyTicket, '/buyTicket')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
