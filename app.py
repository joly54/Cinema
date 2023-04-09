import json
import random
import re
import smtplib
import ssl
import string
import time as systime
from email.message import EmailMessage

import qrcode
from flask import Flask, jsonify, make_response, request, send_file, render_template, Response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__, template_folder="static")
api = Api(app)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="testaccjgh",
    password=config.dbpass,
    hostname="testaccjgh.mysql.pythonanywhere-services.com",
    databasename="testaccjgh$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
base_url = "http://127.0.0.1:5000"
try:
    with open('days.json') as f:
        days = json.load(f)
except:
    pass

#add error handler
@app.errorhandler(404)
def not_found(error):
    html = render_template('404.html')
    return make_response(html, 404)
#add error handler for all error
@app.errorhandler(Exception)
def handle_exception(e):
    if(e.code == 404):
        html = render_template('404.html')
        return make_response(html, 404)
    else:
        html = render_template('fail.html', message="Something went wrong. Please try again later." , description="Error: " + str(e))
        return make_response(html, 500)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    secret_code = db.Column(db.String(8), nullable=False)
    sesionValidTo = db.Column(db.Integer, nullable=False)
    codeToConfirmEmail = db.Column(db.String(16), nullable=False)
    isEmailConfirmed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}', token='{self.token}', secret_code='{self.secret_code}', sesionValidTo='{self.sesionValidTo}', codeToConfirmEmail='{self.codeToConfirmEmail}', isEmailConfirmed='{self.isEmailConfirmed}')"


class Tiket(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.String(255), nullable=False)
    time = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Tiket(id='{self.id}', date='{self.date}', time='{self.time}', title='{self.title}', number='{self.number}', username='{self.username}')"


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


def sendTiket(username, tiket):
    sender_email = config.sender_email
    password = config.password
    receiver_email = username
    subject = "Your ticket"

    body = """
    Your ticket is attached to this email.
    film: {}
    date: {}
    time: {}
    Seats number: {}
    """.format(tiket.title, tiket.date, tiket.time, tiket.number)
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = sender_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        with open(f"mysite/tikets/{tiket.id}.png", 'rb') as f:
            file_data = f.read()
            file_name = f"{tiket.title} {tiket.time} Seats: {tiket.number} {tiket.date}.png"
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)
        server.send_message(msg)
