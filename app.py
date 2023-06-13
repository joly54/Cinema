import hashlib
import json
import os
import random
import re
import smtplib
import ssl
import string
import threading
import time as systime
import uuid
from email.message import EmailMessage

import qrcode
from flask import Flask, make_response, send_file, render_template, Response, redirect, url_for, flash, jsonify
from flask import request
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

import config

app = Flask(__name__, template_folder="static")
CORS(app, supports_credentials=True)
api = Api(app)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
login_manager = LoginManager(app)
login_manager.login_view = 'adminlog'
is_local = config.is_local
if is_local:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
    base_url = "http://127.0.0.1:5000"
else:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username="vincinemaApi",
        password=config.dbpass,
        hostname="vincinemaApi.mysql.pythonanywhere-services.com",
        databasename="vincinemaApi$default",
    )
    base_url = "https://vincinemaApi.pythonanywhere.com"
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4', name='Vin-cinema')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ses_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(5), db.ForeignKey('sessions.time'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    expired = db.Column(db.Integer, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)

    user = db.relationship(
        'User',
        backref=backref('payments', cascade='all, delete-orphan'),
        foreign_keys=[user_id]
    )

    session = db.relationship(
        'Sessions',
        backref=backref('payments', cascade='all, delete-orphan'),
        foreign_keys=[ses_id],
    )

    def __repr__(self):
        return "Payment: " + str(self.user_id) + " " + str(self.ses_id) + " " + self.seats + " " + str(
            self.time) + " " + str(self.amount) + " " + str(self.expired) + " " + str(self.confirmed)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False, index=True)
    duration = db.Column(db.Integer, nullable=False)
    trailer = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False, index=True)

    def __repr__(self):
        return "Film: " + self.title + " " + self.trailer + " " + self.description


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), db.ForeignKey('film.title'), nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(10), nullable=False, index=True)
    date = db.Column(db.String(10), nullable=False, index=True)

    film = db.relationship(
        'Film',
        backref=backref('sessions', cascade='all, delete-orphan', lazy='dynamic'),
        foreign_keys=[title, film_id],
        primaryjoin='and_(Sessions.title == Film.title, Sessions.film_id == Film.id)'
    )

    def __repr__(self):
        return "Sessions: " + self.title + " " + str(self.film) + " " + self.seats


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    secret_code = db.Column(db.String(8), nullable=False)
    codeToConfirmEmail = db.Column(db.String(16), nullable=False)
    isEmailConfirmed = db.Column(db.Boolean, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def is_active(self):
        return self.is_admin

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "User: " + self.username + " " + self.password + " " + self.secret_code + " " + self.codeToConfirmEmail + " " + str(
            self.isEmailConfirmed) + " " + str(self.is_admin)


class Tiket(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    date = db.Column(db.String(255), db.ForeignKey('sessions.date'), nullable=False)
    time = db.Column(db.String(255), db.ForeignKey('sessions.time'), nullable=False)
    title = db.Column(db.String(255), db.ForeignKey('sessions.title'), nullable=False)
    seats = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)

    user = db.relationship(
        'User',
        backref=backref('tikets', cascade='all, delete-orphan', lazy='dynamic'),
        foreign_keys=[username],
        primaryjoin='Tiket.username == User.username'
    )

    session = db.relationship(
        'Sessions',
        backref=backref('tikets', cascade='all, delete-orphan', lazy='dynamic'),
        primaryjoin='and_(Tiket.title == Sessions.title, Tiket.date == Sessions.date, Tiket.time == Sessions.time)'
    )

    def __repr__(self):
        return f"Tiket(id='{self.id}', date='{self.date}', time='{self.time}', title='{self.title}', seats='{self.seats}', username='{self.username}')"


# add user but dont show password


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/admin')
@login_required
def admin_panel():
    print(465465655)
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.index'))


class BaseViewer(ModelView):
    can_edit = True
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('adminlog'))


class PaymentView(BaseViewer):
    column_list = ['id', "user.username", "session.title", "seats", "session.date", "session.time", "amount",
                   "confirmed"]
    column_searchable_list = ['id', "user.username", "session.title", "seats", "session.date", "session.time", "amount",
                              "confirmed"]
    column_filters = ['id', "user.username", "session.title", "seats", "session.date", "session.time", "amount",
                      "confirmed"]
    column_sortable_list = ['id', "user.username", "session.title", "seats", "session.date", "session.time", "amount",
                            "confirmed"]
    # add titles for columns
    column_labels = {
        'id': 'ID',
        'user.username': 'Username',
        'session.title': 'Title',
        'seats': 'Seats',
        'session.date': 'Date',
        'session.time': 'Time',
        'amount': 'Amount',
        'confirmed': 'Confirmed'
    }
    column_editable_list = ['confirmed']


