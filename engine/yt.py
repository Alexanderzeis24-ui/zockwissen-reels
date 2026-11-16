"""16:9-YouTube-Engine (1920x1080). Ein Satz = ein Bild. Visuals aus den Reel-Szenen (Hochformat-Panel) + generische Karten.
Aufrufe:
  python3 yt.py preview            -> Vorschau-Bilder yt/prev_*.png
  python3 yt.py timing [voice.mp3] -> yt/timing.json (mit Stimme: an Pausen ausgerichtet)
  python3 yt.py render A B         -> rendert Sätze A..B-1 nach yt/seg_A.mp4
  python3 yt.py final [voice.mp3]  -> fügt zusammen, mischt Stimme + Beat"""
import sys, os, math, json, subprocess, random, importlib, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import scenes13 as S13
import scenes14, scenes15, scenes16, scenes17, scenes18, scenes19, scenes25, scenes27
import scenes12, mascot
from scenes13 import FX, FS, ease, back, gtext, atext, chip
from scenes14 import person, stamp
from reel2 import draw_character, CH_X, CH_FEET
import yt_script as Y

OUT = os.path.join(HERE, "yt"); os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1920, 1080, 30
LIME = (198, 255, 61); CY = (56, 217, 255); MAG = (255, 74, 163); ORG = (255, 160, 60); RD = (255, 70, 80); VIO = (124, 92, 255); GOLD = (255, 205, 70); GRN = (90, 210, 120)
WH = (255, 255, 255); INK = (14, 16, 30); YTR = (255, 0, 51)
CH_COL = {0: (MAG, VIO), 1: (CY, VIO), 2: (GOLD, ORG), 3: (CY, (60, 120, 255)), 4: (VIO, CY), 5: (GRN, LIME), 6: (MAG, ORG), 7: (RD, VIO), 8: (LIME, CY), 9: (GOLD, MAG), 10: (VIO, MAG), 11: (LIME, CY), 12: (LIME, MAG)}

# ---------------- data ----------------
def build():
    sl = []; ch = 0; chname = "INTRO"; first = False
    for e in Y.S:
        if e[0] == "#": ch, chname, first = e[1], e[2], True; continue
        sl.append(dict(text=e[0], vis=e[1], h1=e[2], h2=e[3], ch=ch, chname=chname, chfirst=first)); first = False
    return sl
SL = build()

def disp(w):
    k = w.strip(".,!?:;").lower()
    if k in Y.DISPLAY:
        tail = w[len(w.rstrip(".,!?:;")):]
        return Y.DISPLAY[k] + tail
    return w

# ---------------- timing ----------------
def est():
    return [max(2.2, len(s["text"]) / 14.5 + 0.45) for s in SL]

def silences(mp3):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
    st, out = None, []
    for line in r.splitlines():
        if "silence_start" in line: st = float(line.split("silence_start:")[1])
        elif "silence_end" in line and st is not None:
            en = float(line.split("silence_end:")[1].split("|")[0]); out.append((st, en)); st = None
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3], capture_output=True, text=True).stdout)
    return out, dur

def align(mp3):
    sil, total = silences(mp3)
    n = len(SL); L = np.array([len(s["text"]) + 12 for s in SL], float)
    speech_end = sil[-1][0] if sil and sil[-1][1] > total - 0.3 else total
    exp = np.cumsum(L)[:-1] / L.sum() * speech_end
    cand = [((a + b) / 2, b - a) for a, b in sil if a > 0.3 and b < speech_end - 0.1]
    M = len(cand); INF = 1e18
    # DP: choose n-1 increasing candidates
    cost = np.full((n, M + 1), INF); prev = np.zeros((n, M + 1), int)
    cost[0, :] = 0
    for k in range(1, n):
        best, bi = INF, -1
        for j in range(M):
            if cost[k - 1, j] < best and j >= 0: best, bi = cost[k - 1, j], j
            c = (cand[j][0] - exp[k - 1]) ** 2 * 0.15 - 2.5 * min(cand[j][1], 0.9)
            # best over earlier j' < j handled by running min of row k-1 up to j-1
            cost[k, j + 1] = (cost[k - 1, :j + 1].min() if j >= 0 else INF) + c
            prev[k, j + 1] = int(cost[k - 1, :j + 1].argmin())
    j = int(cost[n - 1, 1:].argmin()) + 1; cuts = []
    for k in range(n - 1, 0, -1):
        cuts.append(cand[j - 1][1] and cand[j - 1][0]); j = prev[k, j]
        if j == 0 and k > 1: j = 1
    cuts = sorted(cuts)
    starts = [0.0] + [c for c in cuts]
    ends = starts[1:] + [total + 1.2]
    return [e - s for s, e in zip(starts, ends)], total

def timing(mp3=None):
    if mp3:
        durs, total = align(mp3)
    else:
        durs = est(); total = sum(durs)
    words = []; t0 = 0
    for s, d in zip(SL, durs):
        ws = s["text"].split(); tot = sum(len(w) + 2 for w in ws); speak = max(0.5, d - 0.45); x = t0 + 0.05
        for w in ws:
            wd = speak * (len(w) + 2) / tot; words.append((x, x + wd, disp(w))); x += wd
        t0 += d
    json.dump(dict(durs=durs, words=words, voice=mp3), open(os.path.join(OUT, "timing.json"), "w"))
    return durs, words

