"""Reel 37 – Gameplay-Look: animierte Nachtfahrt als Hintergrund + Info-Karten. Thema: Polizei-System."""
import sys, os, math, random, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
import scenes12
from scenes13 import FX, FS, LIME, CY, MAG, ORG, RD, WH, INK, ease, back, W, H
from reel2 import draw_character, CH_X, CH_FEET
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

VID = "37_Polizei_Gameplay"
S7.SCRIPTS7[VID] = [
    "Die Polizei in G T A sechs ist so schlau wie nie! Folg mir für mehr G T A sechs Wissen!",
    "Eins: Sie merkt sich dein Outfit und deine Waffen.",
    "Zwei: Neue Klamotten machen dich schwerer erkennbar.",
    "Drei: Polizeihunde können dich schnappen.",
    "Vier: Nagelbänder siehst du nachts kaum.",
    "Fünf: Teure Autos haben Peilsender.",
    "Welcher Trick ist am fiesesten? Schreib die Zahl! Und merk dir:",
]
S7.COMMENT[VID] = ("WELCHER TRICK?", "Die Hunde sind fies!")
S7.COVER[VID] = ("GTA 6", "POLIZEI")
GREEN = (90, 230, 120)
CARDS = [("eye", "Polizei merkt sich alles", "Outfit, Waffen, Aussehen"), ("shirt", "Outfit wechseln", "= schwerer erkennbar"),
         ("paw", "Polizeihunde", "schnappen dich"), ("spike", "Nagelbänder", "nachts kaum sichtbar"), ("pin", "Peilsender", "in teuren Autos")]
SRC = "Quelle: Edge-Magazin, Vorschau"

# ---------------- procedural night drive ----------------
HZ = 820; F = 1.0; CAMH = 180
rng = random.Random(7)
OBJS = []
for i in range(40):
    z0 = 0.15 + i * 0.16
    for side in (-1, 1):
        kind = "lamp" if i % 3 == 0 else ("palm" if i % 3 == 1 else None)
        if kind: OBJS.append((z0 + (0.08 if side > 0 else 0), side, kind, rng.random()))
BLD = []
for i in range(60):
    BLD.append((0.3 + i * 0.11, -1 if i % 2 else 1, rng.uniform(560, 900), rng.uniform(500, 1500), rng.choice([(150, 60, 160), (60, 80, 170), (40, 140, 180), (180, 70, 110)]), rng.random()))
SPAN = 6.4

def sky():
    y = np.linspace(0, 1, HZ, dtype=np.float32)[:, None, None]
    top = np.array([12, 10, 40], np.float32); mid = np.array([120, 40, 120], np.float32); low = np.array([255, 120, 80], np.float32)
    c = np.where(y < 0.6, top * (1 - y / 0.6) + mid * (y / 0.6), mid * (1 - (y - 0.6) / 0.4) + low * ((y - 0.6) / 0.4))
    return Image.fromarray(np.repeat(c, W, 1).astype(np.uint8))
SKY = sky()

def proj(x, z, h=0.0):
    s = F / z
    return 540 + x * s * 1.6, HZ + (CAMH - h) * s

def fogc(c, z):
    k = min(1, max(0, (z - 0.4) / 5.5))
    f = (130, 50, 120)
    return tuple(int(c[i] * (1 - k) + f[i] * k) for i in range(3))

