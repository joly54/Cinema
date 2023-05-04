import datetime
import random

from flask import Flask
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="vincinemaApi",
    password=config.dbpass,
    hostname="vincinemaApi.mysql.pythonanywhere-services.com",
    #databasename="vincinemaApi$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    trailer = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return "Film: " + self.title + " " + self.trailer + " " + self.description


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    film = db.relationship('Film', backref='sessions')
    seats = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "Sessions: " + self.title + " " + str(self.film) + " " + self.seats



class Days(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), unique=True, nullable=False, index=True)
    t_9 = db.Column(db.Integer, nullable=True)
    t_12 = db.Column(db.Integer, nullable=True)
    t_15 = db.Column(db.Integer, nullable=True)
    t_18 = db.Column(db.Integer, nullable=True)
    t_21 = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "Day: " + self.date + " " + str(self.t_9) + " " + str(self.t_12) + " " + str(self.t_15) + " " + str(
            self.t_18) + " " + str(self.t_21)
def randSeats():
    list = []
    for i in range(1, 49):
        if (random.randint(0, random.randint(0, 4)) == 1):
            list.append(i)
    return list


class Schedule(Resource):
    def get(self):
        # get all days
        days = Days.query.all()
        # get all sessions
        sessions = Sessions.query.all()
        # get all films
        films = Film.query.all()
        answer = []
        for day in days:
            answer.append({"date": day.date, "sessions": {}})
            if day.t_9 is not None:
                answer[-1]["sessions"]["09:00"] = {"title": sessions[day.t_9 - 1].title,
                                                  "trailer": sessions[day.t_9 - 1].film.trailer,
                                                  "seats": sessions[day.t_9 - 1].seats}
            if day.t_12 is not None:
                answer[-1]["sessions"]["12:00"] = {"title": sessions[day.t_12 - 1].title,
                                                   "trailer": sessions[day.t_12 - 1].film.trailer,
                                                   "seats": sessions[day.t_12 - 1].seats}
            if day.t_15 is not None:
                answer[-1]["sessions"]["15:00"] = {"title": sessions[day.t_15 - 1].title,
                                                   "trailer": sessions[day.t_15 - 1].film.trailer,
                                                   "seats": sessions[day.t_15 - 1].seats}
            if day.t_18 is not None:
                answer[-1]["sessions"]["18:00"] = {"title": sessions[day.t_18 - 1].title,
                                                   "trailer": sessions[day.t_18 - 1].film.trailer,
                                                   "seats": sessions[day.t_18 - 1].seats}
            if day.t_21 is not None:
                answer[-1]["sessions"]["21:00"] = {"title": sessions[day.t_21 - 1].title,
                                                   "trailer": sessions[day.t_21 - 1].film.trailer,
                                                   "seats": sessions[day.t_21 - 1].seats}

        return answer



app.add_url_rule('/', view_func=Schedule.as_view('schedule'))


def createFilm(
        title,
        duration,
        trailer,
        description
):
    newFilm = Film(title=title,
                   duration=duration,
                   trailer=trailer,
                   description=description)
    db.session.add(newFilm)
    db.session.commit()
    return newFilm


