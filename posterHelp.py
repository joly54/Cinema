from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pyperclip
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
db = SQLAlchemy(app)
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    trailer = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Film: " + self.title + " " + self.trailer + " " + self.description
if __name__ == "__main__":
    with app.app_context():
        films = Film.query.all()
        for film in films:
            print(f"Id: {film.id} || Title {film.title}")
            pyperclip.copy(film.title + " wallpaper")
            input("Press Enter to continue...")
        #app.run(debug=True)