"""Reel 35 – Countdown Teil 3: Die 6 Regionen von Leonida."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes18 as S18
import scenes17 as S17
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import person
from PIL import Image, ImageDraw

VID = "35_Countdown_Teil3_Leonida"
S18.DAYS = "04"; S18.PART = 3
S18.NEXT_T, S18.NEXT_SUB = "TEIL 4", "ALLES ZUM RELEASE"
S7.SCRIPTS7[VID] = [
    "Noch vier Tage bis G T A sechs! Teil drei: Die sechs Regionen von Leonida!",
    "Eins: Vice City, die Partystadt mit Strand und Neonlichtern.",
    "Zwei: Die Leonida Keys, Inseln voller Jachten und Bars.",
    "Drei: Grassrivers, Sümpfe mit Flamingos und Alligatoren.",
    "Vier: Port Gellhorn, die vergessene Küste mit billigen Motels.",
    "Fünf: Ambrosia, mit riesiger Zuckerfabrik und einer Biker-Gang.",
    "Sechs: Mount Kalaga, Berge zum Jagen, Angeln und Offroad fahren.",
    "Morgen in Teil vier: Alles zum Release, Uhrzeit, Download und Preis. Folg mir, sonst verpasst du es!",
]
S7.COMMENT[VID] = ("", "")
S7.COVER[VID] = ("GTA 6", "COUNTDOWN")
HEAD = [("NOCH 4 TAGE", "BIS GTA 6!"), ("REGION 1", "VICE CITY"), ("REGION 2", "LEONIDA KEYS"), ("REGION 3", "GRASSRIVERS"),
        ("REGION 4", "PORT GELLHORN"), ("REGION 5", "AMBROSIA"), ("REGION 6", "MOUNT KALAGA"), ("MORGEN TEIL 4", "NICHT VERPASSEN!")]
SRC = [None] + ["QUELLE: ROCKSTAR GAMES"] * 6 + [None]
GOLD = (255, 205, 70); GRN = (90, 210, 120); BLUE = (60, 120, 255); PINK = (255, 120, 170)
ACC = [(RD, MAG), (MAG, CY), (CY, BLUE), (GRN, LIME), (ORG, VIO), (GOLD, ORG), (GRN, CY), (LIME, CY)]

# ---------- mini map ----------
MAP = [(0.05, 0.05), (0.55, 0.02), (0.75, 0.08), (0.78, 0.35), (0.92, 0.62), (0.88, 0.82), (0.72, 0.9), (0.58, 0.78), (0.48, 0.55), (0.35, 0.3), (0.1, 0.22)]
PINS = {1: (0.84, 0.66), 2: (0.66, 0.94), 3: (0.66, 0.72), 4: (0.2, 0.14), 5: (0.55, 0.3), 6: (0.6, 0.12)}
def minimap(im, idx, t):
    x0, y0, w, h = 452, 584, 140, 150
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([x0 - 6, y0 - 6, x0 + w + 6, y0 + h + 6], 14, fill=(8, 10, 22, 220), outline=(255, 255, 255, 80), width=2)
    D.polygon([(x0 + px * w, y0 + py * h) for px, py in MAP], fill=(70, 90, 120, 255))
    for k in (2, 6):
        for j in range(3): D.ellipse([x0 + (0.62 + j * 0.06) * w - 4, y0 + (0.97 - j * 0.015) * h - 3, x0 + (0.62 + j * 0.06) * w + 4, y0 + (0.97 - j * 0.015) * h + 3], fill=(70, 90, 120, 255))
    for i, (px, py) in PINS.items():
        cx, cy = x0 + px * w, y0 + py * h
        if i == idx:
            r = 8 + 6 * abs(math.sin(t * 5))
            D.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], outline=LIME + (160,), width=3)
            D.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=LIME + (255,))
        else:
            D.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 110))

def palm(D, x, yb, s, t, col=(20, 24, 40)):
    c = col + (255,); sw = 6 * math.sin(t * 1.5 + x) * s
    pts = [(x + sw * (k / 6) ** 2 + 18 * s * (k / 6), yb - k * 30 * s) for k in range(7)]
    D.line(pts, fill=c, width=max(4, int(12 * s)))
    tx, ty = pts[-1]
    for k in range(6):
        a = -math.pi / 2 + (k - 2.5) * 0.55 + 0.05 * math.sin(t * 2 + k)
        ex, ey = tx + math.cos(a) * 90 * s, ty + math.sin(a) * 50 * s + 35 * s
        D.polygon([(tx, ty), (ex, ey), (tx + math.cos(a) * 45 * s, ty + math.sin(a) * 25 * s + 12 * s)], fill=c)

def sea(D, y0, y1, c1, c2, t):
    for k in range(int((y1 - y0) / 12)):
        f = k / ((y1 - y0) / 12)
        c = tuple(int(c1[i] * (1 - f) + c2[i] * f) for i in range(3))
        D.rectangle([434, y0 + k * 12, 1006, y0 + k * 12 + 12], fill=c + (255,))
    for k in range(5):
        y = y0 + 30 + k * (y1 - y0 - 40) / 5; off = (t * 40 + k * 70) % 120
        for x in range(int(450 + off), 1000, 120): D.line([(x, y), (x + 40, y)], fill=(255, 255, 255, 60), width=3)

# ---------- scenes ----------
def l_vice(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    r = 120; D.ellipse([720 - r, 760 - r, 720 + r, 760 + r], fill=(255, 120, 90, 220))
    for k in range(5): D.rectangle([600, 790 + k * 20, 840, 796 + k * 20 + k], fill=(10, 12, 28, 255))
    S13.skyline(im, 470, 980, 1040, 11, [(214, 62, 150), (116, 86, 236), (58, 176, 226)], t, 280)
    D = ImageDraw.Draw(im, "RGBA")
    D.rectangle([434, 1040, 1006, 1090], fill=(245, 215, 160, 255))
    sea(D, 1090, 1220, (40, 160, 220), (20, 80, 160), t)
    palm(D, 500, 1060, 1.2, t); palm(D, 950, 1060, 1.0, t)
    fl = int(t * 3) % 3 != 0
    D.rounded_rectangle([630, 640, 810, 700], 14, outline=(MAG if fl else (120, 60, 100)) + (255,), width=5)
    atext(im, 720, 670, "NEON", FX(34), MAG if fl else (120, 60, 100))
    return (720, 900)

def yacht(D, x, y, s, col=(245, 245, 252)):
    c = col + (255,)
    D.polygon([(x - 110 * s, y), (x + 120 * s, y), (x + 90 * s, y + 34 * s), (x - 90 * s, y + 34 * s)], fill=c)
    D.polygon([(x - 60 * s, y), (x - 40 * s, y - 34 * s), (x + 60 * s, y - 34 * s), (x + 80 * s, y)], fill=c)
    D.rectangle([x - 30 * s, y - 28 * s, x + 50 * s, y - 14 * s], fill=(40, 60, 100, 255))

def l_keys(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    sea(D, 590, 1220, (60, 210, 230), (20, 110, 190), t)
    for (x, y, rx) in ((560, 860, 90), (800, 980, 120), (650, 1130, 70)):
        D.ellipse([x - rx, y - 26, x + rx, y + 26], fill=(245, 220, 160, 255))
        palm(D, x, y, 0.8, t, (40, 120, 60))
    p = (t * 0.12) % 1
    yacht(D, 1050 - 700 * p, 1050 + 4 * math.sin(t * 3), 0.9)
    for k in range(3):
        ph = (t * 0.6 + k / 3) % 1
        D.line([(1050 - 700 * p + 110 + ph * 80, 1070 + k * 6), (1050 - 700 * p + 150 + ph * 80, 1070 + k * 6)], fill=(255, 255, 255, int(150 * (1 - ph))), width=3)
    chip(im, "BAR", 800, 900, 26, GOLD, INK, back((t - 0.6) / 0.35))
    return (800, 960)

def flamingo(D, x, yb, s, t):
    c = PINK + (255,)
    D.line([(x - 6 * s, yb), (x - 4 * s, yb - 90 * s)], fill=c, width=max(3, int(5 * s)))
    D.line([(x + 8 * s, yb), (x + 6 * s, yb - 60 * s), (x - 10 * s, yb - 80 * s)], fill=c, width=max(3, int(5 * s)))
    D.ellipse([x - 40 * s, yb - 130 * s, x + 30 * s, yb - 86 * s], fill=c)
    nb = math.sin(t * 2) * 6 * s
    D.line([(x + 22 * s, yb - 116 * s), (x + 40 * s, yb - 170 * s), (x + 30 * s + nb, yb - 210 * s)], fill=c, width=max(4, int(9 * s)))
    D.ellipse([x + 18 * s + nb, yb - 226 * s, x + 44 * s + nb, yb - 202 * s], fill=c)
    D.polygon([(x + 40 * s + nb, yb - 216 * s), (x + 60 * s + nb, yb - 206 * s), (x + 40 * s + nb, yb - 204 * s)], fill=(30, 30, 30, 255))

def gator(D, x, y, s):
    c = (60, 110, 60, 255)
    D.rounded_rectangle([x - 130 * s, y - 14 * s, x + 110 * s, y + 10 * s], int(12 * s), fill=c)
    D.polygon([(x + 100 * s, y - 12 * s), (x + 190 * s, y - 4 * s), (x + 100 * s, y + 8 * s)], fill=c)
    for ex in (60, 82): D.ellipse([x + ex * s, y - 26 * s, x + (ex + 16) * s, y - 10 * s], fill=c); D.ellipse([x + (ex + 5) * s, y - 22 * s, x + (ex + 11) * s, y - 16 * s], fill=(255, 220, 60, 255))
    for k in range(6): D.polygon([(x - 110 * s + k * 34 * s, y - 14 * s), (x - 96 * s + k * 34 * s, y - 26 * s), (x - 82 * s + k * 34 * s, y - 14 * s)], fill=c)

def l_grass(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    sea(D, 900, 1220, (40, 80, 60), (20, 50, 40), t)
    for k in range(18):
        x = 450 + k * 31; h = 80 + (k * 37) % 70
        D.line([(x, 905), (x + 8 * math.sin(t * 2 + k), 905 - h)], fill=(90, 150, 80, 255), width=6)
    flamingo(D, 560, 1000, 1.1, t); flamingo(D, 650, 1020, 0.9, t + 1)
    gx = 1000 - 260 * ease((t - 0.3) / 1.6)
    gator(D, gx, 1120, 1.1)
    D.arc([gx - 160, 1100, gx + 220, 1150], 200, 340, fill=(255, 255, 255, 60), width=3)
    return (gx, 1110)

def l_motel(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.rectangle([434, 1090, 1006, 1220], fill=(40, 42, 56, 255))
    for x in range(470, 1000, 90): D.line([(x, 1150), (x + 40, 1150)], fill=(230, 220, 120, 200), width=4)
    D.rectangle([480, 880, 960, 1090], fill=(150, 120, 110, 255))
    D.rectangle([470, 860, 970, 890], fill=(110, 80, 70, 255))
    for k in range(5):
        x = 500 + k * 92
        lit = (k * 7 + int(t * 1.5)) % 4 != 0
        D.rectangle([x, 920, x + 60, 980], fill=((255, 220, 140) if lit else (60, 60, 80)) + (255,))
        D.rectangle([x + 18, 1010, x + 48, 1090], fill=(90, 60, 50, 255))
    D.line([(880, 860), (880, 640)], fill=(80, 80, 96, 255), width=10)
    fl = int(t * 7) % 5
    for i, ch in enumerate("MOTEL"):
        on = not (i == 1 and fl == 0) and not (i == 3 and fl == 2)
        atext(im, 800 + i * 40, 680, ch, FX(44), RD if on else (90, 40, 50))
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([780, 640, 1000, 720], 12, outline=(RD if fl != 4 else (90, 40, 50)) + (255,), width=4)
    chip(im, "BILLIG", 610, 760, 30, ORG, INK, back((t - 0.6) / 0.35))
    return (720, 930)

def bike(D, x, y, s, t):
    c = (20, 22, 34, 255)
    for wx in (-60, 60):
        D.ellipse([x + (wx - 34) * s, y - 34 * s, x + (wx + 34) * s, y + 34 * s], outline=c, width=max(4, int(10 * s)))
    D.polygon([(x - 50 * s, y - 20 * s), (x + 10 * s, y - 50 * s), (x + 50 * s, y - 40 * s), (x + 60 * s, y), (x - 20 * s, y)], fill=c)
    D.line([(x + 40 * s, y - 50 * s), (x + 70 * s, y - 80 * s)], fill=c, width=max(3, int(8 * s)))
    D.ellipse([x - 20 * s, y - 120 * s, x + 14 * s, y - 86 * s], fill=c)
    D.line([(x - 4 * s, y - 86 * s), (x + 6 * s, y - 40 * s)], fill=c, width=max(4, int(16 * s)))

def l_ambrosia(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.rectangle([480, 860, 940, 1080], fill=(200, 196, 190, 255))
    for k, x in enumerate((540, 640, 760)):
        D.rectangle([x, 660 + k * 30, x + 46, 860], fill=(170, 166, 160, 255))
        for j in range(4):
            ph = (t * 0.5 + j / 4 + k * 0.3) % 1; r = 16 + 36 * ph
            D.ellipse([x + 23 - r + ph * 40, 640 + k * 30 - ph * 120 - r, x + 23 + r + ph * 40, 640 + k * 30 - ph * 120 + r], fill=(235, 235, 245, int(160 * (1 - ph))))
    for r in range(2):
        for c in range(7): D.rectangle([500 + c * 62, 900 + r * 70, 540 + c * 62, 940 + r * 70], fill=(80, 110, 160, 255))
    atext(im, 710, 1050, "ZUCKER", FX(36), INK)
    D.line([(434, 1160), (1006, 1160)], fill=(255, 255, 255, 110), width=4)
    bx = 400 + ((t * 260) % 760)
    if 440 < bx < 1000: bike(D, bx, 1128, 0.75, t)
    chip(im, "BIKER-GANG", 870, 1205, 24, GOLD, INK, back((t - 0.9) / 0.35))
    return (710, 900)

def l_kalaga(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.polygon([(434, 1000), (600, 720), (760, 1000)], fill=(70, 120, 90, 255))
    D.polygon([(600, 1000), (800, 660), (1006, 1000)], fill=(50, 100, 80, 255))
    D.polygon([(760, 730), (800, 660), (840, 730), (815, 720), (800, 740), (785, 722)], fill=(200, 220, 210, 255))
    sea(D, 1000, 1220, (40, 120, 160), (20, 70, 120), t)
    for k, x in enumerate((470, 520, 950, 990)):
        D.polygon([(x, 1000), (x + 22, 930), (x + 44, 1000)], fill=(30, 70, 50, 255))
    D.line([(470, 980), (680, 900), (700, 1080)], fill=(220, 220, 230, 255), width=3)
    ph = (t * 0.6) % 1
    fx = 720 + 120 * ph; fy = 1110 - 180 * math.sin(ph * math.pi)
    D.ellipse([fx - 30, fy - 12, fx + 30, fy + 12], fill=(200, 210, 230, 255))
    D.polygon([(fx - 30, fy), (fx - 52, fy - 14), (fx - 52, fy + 14)], fill=(200, 210, 230, 255))
    if ph > 0.85:
        for k in range(5): D.line([(fx, 1110), (fx + (k - 2) * 20, 1080)], fill=(255, 255, 255, 180), width=3)
    chip(im, "JAGEN · ANGELN · OFFROAD", 720, 1185, 24, GRN, INK, back((t - 0.6) / 0.35))
    return (800, 820)

_OUT = Image.new("L", (W, H), 255); ImageDraw.Draw(_OUT).rounded_rectangle([432, 562, 1008, 1228], 46, fill=0)
def wrap(fn, idx):
    def f(im, d, t, dur):
        before = im.copy()
        r = fn(im, d, t, dur)
        im.paste(before, (0, 0), _OUT)
        minimap(im, idx, t)
        return r
    return f

def hook(im, d, t, dur):
    r = S18.d_hook(im, d, t, dur)
    return r

SC = [hook] + [wrap(f, i + 1) for i, f in enumerate([l_vice, l_keys, l_grass, l_motel, l_ambrosia, l_kalaga])] + [S18.d_end]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "TEIL 3: 6 REGIONEN"
S13.TOP0 = "COUNTDOWN · TEIL 3"; S13.TOPLAST = "TEIL 4 MORGEN"; S13.EXTRA = S18.nudge
S13.comment13 = S17.end_overlay

# hook chip text override
_orig_chip = S18.chip
def _chip(im, txt, *a, **k):
    if txt == "TEIL 2: RICHTIG ABRAUBEN": txt = "TEIL 3: 6 REGIONEN"
    return _orig_chip(im, txt, *a, **k)
S18.chip = _chip

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.45]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 3, 0.4, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p19_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
