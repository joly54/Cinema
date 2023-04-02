import string
import random
from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@app.after_request
def set_default_content_type(response):
    response.headers['Content-Type'] = 'application/json'
    return response

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    message = 'Internal server error'

    # Check if the error has a status code
    if hasattr(e, 'code'):
        code = e.code
        message = e.description

    # Return JSON response
    return make_response(jsonify({'error': message}), code)

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            return {'error': 'Invalid username or password'}, 401

        if user.password != password:
            return {'error': 'Invalid username or password'}, 401

        return {'message': 'Logged in successfully', 'token': user.token}, 200

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user is not None:
            return {'error': 'Username already exists'}, 409

        token = get_random_string(32)
        new_user = User(username=username, password=password, token=token)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully', 'token': token}, 201

api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
