import datetime
import random

from flask import Flask
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
import config
from app import is_local

app = Flask(__name__)
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


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship('Film', backref='sessions')
    seats = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "Sessions: " + self.title + " " + str(self.film) + " " + self.seats


change = 100

def RandBool(probability):
    new_probability = 100-probability
    rand_num = random.uniform(0, 1)
    if rand_num < new_probability/100:
        return 1
    else:
        return 0
def randSeats():
    global change
    seat_list = []
    for i in range(1, 49):
        if RandBool(change):
            seat_list.append(i)
    change *= 0.98
    print(change)
    return seat_list


def createFilm(
        title,
        duration,
        trailer,
        description,
):
    newFilm = Film(title=title,
                   duration=duration,
                   trailer=trailer,
                   description=description,
                   price=random.randint(20, 30) * 10 - 1)
    db.session.add(newFilm)
    db.session.commit()
    return newFilm


def CreateAllFilms():
    films = [createFilm(
        "Interstellar",
        169,
        "https://www.youtube.com/watch?v=0vxOhd4qlnA",
        "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    ), createFilm(
        "Avatar: The way of water",
        192,
        "https://www.youtube.com/watch?v=o5F8MOz_IDw",
        "Avatar: The Way of Water reaches new heights and explores undiscovered depths as James Cameron returns to the world of Pandora in this emotionally packed action adventure."
    ), createFilm(
        "The Martian",
        144,
        "https://www.youtube.com/watch?v=ej3ioOneTy8",
        "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive."
    ), createFilm(
        "Titanic",
        194,
        "https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
        "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
    ), createFilm(
        "Top Gun: Maverick",
        144,
        "https://www.youtube.com/watch?v=qSqVVswa420",
        "After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him."
    ), createFilm(
        "Top Gun 1984",
        110,
        "https://www.youtube.com/watch?v=xa_z57UatDY",
        "As students at the United States Navy's elite fighter weapons school compete to be best in the class, one daring young pilot learns a few things from a civilian instructor that are not taught in the classroom."
    ), createFilm(
        "Joker",
        122,
        "https://www.youtube.com/watch?v=zAGVQLHvwOY",
        "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime."
    ), createFilm(
        "The Shawshank Redemption",
        142,
        "https://www.youtube.com/watch?v=6hB3S9bIaco",
        "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    ), createFilm(
        "The Godfather",
        175,
        "https://www.youtube.com/watch?v=P9mwtI82k6E",
        "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    ), createFilm(
        "The Godfather: Part II",
        202,
        "https://www.youtube.com/watch?v=8PyZCU2vpi8",
        "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate."
    ), createFilm(
        "The Dark Knight",
        152,
        "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    ), createFilm(
        "Inception",
        148,
        "https://www.youtube.com/watch?v=8hP9D6kZseM",
        "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."
    ), createFilm(
        "The Matrix",
        136,
        "https://www.youtube.com/watch?v=m8e-FF8MsqU",
        "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    ), createFilm(
        "Forrest Gump",
        142,
        "https://www.youtube.com/watch?v=bLvqoHBptjg",
        "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart."
    ), createFilm(
        "The Silence of the Lambs",
        118,
        "https://www.youtube.com/watch?v=W6Mm8Sbe__o",
        "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."
    ), createFilm(
        "The Lord of the Rings: The Fellowship of the Ring",
        178,
        "https://www.youtube.com/watch?v=V75dMMIW2B4",
        "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."
    )]
    return films


def createSession(
        title,
        film_id,
        film,
        seats,
        date,
        time,
):
    newSession = Sessions(title=title,
                          film_id=film_id,
                          film=film,
                          seats=seats,
                          date=date,
                          time=time)
    db.session.add(newSession)
    db.session.commit()
    return newSession


def CreateAllSessions(films):
    sessions = []
    date = 0
    for i in range(31):
        time = 8
        for g in range(6):
            if random.randint(1, 3)/3.0 < 0.5:
                time += 2
                continue
            index = random.randint(0, len(films) - 1)
            film = films[index]
            createSession(
                title=film.title,
                film_id=film.id,
                film=film,
                seats=str(randSeats()),
                date=getPlusedDay(date),
                time=time < 10 and f"0{time}:00" or f"{time}:00",
            )
            time += 2
        date += 1


def getPlusedDay(numDays):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numDays)
    newDate = now + delta
    return newDate.strftime("%Y.%m.%d")


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        CreateAllFilms()
        CreateAllSessions(Film.query.all())
        # app.run(debug=True)
