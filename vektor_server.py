from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/vektor":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length))

            achse = data.get("achse", "X")
            betrag = float(data.get("betrag", 0.5))

            if achse not in {"X", "Y", "Z"} or not 0 <= betrag <= 1:
                raise ValueError("Achse muss X/Y/Z und Betrag 0–1 sein.")

            # Lädt das echte vektor.js-Modul und ruft setBetrag auf.
            script = """
            const { VEKTOR } = require('./vektor.js');
            const v = VEKTOR.setBetrag(process.argv[1], Number(process.argv[2]));
            console.log(JSON.stringify({
              achse: v.achse,
              name: v.name,
              betrag: v.betrag,
              vektor: v.richtung.map(c => c * v.betrag),
              laenge: VEKTOR.laenge(v)
            }));
            """
            result = subprocess.run(
                ["node", "-e", script, achse, str(betrag)],
                cwd=ROOT, capture_output=True, text=True, check=True
            )

            body = result.stdout.encode()
            self.send_response(200)
        except Exception as exc:
            body = json.dumps({"fehler": str(exc)}).encode()
            self.send_response(400)

        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
