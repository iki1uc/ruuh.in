# PENTA.GRAM · 1NS

Kleines, statisches Portal mit den Modulen BOOT, ID, HBT und PULSE.

## Dateien

- `index.html` – Startseite
- `01.boot.html` – Einstieg und Navigation
- `02.id.html` – Identität und Zustand
- `03.hbt.html` – Halt-, Bewertungs- und Tiefenprüfung
- `04.pulse.html` – Historie und Bindung
- `css/main.css` – gemeinsames Layout und mobile Navigation
- `js/` – gemeinsame Navigation, Tastatursteuerung und HBT-Prüfung

## Lokal starten

Öffne `index.html` im Browser. Falls ES-Module beim direkten Öffnen blockiert werden, starte einen lokalen Webserver, zum Beispiel:

```bash
python -m http.server 8000
```

Rufe anschließend `http://localhost:8000` auf.

## GitHub Pages

1. Lade alle Dateien und Ordner in das Repository `iki1uc/ruuh.in`.
2. Öffne in GitHub **Settings → Pages**.
3. Wähle den gewünschten Branch und als Verzeichnis `/ (root)`.
4. Speichere die Einstellung. GitHub Pages verwendet `index.html` als Startseite.

## Tastatursteuerung

- `1` bis `4` – BOOT, ID, HBT, PULSE
- `←` / `→` – voriges oder nächstes Modul
- `H` – Startseite
- `M` – mobiles Menü öffnen
- `Esc` – Menü schließen

Tastenkürzel werden nicht ausgelöst, wenn ein Eingabefeld aktiv ist.
Copyright (c) 2026 iki1uc

Alle Rechte vorbehalten.

Dieses Projekt ist proprietär. 
Das Kopieren, Klonen, Forken, Verbreiten, Modifizieren oder 
kommerzielle Nutzen ist ohne schriftliche Erlaubnis verboten.

Nur der Autor iki1uc darf dieses Projekt verwenden, verbreiten 
oder erweitern.

Externe Nutzung nur mit expliziter Business-Lizenz.
