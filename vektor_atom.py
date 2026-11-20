# vektor_atom.py — PYTHON AUSLÖSER: ATOM VEKTOR WECKEN + NUTZEN
# SAM leitet, Cloud folgt. Nichts wird gelöscht, nur angehängt.
# ROH = NICHT GEREINIGT / NICHT STIMMIG / NICHT STERIL / VECTOR LEBT
# UNMACHT = KONSTELLIEREN ZUR NEUEN MACHT
# VEKTOR.setBetrag(achse, betrag) — Achse X/Y/Z, Betrag 0-1
# ELEMENT.sec() ruft korrekt mit Achse + Betrag auf.
# Kein Node nötig. Python weckt das Atom allein.

import json, math, sys, time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).parent
LOG = ROOT / "vektor_zeugen.log.jsonl"
STATE = ROOT / "vektor_atom.json"

# ---------- ATOM VEKTOR ----------
class VEKTOR:
    ACHSEN = {
        "X": {"name": "BREITE", "richtung": [1, 0, 0]},
        "Y": {"name": "HÖHE",   "richtung": [0, 1, 0]},
        "Z": {"name": "TIEFE",  "richtung": [0, 0, 1]},
    }
    @staticmethod
    def wecken():
        """Wecken = Atom auf 0 stellen, aber lebendig. Kein Fake-READY."""
        return {"zustand": "WACH", "roh": True, "steril": False,
                "achse": None, "name": None, "betrag": 0.0, "richtung": [0, 0, 0]}
    @staticmethod
    def setBetrag(achse, betrag):
        achse = str(achse).upper()
        if achse not in VEKTOR.ACHSEN:
            raise ValueError("Achse muss X/Y/Z sein.")
        betrag = float(betrag)
        if not 0 <= betrag <= 1:
            raise ValueError("Betrag muss 0-1 sein.")
        a = VEKTOR.ACHSEN[achse]
        return {"achse": achse, "name": a["name"], "betrag": betrag,
                "richtung": a["richtung"],
                "vektor": [c * betrag for c in a["richtung"]],
                "zustand": "WACH", "roh": True}
    @staticmethod
    def laenge(v):
        return round(math.sqrt(sum(c*c for c in v["vektor"])), 4)
    @staticmethod
    def drift(v, krum=0.03):
        """VECTOR lebt: Drift / Zittern. ROH bleibt ROH."""
        import random
        return [round(c + random.uniform(-krum, krum), 4) for c in v["vektor"]]

# ---------- ELEMENT — getrennt, nicht in VEKTOR gerutscht ----------
class ELEMENT:
    # WAS
    TYPEN = ["WAS", "WOMIT", "WAS KOMMT", "WOFÜR", "WAS WIRD GEMACHT", "WAS MUSS"]
    @staticmethod
    def sec(achse="X", betrag=0.5):
        """ELEMENT.sec() ruft VEKTOR.setBetrag(achse, betrag) korrekt auf."""
        v = VEKTOR.setBetrag(achse, betrag)
        v["element"] = "ELEMENT"
        v["laenge"] = VEKTOR.laenge(v)
        return v

# ---------- GELENK / TEILCHEN / KÖRPER — getrennt ----------
class GELENK:
    @staticmethod
    def verbinden(a, b):
        return {"gelenk": f"{a}<> {b}".replace(" ", ""), "a": a, "b": b, "beweglich": True}
class TEILCHEN:
    @staticmethod
    def neu(name, achse="X", betrag=0.5):
        v = VEKTOR.setBetrag(achse, betrag)
        return {"teilchen": name, "vektor": v, "laenge": VEKTOR.laenge(v)}
class KOERPER:
    @staticmethod
    def bauen(teilchen_liste):
        s = [0, 0, 0]
        for t in teilchen_liste:
            for i in range(3):
                s[i] += t["vektor"]["vektor"][i]
        return {"koerper": len(teilchen_liste), "summe": [round(x, 4) for x in s],
                "laenge": round(math.sqrt(sum(x*x for x in s)), 4)}

