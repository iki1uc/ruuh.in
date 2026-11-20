# client_atom.py — NUR ATOM + ELEMENT, korrigiert
# Dein Paste nutzte noch /vektor — das ist alt. Server ist /atom.
import json
from urllib.request import Request, urlopen

daten = json.dumps({"achse": "X", "betrag": 0.9, "m1": 8, "m2": 7, "m3": 9}).encode()
req = Request("http://127.0.0.1:8765/atom", data=daten,
              headers={"Content-Type": "application/json"})

with urlopen(req) as antwort:
    print(json.load(antwort))
# Start: python atom_element.py server
# Dann: python client_atom.py
