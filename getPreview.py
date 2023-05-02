import json
import urllib.request
from urllib.parse import urlparse, parse_qs
import os
import requests


def dowloadImage(url, name):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error downloading image" + str(response.status_code) + " " + url + " " + name)
        with open(name, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print("Error downloading image" + str(e) + " " + url + " " + name)
with open("days.json") as f:
    data = json.load(f)
urls = []
for key in data:
    for film in data[key]["films"]:
        if [film["trailer"], film["title"]] not in urls:
            urls.append([film["trailer"], film["title"]])
for i in range(len(urls)):
    urls[i][0] = parse_qs(urlparse(urls[i][0]).query)['v'][0]
for i in range(len(urls)):
    urls[i][0] = "https://img.youtube.com/vi/" + urls[i][0] + "/maxresdefault.jpg"
# sort by title
urls.sort(key=lambda x: x[1])
for url in urls:
    dowloadImage(url[0], "preview/" + url[1] + ".jpg")