class FilmView(BaseViewer):
    column_list = ['id', 'title', 'trailer', 'description']
    column_searchable_list = ['id', 'title', 'trailer', 'description']
    column_filters = ['id', 'title', 'trailer', 'description']
    column_sortable_list = ['id', 'title', 'trailer', 'description']
    column_editable_list = ['title', 'trailer', 'description']


class SessionsView(BaseViewer):
    column_list = ['title', 'seats', 'time', 'date']
    column_searchable_list = ['title', 'seats', 'time', 'date']
    column_filters = ['title', 'seats', 'time', 'date']
    column_sortable_list = ['title', 'seats', 'time', 'date']
    column_editable_list = ['seats', 'time', 'date']


class UserView(BaseViewer):
    column_list = ('id', 'username', 'is_admin', 'isEmailConfirmed')
    column_searchable_list = ('id', 'username', 'is_admin', 'isEmailConfirmed')
    column_filters = ('id', 'username', 'is_admin', 'isEmailConfirmed')
    column_sortable_list = ('id', 'username', 'is_admin', 'isEmailConfirmed')
    column_labels = {
        'id': 'ID',
        'username': 'Username',
        'is_admin': 'Admin',
        'isEmailConfirmed': 'Email Confirmed'
    }
    column_editable_list = ('is_admin', 'isEmailConfirmed', 'username')


class TiketView(BaseViewer):
    column_list = ('id', 'date', 'time', 'title', 'seats', 'username')
    column_searchable_list = ('id', 'date', 'time', 'title', 'seats', 'username')
    column_filters = ('id', 'date', 'time', 'title', 'seats', 'username')
    column_sortable_list = ('id', 'date', 'time', 'title', 'seats', 'username')


class LogoutView(BaseView):

    @expose('/')
    def index(self):
        logout_user()
        return redirect(url_for('adminlog'))


class FillDB(BaseView):
    @expose('/')
    def index(self):
        # check if db is empty
        if Film.query.first() is None:
            import os
            os.system("python newFilingFilms.py")
        else:
            return redirect(url_for('admin.index'))
        return redirect(url_for('admin.index'))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(UserView(User, db.session, name="Users"))
admin.add_view(FilmView(Film, db.session, name="Films"))
admin.add_view(SessionsView(Sessions, db.session, name="Sessions"))
admin.add_view(PaymentView(Payment, db.session, name="Payments"))
admin.add_view(TiketView(Tiket, db.session, name="Tikets"))
admin.add_view(LogoutView(name="Logout"))
admin.add_view(FillDB(name="Fill Database"))


@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    print(current_user.is_authenticated)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        # hash password using md5
        password = hashlib.md5(password.encode()).hexdigest()
        password = hashlib.md5(password.encode()).hexdigest()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('adminlog'))


@app.errorhandler(Exception)
def handle_exception(e):
    try:
        if (e.code == 404):
            html = render_template('404.html')
            return make_response(html, 404)
    except:
        html = render_template('fail.html', message="Something went wrong. Please try again later.",
                               description="Error: " + str(e))
        return make_response(html, 500)


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


def sendTiket(username, tikets):
    sender_email = config.sender_email
    password = config.password
    receiver_email = username
    subject = "Your ticket"

    seat_list = ""
    for seat in tikets.seats:
        seat_list += str(seat) + " "

    body = """
           Your ticket is attached to this email.
           film: {}
           date: {}
           time: {}
           Seats seats: {}
           """.format(tikets.title, tikets.date, tikets.time, seat_list)
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['To'] = receiver_email
    msg['From'] = sender_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        with open(f"tikets/{tikets.id}.png", 'rb') as f:
            file_data = f.read()
            file_name = f"{tikets.title} {tikets.time} Seats: {seat_list} {tikets.date}.png"
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
        print(request.cookies)
        data = request.data.decode('utf-8')
        data = json.loads(data)
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return {'message': 'Wrong username or password'}, 400
        login_user(user)
        return {"message": "OK"}, 200


