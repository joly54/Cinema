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
from PIL import Image
from flasgger import Swagger
from flask import Flask, make_response, send_file, render_template, Response, redirect, url_for, flash
from flask import request
from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from sqlalchemy import DateTime
from sqlalchemy.orm import backref

import config

app = Flask(__name__, template_folder="static")
swagger = Swagger(app)
CORS(app, supports_credentials=True)
api = Api(app)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'None'
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

app.config['TIMEZONE'] = 'Europe/Kiev'
# set app title
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

login_manager = LoginManager(app)
login_manager.login_view = 'adminlog'

is_local = config.is_local
if is_local:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
    base_url = "http://127.0.0.1:5000"
    base_dir = ""
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
    base_dir = "/home/vincinemaApi/Cinema/"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"
db = SQLAlchemy(app)
admin = Admin(app, template_mode='bootstrap4', name='Vin-cinema')

# init flask migrate
migrate = Migrate(app, db)
migrate.init_app(app, db)


class User(UserMixin, db.Model):
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

    def __repr__(self):
        return "Email: " + self.username


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False, index=True)
    duration = db.Column(db.Integer, nullable=False)
    trailer = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False, index=True)

    pos = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return self.title


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
        return "Session: " + self.title + " Time: " + self.time + " Date: " + self.date + " Seats: " + self.seats


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ses_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    seats = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(5), db.ForeignKey('sessions.time'), nullable=True)
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


class Tiket(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=str(uuid.uuid4()))
    date = db.Column(db.String(255), db.ForeignKey('sessions.date'), nullable=False)
    time = db.Column(db.String(255), db.ForeignKey('sessions.time'), nullable=False)
    title = db.Column(db.String(255), db.ForeignKey('sessions.title'), nullable=False)
    seats = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), db.ForeignKey('user.username'), nullable=False)

    checked = db.Column(DateTime, nullable=True)

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
    can_create = False


class FilmView(BaseViewer):
    column_list = ['id', 'title', 'trailer', 'description', 'price', 'pos']
    column_searchable_list = ['id', 'title', 'trailer', 'description']
    column_filters = ['id', 'title', 'trailer', 'description', 'price']
    column_sortable_list = ['id', 'title', 'trailer', 'description', 'price']
    column_editable_list = ['title', 'trailer', 'description', 'price']

    form_columns = ['title', 'trailer', 'description', 'price', 'pos']


class SessionsView(BaseViewer):
    column_list = ['title', 'seats', 'time', 'date']
    column_searchable_list = ['title', 'seats', 'time', 'date']
    column_filters = ['title', 'seats', 'time', 'date']
    column_sortable_list = ['title', 'seats', 'time', 'date']
    column_editable_list = ['seats', 'time', 'date']

    # add film to form
    form_columns = ['title', 'seats', 'time', 'date', 'film']


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
    column_list = ('id', 'date', 'time', 'title', 'seats', 'username', 'checked')
    column_searchable_list = ('id', 'date', 'time', 'title', 'seats', 'username', 'checked')
    column_filters = ('id', 'date', 'time', 'title', 'seats', 'username')
    column_sortable_list = ('id', 'date', 'time', 'title', 'seats', 'username', 'checked')
    # add id in create form
    form_columns = ('id', "user", "session", "seats", "checked")

    def on_model_delete(self, model):
        print(model)
        if os.path.exists(f"{base_dir}tikets/{model.id}.png"):
            flash(f"Deleted Image {model.id}.png Title: {model.title} Username: {model.username} ", "success")
            os.remove(f"{base_dir}tikets/{model.id}.png")
        else:
            flash(f"Image {model.id}.png not found", "danger")

    # make some actions on create
    def on_model_change(self, form, model, is_created):

        if not is_created:
            return

        if os.path.exists(f"{base_dir}tikets/{model.id}.png"):
            os.remove(f"{base_dir}tikets/{model.id}.png")
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(f"{base_url}/check_ticket/{model.id}")
        qr.make(fit=True)
        mask = Image.open(base_dir + "Posters/mask.jpg")

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=ImageColorMask(
                color_mask_image=mask
            )
        )

        if not os.path.exists("tikets"):
            os.makedirs("tikets")
        img.save("tikets/" + model.id + '.png')
        sendTiket(model.user.username, model)
        flash(f"Created Image {model.id}.png Title: {model.title} Username: {model.username} ", "success")


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


