from typing import TypedDict


class Film(TypedDict):
    title: str
    duration: int
    trailer: str
    aviableTikets: list[int]
    beginTime: str


class Day(TypedDict):
    films: list[Film]
import random
def rand():
    list = []
    for i in range(1, 49):
        if(random.randint(0, random.randint(0,4)) == 1):
            list.append(i)
    return list


film1 = Film(title="Avengers: Endgame", duration=181, trailer="https://www.youtube.com/watch?v=TcMBFSGVi1c",
             aviableTikets=rand(), beginTime="10:00")
film2 = Film(title="Jurassic World: Fallen Kingdom", duration=128,
             trailer="https://www.youtube.com/watch?v=1FJD7jZqZEk",
             aviableTikets=rand(), beginTime="12:00")
film3 = Film(title="The Dark Knight", duration=152, trailer="https://www.youtube.com/watch?v=EXeTwQWrcwY",
             aviableTikets=rand(), beginTime="14:00")
film4 = Film(title="Interstellar", duration=169, trailer="https://www.youtube.com/watch?v=zSWdZVtXT7E",
             aviableTikets=rand(), beginTime="16:00")
film5 = Film(title="The Godfather", duration=175, trailer="https://www.youtube.com/watch?v=sY1S34973zA",
             aviableTikets=rand(), beginTime="18:00")
day1 = Day(films=[film1, film2, film3, film4, film5])
film1 = Film(title="Inception", duration=148, trailer="https://www.youtube.com/watch?v=YoHD9XEInc0",
             aviableTikets=rand(), beginTime="10:00")
film2 = Film(title="The Shawshank Redemption", duration=142,
             trailer="https://www.youtube.com/watch?v=6hB3S9bIaco",
             aviableTikets=rand(), beginTime="12:00")
film3 = Film(title="Pulp Fiction", duration=154, trailer="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
             aviableTikets=rand(), beginTime="14:00")
film4 = Film(title="The Matrix", duration=136, trailer="https://www.youtube.com/watch?v=m8e-FF8MsqU",
             aviableTikets=rand(), beginTime="16:00")
film5 = Film(title="Forrest Gump", duration=142, trailer="https://www.youtube.com/watch?v=bLvqoHBptjg",
             aviableTikets=rand(), beginTime="18:00")
day2 = Day( films=[film1, film2, film3, film4, film5])
film1 = Film(title="The Lion King", duration=118, trailer="https://www.youtube.com/watch?v=7TavVZMewpY",
             aviableTikets=rand(), beginTime="10:00")
film2 = Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178,
             trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY",
             aviableTikets=rand(), beginTime="12:00")
film3 = Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM",
             aviableTikets=rand(), beginTime="14:00")
film4 = Film(title="Joker", duration=122, trailer="https://www.youtube.com/watch?v=zAGVQLHvwOY",
             aviableTikets=rand(), beginTime="16:00")
film5 = Film(title="Fight Club", duration=139, trailer="https://www.youtube.com/watch?v=SUXWAEX2jlg",
             aviableTikets=rand(), beginTime="18:00")
day3 = Day( films=[film1, film2, film3, film4, film5])
film1 = Film(title="Pulp Fiction", duration=154, trailer="https://www.youtube.com/watch?v=s7EdQ4FqbhY",
             aviableTikets=rand(), beginTime="10:00")
film2 = Film(title="The Silence of the Lambs", duration=118,
             trailer="https://www.youtube.com/watch?v=W6Mm8Sbe__o",
             aviableTikets=rand(), beginTime="12:00")
film3 = Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w",
             aviableTikets=rand(), beginTime="14:00")
film4 = Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg",
             aviableTikets=rand(), beginTime="16:00")
film5 = Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4",
             aviableTikets=rand(), beginTime="18:00")

day4 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day5 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day6 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day7 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day8 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day9 = Day(films=[film1, film2, film3, film4, film5])
film1=Film(title="The Lord of the Rings: The Fellowship of the Ring", duration=178, trailer="https://www.youtube.com/watch?v=Pki6jbSbXIY", aviableTikets=rand(), beginTime="10:00")
film2=Film(title="The Silence of the Lambs", duration=118, trailer="https://www.youtube.com/watch?v=RuX2MQeb8UM", aviableTikets=rand(), beginTime="12:00")
film3=Film(title="The Usual Suspects", duration=106, trailer="https://www.youtube.com/watch?v=oiXdPolca5w", aviableTikets=rand(), beginTime="14:00")
film4=Film(title="Avatar: The Way of Water", duration=150, trailer="https://www.youtube.com/watch?v=_rJYzq_1VYg", aviableTikets=rand(), beginTime="16:00")
film5=Film(title="The Social Network", duration=120, trailer="https://www.youtube.com/watch?v=lB95KLmpLR4", aviableTikets=rand(), beginTime="18:00")
day10 = Day(films=[film1, film2, film3, film4, film5])
days = {
        "2023.04.11": day1,
        "2023.04.12": day2,
        "2023.04.13": day3,
        "2023.04.14": day4,
        "2023.04.15": day5,
        "2023.04.16": day6,
        "2023.04.17": day7,
        "2023.04.18": day8,
        "2023.04.19": day9,
        "2023.04.20": day10,
    }
#
import json
with open('days.json', 'w') as f:
    json.dump(days, f)