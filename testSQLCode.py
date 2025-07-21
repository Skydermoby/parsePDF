import requests
import json

#Upload example hero
files = {"id": 999, "name": "Fortnite", "age": 21, "secret_name": "Battlepass"}
print(files)
res = requests.post(url= "http://127.0.0.1:8000/heroes/", json=files)

res = requests.get(url= "http://127.0.0.1:8000/heroes/")
print(res.text)