def background(gt):
    im = Image.new("RGB", (W, H), (20, 18, 30)); im.paste(SKY, (0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([540 - 170, HZ - 230, 540 + 170, HZ + 110], fill=(255, 170, 90, 255))
    for k in range(6): d.rectangle([360, HZ - 70 + k * 18, 720, HZ - 64 + k * 18 + k], fill=(120, 40, 120, 255))
    d.polygon([(0, HZ), (W, HZ), (W, H), (0, H)], fill=(24, 22, 34, 255))
    # road
    d.polygon([proj(-330, 8), proj(330, 8), proj(330, 0.12), proj(-330, 0.12)], fill=(46, 44, 58, 255))
    sp = gt * 2.2
    for i in range(30):
        z = SPAN - ((i * 0.45 + sp) % SPAN)
        if z < 0.45: continue
        z2 = z + 0.18
        for x in (-110, 110):
            a, b = proj(x - 6, z), proj(x + 6, z); c_, e = proj(x + 6, z2), proj(x - 6, z2)
            d.polygon([a, b, c_, e], fill=fogc((235, 230, 200), z) + (255,))
    for x in (-330, 330):
        d.line([proj(x, 8), proj(x, 0.12)], fill=(255, 200, 120, 160), width=4)
    items = []
    for (z0, side, col_h, hgt, col, r) in BLD:
        z = SPAN - ((z0 + sp) % SPAN)
        if z > 0.2: items.append((z, "bld", side, col_h, hgt, col, r))
    for (z0, side, kind, r) in OBJS:
        z = SPAN - ((z0 + sp) % SPAN)
        if z > 0.13: items.append((z, kind, side, 0, 0, None, r))
    items.sort(key=lambda o: -o[0])
    for z, kind, side, xw, hgt, col, r in items:
        if kind == "bld":
            x0 = side * xw; x1 = side * (xw + 260)
            p1 = proj(x0, z, hgt); p2 = proj(x1, z, hgt); p3 = proj(x1, z); p4 = proj(x0, z)
            d.polygon([p1, p2, p3, p4], fill=fogc((20, 20, 34), z) + (255,))
            wcol = fogc(col, z)
            s = F / z
            if s > 0.25:
                cols = 4; rows = int(hgt / 120)
                for rr in range(rows):
                    for cc in range(cols):
                        if (rr * 7 + cc * 3 + int(r * 10)) % 3 == 0: continue
                        wx = x0 + side * (30 + cc * 60); wy = 60 + rr * 120
                        a = proj(wx, z, wy + 50); b = proj(wx + side * 30, z, wy)
                        d.rectangle([min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])], fill=wcol + (230,))
            if r > 0.6 and s > 0.3:
                a = proj(x0 + side * 40, z, hgt - 60); b = proj(x0 + side * 220, z, hgt - 140)
                nc = (255, 70, 180) if r > 0.8 else (60, 230, 255)
                d.rectangle([min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])], outline=nc + (255,), width=max(2, int(6 * s)))
        elif kind == "lamp":
            base = proj(side * 400, z); top = proj(side * 400, z, 520); arm = proj(side * 330, z, 520)
            s = F / z; wdt = max(2, int(10 * s))
            d.line([base, top, arm], fill=fogc((40, 40, 50), z) + (255,), width=wdt)
            r_ = 18 * s
            d.ellipse([arm[0] - r_ * 2.5, arm[1] - r_ * 2.5, arm[0] + r_ * 2.5, arm[1] + r_ * 2.5], fill=(255, 200, 120, 40))
            d.ellipse([arm[0] - r_, arm[1] - r_ * 0.6, arm[0] + r_, arm[1] + r_ * 0.6], fill=(255, 230, 170, 255))
        elif kind == "palm":
            base = proj(side * 470, z); s = F / z
            pts = [proj(side * (470 + 40 * (k / 6) ** 2), z, k * 110) for k in range(7)]
            d.line(pts, fill=fogc((20, 18, 30), z) + (255,), width=max(2, int(16 * s)))
            tx, ty = pts[-1]
            for k in range(7):
                a = -math.pi / 2 + (k - 3) * 0.5 + 0.06 * math.sin(gt * 2 + k + r * 5)
                ex, ey = tx + math.cos(a) * 160 * s, ty + math.sin(a) * 70 * s + 70 * s
                d.polygon([(tx, ty), (ex, ey), (tx + math.cos(a) * 80 * s, ty + math.sin(a) * 35 * s + 25 * s)], fill=fogc((20, 18, 30), z) + (255,))
    # player car (rear view)
    cx = 540 + 14 * math.sin(gt * 0.9); cy = 1530 + 4 * math.sin(gt * 9)
    d.ellipse([cx - 260, cy + 90, cx + 260, cy + 150], fill=(0, 0, 0, 140))
    d.rounded_rectangle([cx - 250, cy - 40, cx + 250, cy + 110], 40, fill=(30, 32, 44, 255))
    d.polygon([(cx - 170, cy - 40), (cx - 120, cy - 150), (cx + 120, cy - 150), (cx + 170, cy - 40)], fill=(24, 26, 36, 255))
    d.polygon([(cx - 140, cy - 48), (cx - 105, cy - 135), (cx + 105, cy - 135), (cx + 140, cy - 48)], fill=(60, 70, 100, 255))
    for sx in (-1, 1):
        d.rounded_rectangle([cx + sx * 245 - (60 if sx > 0 else 0), cy - 10, cx + sx * 245 + (0 if sx > 0 else 60), cy + 30], 10, fill=(255, 40, 60, 255))
        d.ellipse([cx + sx * 215 - 70, cy - 40, cx + sx * 215 + 70, cy + 60], fill=(255, 40, 60, 40))
        d.rounded_rectangle([cx + sx * 190 - 34, cy + 90, cx + sx * 190 + 34, cy + 160], 12, fill=(12, 12, 16, 255))
    d.rounded_rectangle([cx - 70, cy + 40, cx + 70, cy + 76], 6, fill=(230, 230, 236, 255))
    d.text((cx, cy + 58), "ZOCK 6", font=FX(26), fill=INK, anchor="mm")
    # police lights hint behind
    fl = int(gt * 6) % 2
    for side, col in ((-1, RD), (1, (60, 120, 255))):
        on = (fl == 0) == (side < 0)
        if on:
            m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse([540 + side * 420 - 260, 1880 - 200, 540 + side * 420 + 260, 1880 + 200], fill=110)
            im.paste(col, (0, 0), m.filter(ImageFilter.GaussianBlur(60)))
    im = im.filter(ImageFilter.GaussianBlur(1.6))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.blend(im, dark, 0.28)

