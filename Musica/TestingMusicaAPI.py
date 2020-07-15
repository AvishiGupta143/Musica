import requests
import json

URL = 'http://127.0.0.1:8000/MusicaAPI/Song/5'
s = requests.get(URL)
print(s.json())