class all_images(BaseView):
    @expose('/')
    def index(self):
        images = os.listdir(base_dir + 'Posters')
        for image in images:
            if image.find(".") == -1:
                images.remove(image)
        images.sort()
        return render_template('admin/all_images.html', images=images)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(UserView(User, db.session, name="Users"))
admin.add_view(FilmView(Film, db.session, name="Films"))
admin.add_view(SessionsView(Sessions, db.session, name="Sessions"))
admin.add_view(PaymentView(Payment, db.session, name="Payments"))
admin.add_view(TiketView(Tiket, db.session, name="Tikets"))
admin.add_view(all_images(name="All Images"))
admin.add_view(FillDB(name="Fill Database"))
admin.add_view(LogoutView(name="Logout"))


@app.route('/fix_names')
def fix_names():
    films = Film.query.all()
    for film in films:
        os.rename(f"Posters/{film.id}.jpg", f"Posters/{film.title.replace(' ', '_').replace(':', '').lower()}.jpg")
        film.poster = f"{film.title.replace(' ', '_').lower()}.jpg"
        db.session.commit()
    return {"status": "ok"}

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
            login_user(user, remember=True)
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('adminlog'))


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
    for seat in eval(tikets.seats):
        seat_list += str(seat) + ", "
    seat_list = seat_list[:-2]

    body = """
           Your ticket is attached to this email.
           film: {}
           date: {}
           time: {}
           Seats: {}
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
        """
        Authenticate user credentials and initiate a login session.

        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The username of the user.
                password:
                  type: string
                  description: The password of the user.

        responses:
          200:
            description: Authentication successful. Returns a success message.
          400:
            description: Invalid username or password. Returns an error message.

        """
        print(request.cookies)
        data = request.data.decode('utf-8')
        data = json.loads(data)
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if user is None or user.password != password:
            return {'message': 'Invalid username or password'}, 400
        login_user(user, remember=True)
        return {"message": "Authentication successful"}, 200


@app.route('/delete_image/<string:filename>')
def delete_image(filename):
    os.remove(base_dir + "Posters/" + filename)
    flash(f"Image {filename} deleted successfully", "success")
    return redirect("/admin/all_images/")


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        flash('No image file selected.', 'error')
        return redirect('/')

    image = request.files['image']
    if image.filename == '':
        flash('No image file selected.', 'error')
        return redirect('/')

    filename = image.filename
    image.save(base_dir + "Posters/" + filename.replace(' ', '_').replace(':', '').lower())
    flash('Image uploaded successfully.', 'success')
    return redirect('/admin/all_images/')


class Register(Resource):
    def post(self):
        """
        Register a new user with the provided username and password.

        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The email address to be used as the username.
                password:
                  type: string
                  description: The password for the new user.

        responses:
          200:
            description: Registration successful. Returns a success message.
          400:
            description: Invalid username or password format. Returns an error message.
          409:
            description: User already exists. Returns an error message.

        """
        data = request.data.decode('utf-8')
        data = json.loads(data)
        username = data['username']
        password = data['password']

        if username is None or password is None or not is_email(username):
            return {'message': 'Invalid username format. Please provide a valid email address.'}, 400

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
            return {'message': 'Registration successful'}, 200

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
        """
        Confirm the email address of a user.

        ---
        parameters:
          - name: username
            in: query
            type: string
            required: true
            description: The username (email address) of the user.
          - name: code
            in: query
            type: string
            required: false
            description: The verification code sent to the user's email address.

        responses:
          200:
            description: Email confirmation status or success messages returned.
          400:
            description: Invalid verification code or email already confirmed. Returns an error message.
          404:
            description: User not found. Returns an error message.

        """
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
            return {'message': 'Verification code sent successfully'}, 200

        if user.codeToConfirmEmail != code:
            return {'message': 'Invalid verification code'}, 400

        if code == user.codeToConfirmEmail:
            user.isEmailConfirmed = True
            db.session.commit()
            return {'message': 'Email confirmed'}, 200


class ForgotPassword(Resource):
    def post(self):
        """
        Initiate the password reset process for a user.

        ---
        parameters:
          - name: username
            in: query
            type: string
            required: true
            description: The username (email address) of the user.

        responses:
          200:
            description: Password reset email sent successfully.
          404:
            description: User not found. Returns an error message.

        """
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()

        if user is None:
            return {'message': 'User not found'}, 404

        user.secret_code = get_random_string(8)
        User.query.filter_by(username=username).update(dict(secret_code=user.secret_code))
        db.session.commit()

        send_email(username, user.secret_code)
        return {'message': 'Password reset email sent successfully'}, 200


class ResetPassword(Resource):
    def post(self):
        """
        Reset the password for a user.

        ---
        parameters:
          - name: username
            in: query
            type: string
            required: true
            description: The username (email address) of the user.
          - name: password
            in: query
            type: string
            required: true
            description: The new password for the user.
          - name: secret_code
            in: query
            type: string
            required: true
            description: The secret code sent to the user for password reset.

        responses:
          200:
            description: Password reset successful. Returns a success message.
          400:
            description: Invalid secret code or user not found. Returns an error message.
          404:
            description: User not found. Returns an error message.

        """
        username = request.args.get('username')
        password = request.args.get('password')
        secret_code = request.args.get('secret_code')

        user = User.query.filter_by(username=username).first()

        if user is None:
            return {'message': 'User not found'}, 404

        if user.secret_code != secret_code:
            return {'message': 'Invalid secret code'}, 400

        user.password = password
        user.secret_code = get_random_string(8)
        User.query.filter_by(username=username).update(dict(password=password, secret_code=user.secret_code))

        return {'message': 'Password reset successful'}, 200


class Schedule(Resource):
    def get(self):
        """
        Get the schedule of movie sessions.

        ---
        responses:
          200:
            description: Schedule retrieved successfully. Returns a list of sessions grouped by date.

        """
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
                    "poster": base_url + "/Posters/" + str(session.film.pos)
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
        filename = "tikets/" + id
        if not os.path.isfile(filename):
            return {'message': 'Ticket not found'}, 404
        return send_file(filename, mimetype='image/png')


class send_poster(Resource):
    def get(self, id):
        filename = base_dir + "Posters/" + id
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        if not os.path.isfile(filename):
            return {'message': 'Poster not found'}, 404
        return send_file(filename, mimetype='image/png')


class GetNav(Resource):
    def get(self):
        """
        Get the navigation links for the current user.

        ---
        responses:
          200:
            description: Navigation links retrieved successfully. Returns a list of navigation links.

        """
        if current_user.is_authenticated and current_user.is_admin:
            return [{
                "title": "Admin Panel",
                "url": base_url + "/adminlog"
            }], 200
        return [], 200


class ResendEmailValidationCode(Resource):
    def get(self):
        """
        Resend the email validation code to a user.

        ---
        parameters:
          - name: username
            in: query
            type: string
            required: true
            description: The username (email address) of the user.

        responses:
          200:
            description: Email validation code resent successfully.
          400:
            description: Email already confirmed. Returns an error message.
          404:
            description: User not found. Returns an error message.

        """
        username = request.args.get('username')
        user = User.query.filter_by(username=username).first()

        if user is None:
            return {'message': 'User not found'}, 404

        if user.isEmailConfirmed:
            return {'message': 'Email already confirmed'}, 400

        user.codeToConfirmEmail = get_random_string(16)
        db.session.commit()

        sendValidationCode(username, user.codeToConfirmEmail)
        return {'message': 'Email validation code resent successfully'}, 200


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

        """
                Get the information of the currently logged-in user.

                ---
                responses:
                  200:
                    description: User information retrieved successfully. Returns user information.
                  400:
                    description: User not logged in. Returns an error message.

                """

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
                "seats": eval(tiket.seats),
                "id": tiket.id,
                "checked": True if tiket.checked else False,
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
        """
                Create a payment for buying tickets.

                ---
                parameters:
                  - name: sessions_id
                    in: query
                    type: integer
                    required: true
                    description: The ID of the session for which tickets are being purchased.
                  - name: body
                    in: body
                    required: true
                    schema:
                      type: object
                      properties:
                        seats:
                            type: array
                            items:
                                type: integer
                            description: The seats to be purchased.
                      example:
                        seats: [1, 2, 3]

                requestBody:
                  required: true
                  content:
                    application/json:
                      schema:
                        type: object
                        properties:
                          seats:
                            type: array
                            items: integer
                            description: The seats to be purchased.

                responses:
                  200:
                    description: Payment created successfully. Returns the payment details.
                  400:
                    description: Invalid data or user not logged in or email not confirmed. Returns an error message.
                  404:
                    description: Session not found. Returns an error message.
                """

        data = request.data.decode('utf-8')
        print(data)
        data = json.loads(data)
        seats = data['seats']
        ses_id = request.args.get('sessions_id')

        if current_user.username is None or seats is None or ses_id is None:
            return {'message': 'Invalid data'}, 400
        if not current_user.is_authenticated:
            return {'message': 'User not logged in'}, 400
        if not current_user.isEmailConfirmed:
            return {'message': 'Email not confirmed'}, 400

        ses = Sessions.query.filter_by(id=ses_id).first()
        if ses is None:
            return {'message': 'Session not found'}, 404
        if len(seats) == 0:
            return {'message': 'No seats selected'}, 400

        available_seats = json.loads(ses.seats)
        if not all(elem in available_seats for elem in seats):
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
            available_seats.remove(seat)

        ses.seats = str(available_seats)
        db.session.add(pay)
        db.session.commit()
        threading.Thread(target=checkPayment, args=(pay.id, pay.expired)).start()

        return {
            'message': 'Payment created',
            'id': pay.id,
            'amount': pay.amount,
            'Pay_created': pay.time,
            'expired': pay.expired,
            'title': ses.title,
            'date': ses.date,
            'time': ses.time,
            'seats': pay.seats
        }, 200


class confirm_Payment(Resource):
    def get(self):
        """
        Confirm a payment and generate tickets.

        ---
        parameters:
          - name: payment_id
            in: query
            type: integer
            required: true
            description: The ID of the payment to confirm.

        responses:
          200:
            description: Payment confirmed and tickets generated successfully.
          400:
            description: Payment already confirmed or an error occurred. Returns an error message.
          404:
            description: Payment not found. Returns an error message.
        """

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
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(f"{base_url}/check_ticket/{tiket.id}")
        qr.make(fit=True)
        mask = Image.open(base_dir + "Posters/Ready_masks/" + str(ses.film.id) + "_mask.png")

        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=ImageColorMask(
                color_mask_image=mask
            )
        )

        if not os.path.exists("tikets"):
            os.makedirs("tikets")
        img.save("tikets/" + tiket.id + '.png')

        db.session.add(tiket)
        db.session.commit()
        sendTiket(username, tiket)

        return {"message": "Tickets bought successfully"}, 200


# @app.route('/buy_ticket_for_all_films', methods=['GET'])
def buy_ticket_for_all_films():
    films = Film.query.all()
    for film in films:
        print(film.title)
        sessions = Sessions.query.filter_by(film_id=film.id).all()
        for ses in sessions:
            seats = json.loads(ses.seats)
            if len(seats) > 0:
                # creating tiket
                tiket = Tiket(username="perepelukdanilo@gmail.com", date=ses.date, title=ses.title, time=ses.time,
                              seats=f"[{str(seats[0])}]", id=get_random_string(16))
                qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
                qr.add_data(f"{base_url}/check_ticket/{tiket.id}")
                qr.make(fit=True)
                mask = Image.open(base_dir + "Posters/Ready_masks/" + str(ses.film.id) + "_mask.png")
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                    color_mask=ImageColorMask(
                        color_mask_image=mask
                    )
                )
                if not os.path.exists("tikets"):
                    os.makedirs("tikets")
                img.save("tikets/" + tiket.id + '.png')
                db.session.add(tiket)
                db.session.commit()
                break
    return {"message": "Tickets bought successfully"}, 200


class GetSessionInfo(Resource):
    def get(self):
        """
        Get information about a session.

        ---
        parameters:
          - name: ses_id
            in: query
            type: integer
            required: true
            description: The ID of the session to retrieve information about.

        responses:
          200:
            description: Session information retrieved successfully.
          404:
            description: Session not found. Returns an error message.

        """
        session_id = request.args.get('ses_id')
        session = Sessions.query.filter_by(id=session_id).first()

        if session is None:
            return {'message': 'Session not found'}, 404

        response = {}
        response['message'] = 'Success'
        response['title'] = session.title

        film = Film.query.filter_by(id=session.film_id).first()
        response['film_title'] = film.title
        response['trailer'] = film.trailer
        response['seats'] = json.loads(session.seats)
        response['description'] = film.description
        response['price'] = film.price
        response['poster'] = base_url + "/posters/" + str(film.id)

        return response, 200


class dbinfo(Resource):
    def get(self):
        metadata = db.MetaData()

        # Reflect the database schema
        metadata.reflect(bind=db.engine)

        # Get all table names
        table_names = metadata.tables.keys()
        return str(table_names), 200


class IsUserAuthenticated(Resource):
    def get(self):
        """
        Check if the user is authenticated.

        ---
        responses:
          200:
            description: User is authenticated.
          400:
            description: User is not authenticated.

        """
        if current_user.is_authenticated:
            return {'message': 'User is authenticated'}, 200
        else:
            return {'message': 'User is not authenticated'}, 400


class GetFilms(Resource):
    def get(self):
        """
        Get information about all films.

        ---
        responses:
          200:
            description: Film information retrieved successfully.
          404:
            description: No films found. Returns an empty list.

        """
        films = Film.query.all()
        response = []

        for film in films:
            film_data = {
                "id": film.id,
                "duration": film.duration,
                "title": film.title,
                "description": film.description,
                "price": film.price,
                "trailer": film.trailer,
                "poster": base_url + "/Posters/" + film.pos
            }
            response.append(film_data)

        if len(response) == 0:
            return [], 404

        return response, 200


class getSessions(Resource):
    def get(self):

        """
                Get sessions for a specific film.

                ---
                parameters:
                  - name: film_id
                    in: query
                    type: integer
                    required: true
                    description: The ID of the film.

                responses:
                  200:
                    description: Sessions retrieved successfully.
                  400:
                    description: Bad request. Invalid film ID.
                  404:
                    description: Film not found.
                """

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

        """
                Get details of a specific session.

                ---
                parameters:
                  - name: ses_id
                    in: query
                    type: integer
                    required: true
                    description: The ID of the session.

                responses:
                  200:
                    description: Session details retrieved successfully.
                  404:
                    description: Session or associated film not found.
                """

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
        ans["poster"] = base_url + "/Posters/" + film.pos
        return ans, 200


from datetime import datetime


@app.route('/check_ticket/<id>', methods=['GET'])
def check_ticket(id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect("https://joly54.github.io/Cinema/")
    tiket = Tiket.query.filter_by(id=id).first()
    if tiket is None:
        return render_template('tiket-checker.html', data={'message': 'Ticket not found'})
    if tiket.checked:
        data = {
            'message': 'Ticket has already been checked',
            'title': tiket.session.title,
            'date': tiket.session.date,
            'time': tiket.session.time,
            'seats': json.loads(tiket.seats)
        }

        return render_template('tiket-checker.html', data=data)
    tiket.checked = datetime.now()
    db.session.commit()

    data = {
        'message': 'Ticket checked',
        'title': tiket.session.title,
        'date': tiket.session.date,
        'time': tiket.session.time,
        'seats': json.loads(tiket.seats)
    }

    return render_template('tiket-checker.html', data=data)


class History(Resource):
    def get(self):

        """
           Get the history of all bookings made by the user.

           ---
           responses:
             200:
               description: History retrieved successfully.
             400:
               description: User is not authenticated.
             404:
               description: User has not made any bookings.
           """

        if current_user.is_authenticated:
            user_id = current_user.id
            payments = Payment.query.filter_by(user_id=user_id).all()
            response = []
            for payment in payments:
                payment_data = {
                    "id": payment.id,
                    "amount": payment.amount,
                    'Pay_created': payment.time,
                    "expired": payment.expired,
                    "title": payment.session.title,
                    "date": payment.session.date,
                    "time": payment.session.time,
                    "confirmed": payment.confirmed,
                    "seats": json.loads(payment.seats),
                }
                response.append(payment_data)
                response.reverse()
            return response, 200
        else:
            return {'message': 'User is not authenticated'}, 400


class logout_us(Resource):
    def get(self):
        # Create a new response object
        response = make_response({'message': 'User logged out'}, 200)

        # Clear cookies by setting them to expire immediately
        for cookie in request.cookies:
            response.set_cookie(cookie, expires=0, samesite='None', secure=True)

        return response


import requests
import time

BANNED_IPS = []
WHITE_LIST = ["127.0.0.1", "91.225.38.80"]
REQUEST_THRESHOLD = 300
TIME_WINDOW = 60

us_req = {}


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

        if ip_address not in us_req:
            us_req[ip_address] = []

        current_time = time.time()

        us_req[ip_address].append(current_time)

        # Remove old requests
        us_req[ip_address] = [t for t in us_req[ip_address] if t > current_time - TIME_WINDOW]
        if len(us_req[ip_address]) > REQUEST_THRESHOLD and ip_address not in WHITE_LIST and not (
                current_user.is_authenticated and current_user.is_admin):
            BANNED_IPS.append(ip_address)
            send_notification(f"IP {ip_address} was banned")
            start_response('403 Forbidden', [('Content-Type', 'text/plain')])
            return [b'Forbidden']

        return self.app(environ, start_response)


app.wsgi_app = BanMiddleware(app.wsgi_app)

# User Authentication and Account Management
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(ForgotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password')
api.add_resource(ConfirmEmail, '/confirmEmail')
api.add_resource(isEmailConfirmed, '/isEmailConfirmed')
api.add_resource(ResendEmailValidationCode, '/resendEmailValidationCode')
api.add_resource(userConfirmEmail, '/userConfirmEmail')
api.add_resource(GetNav, '/getnav')
api.add_resource(IsUserAuthenticated, '/isUserAuthenticated')
api.add_resource(logout_us, '/logout_us')

# Displaying Information
api.add_resource(DisplayTikets, '/displayTikets')
api.add_resource(GetSessionInfo, '/getSessionInfo')
api.add_resource(GetFilms, '/getFilms')
api.add_resource(Schedule, '/schedule')
api.add_resource(getSessions, '/getSessions')
api.add_resource(GetSession, '/getSession')

# Ticket Management
api.add_resource(BuyTikets, '/buyTikets')
api.add_resource(confirm_Payment, '/confirmPayment')

# User Information
api.add_resource(UserInformation, '/userinfo')
api.add_resource(History, '/history')

# image
api.add_resource(ticket_qr, '/tikets/<id>')
api.add_resource(send_poster, '/Posters/<id>')

# Database Information
api.add_resource(dbinfo, '/dbinfo')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