# ---------------- icons / cards ----------------
def icon(d, kind, cx, cy, s, col):
    c = col + (255,)
    if kind == "eye":
        d.ellipse([cx - 46 * s, cy - 26 * s, cx + 46 * s, cy + 26 * s], outline=c, width=int(8 * s)); d.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s], fill=c)
    elif kind == "shirt":
        d.polygon([(cx - 44 * s, cy - 26 * s), (cx - 20 * s, cy - 38 * s), (cx - 10 * s, cy - 28 * s), (cx + 10 * s, cy - 28 * s), (cx + 20 * s, cy - 38 * s), (cx + 44 * s, cy - 26 * s), (cx + 34 * s, cy - 4 * s), (cx + 24 * s, cy - 10 * s), (cx + 24 * s, cy + 38 * s), (cx - 24 * s, cy + 38 * s), (cx - 24 * s, cy - 10 * s), (cx - 34 * s, cy - 4 * s)], fill=c)
    elif kind == "paw":
        d.ellipse([cx - 26 * s, cy - 4 * s, cx + 26 * s, cy + 38 * s], fill=c)
        for dx, dy in ((-36, -18), (-14, -38), (14, -38), (36, -18)): d.ellipse([cx + (dx - 11) * s, cy + (dy - 13) * s, cx + (dx + 11) * s, cy + (dy + 13) * s], fill=c)
    elif kind == "spike":
        d.rectangle([cx - 50 * s, cy + 14 * s, cx + 50 * s, cy + 26 * s], fill=c)
        for k in range(5): x = cx - 40 * s + k * 20 * s; d.polygon([(x - 8 * s, cy + 14 * s), (x, cy - 26 * s), (x + 8 * s, cy + 14 * s)], fill=c)
    elif kind == "pin":
        d.ellipse([cx - 30 * s, cy - 44 * s, cx + 30 * s, cy + 16 * s], fill=c); d.polygon([(cx - 26 * s, cy), (cx + 26 * s, cy), (cx, cy + 46 * s)], fill=c)
        d.ellipse([cx - 11 * s, cy - 25 * s, cx + 11 * s, cy - 3 * s], fill=(20, 22, 34, 255))
    elif kind == "siren":
        d.chord([cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s], 180, 360, fill=c); d.rectangle([cx - 50 * s, cy, cx + 50 * s, cy + 16 * s], fill=c)
        for k in (-1, 0, 1): d.line([(cx + k * 46 * s, cy - 54 * s), (cx + k * 60 * s, cy - 74 * s + abs(k) * 12 * s)], fill=c, width=int(7 * s))

