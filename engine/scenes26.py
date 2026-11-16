"""Reel 41 – Countdown Teil 4: Alles zum Release (Uhrzeit, Preis, Download). Mit Upgrades aus scenes27:
Lippensynchron (VOICE env), Synthwave-Beat + Bass-Hits, Figur reagiert."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import yt as Y          # generische Karten (v_big, v_icon …) im Hochformat-Panel
import scenes27 as S27  # Upgrades (patcht mascot.mouth_at + S2.sfx)
import scenes25 as S25
import scenes18 as S18
import scenes17 as S17
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, chip, FX, LIME, VIO, CY, MAG, ORG, RD, WH, INK, back, W, H)
from PIL import Image

VID = "41_Countdown_Teil4_Release"
S27.VID = VID  # Beat + Bass-Hits für dieses Reel
S18.DAYS = "03"; S18.PART = 4
S18.NEXT_T, S18.NEXT_SUB = "TEIL 5", "JASON & LUCIA"
S7.SCRIPTS7[VID] = [
    "Noch drei Tage bis G T A sechs! Alles zum Release in dreißig Sekunden. Folg mir!",
    "Eins: Am neunzehnten November um Mitternacht wird G T A sechs freigeschaltet.",
    "Zwei: Die Standard Edition kostet neunundsiebzig Euro neunundneunzig, die Ultimate neunundneunzig Euro neunundneunzig.",
    "Drei: Der Preload läuft schon. Plane bis zu zweihundertzwölf Gigabyte Speicher ein.",
    "Vier: In der Box steckt nur ein Download Code, keine Disc.",
    "Fünf: Zum Start nur PS fünf und Xbox Series. Für den PC gibt es noch kein Datum.",
    "Morgen in Teil fünf: Jason und Lucia, alles zur Story. Folg mir! Und merk dir:",
]
S7.DISPLAY.update({"neunzehnten": "19.", "neunundsiebzig": "79", "neunundneunzig": "99", "neunundneunzig,": "99,", "zweihundertzwölf": "212",
                   "dreißig": "30", "Eins:": "1:", "Zwei:": "2:", "Drei:": "3:", "Vier:": "4:", "Fünf:": "5:"})
S7.COMMENT[VID] = ("", "")
S7.COVER[VID] = ("GTA 6", "COUNTDOWN")
GOLD = (255, 205, 70); GRN = (90, 210, 120); BLUE = (60, 120, 255)
HEAD = [("NOCH 3 TAGE", "BIS GTA 6!"), ("19. NOVEMBER", "UM 0 UHR"), ("PREIS", "AB 79,99 €"), ("PRELOAD LÄUFT", "BIS 212 GB"),
        ("IN DER BOX", "KEINE DISC!"), ("NUR KONSOLE", "PC? NOCH OFFEN"), ("MORGEN TEIL 5", "JASON & LUCIA")]
SRC = [None, "QUELLE: ROCKSTAR / PLAYSTATION STORE", "QUELLE: ROCKSTAR GAMES", "QUELLE: PLAYSTATION / XBOX STORE",
       "QUELLE: HÄNDLER-ANGABEN", "QUELLE: ROCKSTAR GAMES", None]
ACC = [(RD, MAG), (CY, VIO), (GOLD, ORG), (CY, BLUE), (RD, VIO), (GRN, LIME), (LIME, CY)]

def hook(im, d, t, dur):
    S18.d_hook(im, d, t, dur)
    q = dur * 0.55
    if t > q:
        S25._follow(im, t - q, 720, 1170); return (720, 1170)
    return (720, 880)

def card(fn, *args):
    def f(im, d, t, dur):
        fn(im, t, dur, *args); return (720, 860)
    return f

SC = [hook,
      card(Y.v_big, "19.11.", "0 UHR · MITTERNACHT", (CY, VIO)),
      card(Y.v_big, "79,99 €", "ULTIMATE: 99,99 €", (GOLD, ORG)),
      card(Y.v_icon, "download", "BIS ZU 212 GB", (CY, BLUE)),
      card(Y.v_icon, "nodisc", "NUR DOWNLOAD-CODE", (RD, VIO)),
      card(Y.v_icon, "console", "PS5 + XBOX SERIES", (GRN, LIME)),
      S18.d_end]

S27.REACT = {1: 1.0, 2: 1.1, 3: 1.0, 4: 1.0, 5: 1.6}
def fx(fr, idx, t, dur):
    n = len(SC)
    if idx == 0 and t < 0.25: fr.paste(RD, (0, 0), Image.new("L", (W, H), int(140 * (1 - t / 0.25))))
    if idx == n - 1 and t > dur - 0.3: fr.paste(RD, (0, 0), Image.new("L", (W, H), int(140 * (t - (dur - 0.3)) / 0.3)))
    S18.nudge(fr, idx, t, dur)
    S27.react_fx(fr, idx, t, dur)

S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "TEIL 4: ALLES ZUM RELEASE"; S13.FACTLBL = "FAKT"
S13.TOP0 = "COUNTDOWN · TEIL 4"; S13.TOPLAST = "TEIL 5 MORGEN"; S13.EXTRA = fx
S13.POSEFN = S27.posefn
S13.comment13 = S17.end_overlay

_orig_chip = S18.chip
def _chip(im, txt, *a, **k):
    if txt == "TEIL 2: RICHTIG ABRAUBEN": txt = "TEIL 4: ALLES ZUM RELEASE"
    return _orig_chip(im, txt, *a, **k)
S18.chip = _chip

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.8, 0.8, 0.8, 0.8, 0.8, 0.5]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.85, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 1, S27.REACT[1] + 0.35, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p26_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