class Register(Resource):
    def post(self):
        data = request.data.decode('utf-8')
        data = json.loads(data)
        username = data['username']
        password = data['password']
        if username is None or password is None or not is_email(username):
            return {'message': 'Username not email'}, 400
        user = User.query.filter_by(username=username).first()
        if user is None:
            secret_code = get_random_string(8)
            user = User(username=username,
                        password=password,
                        secret_code=secret_code,
                        codeToConfirmEmail=get_random_string(16),
                        isEmailConfirmed=False)
            db.session.add(user)
            db.session.commit()
            sendValidationCode(username, user.codeToConfirmEmail)
            login_user(user)
            return {'message': 'Registered successfully'}, 200
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
    threading.Thread(target=th_sendValidationCode, args=(username, code)).start()


def th_sendValidationCode(username, code):
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
        user.secret_code = get_random_string(8)
        User.query.filter_by(username=username).update(dict(secret_code=user.secret_code))
        db.session.commit()
        send_email(username, user.secret_code)
        return {'message': 'Email sent successfully'}, 200


class ResetPassword(Resource):
    def post(self):
        username = request.args.get('username')
        password = request.args.get('password')
        secret_code = request.args.get('secret_code')
        # return {"Secret code": secret_code, "Password": password, "Username": username, "Message": "OK"},200
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {'message': 'User not found'}, 404
        if user.secret_code != secret_code:
            return {'message': 'Wrong secret code'}, 400
        user.password = password
        user.secret_code = get_random_string(8)
        User.query.filter_by(username=username).update(dict(password=password, secret_code=user.secret_code))
        return {'message': 'Password reset successfully'}, 200


class Schedule(Resource):
    def get(self):
        sessions = Sessions.query.all()
        answer = []
        dates = {}
        for session in sessions:
            if session.date not in dates:
                dates[session.date] = []
        for session in sessions:
            dates[session.date].append(
                {
                    "time": session.time,
                    "title": session.title,
                    "trailer": session.film.trailer,
                    "seats": eval(session.seats),
                    "session_id": session.id,
                    "price": session.film.price,
                    "description": session.film.description,
                    "film_id": session.film_id,
                    "poster": base_url + "/Posters/" + str(session.film_id)
                }
            )
        for date in dates:
            answer.append({"date": date, "sessions": dates[date]})
        return answer, 200


class DisplayTikets(Resource):
    def get(self):
        tikets = Tiket.query.all()
        for tiket in tikets:
            print(
                f"Username: {tiket.username} Date: {tiket.date} Title: {tiket.title} Time: {tiket.time} seats: {tiket.seats} Id: {tiket.id}")
        return {'message': 'Data displayed successfully'}, 200


class ticket_qr(Resource):
    def get(self, id):
        filename = "/home/vincinemaApi/tikets/" + id
        return send_file(filename, mimetype='image/png')


class send_poster(Resource):
    def get(self, id):
        filename = "/home/vincinemaApi/Cinema/Posters/" + id + ".jpg"
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not os.path.isfile(filename):
            return {'message': 'Poster not found'}, 404
        return send_file(filename, mimetype='image/png')


class get_nav(Resource):
    def get(self):
        if current_user.is_authenticated and current_user.is_admin:
            return [{
                "title": "Admin Panel",
                "url": base_url + "/adminlog"
            }], 200
        return [], 200


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


class UserInformation(Resource):
    def get(self):
        if not current_user.is_authenticated:
            return {'message': 'User not logged in'}, 400
        res = {}
        res['username'] = current_user.username
        res['isEmailConfirmed'] = current_user.isEmailConfirmed
        tikets = Tiket.query.filter_by(username=current_user.username).all()
        res['tikets'] = []
        for tiket in tikets:
            data = {
                "username": tiket.username,
                "date": tiket.date,
                "title": tiket.title,
                "time": tiket.time,
                "seats": tiket.seats,
                "id": tiket.id,
                "urltoqr": base_url + "/tikets/" + tiket.id + '.png'
            }
            res['tikets'].append(data)
        return res, 200


def checkPayment(id, expired):
    print("running checkPayment")
    time = systime.time()
    systime.sleep(expired - time)
    with app.app_context():
        payment = Payment.query.filter_by(id=id).first()
        if payment is None:
            return
        if payment.confirmed:
            return
        else:
            print("Payment not confirmed, id: " + str(id))
            f = open("log.txt", "a")
            f.write("Payment not confirmed, id: " + str(id) + "\n")
            f.close()
            session = Sessions.query.filter_by(id=payment.ses_id).first()
            seats = eval(session.seats)
            mised_seats = eval(payment.seats)
            for seat in mised_seats:
                seats.append(seat)
            seats.sort()
            session.seats = str(seats)
            db.session.commit()
            db.session.delete(payment)
            db.session.commit()
            return