@functools.lru_cache(None)
def _cardglow(w, h):
    m = Image.new("L", (w + 120, h + 120), 0); ImageDraw.Draw(m).rounded_rectangle([60, 60, w + 60, h + 60], 50, outline=255, width=14)
    return m.filter(ImageFilter.GaussianBlur(18))

def card(im, kind, title, sub, t, cy=800, col=GREEN, pulse=True):
    s = back(t / 0.35)
    if s < 0.08: return
    w0, h0 = 760, 360
    L = Image.new("RGBA", (w0 + 120, h0 + 120), (0, 0, 0, 0))
    L.paste(col, (0, 0), _cardglow(w0, h0).point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(L, "RGBA")
    d.rounded_rectangle([60, 60, w0 + 60, h0 + 60], 50, fill=(22, 24, 36, 240), outline=col + (255,), width=7)
    ic = 60 + w0 / 2
    d.ellipse([ic - 70, 92, ic + 70, 232], fill=(36, 40, 60, 255))
    ip = back((t - 0.15) / 0.3)
    if ip > 0.1: icon(d, kind, ic, 162, ip * 1.15, col)
    if t > 0.2:
        a = 2 * math.pi * min(1, (t - 0.2) / 0.5)
        d.arc([ic - 82, 80, ic + 82, 244], -90, -90 + math.degrees(a), fill=col + (255,), width=7)
    f1 = S13.fit(FX, title, 64, w0 - 60); f2 = S13.fit(FX, sub, 42, w0 - 80)
    d.text((ic, 300), title, font=f1, fill=WH, anchor="mm")
    d.text((ic, 362), sub, font=f2, fill=(220, 224, 240), anchor="mm")
    L = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s))), Image.BILINEAR)
    im.paste(L, (int(540 - L.width / 2), int(cy - L.height / 2)), L)

def outlined(d, xy, txt, f, fill, stroke=9):
    d.text(xy, txt, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(0, 0, 0))

def captions(im, words, gt):
    groups = []; cur = []
    for i, (a, b, w) in enumerate(words):
        cur.append(i)
        if len(cur) == 2 or w[-1] in ".!?:": groups.append(cur); cur = []
    if cur: groups.append(cur)
    act = None
    for i, (a, b, w) in enumerate(words):
        if a <= gt < b + 0.05: act = i
    if act is None:
        prev = [i for i, (a, b, w) in enumerate(words) if b <= gt]
        if not prev or gt - words[prev[-1]][1] > 0.35: return
        act = prev[-1]
    g = next(g for g in groups if act in g)
    d = ImageDraw.Draw(im); f = FX(92)
    txts = [words[i][2] for i in g]; ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 30 * (len(ws) - 1)
    if tot > 960: f = FX(int(92 * 960 / tot)); ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 30 * (len(ws) - 1)
    x = 540 - tot / 2
    for i, tx, w in zip(g, txts, ws):
        on = i == act
        pop = 1 + 0.12 * (1 - ease((gt - words[i][0]) / 0.12)) if on else 1
        outlined(d, (x + w / 2, 1300), tx, FX(int(f.size * pop)), (255, 230, 60) if on else WH)
        x += w + 30

