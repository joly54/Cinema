from typing import TypedDict


class Film(TypedDict):
    title: str
    duration: int
    trailer: str
    aviableTikets: list[int]


class Day(TypedDict):
    date: str
    films: list[Film]

film1 = Film(title="Avengers: Endgame", duration=181, trailer="https://www.youtube.com/watch?v=TcMBFSGVi1c",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film2 = Film(title="Jurassic World: Fallen Kingdom", duration=128,
             trailer="https://www.youtube.com/watch?v=1FJD7jZqZEk",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film3 = Film(title="The Dark Knight", duration=152, trailer="https://www.youtube.com/watch?v=EXeTwQWrcwY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film4 = Film(title="Interstellar", duration=169, trailer="https://www.youtube.com/watch?v=zSWdZVtXT7E",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film5 = Film(title="The Godfather", duration=175, trailer="https://www.youtube.com/watch?v=sY1S34973zA",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
day1 = Day(date="2020-12-12", films=[film1, film2, film3, film4, film5])
film1 = Film(title="Inception", duration=148, trailer="https://www.youtube.com/watch?v=YoHD9XEInc0",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film2 = Film(title="The Shawshank Redemption", duration=142,
             trailer="https://www.youtube.com/watch?v=6hB3S9bIaco",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film3 = Film(title="Pulp Fiction", duration=154, trailer="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film4 = Film(title="The Matrix", duration=136, trailer="https://www.youtube.com/watch?v=m8e-FF8MsqU",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film5 = Film(title="Forrest Gump", duration=142, trailer="https://www.youtube.com/watch?v=bLvqoHBptjg",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
day2 = Day(date="2023-05-17", films=[film1, film2, film3, film4, film5])
film1 = Film(title="The Lion King", duration=118, trailer="https://www.youtube.com/watch?v=7TavVZMewpY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film2 = Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178,
             trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film3 = Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film4 = Film(title="Joker", duration=122, trailer="https://www.youtube.com/watch?v=zAGVQLHvwOY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film5 = Film(title="Fight Club", duration=139, trailer="https://www.youtube.com/watch?v=SUXWAEX2jlg",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
day3 = Day(date="2023-06-20", films=[film1, film2, film3, film4, film5])
film1 = Film(title="Pulp Fiction", duration=154, trailer="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film2 = Film(title="The Silence of the Lambs", duration=118,
             trailer="https://www.youtube.com/watch?v=W6Mm8Sbe__o",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film3 = Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film4 = Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])
film5 = Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4",
             aviableTikets=[1, 2, 3, 5, 8, 11, 12, 15, 19, 20])

day4 = Day(date="2023-04-08", films=[film1, film2, film3, film4, film5])
days = [day1, day2, day3, day4]
#
import json
with open('days.json', 'w') as f:
    json.dump(days, f)