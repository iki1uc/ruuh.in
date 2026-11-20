import json
from urllib.request import Request, urlopen

daten = json.dumps({"achse": "X", "betrag": 0.9}).encode()
req = Request("http://127.0.0.1:8765/vektor", data=daten,
              headers={"Content-Type": "application/json"})

with urlopen(req) as antwort:
    print(json.load(antwort))