def follow_btn(im, ot, cx=540, cy=1110):
    done = ot > 1.9
    b = back(ot / 0.3) * (1 + (0.06 * math.sin(ot * 10) if not done else 0))
    if b < 0.12: return
    hw, hh = 200 * b, 56 * b
    col1, col2 = (LIME, CY) if not done else ((60, 66, 100), (60, 66, 100))
    k = np.linspace(0, 1, int(2 * hw), dtype=np.float32)[None, :, None]
    g = (np.array(col1, np.float32) * (1 - k) + np.array(col2, np.float32) * k).astype(np.uint8)
    gi = Image.fromarray(np.repeat(g, int(2 * hh), 0)); m = Image.new("L", gi.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, gi.width - 1, gi.height - 1], int(hh), fill=255)
    D = ImageDraw.Draw(im, "RGBA")
    if not done:
        for r in range(3):
            ph = (ot * 1.2 + r / 3) % 1; e = 10 + ph * 46
            D.rounded_rectangle([cx - hw - e, cy - hh - e, cx + hw + e, cy + hh + e], int(hh + e), outline=LIME + (int(120 * (1 - ph)),), width=3)
    im.paste(gi, (int(cx - hw), int(cy - hh)), m)
    ImageDraw.Draw(im).text((cx, cy), "+ FOLGEN" if not done else "✓ GEFOLGT", font=FX(50 * b), fill=INK if not done else WH, anchor="mm")
    p = ease((ot - 0.7) / 0.6)
    if p > 0:
        fx, fy = cx + 230 - 130 * p, cy + 150 - 130 * p; tap = 1.6 < ot < 1.9
        D = ImageDraw.Draw(im, "RGBA")
        D.ellipse([fx - 26, fy - 26, fx + 26, fy + 26], fill=(236, 190, 150, 255), outline=(255, 255, 255, 255), width=4)
        if tap: D.ellipse([fx - 50, fy - 50, fx + 50, fy + 50], outline=(255, 255, 255, 160), width=4)

def mascot(im, t, gt, target):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_character(layer, t, gt, "point", target)
    box = layer.crop((0, 900, 760, 1620)).resize((380, 360), Image.LANCZOS)
    im.paste(box, (-10, 1440), box)

def stars(im, n_on, t, cy=560):
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(5):
        cx = 380 + i * 80; on = i < n_on
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5; r = 30 if k % 2 == 0 else 13
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=((255, 214, 64, 255) if on else (255, 255, 255, 60)), outline=(0, 0, 0, 200), width=3)