class BuyTikets(Resource):
    def post(self):
        seats = request.headers.get('seats')
        ses_id = request.args.get('sessions_id')
        if current_user.username is None or seats is None or ses_id is None:
            return {'message': 'Wrong data'}, 400
        if not current_user.is_authenticated:
            return {'message': 'User not logged in'}, 400
        if current_user.isEmailConfirmed == False:
            return {'message': 'Email not confirmed'}, 400
        ses = Sessions.query.filter_by(id=ses_id).first()
        if ses is None:
            return {'message': 'Session not found'}, 404
        seats = json.loads(seats)
        if len(seats) == 0:
            return {'message': 'No seats selected'}, 400
        aviable_seats = json.loads(ses.seats)
        if not all(elem in aviable_seats for elem in seats):
            return {'message': 'Seats not available'}, 400
        pay = Payment(
            ses_id=ses.id,
            seats=str(seats),
            amount=ses.film.price * len(seats),
            time=ses.time,
            expired=int(systime.time()) + 60 * 5,
            confirmed=False,
            user=current_user
        )
        for seat in seats:
            aviable_seats.remove(seat)
        ses.seats = str(aviable_seats)
        db.session.add(pay)
        db.session.commit()
        threading.Thread(target=checkPayment, args=(pay.id, pay.expired)).start()
        return {
            'message': 'Payment created',
            'id': pay.id,
            "amount": pay.amount,
            "Pay_created": pay.time,
            "expired": pay.expired,
            "title": ses.title,
            "date": ses.date,
            "time": ses.time,
            "seats": pay.seats
        }, 200


class confirm_Payment(Resource):
    def get(self):
        id = request.args.get('payment_id')
        payment = Payment.query.filter_by(id=id).first()
        if payment is None:
            return {'message': 'Payment not found'}, 404
        if payment.confirmed:
            return {'message': 'Payment already confirmed'}, 400
        payment.confirmed = True
        db.session.commit()
        ses = Sessions.query.filter_by(id=payment.ses_id).first()
        seats = payment.seats
        date = ses.date
        title = ses.title
        time = ses.time
        username = User.query.filter_by(id=payment.user_id).first().username
        tiket = Tiket(username=username, date=date, title=title, time=time, seats=str(seats), id=get_random_string(16))
        data = {
            "username": tiket.username,
            "date": tiket.date,
            "title": tiket.title,
            "time": tiket.time,
            "seats": tiket.seats,
            "id": tiket.id,
            "urltoqr": base_url + "/tikets/" + tiket.id + '.png'
        }
        img = qrcode.make(data)
        img.save("tikets/" + tiket.id + '.png')
        db.session.add(tiket)
        db.session.commit()
        sendTiket(username, tiket)
        return {"message": "Tikets bought successfully"}, 200


class getSessionInfo(Resource):
    def get(self):
        ses_id = request.args.get('ses_id')
        ses = Sessions.query.filter_by(id=ses_id).first()
        if ses is None:
            return {'message': 'Session not found'}, 404
        ans = {}
        ans['message'] = 'Success'
        ans['title'] = ses.title
        film = Film.query.filter_by(id=ses.film_id).first()
        ans['title'] = film.title
        ans['trailer'] = film.trailer
        ans['seats'] = json.loads(ses.seats)
        ans['description'] = film.description
        ans['price'] = film.price
        ans['poster'] = base_url + "/Posters/" + str(film.id)
        return ans, 200


class dbinfo(Resource):
    def get(self):
        metadata = db.MetaData()

        # Reflect the database schema
        metadata.reflect(bind=db.engine)

        # Get all table names
        table_names = metadata.tables.keys()
        return str(table_names), 200


class is_user_Authenticated(Resource):
    def get(self):
        if current_user.is_authenticated:
            return {'message': 'User is authenticated'}, 200
        else:
            return {'message': 'User is not authenticated'}, 400


class getFilms(Resource):
    def get(self):
        films = Film.query.all()
        res = []
        for film in films:
            res.append({
                "id": film.id,
                "duration": film.duration,
                "title": film.title,
                "description": film.description,
                "price": film.price,
                "trailer": film.trailer,
                "poster": base_url + "/Posters/" + str(film.id)
            })
        return res, 200