def load_timing():
    j = json.load(open(os.path.join(OUT, "timing.json")))
    return j["durs"], [tuple(w) for w in j["words"]]

# ---------------- background ----------------
_yy, _xx = np.mgrid[0:108, 0:192].astype(np.float32)
def aurora(gt, c1, c2):
    a = np.zeros((108, 192, 3), np.float32) + np.array([7, 8, 18], np.float32)
    for bx, by, r, c, k in [(60 + 40 * math.sin(gt * .4), 30 + 14 * math.cos(gt * .3), 46, c1, .30), (150 + 30 * math.cos(gt * .35), 80 + 16 * math.sin(gt * .45), 52, c2, .34),
                            (20 + 14 * math.sin(gt * .3 + 2), 100, 40, c1, .16)]:
        g = np.exp(-((_xx - bx) ** 2 + (_yy - by) ** 2) / (2 * r * r)) * k
        a += g[..., None] * np.array(c, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)

def _over():
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for x in range(0, W, 80): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 8))
    for y in range(0, H, 80): d.line([(0, y), (W, y)], fill=(255, 255, 255, 8))
    v = Image.new("L", (W // 8, H // 8), 0); ImageDraw.Draw(v).ellipse([-40, -30, W // 8 + 40, H // 8 + 30], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(18)).resize((W, H))
    dark = Image.new("RGBA", (W, H), (3, 3, 10, 255)); dark.putalpha(ImageChops.invert(v).point(lambda z: int(z * 0.75)))
    return Image.alpha_composite(o, dark)
OVER = _over()

# ---------------- icons ----------------
def icon(d, im, name, cx, cy, s, col):
    c = col + (255,); w = max(4, int(14 * s))
    def R(x0, y0, x1, y1, **k): d.rounded_rectangle([cx + x0 * s, cy + y0 * s, cx + x1 * s, cy + y1 * s], **k)
    def E(x0, y0, x1, y1, **k): d.ellipse([cx + x0 * s, cy + y0 * s, cx + x1 * s, cy + y1 * s], **k)
    def P(pts, **k): d.polygon([(cx + x * s, cy + y * s) for x, y in pts], **k)
    def L(pts, **k): d.line([(cx + x * s, cy + y * s) for x, y in pts], **k)
    if name == "calendar":
        R(-110, -90, 110, 110, radius=int(20 * s), outline=c, width=w); R(-110, -90, 110, -40, radius=int(20 * s), fill=c)
        for x in (-60, 60): R(x - 8, -120, x + 8, -70, radius=int(6 * s), fill=c)
        for i in range(3):
            for j in range(4): R(-85 + j * 47, -15 + i * 40, -60 + j * 47, 10 + i * 40, radius=int(4 * s), fill=c)
    elif name == "clock":
        E(-110, -110, 110, 110, outline=c, width=w); L([(0, 0), (0, -70)], fill=c, width=w); L([(0, 0), (55, 30)], fill=c, width=w); E(-14, -14, 14, 14, fill=c)
    elif name == "console":
        R(-50, -120, 50, 120, radius=int(24 * s), outline=c, width=w); L([(-50, -40), (50, -40)], fill=c, width=max(3, w // 2)); E(-10, 60, 10, 80, fill=c)
    elif name == "moon":
        E(-100, -100, 100, 100, fill=c); E(-50, -130, 150, 70, fill=(14, 16, 30, 255))
        for x, y in ((60, 60), (90, -10), (30, 100)): E(x - 8, y - 8, x + 8, y + 8, fill=c)
    elif name == "globe":
        E(-110, -110, 110, 110, outline=c, width=w); E(-50, -110, 50, 110, outline=c, width=max(3, w // 2)); L([(-110, 0), (110, 0)], fill=c, width=max(3, w // 2))
        L([(-95, -55), (95, -55)], fill=c, width=max(3, w // 2)); L([(-95, 55), (95, 55)], fill=c, width=max(3, w // 2))
    elif name == "euro":
        E(-110, -110, 110, 110, outline=c, width=w); f = FX(int(150 * s)); d.text((cx, cy), "€", font=f, fill=c, anchor="mm")
    elif name == "arrowup":
        P([(0, -120), (100, 0), (40, 0), (40, 110), (-40, 110), (-40, 0), (-100, 0)], fill=c)
    elif name == "gift":
        R(-100, -20, 100, 110, radius=int(10 * s), fill=c); R(-115, -60, 115, -10, radius=int(10 * s), fill=c)
        R(-14, -60, 14, 110, radius=0, fill=(14, 16, 30, 255)); E(-70, -110, -5, -55, outline=c, width=w); E(5, -110, 70, -55, outline=c, width=w)
    elif name == "shirt":
        P([(-110, -70), (-45, -100), (-20, -75), (20, -75), (45, -100), (110, -70), (85, -10), (60, -25), (60, 110), (-60, 110), (-60, -25), (-85, -10)], fill=c)
    elif name == "box":
        P([(0, -110), (110, -55), (0, 0), (-110, -55)], fill=c); P([(-110, -45), (-5, 10), (-5, 120), (-110, 65)], fill=tuple(int(v * 0.75) for v in col) + (255,))
        P([(110, -45), (5, 10), (5, 120), (110, 65)], fill=tuple(int(v * 0.55) for v in col) + (255,))
    elif name == "person":
        E(-45, -115, 45, -25, fill=c); d.chord([cx - 100 * s, cy - 10 * s, cx + 100 * s, cy + 190 * s], 180, 360, fill=c)
    elif name == "tag":
        P([(-110, -40), (20, -110), (110, -110), (110, -20), (-20, 110)], fill=c); E(55, -80, 85, -50, fill=(14, 16, 30, 255))
    elif name == "download":
        P([(-40, -120), (40, -120), (40, -10), (90, -10), (0, 70), (-90, -10), (-40, -10)], fill=c); R(-110, 85, 110, 115, radius=int(12 * s), fill=c)
    elif name == "check":
        E(-110, -110, 110, 110, outline=c, width=w); L([(-55, 0), (-15, 45), (60, -45)], fill=c, width=int(w * 1.4))
    elif name == "trash":
        R(-80, -60, 80, 115, radius=int(14 * s), outline=c, width=w); R(-105, -85, 105, -60, radius=int(8 * s), fill=c); R(-30, -110, 30, -85, radius=int(6 * s), fill=c)
        for x in (-35, 0, 35): L([(x, -30), (x, 85)], fill=c, width=max(3, w // 2))
    elif name == "pc":
        R(-120, -100, 120, 50, radius=int(12 * s), outline=c, width=w); R(-20, 50, 20, 90, radius=0, fill=c); R(-70, 90, 70, 110, radius=int(8 * s), fill=c)
    elif name == "nodisc":
        E(-110, -110, 110, 110, outline=c, width=w); E(-25, -25, 25, 25, outline=c, width=w); L([(-90, 90), (90, -90)], fill=RD + (255,), width=int(w * 1.3))
    elif name == "palm":
        L([(0, 120), (10, 40), (25, -40)], fill=c, width=int(w * 1.4))
        for a in (-150, -110, -70, -30, 10):
            r = math.radians(a); P([(25, -40), (25 + 120 * math.cos(r), -40 + 70 * math.sin(r) + 40), (25 + 60 * math.cos(r), -40 + 30 * math.sin(r) + 10)], fill=c)
    elif name == "book":
        P([(0, -80), (-120, -100), (-120, 90), (0, 110)], fill=c); P([(0, -80), (120, -100), (120, 90), (0, 110)], fill=tuple(int(v * 0.75) for v in col) + (255,))
    elif name == "heart":
        E(-110, -90, 5, 25, fill=c); E(-5, -90, 110, 25, fill=c); P([(-107, -10), (107, -10), (0, 115)], fill=c)
    elif name == "pad":
        R(-130, -60, 130, 60, radius=int(60 * s), fill=c); E(-130, -20, -40, 100, fill=c); E(40, -20, 130, 100, fill=c)
        R(-95, -10, -45, 10, radius=0, fill=(14, 16, 30, 255)); R(-80, -25, -60, 25, radius=0, fill=(14, 16, 30, 255))
        for x, y in ((60, -15), (85, 10), (60, 35), (35, 10)): E(x - 10, y - 10, x + 10, y + 10, fill=(14, 16, 30, 255))
    elif name == "mask":
        R(-120, -60, 120, 40, radius=int(40 * s), fill=c); E(-80, -35, -25, 10, fill=(14, 16, 30, 255)); E(25, -35, 80, 10, fill=(14, 16, 30, 255))
    elif name == "atm":
        R(-90, -120, 90, 120, radius=int(14 * s), fill=c); R(-65, -95, 65, -30, radius=int(8 * s), fill=(14, 16, 30, 255))
        d.text((cx, cy - 62 * s), "$", font=FX(int(48 * s)), fill=col, anchor="mm")
        for i in range(3):
            for j in range(3): R(-55 + j * 40, -5 + i * 35, -30 + j * 40, 20 + i * 35, radius=int(4 * s), fill=(14, 16, 30, 255))
    elif name == "trophy":
        P([(-90, -110), (90, -110), (70, 0), (25, 40), (-25, 40), (-70, 0)], fill=c)
        d.arc([cx - 135 * s, cy - 100 * s, cx - 45 * s, cy - 10 * s], 90, 270, fill=c, width=w); d.arc([cx + 45 * s, cy - 100 * s, cx + 135 * s, cy - 10 * s], -90, 90, fill=c, width=w)
        R(-15, 40, 15, 80, radius=0, fill=c); R(-70, 80, 70, 110, radius=int(8 * s), fill=c)
    elif name == "battery":
        R(-120, -60, 100, 60, radius=int(14 * s), outline=c, width=w); R(100, -25, 125, 25, radius=int(6 * s), fill=c)
        for i in range(4): R(-100 + i * 50, -40, -60 + i * 50, 40, radius=int(4 * s), fill=c)
    elif name == "eye":
        d.chord([cx - 130 * s, cy - 90 * s, cx + 130 * s, cy + 90 * s], 180, 360, fill=c); d.chord([cx - 130 * s, cy - 90 * s, cx + 130 * s, cy + 90 * s], 0, 180, fill=c)
        E(-50, -50, 50, 50, fill=(14, 16, 30, 255)); E(-20, -20, 20, 20, fill=c)
    elif name == "star":
        pts = [(110 * (1 if k % 2 == 0 else 0.45) * math.cos(-math.pi / 2 + k * math.pi / 5), 110 * (1 if k % 2 == 0 else 0.45) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
        P(pts, fill=c)
    elif name == "question":
        E(-110, -110, 110, 110, outline=c, width=w); d.text((cx, cy), "?", font=FX(int(150 * s)), fill=c, anchor="mm")
    else:
        E(-100, -100, 100, 100, outline=c, width=w)

# ---------------- generic panel visuals (Hochformat-Panel: 430..1010 x 560..1230) ----------------
PCX, PCY = 720, 880
def rays(d, t, col):
    for k in range(12):
        a = k * math.pi / 6 + t * 0.4; r0, r1 = 140, 330
        d.polygon([(PCX + r0 * math.cos(a - 0.08), PCY + r0 * math.sin(a - 0.08)), (PCX + r1 * math.cos(a), PCY + r1 * math.sin(a)), (PCX + r0 * math.cos(a + 0.08), PCY + r0 * math.sin(a + 0.08))], fill=col + (40,))

def v_big(im, t, dur, val, lab, col):
    d = ImageDraw.Draw(im, "RGBA"); rays(d, t, col[0])
    s = back(t / 0.4)
    if s > 0.05: gtext(im, val, PCX, PCY - 30, S13.fit(FX, val, 170 * min(1.0, s), 540), col[0], col[1])
    chip(im, lab, PCX, PCY + 140, 30, WH, INK, back((t - 0.3) / 0.35))

def v_icon(im, t, dur, name, lab, col):
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(3):
        ph = (t * 0.6 + k / 3) % 1; r = 150 + ph * 160
        d.ellipse([PCX - r, PCY - 40 - r, PCX + r, PCY - 40 + r], outline=col[0] + (int(120 * (1 - ph)),), width=4)
    s = back(t / 0.4) * (1 + 0.04 * math.sin(t * 5))
    if s > 0.1:
        d.ellipse([PCX - 165 * s, PCY - 205 * s, PCX + 165 * s, PCY + 125 * s], fill=(14, 16, 30, 230), outline=col[0] + (255,), width=6)
        icon(d, im, name, PCX, PCY - 40, s * 0.95, col[0])
    chip(im, lab, PCX, PCY + 200, 30, col[0], INK if sum(col[0]) > 450 else WH, back((t - 0.3) / 0.35))

def v_list(im, t, dur, items, col):
    d = ImageDraw.Draw(im, "RGBA"); n = len(items); gap = 560 / max(4, n)
    for i, it in enumerate(items):
        p = ease((t - 0.1 - i * 0.22) / 0.3)
        if p <= 0.02: continue
        y = 640 + i * gap + gap / 2; off = (1 - p) * 120
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle([470 + off, y - 50, 970 + off, y + 50], 26, fill=(255, 255, 255, int(24 * p)), outline=col[0] + (int(200 * p),), width=3)
        d.ellipse([492 + off, y - 30, 552 + off, y + 30], fill=col[0] + (int(255 * p),))
        d.line([(506 + off, y), (518 + off, y + 13), (540 + off, y - 14)], fill=INK + (255,), width=7)
        atext(im, 578 + off, y, it, S13.fit(FX, it, 40, 360), WH, p, "lm")

def v_bars(im, t, dur, items, col):
    items = [(l, float(v)) for l, v in items]; mx = max(v for _, v in items)
    for i, (lab, v) in enumerate(items):
        p = ease((t - 0.2 - i * 0.25) / 0.9); y = 720 + i * 190
        d = ImageDraw.Draw(im, "RGBA")
        atext(im, 470, y - 45, lab, FX(36), WH, ease((t - i * 0.2) / 0.3), "lm")
        d.rounded_rectangle([470, y, 970, y + 60], 30, fill=(255, 255, 255, 30))
        w = 500 * v / mx * p
        if w > 30: d.rounded_rectangle([470, y, 470 + w, y + 60], 30, fill=(col[0] if i == 0 else (130, 136, 170)) + (255,))
        if p > 0.6: atext(im, 470 + w - 16, y + 30, (f"{int(v):,}".replace(",", ".") if v >= 100 else f"{v:g}"), FX(30), INK if i == 0 else WH, 1, "rm")

def v_warn(im, t, dur, txt, col):
    d = ImageDraw.Draw(im, "RGBA"); s = back(t / 0.35) * (1 + 0.05 * math.sin(t * 10))
    if s > 0.1:
        pts = [(PCX, PCY - 210 * s), (PCX + 200 * s, PCY + 130 * s), (PCX - 200 * s, PCY + 130 * s)]
        d.polygon(pts, fill=RD + (255,)); d.line(pts + [pts[0]], fill=WH + (255,), width=10)
        d.rounded_rectangle([PCX - 18 * s, PCY - 120 * s, PCX + 18 * s, PCY + 30 * s], 10, fill=WH + (255,)); d.ellipse([PCX - 20 * s, PCY + 55 * s, PCX + 20 * s, PCY + 95 * s], fill=WH + (255,))
    stamp(im, txt, PCX, PCY + 230, t - 0.6, RD, -6, 44)

def v_rumor(im, t, dur, val, lab, col):
    v_big(im, t, dur, val, lab, col)
    stamp(im, "GERÜCHT", PCX, PCY - 30, t - 0.9, RD, 10, 76)

def v_follow(im, t, dur, col):
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle([470, 680, 970, 820], 30, fill=(20, 22, 34, 255), outline=(255, 255, 255, 60), width=3)
    d.ellipse([495, 705, 585, 795], fill=(60, 160, 95, 255)); atext(im, 610, 728, "ZOCKWISSEN", FX(32), WH, 1, "lm"); atext(im, 610, 772, "GTA 6 jeden Tag", FS(24), (180, 186, 210), 1, "lm")
    done = t > 1.6
    b = back((t - 0.2) / 0.35) * (1 + (0.05 * math.sin(t * 9) if not done else 0))
    if b > 0.12:
        w, h = 210 * b, 56 * b
        d.rounded_rectangle([PCX - w, 930 - h, PCX + w, 930 + h], int(h), fill=(YTR if not done else (70, 74, 96)) + (255,))
        atext(im, PCX, 930, "ABONNIEREN" if not done else "ABONNIERT ✓", FX(int(46 * b)), WH)
    if done:
        bs = back((t - 1.8) / 0.3)
        if bs > 0.1:
            bx, by = PCX, 1090; d = ImageDraw.Draw(im, "RGBA")
            d.chord([bx - 50 * bs, by - 60 * bs, bx + 50 * bs, by + 40 * bs], 180, 360, fill=GOLD + (255,)); d.rectangle([bx - 50 * bs, by - 10 * bs, bx + 50 * bs, by + 30 * bs], fill=GOLD + (255,))
            d.rectangle([bx - 62 * bs, by + 30 * bs, bx + 62 * bs, by + 42 * bs], fill=GOLD + (255,)); d.ellipse([bx - 12 * bs, by + 42 * bs, bx + 12 * bs, by + 64 * bs], fill=GOLD + (255,))
            for k in (-1, 1): d.arc([bx - 95 * bs, by - 80 * bs, bx + 95 * bs, by + 60 * bs], 200 if k < 0 else -20, 230 if k < 0 else 10, fill=GOLD + (255,), width=6)
    p = ease((t - 0.7) / 0.6)
    if p > 0 and not t > 2.2:
        fx, fy = 900 - 120 * p, 1080 - 120 * p
        d = ImageDraw.Draw(im, "RGBA"); d.ellipse([fx - 26, fy - 26, fx + 26, fy + 26], fill=(236, 190, 150, 255), outline=(255, 255, 255, 255), width=4)
        if 1.4 < t < 1.7: d.ellipse([fx - 50, fy - 50, fx + 50, fy + 50], outline=(255, 255, 255, 160), width=4)

def v_comment(im, t, dur, col):
    d = ImageDraw.Draw(im, "RGBA"); s = ease(t / 0.3)
    d.rounded_rectangle([460, 700, 980, 900], 30, fill=(20, 22, 34, int(240 * s)), outline=(255, 255, 255, int(80 * s)), width=3)
    d.ellipse([485, 725, 555, 795], fill=(60, 160, 95, int(255 * s)))
    ans = "Die Polizei, krass!"; n = int(len(ans) * ease((t - 0.4) / 1.2))
    atext(im, 575, 745, "du", FS(28), (170, 174, 200), s, "lm"); atext(im, 575, 800, ans[:n] + ("|" if int(t * 3) % 2 == 0 and n < len(ans) else ""), FX(40), WH, s, "lm")
    if t > 1.7: import scenes12 as _s; _s.heart(ImageDraw.Draw(im), 930, 870, back((t - 1.7) / 0.3), RD)
    for k in range(3):
        st = t - 0.8 - k * 0.4
        if st > 0:
            y = 1190 - (st % 1.5) * 200; a = 1 - (st % 1.5) / 1.5
            d = ImageDraw.Draw(im, "RGBA"); d.rounded_rectangle([520 + k * 140, y - 30, 640 + k * 140, y + 30], 20, fill=(255, 255, 255, int(200 * a)))
            d.text((580 + k * 140, y), ["🔥", "😱", "❤"][k] if False else ["WOW", "OMG", "<3"][k], font=FX(26), fill=INK + (int(255 * a),), anchor="mm")

def v_duo(im, t, dur, col):
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(4):
        d.ellipse([520 - k * 20, 1100 - k * 4, 920 + k * 20, 1140 + k * 4], fill=col[0] + (14,))
    for i, (x, c, lab) in enumerate(((620, (120, 160, 255), "JASON"), (820, (255, 120, 190), "LUCIA"))):
        p = back((t - i * 0.2) / 0.4)
        if p > 0.15: person(d, x, 1120, 400 * p, c, "down", t + i); chip(im, lab, x, 650, 30, c, INK, p)
        d = ImageDraw.Draw(im, "RGBA")
    if t > 0.8:
        hs = back((t - 0.8) / 0.3) * (1 + 0.08 * math.sin(t * 6))
        import scenes12 as _s; _s.heart(ImageDraw.Draw(im), 720, 820, hs * 1.4, RD)

def v_people(im, t, dur, col):
    cols = [(255, 190, 90), (120, 200, 255), (190, 140, 255), (120, 230, 150)]
    for i in range(4):
        p = back((t - i * 0.15) / 0.4)
        if p < 0.15: continue
        d = ImageDraw.Draw(im, "RGBA"); x = 520 + i * 135
        person(d, x, 1120, 320 * p, cols[i], "down", t + i)
        atext(im, x, 760, "?", FX(int(60 * p)), cols[i])

def v_countdown(im, t, dur, col):
    d = ImageDraw.Draw(im, "RGBA")
    rem = max(0, 23 * 3600 + 59 * 60 + 59 - int(t * 7))
    vals = ["03", f"{rem // 3600:02d}", f"{rem // 60 % 60:02d}", f"{rem % 60:02d}"]
    for i, (v, l) in enumerate(zip(vals, ["TAGE", "STD", "MIN", "SEK"])):
        s = back((t - i * 0.1) / 0.35)
        if s < 0.15: continue
        cx = 520 + i * 135; hw, hh = 58 * s, 80 * s
        d.rounded_rectangle([cx - hw, PCY - hh, cx + hw, PCY + hh], 18, fill=(255, 255, 255, 24), outline=(RD if i == 0 else WH) + (160,), width=3)
        if i == 0: gtext(im, v, cx, PCY, FX(84 * s), RD, MAG)
        else: atext(im, cx, PCY, v, FX(70 * s), WH)
        atext(im, cx, PCY + 112, l, FS(24), (200, 204, 225), s); d = ImageDraw.Draw(im, "RGBA")
    chip(im, "19.11. · 0 UHR", PCX, PCY + 230, 32, LIME, INK, back((t - 0.8) / 0.4))

def v_map(im, t, dur, col):
    d = ImageDraw.Draw(im, "RGBA"); x0, y0, w, h = 470, 660, 480, 500
    d.polygon([(x0 + px * w, y0 + py * h) for px, py in scenes19.MAP], fill=(70, 90, 120, 255), outline=(255, 255, 255, 140))
    names = {1: "VICE CITY", 2: "KEYS", 3: "GRASSRIVERS", 4: "PORT GELLHORN", 5: "AMBROSIA", 6: "KALAGA"}
    for i, (k, (px, py)) in enumerate(scenes19.PINS.items()):
        s = back((t - 0.2 - i * 0.15) / 0.3)
        if s < 0.1: continue
        cx, cy = x0 + px * w, y0 + py * h; d = ImageDraw.Draw(im, "RGBA")
        r = 16 + 6 * math.sin(t * 5 + i)
        d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], outline=col[0] + (140,), width=3)
        d.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s], fill=col[0] + (255,), outline=WH + (255,), width=3)
        dx, dy, an = {1: (0, -34, "mm"), 2: (-26, 0, "rm"), 3: (-26, 0, "rm"), 4: (0, 40, "mm"), 5: (26, 0, "lm"), 6: (0, -36, "mm")}[k]
        atext(im, cx + dx, cy + dy, names[k], FX(24), WH, min(1, s), an)

def v_kw(im, t, dur, txt, col):
    d = ImageDraw.Draw(im, "RGBA"); rays(d, t, col[1])
    words = txt.split(); lines = []; cur = ""
    for w in words:
        if len(cur + " " + w) > 11 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    for i, ln in enumerate(lines[:3]):
        s = back((t - i * 0.1) / 0.35)
        if s > 0.1: gtext(im, ln, PCX, PCY - (len(lines) - 1) * 70 + i * 140, S13.fit(FX, ln, 120 * min(1, s), 540), col[0], col[1])

def render_panel(vis, t, dur, col, h2):
    im = Image.new("RGB", (1080, 1920), (12, 14, 30))
    d = ImageDraw.Draw(im)
    kind, _, arg = vis.partition(":")
    try:
        if kind == "S":
            mod, fn = arg.split("."); f = getattr(importlib.import_module(mod), fn)
            f(im, ImageDraw.Draw(im), t, max(dur, 3.0))
        elif kind == "big": a, b = arg.split("|"); v_big(im, t, dur, a, b, col)
        elif kind == "icon": a, b = arg.split("|"); v_icon(im, t, dur, a, b, col)
        elif kind == "list": v_list(im, t, dur, arg.split(";"), col)
        elif kind == "bars": v_bars(im, t, dur, [x.split("=") for x in arg.split(";")], col)
        elif kind == "warn": v_warn(im, t, dur, arg, col)
        elif kind == "rumor": a, b = arg.split("|"); v_rumor(im, t, dur, a, b, col)
        elif kind == "follow": v_follow(im, t, dur, col)
        elif kind == "comment": v_comment(im, t, dur, col)
        elif kind == "duo": v_duo(im, t, dur, col)
        elif kind == "people": v_people(im, t, dur, col)
        elif kind == "countdown": v_countdown(im, t, dur, col)
        elif kind == "map": v_map(im, t, dur, col)
        elif kind == "kw": v_kw(im, t, dur, arg, col)
    except Exception as ex:
        v_kw(im, t, dur, h2, col)
    return im.crop((430, 560, 1010, 1230))

@functools.lru_cache(None)
def _panel_mask(w, h):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], 40, fill=255); return m

@functools.lru_cache(None)
def _glow(w, h):
    m = Image.new("L", ((w + 200) // 8, (h + 200) // 8), 0)
    ImageDraw.Draw(m).rounded_rectangle([12, 12, m.width - 12, m.height - 12], 6, fill=255)
    return m.filter(ImageFilter.GaussianBlur(8)).resize((w + 200, h + 200), Image.BILINEAR)

def mascot_sprite(t, gt, pose, target):
    layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw_character(layer, t, gt, pose, target)
    bb = layer.getbbox()
    spr = layer.crop(bb) if bb else layer
    s = 500 / spr.height
    return spr.resize((max(1, int(spr.width * s)), 500), Image.LANCZOS)

def captions(im, words, gt):
    groups = []; cur = []
    for i, (a, b, w) in enumerate(words):
        cur.append(i)
        if len(cur) == 4 or w[-1] in ".!?:": groups.append(cur); cur = []
    if cur: groups.append(cur)
    act = None
    for i, (a, b, w) in enumerate(words):
        if a <= gt < b + 0.05: act = i
    if act is None:
        prev = [i for i, (a, b, w) in enumerate(words) if b <= gt]
        if not prev or gt - words[prev[-1]][1] > 0.4: return
        act = prev[-1]
    g = next(g for g in groups if act in g)
    d = ImageDraw.Draw(im, "RGBA"); f = FX(58)
    txts = [words[i][2] for i in g]; ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 20 * (len(ws) - 1)
    if tot > 720: f = FX(int(58 * 720 / tot)); ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 20 * (len(ws) - 1)
    x = 450 - tot / 2; y = 930
    d.rounded_rectangle([x - 30, y - 52, x + tot + 30, y + 52], 30, fill=(6, 7, 16, 190), outline=(255, 255, 255, 50), width=2)
    for i, tx, w in zip(g, txts, ws):
        on = i == act
        d.text((x + w / 2, y), tx, font=f, fill=LIME if on else WH, anchor="mm")
        if on: d.rounded_rectangle([x, y + 36, x + w, y + 42], 3, fill=LIME + (255,))
        x += w + 20

def frame(i, t, durs, words, starts, total):
    s = SL[i]; dur = durs[i]; gt = starts[i] + t
    col = CH_COL.get(s["ch"], (LIME, CY))
    im = aurora(gt, col[0], col[1]); im.paste(OVER, (0, 0), OVER)
    d = ImageDraw.Draw(im, "RGBA")
    # top bar + chapter progress
    d.ellipse([60, 52, 80, 72], fill=LIME + (255,)); d.text((92, 62), "ZOCKWISSEN", font=FS(30), fill=(255, 255, 255, 235), anchor="lm")
    lab = "INTRO" if s["ch"] == 0 else f"KAPITEL {s['ch']} · {s['chname']}"
    d.text((1860, 62), lab, font=FS(28), fill=(255, 255, 255, 220), anchor="rm")
    d.rounded_rectangle([60, 100, 1860, 108], 4, fill=(255, 255, 255, 40)); d.rounded_rectangle([60, 100, 60 + 1800 * gt / total, 108], 4, fill=col[0] + (255,))
    # headline
    p1 = ease(t / 0.3); p2 = ease((t - 0.12) / 0.3)
    atext(im, 90, 300 + (1 - p1) * 40, s["h1"], S13.fit(FX, s["h1"], 72, 980), WH, p1, "lm")
    if p2 > 0: gtext(im, s["h2"], 0, 420 + (1 - p2) * 40, S13.fit(FX, s["h2"], 120, 1000), col[0], col[1], p2, left=90)
    # panel
    alt = dur > 4.6 and t > dur * 0.55 and s["vis"].split(":")[0] not in ("follow", "comment", "list", "bars", "countdown")
    vis = ("kw:" + s["h2"]) if alt else s["vis"]
    tt = (t - dur * 0.55) if alt else t
    pan = render_panel(vis, tt, dur, col, s["h2"])
    sc = 1.15 + (0.03 * ease(tt / max(dur, 1)))
    pan = pan.resize((int(580 * sc), int(670 * sc)), Image.BILINEAR)
    pop = back(tt / 0.35) if tt < 0.35 else 1.0
    pw, ph = pan.size; px, py = 1210 + (1 - pop) * 60, 170
    im.paste(col[0], (int(px - 100), int(py - 100)), _glow(pw, ph).point(lambda v: int(v * 0.28)))
    im.paste(pan, (int(px), int(py)), _panel_mask(pw, ph))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle([px, py, px + pw, py + ph], 40, outline=(255, 255, 255, 80), width=3)
    # mascot
    pose = "cheer" if (s["chfirst"] and t < 1.2) or s["vis"] == "follow" and t < 1.0 else "point"
    spr = mascot_sprite(t, gt, pose, (CH_X + 900, CH_FEET - 1000))
    for k in range(5): d.ellipse([1000 - 150 + k * 18, 1040 - 10 + k * 3, 1000 + 150 - k * 18, 1070 - k * 3], fill=col[0] + (14,))
    im.paste(spr, (int(1000 - spr.width * 0.42), 1055 - spr.height), spr)
    captions(im, words, gt)
    # chapter banner
    if s["chfirst"] and t < 1.3:
        p = ease(t / 0.25) * (1 - ease((t - 1.0) / 0.3))
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, 470, W, 610], fill=(8, 10, 22, int(225 * p)))
        d.rectangle([0, 470, int(W * p), 478], fill=col[0] + (255,)); d.rectangle([W - int(W * p), 602, W, 610], fill=col[1] + (255,))
        if p > 0.3: gtext(im, f"KAPITEL {s['ch']}: {s['chname']}", 960, 540, S13.fit(FX, f"KAPITEL {s['ch']}: {s['chname']}", 80, 1700), col[0], col[1], min(1, p))
    # zoom punch + flash
    if t < 0.3 and i > 0:
        z = 1 + 0.05 * (1 - ease(t / 0.3)); zw, zh = int(W * z), int(H * z)
        im = im.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
        if t < 0.12: im = Image.blend(im, Image.new("RGB", (W, H), col[0]), 0.22 * (1 - t / 0.12))
    if alt and 0 <= tt < 0.1: im = Image.blend(im, Image.new("RGB", (W, H), WH), 0.18 * (1 - tt / 0.1))
    return im

def render(a, b):
    durs, words = load_timing(); starts = list(np.cumsum([0] + durs[:-1])); total = sum(durs)
    tmp = os.path.join(OUT, f"seg_{a:03d}.tmp.mp4"); out = os.path.join(OUT, f"seg_{a:03d}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(a, b):
        n = int(round((starts[i] + durs[i]) * FPS)) - int(round(starts[i] * FPS))
        for f in range(n):
            p.stdin.write(frame(i, f / FPS, durs, words, starts, total).tobytes())
    p.stdin.close(); p.wait(); os.replace(tmp, out)

def sfx_music(total, durs):
    sys.path.insert(0, HERE)
    mus = scenes27.synthwave(total + 1)
    SR = scenes27.SR; t0 = 0
    for i, s in enumerate(SL):
        if s["chfirst"]:
            i0 = int(t0 * SR); bm = scenes27.boom(int(0.9 * SR)); j = min(len(mus), i0 + len(bm)); mus[i0:j] += 1.0 * bm[: j - i0]
        t0 += durs[i]
    import wave
    path = os.path.join(OUT, "music.wav")
    st = (np.clip(np.stack([mus, mus], 1), -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    return path

def final(voice=None):
    durs, words = load_timing(); total = sum(durs)
    segs = sorted(f for f in os.listdir(OUT) if f.startswith("seg_") and f.endswith(".mp4") and ".tmp" not in f)
    lst = os.path.join(OUT, "list.txt"); open(lst, "w").write("".join(f"file '{os.path.join(OUT, s)}'\n" for s in segs))
    vid = os.path.join(OUT, "video_only.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid], check=True)
    mus = sfx_music(total, durs)
    name = "GTA6_Release_Alles_was_du_wissen_musst" + ("_FERTIG.mp4" if voice else "_VORSCHAU_ohne_Stimme.mp4")
    out = os.path.join(OUT, name)
    if voice:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", voice, "-i", mus, "-filter_complex",
                        f"[1:a]volume=1.0,apad[v];[2:a]volume=0.16[m];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total},alimiter=limit=0.95[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-movflags", "+faststart", out], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", mus, "-filter_complex", "[1:a]volume=0.5[a]", "-map", "0:v", "-map", "[a]",
                        "-c:v", "copy", "-c:a", "aac", "-t", str(total), "-movflags", "+faststart", out], check=True)
    print("OK", out, total)

def chapters():
    durs, _ = load_timing(); t0 = 0; out = []
    for s, d in zip(SL, durs):
        if s["chfirst"] or not out: out.append((t0, "Intro" if s["ch"] == 0 else f"Kapitel {s['ch']}: {s['chname'].title()}"))
        t0 += d
    return [f"{int(a // 60)}:{int(a % 60):02d} {b}" for a, b in out]

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "timing": timing(sys.argv[2] if len(sys.argv) > 2 else None); d, _ = load_timing(); print(len(d), "Sätze", round(sum(d), 1), "s")
    elif cmd == "preview":
        durs, words = load_timing(); starts = list(np.cumsum([0] + durs[:-1])); total = sum(durs)
        idx = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(0, len(SL), max(1, len(SL) // 12)))
        ims = [frame(i, min(durs[i] * 0.45, 1.6), durs, words, starts, total).resize((640, 360)) for i in idx]
        for k in range(0, len(ims), 6):
            sheet = Image.new("RGB", (640 * 2, 360 * 3))
            for j, im in enumerate(ims[k:k + 6]): sheet.paste(im, ((j % 2) * 640, (j // 2) * 360))
            sheet.save(os.path.join(OUT, f"prev_{k // 6}.png"))
        print(len(ims))
    elif cmd == "render": render(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "final": final(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "chapters": print("\n".join(chapters()))