def frame22(vid, idx, t, T, words, cover=False, no_sticker=False):
    R = S2.R[vid]; dur = R[idx][0]; n = len(R)
    gt = sum(s[0] for s in R[:idx]) + t
    im = background(gt)
    d = ImageDraw.Draw(im, "RGBA")
    # top bar
    d.ellipse([60, 120, 80, 140], fill=LIME + (255,)); d.text((92, 130), "ZOCKWISSEN", font=FS(32), fill=(255, 255, 255, 235), anchor="lm")
    last = idx == n - 1
    if idx == 0:
        tt = t + 0.4
        card(im, "siren", "GTA 6 Polizei", "schlauer als je zuvor", tt, cy=800, col=RD)
        stars(im, min(5, int(tt * 4)), tt, cy=560)
        if not cover and t > dur * 0.45: follow_btn(im, t - dur * 0.45)
        if cover:
            outlined(ImageDraw.Draw(im), (540, 1150), "SO SCHLAU IST", FX(84), WH)
            outlined(ImageDraw.Draw(im), (540, 1250), "DIE POLIZEI!", FX(110), (255, 230, 60), 11)
    elif not last:
        kind, title, sub = CARDS[idx - 1]
        card(im, kind, title, sub, t, cy=800)
        d = ImageDraw.Draw(im, "RGBA")
        f = FX(40); lab = f"#{idx}"
        d.rounded_rectangle([60, 470, 170, 540], 20, fill=GREEN + (255,)); d.text((115, 505), lab, font=f, fill=INK, anchor="mm")
        sa = ease((t - 0.5) / 0.3)
        if sa > 0:
            fs = FS(26); w_ = d.textlength(SRC, font=fs)
            d.rounded_rectangle([540 - w_ / 2 - 24, 1020, 540 + w_ / 2 + 24, 1064], 22, fill=(0, 0, 0, int(150 * sa)))
            d.text((540, 1042), SRC, font=fs, fill=(255, 255, 255, int(220 * sa)), anchor="mm")
    else:
        act = int(t * 2.4) % 5
        for i in range(5):
            s = back((t - i * 0.07) / 0.3)
            if s < 0.1: continue
            cx = 320 + i * 110; on = i == act; h_ = 46 * s * (1.15 if on else 1)
            d.rounded_rectangle([cx - h_, 700 - h_, cx + h_, 700 + h_], 20, fill=(GREEN + (255,)) if on else (0, 0, 0, 150), outline=(255, 255, 255, 160), width=3)
            d.text((cx, 700), str(i + 1), font=FX(56 * s), fill=INK if on else WH, anchor="mm")
        outlined(ImageDraw.Draw(im), (540, 560), "WELCHER TRICK?", FX(70), WH)
        if t > 0.8:
            ot = t - 0.8; s = ease(ot / 0.3); off = (1 - back(ot / 0.4)) * 80
            d = ImageDraw.Draw(im, "RGBA")
            d.rounded_rectangle([250, 860 + off, 830, 1060 + off], 36, fill=(14, 16, 28, int(230 * s)), outline=(255, 255, 255, int(90 * s)), width=3)
            d.ellipse([280, 890 + off, 344, 954 + off], fill=(60, 160, 95, int(255 * s)))
            ans = S7.COMMENT[VID][1]; nn = int(len(ans) * ease((ot - 0.4) / 1.0))
            d.text((364, 906 + off), "du", font=FS(28), fill=(170, 174, 200, int(255 * s)), anchor="lm")
            d.text((364, 960 + off), ans[:nn], font=FX(40), fill=(255, 255, 255, int(255 * s)), anchor="lm")
            if ot > 1.6: scenes12.heart(ImageDraw.Draw(im), 790, 1020 + off, back((ot - 1.6) / 0.3), RD)
    if not cover:
        captions(im, words, gt)
        mascot(im, t, gt, (540, 800))
        # progress bar
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, H - 10, W, H], fill=(255, 255, 255, 40)); d.rectangle([0, H - 10, W * min(1, gt / sum(s[0] for s in R)), H], fill=LIME + (255,))
    # scene punch + loop flash
    z = 1.0 + 0.03 * ease(t / dur) + (0.08 * (1 - ease(t / 0.3)) if idx > 0 and not cover else 0)
    if z > 1.001:
        zw, zh = int(W * z), int(H * z); big = im.resize((zw, zh), Image.BILINEAR); ox, oy = (zw - W) // 2, (zh - H) // 2
        im = big.crop((ox, oy, ox + W, oy + H))
    if not cover:
        if idx == 0 and t < 0.25: im = Image.blend(im, Image.new("RGB", (W, H), WH), 0.6 * (1 - t / 0.25))
        if last and t > dur - 0.25: im = Image.blend(im, Image.new("RGB", (W, H), WH), 0.6 * (t - (dur - 0.25)) / 0.25)
        if 0 < idx and t < 0.15: im = Image.blend(im, Image.new("RGB", (W, H), GREEN), 0.3 * (1 - t / 0.15))
    return im

_oldf, _oldd, _oldc = S7.frame, S7.defs, S7.make_cover
def _frame(vid, *a, **k): return frame22(vid, *a, **k) if vid == VID else _oldf(vid, *a, **k)
def _defs(vid, durs):
    if vid != VID: return _oldd(vid, durs)
    return [(durs[i], "night", None, [(0, "", None)], "point") for i in range(len(S7.SCRIPTS7[VID]))]
def _cover(vid, path):
    if vid != VID: return _oldc(vid, path)
    T = S7.setup(vid); frame22(vid, 0, 2.0, T, [], cover=True).save(path)
S7.frame, S7.defs, S7.make_cover = _frame, _defs, _cover

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.2, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.75, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p22_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