class getSessions(Resource):
    def get(self):
        id = request.args.get('film_id')
        try:
            id = int(id)
        except:
            return {'message': 'Bad request'}, 400
        sessions = Sessions.query.filter_by(film_id=id).all()
        if sessions is None:
            return {'message': 'Film not found'}, 404
        res = {}
        film = Film.query.filter_by(id=id).first()
        res['title'] = film.title
        res['poster'] = base_url + "/Posters/" + str(film.id)
        res['trailer'] = film.trailer
        res['description'] = film.description
        res['price'] = film.price
        res['sessions'] = []
        for ses in sessions:
            res['sessions'].append({
                "id": ses.id,
                "title": ses.title,
                "date": ses.date,
                "time": ses.time,
                "seats": json.loads(ses.seats)
            })
        return res, 200


class GetSession(Resource):
    def get(self):
        ses_id = request.args.get('ses_id')
        ses = Sessions.query.filter_by(id=ses_id).first()
        ans = {}
        if ses is None:
            return {'message': 'Session not found'}, 404
        ans['message'] = 'Success'
        film = Film.query.filter_by(id=ses.film_id).first()
        if film is None:
            return {'message': 'Film not found'}, 404
        ans['title'] = ses.title
        ans["date"] = ses.date
        ans["time"] = ses.time
        ans['trailer'] = film.trailer
        ans['seats'] = json.loads(ses.seats)
        ans['description'] = film.description
        ans['price'] = film.price
        ans["duration"] = film.duration
        ans["poster"] = base_url + "/Posters/" + str(film.id)
        return ans, 200


class logout_us(Resource):
    def get(self):
        logout_user()
        return {'message': 'User logged out'}, 200


import requests
import time

BANNED_IPS = []
WHITE_LIST = ["127.0.0.1", "91.225.38.69"]
REQUEST_THRESHOLD = 200
TIME_WINDOW = 60  # Time window in seconds

user_requests = {}  # Dictionary to store the number of requests per user and the last request timestamp


def send_notification(text):
    bot_token = config.bot_token
    chat_id = '800918003'
    message_text = text

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message_text
    }

    response = requests.post(url, data=payload)


class BanMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # get real ip
        ip_address = environ.get('HTTP_X_REAL_IP', environ.get('REMOTE_ADDR'))

        # Check if the IP is already banned
        if ip_address in BANNED_IPS:
            start_response('403 Forbidden', [('Content-Type', 'text/plain')])
            return [b'Forbidden']

        # Check if the IP is whitelisted
        if ip_address not in WHITE_LIST:
            current_time = time.time()
            if ip_address in user_requests:
                requests_info = user_requests[ip_address]
                num_requests, last_request_time = requests_info

                if current_time - last_request_time > TIME_WINDOW:
                    num_requests = 1
                else:
                    num_requests += 1
            else:
                num_requests = 1

            # Update the user_requests dictionary with the new count and timestamp
            user_requests[ip_address] = (num_requests, current_time)
            if num_requests > REQUEST_THRESHOLD:
                BANNED_IPS.append(ip_address)
                send_notification(f'IP {ip_address} is banned')

                start_response('403 Forbidden', [('Content-Type', 'text/plain')])
                return [b'Forbidden']

        return self.app(environ, start_response)


app.wsgi_app = BanMiddleware(app.wsgi_app)

# User Authentication and Account Management
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(FogotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(ConfirmEmail, '/confirmEmail')
api.add_resource(isEmailConfirmed, '/isEmailConfirmed')
api.add_resource(ResendEmailValidationCode, '/resendEmailValidationCode')
api.add_resource(userConfirmEmail, '/userConfirmEmail')
api.add_resource(get_nav, '/getnav')
api.add_resource(is_user_Authenticated, '/isUserAuthenticated')
api.add_resource(logout_us, '/logout')

# Displaying Information
api.add_resource(DisplayTikets, '/displayTikets')
api.add_resource(getSessionInfo, '/getSessionInfo')
api.add_resource(getFilms, '/getFilms')
api.add_resource(Schedule, '/schedule')
api.add_resource(getSessions, '/getSessions')
api.add_resource(GetSession, '/getSession')

# Ticket Management
api.add_resource(BuyTikets, '/buyTikets')
api.add_resource(confirm_Payment, '/confirmPayment')

# User Information
api.add_resource(UserInformation, '/userinfo')

# image
api.add_resource(ticket_qr, '/tikets/<id>')
api.add_resource(send_poster, '/Posters/<id>')

# Database Information
api.add_resource(dbinfo, '/dbinfo')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
