# ZOCKWISSEN Reels – Reel-Maschine

Animierte Instagram-Reels (9:16, 1080×1920, 30 fps) über GTA 6 mit dem ZOCKWISSEN-Maskottchen
(grüner Hoodie, rotes Headset). Alles wird mit Python + Pillow gezeichnet und mit ffmpeg zusammengesetzt –
keine fremden Bilder oder Trailer-Clips.

## Voraussetzungen

- Python 3 mit `pillow` und `numpy`
- `ffmpeg` / `ffprobe`
- Schrift **Inter Display** (Black/SemiBold), z. B. `/usr/share/fonts/opentype/inter/`

## Ablauf für ein neues Reel

1. **Szenen-Datei anlegen:** eine bestehende kopieren (z. B. `engine/scenes25.py`), `VID`, `SCRIPTS7` (ein Satz pro Szene),
   `HEAD`, `SRC`, `ACC` und die Szenen-Funktionen anpassen. Szenen sind `fn(im, d, t, dur) -> (x, y)`;
   der Rückgabewert ist der Punkt, auf den die Figur zeigt.
2. **Finalize-Skript erzeugen:**
   `sed 's/import scenes13, scenes7 as S7/import scenesNN, scenes7 as S7/; s/"scenes13.py"/"scenesNN.py"/' finalize13.py > finalizeNN.py`
3. **Vorschau-Bilder:** `python3 scenesNN.py preview <VID>` → `pNN_0.png`, `pNN_1.png`
4. **Vorschau-Video ohne Stimme:** `python3 finalizeNN.py <VID>`
5. **Stimme:** ElevenLabs, Stimme „Timon – Energetic and Clear“ (voice_id `0i5UT3fATBWphA0jBZug`), Modell `eleven_v4`,
   `[excited]` am Anfang und am Schluss, jeder Satz durch Leerzeile getrennt, Zahlen ausgeschrieben, „G T A“ buchstabiert.
6. **Mit Stimme:** Pausen ansehen
   `ffmpeg -i voice.mp3 -af silencedetect=noise=-35dB:d=0.12 -f null -`
   und die Pausen-Indizes der Satzenden als Schnitte übergeben:
   `CUTS=1,3,5,7,9,11 python3 finalizeNN.py <VID> vo/voice.mp3`
   → `ZOCKWISSEN_Reels_v2/<VID>/<VID>_FERTIG_mit_Stimme.mp4` + `_COVER.png`

## Stile

| Stil | Datei-Vorlage |
|---|---|
| Moderner Stil (dunkle Farbwolken, Glas-Karte, Story-Balken) – **Standard** | `scenes13.py` (Engine), Reels: `scenes14–21.py`, `scenes25.py` |
| Countdown-Serie (Cliffhanger, Folgen-Leiste) | `scenes17.py`, `scenes18.py`, `scenes19.py` |
| Gameplay-Look (animierte Nachtfahrt + Info-Karten) | `scenes22.py` |
| Glow-Sketch (Neon-Linien zeichnen sich selbst) | `scenes23.py` |
| 3D (eigene kleine 3D-Engine, Bühne, Spiegelung) | `scenes24.py` |
| Highlight-Cover + Intro-Storys | `highlights.py` |

Gemeinsame Bausteine: `scenes7.py` (Timing, Untertitel, Rendering), `scenes2.py` (Render-Pipeline, Soundeffekte),
`reel2.py` (Figur `draw_character`), `polish.py`.

## Regeln für jedes Reel

- Hook in Sekunde 0 schon in Bewegung, stärkster Satz zuerst
- Folgen-Aufruf direkt nach dem Hook (gesprochen + „+ FOLGEN“-Button mit Finger-Tipp)
- 5 Fakten, je eine Szene, Quellen-Zeile; Gerüchte/Schätzungen klar markieren
- Ende als Loop („Und merk dir:“ → Anfang), Kommentar-Aufruf mit Zahlen
- Ca. 25–30 Sekunden
- Mitliefern: MP4 mit Stimme, Cover, Sprechtext, Beschreibung + max. 5 Hashtags

## Countdown-Serie

- Teil 1 (13.11., „Noch 6 Tage“): Dein Handy
- Teil 2 (14.11., „Noch 5 Tage“): Richtig abrauben
- Teil 3 (15.11., „Noch 4 Tage“): Die 6 Regionen von Leonida → angekündigt: Teil 4 „Alles zum Release: Uhrzeit, Download und Preis“