def sendManyTikets(username, tikets):
    sender_email = config.sender_email
    password = config.password
    receiver_email = username
    subject = "Your tickets"

    body = """
    Your tickets are attached to this email.
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = sender_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        for tiket in tikets:
            with open(f"mysite/tikets/{tiket['id']}.png", 'rb') as f:

                file_data = f.read()
                file_name = f"{tiket['title']} {tiket['time']} Seats: {tiket['number']} {tiket['date']}.png"
            msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)
        server.send_message(msg)


def is_email(username):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, username))


def get_random_string(length):
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
            return {'message': 'Wrong username or password'}, 400

        user.token = get_random_string(32)
        user.sesionValidTo = int(systime.time()) + 3600 * 24
        db.session.commit()
        resp = make_response(
            jsonify({'message': 'Logged in successfully', "token": user.token, "validDue": user.sesionValidTo}), 200)
        resp.set_cookie('token', user.token)
        return resp


class Register(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        print(password)
        if username is None or password is None or not is_email(username):
            return {'message': 'Bad request'}, 400
        user = User.query.filter_by(username=username).first()
        if user is None:
            token = get_random_string(32)
            secret_code = get_random_string(8)
            user = User(username=username,
                        password=password,
                        token=token,
                        secret_code=secret_code,
                        sesionValidTo=int(systime.time()) + 3600 * 24,
                        codeToConfirmEmail=get_random_string(16),
                        isEmailConfirmed=False)
            db.session.add(user)
            db.session.commit()
            resp = make_response(
                jsonify({'message': 'Registered successfully', "token": token, "validDue": user.sesionValidTo}), 200)
            resp.set_cookie('token', token)
            return resp
        return {'message': 'User already exists'}, 409


class isEmailConfirmed(Resource):
    def get(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if user.isEmailConfirmed:
            return {'message': 'Email confirmed'}, 200
        return {'message': 'Email not confirmed'}, 200


def sendValidationCode(username, code):
    sender_email = config.sender_email
    password = config.password
    receiver_email = username
    subject = "Verification code"
    body = f"To confirm your email, click on the link <a href='{base_url}/userConfirmEmail?username={username}&code={code}'>{base_url}/userConfirmEmail?username={username}&code={code}</a>, or enter code <strong>{code}</strong> in the app. If you didn't register in the app, just ignore this message."
    msg = EmailMessage()
    msg.set_content(body, subtype='html')
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = sender_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)



class ConfirmEmail(Resource):
    def get(self):
        username = request.args.get('username')
        code = request.args.get('code')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if code == "-1":

            if user.isEmailConfirmed:
                return {'message': 'Email confirmed'}, 200
            else:
                return {'message': 'Email not confirmed'}, 200
        if user.isEmailConfirmed:
            return {'message': 'Email already confirmed'}, 400
        if code is None:
            sendValidationCode(username, user.codeToConfirmEmail)
            return {'message': 'Email sent successfully'}, 200
        if user.codeToConfirmEmail != code:
            return {'message': 'Wrong code'}, 400
        if code == user.codeToConfirmEmail:
            user.isEmailConfirmed = True
            db.session.commit()
            return {'message': 'Email confirmed'}, 200


class FogotPassword(Resource):
    def post(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        send_email(username, user.secret_code)
        return {'message': 'Email sent successfully'}, 200


class ResetPassword(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        secret_code = request.args.get('secret_code')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if user.secret_code != secret_code:
            return {'message': 'Wrong secret code'}, 400
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

        token = request.headers.get('token')
        date = request.headers.get('date')
        title = request.headers.get('title')
        time = request.headers.get('time')
        number = int(request.headers.get('number'))
        username = request.headers.get('username')
        print(type(number))
        print(f"token: {token} date: {date} title: {title} time: {time} number: {number}")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        print(f"Curent time: {int(systime.time())} Valid to: {user.sesionValidTo}")
        if token != user.token or username != user.username or int(systime.time()) > user.sesionValidTo:
            return {'message': 'Wrong token or session expired'}, 400
        if user.isEmailConfirmed == False:
            return {'message': 'Email not confirmed'}, 400
        if date in days:
            for film in days[date]['films']:
                if title == film['title']:
                    if time == film["beginTime"]:
                        if number in film["aviableTikets"]:
                            film["aviableTikets"].remove(number)
                            with open('days.json', 'w') as f:
                                json.dump(days, f)
                            id = get_random_string(16)
                            data = {
                                "date": date,
                                "title": title,
                                "time": time,
                                "number": number,
                                "id": id,
                                "urltoqr": base_url + "/tikets/" + id + '.png'
                            }
                            img = qrcode.make(data)
                            type(img)
                            import os
                            if not os.path.exists("tikets"):
                                os.mkdir("tikets")
                            img.save("mysite/tikets/" + id + '.png')

                            tiket = Tiket(username=username, date=date, title=title, time=time, number=number, id=id)
                            db.session.add(tiket)
                            db.session.commit()
                            sendTiket(user.username, tiket)
                            return {'message': 'Ticket bought successfully', "data": data}, 200
                        else:
                            return {'message': 'Seat not found'}, 404
                    else:
                        return {'message': 'Time not found'}, 404
            else:
                return {'message': 'Title not found'}, 404
        else:
            return {'message': 'Date not found'}, 404


class DisplayTikets(Resource):
    def get(self):
        tikets = Tiket.query.all()
        for tiket in tikets:
            print(
                f"Username: {tiket.username} Date: {tiket.date} Title: {tiket.title} Time: {tiket.time} Number: {tiket.number} Id: {tiket.id}")
        return {'message': 'Data displayed successfully'}, 200


class getTikets(Resource):
    def get(self):
        username = request.args.get('username')
        token = request.args.get('token')

        tikets = Tiket.query.filter_by(username=username).all()
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        print(f"username: {username} token: {token} user.token: {user.token}")
        if user.token != token or int(systime.time()) > user.sesionValidTo:
            return {'message': 'Wrong token or sessoin expired'}, 400
        tiketslist = []
        for tiket in tikets:
            tiketslist.append({
                "date": tiket.date,
                "title": tiket.title,
                "time": tiket.time,
                "number": tiket.number,
                "id": tiket.id,
                "urltoqr": base_url + "/tikets/" + tiket.id + '.png'
            })
        return {"message": "succes", "tikets": tiketslist}, 200


class serve_image(Resource):
    def get(self, id):
        filename = "tikets/" + id
        return send_file(filename, mimetype='image/png')


class checkToken(Resource):
    def get(self):
        token = request.args.get('token')
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if token != user.token or username != user.username or int(systime.time()) > user.sesionValidTo:
            return {'message': 'Token not valid'}, 200
        return {'message': 'Token valid'}, 200


class ResendEmailValidationCode(Resource):
    def get(self):
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if user.isEmailConfirmed == True:
            return {'message': 'Email already confirmed'}, 400
        user.codeToConfirmEmail = get_random_string(16)
        db.session.commit()
        sendValidationCode(username, user.codeToConfirmEmail)
        return {'message': 'Email sent successfully'}, 200


class userConfirmEmail(Resource):
    def get(self):
        username = request.args.get('username')
        code = request.args.get('code')
        user = User.query.filter_by(username=username).first()
        if user is None:
            html = render_template("fail.html", message="Something Went Wrong", description="User not found")
            return Response(html, status=404, content_type="text/html")
        if user.codeToConfirmEmail != code or user.isEmailConfirmed == True:
            html = render_template("fail.html", message="Something Went Wrong", description="Wrong code or email "
                                                                                            "already confirmed")
            return Response(html, status=404, content_type="text/html")
        user.isEmailConfirmed = True
        db.session.commit()
        html = render_template("succes.html")
        return Response(html, status=200, content_type="text/html")
class BuyManyTikets(Resource):
    def post(self):

        token = request.headers.get('token')
        date = request.headers.get('date')
        title = request.headers.get('title')
        time = request.headers.get('time')
        numbers = json.loads(request.headers.get('number'))
        username = request.headers.get('username')
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        print(f"Curent time: {int(systime.time())} Valid to: {user.sesionValidTo}")
        if token != user.token or username != user.username or int(systime.time()) > user.sesionValidTo:
            return {'message': 'Wrong token or session expired'}, 400
        if user.isEmailConfirmed == False:
            return {'message': 'Email not confirmed'}, 400
        if date in days:
            for film in days[date]['films']:
                if title == film['title']:
                    if time == film["beginTime"]:
                        if all(item in film['aviableTikets'] for item in numbers):
                            tikets = []
                            for number in numbers:
                                film['aviableTikets'].remove(number)
                                tiket = Tiket(username=username, date=date, title=title, time=time, number=number, id=get_random_string(16))
                                data = {
                                    "username": tiket.username,
                                    "date": tiket.date,
                                    "title": tiket.title,
                                    "time": tiket.time,
                                    "number": tiket.number,
                                    "id": tiket.id,
                                    "urltoqr": base_url + "/tikets/" + tiket.id + '.png'
                                }
                                tikets.append(data)
                                img = qrcode.make(data)
                                type(img)
                                import os
                                if not os.path.exists("tikets"):
                                    os.mkdir("tikets")
                                img.save("mysite/tikets/" + tiket.id + '.png')
                                db.session.add(tiket)
                            db.session.commit()
                            sendManyTikets(username, tikets)
                            return {'message': 'Ticket bought successfully', "data": tikets}, 200
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
api.add_resource(DisplayTikets, '/displayTikets')
api.add_resource(getTikets, '/getTikets')
api.add_resource(serve_image, '/tikets/<id>')
api.add_resource(ConfirmEmail, '/confirmEmail')
api.add_resource(isEmailConfirmed, '/isEmailConfirmed')
api.add_resource(checkToken, '/checkToken')
api.add_resource(ResendEmailValidationCode, '/resendEmailValidationCode')
api.add_resource(userConfirmEmail, '/userConfirmEmail')
api.add_resource(BuyManyTikets, '/buyManyTikets')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
