import datetime
import random

from flask import Flask
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
import config
from app import is_local
import sys
from app import Tiket, Sessions, Film, db, app, User

change = 100


def RandBool(probability):
    new_probability = 100 - probability
    rand_num = random.uniform(0, 1)
    if rand_num < new_probability / 100:
        return 1
    else:
        return 0


def randSeats():
    global change
    seat_list = []
    for i in range(1, 61):
        if RandBool(change):
            seat_list.append(i)
    change *= 0.98
    return seat_list


id_f = 1


def createFilm(
        title,
        duration,
        trailer,
        description,
):
    global id_f
    newFilm = Film(
        id=id_f,
        title=title,
        duration=duration,
        trailer=trailer,
        description=description,
        price=random.randint(30, 600) * 10)
    db.session.add(newFilm)
    db.session.commit()
    id_f += 1
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
        "Ford v Ferrari",
        152,
        "https://www.youtube.com/watch?v=I3h9Z89U9ZA",
        "Ford v Ferrari is a 2019 biographical sports drama film that tells the story of the rivalry between Ford Motor Company and Ferrari during the 1960s, as they both competed to build the fastest race car for the Le Mans race in France. "
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
        "Taxi 3",
        84,
        "https://www.youtube.com/watch?v=icdqQylKgRI",
        "Out to stop a new gang disguised as Santa Claus, Emilien and Daniel must also handle major changes in their personal relationships."
    ), createFilm(
        "Baby driver",
        112,
        "https://www.youtube.com/watch?v=z2z857RSfhk",
        "After being coerced into working for a crime boss, a young getaway driver finds himself taking part in a heist doomed to fail."
    ), createFilm(
        "Rush",
        123,
        "https://www.youtube.com/watch?v=4XA73ni9eVs",
        "The merciless 1970s rivalry between Formula One rivals James Hunt and Niki Lauda."
    ),
        createFilm(
            "Suicide Squad",
            120,
            "https://www.youtube.com/watch?v=eg5ciqQzmK0",
            "A secret government agency recruits some of the most dangerous incarcerated super-villains to form a defensive task force. "
        ), createFilm(
            "Sully",
            96,
            "https://www.youtube.com/watch?v=6Tbkbx4Hz8Q",
            "The film follows Sullenberger's January 2009 emergency landing of US Airways Flight 1549 on the Hudson River, in which all 155 passengers and crew survived - most suffering only minor injuries - and the subsequent publicity and investigation."
        ), createFilm(
            "The Matrix",
            136,
            "https://www.youtube.com/watch?v=m8e-FF8MsqU",
            "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
        ),
        createFilm(
            "The Fast and the Furious: Tokyo Drift",
            104,
            "https://www.youtube.com/watch?v=p8HQ2JLlc4E",
            "In this third installment of the popular Fast and Furious franchise, Sean Boswell is sent to live with his father in Tokyo after getting into trouble with the law. There, he discovers the world of drift racing and soon finds himself in over his head, facing off against the best drivers in the city. With pulse-pounding racing sequences and a killer soundtrack, this film is a must-see for fans of high-octane action."
        ),
        createFilm(
            "Avatar 2009",
            162,
            "https://www.youtube.com/watch?v=5PSNL1qE6VY",
            "Avatar is a 2009 American epic science fiction film directed, written, produced, and co-edited by James Cameron and starring Sam Worthington, Zoe Saldana, Stephen Lang, Michelle Rodriguez, and Sigourney Weaver."
        ), createFilm(
            "Deadpool 2",
            119,
            "https://www.youtube.com/watch?v=D86RtevtfrA",
            "After surviving a near fatal bovine attack, a disfigured cafeteria chef (Wade Wilson) struggles to fulfill his dream of becoming Mayberry’s hottest bartender while also learning to cope with his lost sense of taste. Searching to regain his spice for life, as well as a flux capacitor, Wade must battle ninjas, the yakuza, and a pack of sexually aggressive canines, as he journeys around the world to discover the importance of family, friendship, and flavor – finding a new taste for adventure and earning the coveted coffee mug title of World’s Best Lover. "

        ), createFilm(
            "Star Wars: The Rise of Skywalker",
            142,
            "https://www.youtube.com/watch?v=8Qn_spdM5Zg",
            "The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end."
        )]
    return films


def createSession(
        film,
        seats,
        date,
        time,
):
    newSession = Sessions(
        film=film,
        seats=seats,
        date=date,
        time=time)
    db.session.add(newSession)
    db.session.commit()
    return newSession


def CreateAllSessions(films):
    date = 0
    for i in range(31):
        time = 8
        for g in range(8):
            days_films = []
            if random.randint(1, 4) == 1:
                time += 2
                continue
            while True:
                index = random.randint(0, len(films) - 1)
                if days_films.count(index) == 0:
                    break
            days_films.append(index)
            film = films[index]
            createSession(
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


def clearTicket():
    tickets = Tiket.query.all()
    import os
    ticket_list = os.listdir("/home/vincinemaApi/tikets")
    for tiket in ticket_list:
        if tiket.split(".")[0] not in [ticket.id for ticket in tickets]:
            os.remove(f"/home/vincinemaApi/tikets/{tiket}")
            ticket_list.remove(tiket)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if len(sys.argv) == 1:
            # check if admin exist
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                admin = User(
                    username="perepelukdanilo@gmail.com",
                    # hash
                    password="b0e52a1510c9012ebae9e9dc1ae0c46e",
                    secret_code="sgdf",
                    codeToConfirmEmail="",
                    isEmailConfirmed=True,
                    is_admin=True,
                )
                db.session.add(admin)
                db.session.commit()
            CreateAllFilms()
            CreateAllSessions(Film.query.all())
        elif sys.argv[1] == "clear":
            clearTicket()
        else:
            print("Wrong argument")
        # app.run(debug=True)
