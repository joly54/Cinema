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
    change *= 0.96
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
        price=random.randint(30, 60) * 10,
        pos=title.replace(' ', '_').replace(':', '').lower() + '.jpg'
    )
    db.session.add(newFilm)
    db.session.commit()
    id_f += 1
    return newFilm


def CreateAllFilms():
    films = [createFilm(
        "Interstellar",
        169,
        "https://www.youtube.com/watch?v=0vxOhd4qlnA",
        "ooper experiences a gravitational anomaly in his daughter Murph's bedroom. He deduces it to be a pattern of "
        "GPS coordinates and arrives at a secret NASA facility headed by Professor Brand. Brand explains to Cooper "
        "that they are trying to find an exoplanet capable of supporting life, and that he is working on solving a "
        "gravity equation to provide a way of transporting large numbers of people off the Earth. He enlists Cooper "
        "to pilot an exploratory spacecraft the Endurance, equipped with 2 Ranger craft and 1 Lander craft, "
        "with a crew of three scientists: Romilly, Doyle, and Brand’s daughter Amelia. This is humanity's last "
        "chance; there are no more resources to mount another expedition. A wormhole has been found near Saturn, "
        "enabling the ship to pass through into another galaxy to search for a new home."
    ), createFilm(
        "Avatar: The way of water",
        192,
        "https://www.youtube.com/watch?v=o5F8MOz_IDw",
        "Sixteen years after the Na'vi repelled the RDA invasion of Pandora,[a] Jake Sully lives as chief of the "
        "Omatikaya clan and raises a family with Neytiri, which includes sons Neteyam and Lo'ak, daughter Tuk, "
        "and adopted children Kiri (born from Grace Augustine's inert avatar) and Spider, the Pandora-born human son "
        "of the late Colonel Miles Quaritch. To the Na'vi's dismay, the RDA, led by their new leader Frances Ardmore, "
        "returns to colonize Pandora, as Earth is dying. Among the new arrivals are Recombinants—Na'vi avatars "
        "implanted with the memories of deceased human soldiers—with Quaritch's recombinant serving as the leader."
    ), createFilm(
        "The Martian",
        144,
        "https://www.youtube.com/watch?v=ej3ioOneTy8",
        "In 2035, the crew of the Ares III mission to Mars is exploring Acidalia Planitia on Martian solar day (sol) "
        "18 of their 31-sol expedition. A severe dust storm threatens to topple their Mars Ascent Vehicle (MAV). The "
        "mission is abandoned, but as the crew evacuates, astronaut Mark Watney is struck by debris. The telemetry "
        "from his suit's bio-monitor is damaged and Watney is erroneously presumed dead. With the MAV (Mars Ascent "
        "Vehicle) on the verge of toppling, the remaining crew takes off for their orbiting vessel, the Hermes."
    ), createFilm(
        "Ford v Ferrari",
        152,
        "https://www.youtube.com/watch?v=I3h9Z89U9ZA",
        "In 1963, Ford Motor Company Vice President Lee Iacocca proposes to Henry Ford II to boost their car sales by "
        "purchasing Italian car manufacturer Ferrari, dominant in the 24 Hours of Le Mans. Owner Enzo Ferrari uses "
        "Ford's offer to secure a deal with Fiat that allows him to retain ownership of the firm's racing team, "
        "Scuderia Ferrari. He insults Ford II and the whole Ford Motor Company. Ford orders his racing division to "
        "build a car to defeat Ferrari at Le Mans. Iacocca hires Shelby American owner Carroll Shelby, "
        "a retired driver who won Le Mans in 1959. Shelby enlists his friend Ken Miles, a hot-tempered British racer "
        "and mechanical engineer."
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
        "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then "
        "embarks on a downward spiral of revolution and bloody crime."
    ), createFilm(
        "Taxi 3",
        84,
        "https://www.youtube.com/watch?v=icdqQylKgRI",
        "A group of thieves calling themselves the Santa Claus gang are wreaking havoc, using Santa Claus costumes to "
        "commit heists, and the Marseille police are, as usual, unable to keep up. Superintendent Gibert (played by "
        "Bernard Farcy) is distracted by a Chinese journalist (Bai Ling) writing a story on his squad, and is unable "
        "to stop the robbers."
    ), createFilm(
        "Baby driver",
        112,
        "https://www.youtube.com/watch?v=z2z857RSfhk",
        "Baby is a getaway driver in Atlanta. As a child, he survived a car crash that killed his parents and left "
        "him with tinnitus. He finds catharsis in music, typically using iPods to soothe his tinnitus. Baby ferries "
        "crews of robbers assembled by criminal mastermind Doc as compensation for stealing a car containing Doc's "
        "stolen goods. Between jobs, he remixes snippets of conversations he records and cares for his deaf foster "
        "father, Joseph. He meets a waitress named Debora, and they start dating."
    ), createFilm(
        "Rush",
        123,
        "https://www.youtube.com/watch?v=4XA73ni9eVs",
        "James Hunt, a brash and self-confident individual, and Niki Lauda, a cool and calculating technical genius "
        "who relies on practice and precision, are exceptional racing car drivers who first develop a fierce rivalry "
        "in 1970 at a Formula Three race in London, when both their cars spin before Hunt wins the race. Lauda takes "
        "a large bank loan from Austria's Raiffeisen Bank to buy his way into the BRM Formula One team, "
        "meeting teammate Clay Regazzoni for the first time."
    ),
        createFilm(
            "Suicide Squad",
            120,
            "https://www.youtube.com/watch?v=eg5ciqQzmK0",
            "A secret government agency recruits some of the most dangerous incarcerated super-villains to form a "
            "defensive task force."
        ), createFilm(
            "Sully",
            96,
            "https://www.youtube.com/watch?v=6Tbkbx4Hz8Q",
            "The film follows Sullenberger's January 2009 emergency landing of US Airways Flight 1549 on the Hudson "
            "River, in which all 155 passengers and crew survived - most suffering only minor injuries - and the "
            "subsequent publicity and investigation."
        ), createFilm(
            "The Matrix",
            136,
            "https://www.youtube.com/watch?v=m8e-FF8MsqU",
            "Computer programmer Thomas Anderson, known by his hacking alias Neo, is puzzled by repeated online "
            "encounters with the phrase the Matrix. Trinity contacts him and tells him a man named Morpheus has the "
            "answers Neo seeks. A team of Agents and police, led by Agent Smith, arrives at Neo's workplace in search "
            "of him. Though Morpheus attempts to guide Neo to safety, Neo surrenders rather than risk a dangerous "
            "escape. The Agents offer to erase Neo's criminal record in exchange for his help with locating Morpheus, "
            "who they claim is a terrorist. When Neo refuses to cooperate, they fuse his mouth shut, pin him down, "
            "and implant a robotic bug in his abdomen. Neo wakes up from what he believes to be a nightmare. Soon "
            "after, Neo is taken by Trinity to meet Morpheus, and she removes the bug from Neo."
        ),
        createFilm(
            "The Fast and the Furious: Tokyo Drift",
            104,
            "https://www.youtube.com/watch?v=p8HQ2JLlc4E",
            "In this third installment of the popular Fast and Furious franchise, Sean Boswell is sent to live with "
            "his father in Tokyo after getting into trouble with the law. There, he discovers the world of drift "
            "racing and soon finds himself in over his head, facing off against the best drivers in the city. With "
            "pulse-pounding racing sequences and a killer soundtrack, this film is a must-see for fans of high-octane "
            "action."
        ),
        createFilm(
            "Avatar 2009",
            162,
            "https://www.youtube.com/watch?v=5PSNL1qE6VY",
            "In 2154, the natural resources of the Earth have been depleted. The Resources Development Administration "
            "(RDA) mines the valuable mineral unobtanium on Pandora, a moon in the Alpha Centauri star system. "
            "Pandora, whose atmosphere is inhospitable to humans, is inhabited by the Na'vi, 10-foot-tall (3.0 m), "
            "blue-skinned, sapient humanoids that live in harmony with nature. To explore Pandora, genetically "
            "matched human scientists use Na'vi-human hybrids called avatars. Paraplegic Marine Jake Sully is sent to "
            "Pandora to replace his deceased identical twin, who had signed up to be an operator. Avatar Program head "
            "Dr. Grace Augustine considers Sully inadequate but accepts him as a bodyguard."
        ), createFilm(
            "Deadpool 2",
            119,
            "https://www.youtube.com/watch?v=D86RtevtfrA",
            "After surviving a near fatal bovine attack, a disfigured cafeteria chef (Wade Wilson) struggles to "
            "fulfill his dream of becoming Mayberry’s hottest bartender while also learning to cope with his lost "
            "sense of taste. Searching to regain his spice for life, as well as a flux capacitor, Wade must battle "
            "ninjas, the yakuza, and a pack of sexually aggressive canines, as he journeys around the world to "
            "discover the importance of family, friendship, and flavor – finding a new taste for adventure and "
            "earning the coveted coffee mug title of World’s Best Lover."

        ), createFilm(
            "Star Wars: The Rise of Skywalker",
            142,
            "https://www.youtube.com/watch?v=8Qn_spdM5Zg",
            "The surviving members of the resistance face the First Order once again, and the legendary conflict "
            "between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end."
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