def CreateAllFilms():
    films = []
    films.append(
        createFilm(
            "Interstellar",
            169,
            "https://www.youtube.com/watch?v=0vxOhd4qlnA",
            "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
        )
    )
    films.append(
        createFilm(
            "Avatar: The way of water",
            192,
            "https://www.youtube.com/watch?v=o5F8MOz_IDw",
            "Avatar: The Way of Water reaches new heights and explores undiscovered depths as James Cameron returns to the world of Pandora in this emotionally packed action adventure."
        )
    )
    films.append(
        createFilm(
            "The Martian",
            144,
            "https://www.youtube.com/watch?v=ej3ioOneTy8",
            "An astronaut becomes stranded on Mars after his team assume him dead, and must rely on his ingenuity to find a way to signal to Earth that he is alive."
        )
    )
    films.append(
        createFilm(
            "Titanic",
            194,
            "https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
            "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."
        )
    )
    films.append(
        createFilm(
            "Top Gun: Maverick",
            144,
            "https://www.youtube.com/watch?v=qSqVVswa420",
            "After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs, pushing the envelope as a courageous test pilot and dodging the advancement in rank that would ground him."
        )
    )
    films.append(
        createFilm(
            "Top Gun 1984",
            110,
            "https://www.youtube.com/watch?v=xa_z57UatDY",
            "As students at the United States Navy's elite fighter weapons school compete to be best in the class, one daring young pilot learns a few things from a civilian instructor that are not taught in the classroom."
        )
    )
    films.append(
        createFilm(
            "Joker",
            122,
            "https://www.youtube.com/watch?v=zAGVQLHvwOY",
            "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime."
        )
    )
    films.append(
        createFilm(
            "The Shawshank Redemption",
            142,
            "https://www.youtube.com/watch?v=6hB3S9bIaco",
            "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
        )
    )
    films.append(
        createFilm(
            "The Godfather",
            175,
            "https://www.youtube.com/watch?v=sY1S34973zA",
            "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
        )
    )
    films.append(
        createFilm(
            "The Godfather: Part II",
            202,
            "https://www.youtube.com/watch?v=8PyZCUhCwJ0",
            "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate."
        )
    )
    films.append(
        createFilm(
            "The Dark Knight",
            152,
            "https://www.youtube.com/watch?v=EXeTwQWrcwY",
            "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
        )
    )
    films.append(
        createFilm(
            "Inception",
            148,
            "https://www.youtube.com/watch?v=8hP9D6kZseM",
            "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO."
        )
    )
    films.append(
        createFilm(
            "The Matrix",
            136,
            "https://www.youtube.com/watch?v=m8e-FF8MsqU",
            "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
        )
    )
    films.append(
        createFilm(
            "Forrest Gump",
            142,
            "https://www.youtube.com/watch?v=bLvqoHBptjg",
            "The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate and other historical events unfold through the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart."
        )
    )
    films.append(
        createFilm(
            "The Silence of the Lambs",
            118,
            "https://www.youtube.com/watch?v=W6Mm8Sbe__o",
            "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."
        )
    )
    films.append(
        createFilm(
            "The Lord of the Rings: The Fellowship of the Ring",
            178,
            "https://www.youtube.com/watch?v=Pki6jbSbXIY",
            "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron."
        )
    )
    return films


def createSession(
        title,
        film_id,
        film,
        seats
):
    newSession = Sessions(title=title,
                          film_id=film_id,
                          film=film,
                          seats=seats)
    db.session.add(newSession)
    db.session.commit()
    return newSession


def CreateAllSessions(films):
    sessions = []
    for i in range(100):
        index = random.randint(0, len(films) - 1)
        createSession(
            title=films[index].title,
            film_id=films[index].id,
            film=films[index],
            seats=str(randSeats())
        )
    return sessions


def getPlusedDay(numDays):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=numDays)
    newDate = now + delta
    return newDate.strftime("%Y.%m.%d")


def createDay(
        date,
        t_9,
        t_12,
        t_15,
        t_18,
        t_21
):
    newDay = Days(date=date,
                  t_9=t_9,
                  t_12=t_12,
                  t_15=t_15,
                  t_18=t_18,
                  t_21=t_21)
    db.session.add(newDay)
    db.session.commit()
    return newDay


def CreateAllDays():
    ses = Sessions.query.all()
    pulsDay = 0
    while len(ses) > 0:
        createDay(
            date=getPlusedDay(pulsDay),
            t_9=(ses.pop().id if random.randint(0, 3) / 3.0 < 1 and len(ses) else None),
            t_12=(ses.pop().id if random.randint(0, 1) / 3.0 < 1 and len(ses) else None),
            t_15=(ses.pop().id if random.randint(0, 1) / 3.0 < 1 and len(ses) else None),
            t_18=(ses.pop().id if random.randint(0, 1) / 3.0 < 1 and len(ses) else None),
            t_21=(ses.pop().id if random.randint(0, 1) / 3.0 < 1 and len(ses) else None)
        )
        pulsDay += 1


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        CreateAllFilms()
        CreateAllSessions(Film.query.all())
        CreateAllDays()

        app.run(debug=True)