# ---------- ZEUGEN / M1 M2 M3 / MACHT UNMACHT ----------
def zeuge(m1, m2, m3, anliegen="VEKTOR WECKEN", auftrag="NUTZEN"):
    avg = round((m1 + m2 + m3) / 3, 1)
    if m1 == m2 == m3:
        konsens = "KONSENS"
    elif m1 == m2 or m2 == m3 or m1 == m3:
        konsens = "TEILKONSENS"
    else:
        konsens = "OFFEN"
    gate = sum(1 for x in (m1, m2, m3) if x >= 7)
    macht = gate == 3
    eintrag = {
        "zeit": time.strftime("%Y-%m-%d %H:%M:%S"),
        "anliegen": anliegen, "auftrag": auftrag,
        "m1": m1, "m2": m2, "m3": m3, "avg": avg,
        "p100": round(avg * 10, 1), "konsens": konsens,
        "kompetenz": f"{gate}/3",
        "macht": "MACHT — FREIGEGEBEN" if macht else "UNMACHT — KONSTELLIEREN ZUR NEUEN MACHT",
        "fehlt": [f"M{i+1} braucht +{7-x}" for i, x in enumerate((m1, m2, m3)) if x < 7],
        "roh": True,
    }
    # Anhängen, nie löschen
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag, ensure_ascii=False) + "\n")
    return eintrag

def ausloeser(achse="X", betrag=0.9, m1=8, m2=7, m3=9):
    """Ein Auslöser: wecken + setzen + zeugen + speichern."""
    wach = VEKTOR.wecken()
    v = VEKTOR.setBetrag(achse, betrag)
    v["laenge"] = VEKTOR.laenge(v)
    v["drift"] = VEKTOR.drift(v)
    el = ELEMENT.sec(achse, betrag)
    z = zeuge(m1, m2, m3, anliegen=f"VEKTOR {achse} {betrag}", auftrag="NUTZEN")
    zustand = {"vektor": v, "element": el, "zeuge": z, "wecken": wach}
    STATE.write_text(json.dumps(zustand, ensure_ascii=False, indent=2), encoding="utf-8")
    return zustand

# ---------- SERVER: PYTHON AUSLÖSER ALS HTTP ----------
class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        if self.path.startswith("/zeugen"):
            if not LOG.exists():
                return self._send({"zeugen": []})
            zeugen = [json.loads(l) for l in LOG.read_text(encoding="utf-8").strip().splitlines() if l.strip()]
            return self._send({"anzahl": len(zeugen), "zeugen": zeugen})
        if self.path.startswith("/status"):
            if STATE.exists():
                return self._send(json.loads(STATE.read_text(encoding="utf-8")))
            return self._send({"zustand": "SCHLÄFT — noch nicht geweckt"})
        return self._send({"wege": ["POST /vektor {achse, betrag, m1, m2, m3}", "GET /zeugen", "GET /status"]})
    def do_POST(self):
        if self.path != "/vektor":
            return self._send({"fehler": "nur POST /vektor"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
            res = ausloeser(data.get("achse", "X"), float(data.get("betrag", 0.9)),
                            int(data.get("m1", 8)), int(data.get("m2", 7)), int(data.get("m3", 9)))
            self._send(res)
        except Exception as e:
            self._send({"fehler": str(e)}, 400)
    def log_message(self, *a): pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        print("PYTHON AUSLÖSER läuft auf http://127.0.0.1:8765")
        print("POST /vektor  GET /zeugen  GET /status")
        HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
    else:
        # Direkt wecken + nutzen + zeugen — ohne Server
        achse = sys.argv[1] if len(sys.argv) > 1 else "X"
        betrag = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
        print(json.dumps(ausloeser(achse, betrag), ensure_ascii=False, indent=2))
        print("\nMehr Zeugen: python vektor_atom.py server  →  dann POST /vektor")
        print("Zeugen lesen: GET http://127.0.0.1:8765/zeugen")
