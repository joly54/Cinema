#read days.json
import json
with open("days.json") as f:
    data = json.load(f)
print(data)