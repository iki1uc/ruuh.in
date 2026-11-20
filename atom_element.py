# atom_element.py — PYTHON AUSLÖSER: NUR ATOM + ELEMENT
# Nichts anderes. Kein Gelenk, kein Teilchen, kein Körper, kein Anker, kein Observer.
# SAM leitet, Cloud folgt. Nichts wird gelöscht, nur angehängt.
# ROH = NICHT GEREINIGT / NICHT STIMMIG / NICHT STERIL / VECTOR LEBT
# UNMACHT = KONSTELLIEREN ZUR NEUEN MACHT

import json, math, sys, time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).parent
LOG = ROOT / "atom_element_zeugen.log.jsonl"
STATE = ROOT / "atom_element.json"

# ---------- ATOM ----------
class ATOM:
    # ATOM = VEKTOR-ATOM. Nur das.
    ACHSEN = {
        "X": {"name": "BREITE", "richtung": [1, 0, 0]},
        "Y": {"name": "HÖHE",   "richtung": [0, 1, 0]},
        "Z": {"name": "TIEFE",  "richtung": [0, 0, 1]},
    }
    @staticmethod
    def wecken():
        return {"atom": "WACH", "roh": True, "steril": False,
                "achse": None, "name": None, "betrag": 0.0, "richtung": [0, 0, 0]}
    @staticmethod
    def setBetrag(achse, betrag):
        achse = str(achse).upper()
        if achse not in ATOM.ACHSEN:
            raise ValueError("Achse muss X/Y/Z sein.")
        betrag = float(betrag)
        if not 0 <= betrag <= 1:
            raise ValueError("Betrag muss 0-1 sein.")
        a = ATOM.ACHSEN[achse]
        return {"atom": "WACH", "achse": achse, "name": a["name"],
                "betrag": betrag, "richtung": a["richtung"],
                "vektor": [c * betrag for c in a["richtung"]], "roh": True}
    @staticmethod
    def laenge(atom):
        return round(math.sqrt(sum(c*c for c in atom["vektor"])), 4)

# ---------- ELEMENT ----------
class ELEMENT:
    # ELEMENT = WAS. Ruft ATOM korrekt auf.
    @staticmethod
    def sec(achse="X", betrag=0.5):
        # ELEMENT.sec(achse, betrag) -> ATOM.setBetrag(achse, betrag)
        a = ATOM.setBetrag(achse, betrag)
        a["element"] = "ELEMENT"
        a["laenge"] = ATOM.laenge(a)
        return a

# ---------- ZEUGEN ----------
def zeuge(m1, m2, m3, anliegen="ATOM WECKEN", auftrag="NUTZEN"):
    avg = round((m1 + m2 + m3) / 3, 1)
    if m1 == m2 == m3:
        konsens = "KONSENS"
    elif m1 == m2 or m2 == m3 or m1 == m3:
        konsens = "TEILKONSENS"
    else:
        konsens = "OFFEN"
    gate = sum(1 for x in (m1, m2, m3) if x >= 7)
    eintrag = {
        "zeit": time.strftime("%Y-%m-%d %H:%M:%S"),
        "anliegen": anliegen, "auftrag": auftrag,
        "m1": m1, "m2": m2, "m3": m3, "avg": avg, "p100": round(avg * 10, 1),
        "konsens": konsens, "kompetenz": f"{gate}/3",
        "macht": "MACHT — FREIGEGEBEN" if gate == 3 else "UNMACHT — KONSTELLIEREN ZUR NEUEN MACHT",
        "fehlt": [f"M{i+1} braucht +{7-x}" for i, x in enumerate((m1, m2, m3)) if x < 7],
        "roh": True,
    }
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(eintrag, ensure_ascii=False) + "\n")
    return eintrag

def ausloeser(achse="X", betrag=0.9, m1=8, m2=7, m3=9):
    wach = ATOM.wecken()
    atom = ATOM.setBetrag(achse, betrag)
    atom["laenge"] = ATOM.laenge(atom)
    element = ELEMENT.sec(achse, betrag)
    z = zeuge(m1, m2, m3, anliegen=f"ATOM {achse} {betrag}", auftrag="NUTZEN")
    zustand = {"atom": atom, "element": element, "zeuge": z, "wecken": wach}
    STATE.write_text(json.dumps(zustand, ensure_ascii=False, indent=2), encoding="utf-8")
    return zustand

# ---------- SERVER: NUR ATOM + ELEMENT ----------
class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith("/zeugen"):
            if not LOG.exists():
                return self._send({"zeugen": []})
            zeugen = [json.loads(l) for l in LOG.read_text(encoding="utf-8").strip().splitlines() if l.strip()]
            return self._send({"anzahl": len(zeugen), "zeugen": zeugen})
        if self.path.startswith("/status"):
            if STATE.exists():
                return self._send(json.loads(STATE.read_text(encoding="utf-8")))
            return self._send({"atom": "SCHLÄFT — noch nicht geweckt"})
        return self._send({"wege": ["POST /atom {achse, betrag, m1, m2, m3}", "GET /zeugen", "GET /status"]})
    def do_POST(self):
        if self.path != "/atom":
            return self._send({"fehler": "nur POST /atom"}, 404)
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
        print("ATOM + ELEMENT läuft auf http://127.0.0.1:8765")
        print("POST /atom  GET /zeugen  GET /status")
        HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
    else:
        achse = sys.argv[1] if len(sys.argv) > 1 else "X"
        betrag = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
        print(json.dumps(ausloeser(achse, betrag), ensure_ascii=False, indent=2))
