"""Reel 28 – new look: dark aurora background, glass panels, big kinetic type, story progress bar."""
import sys, os, math, random, json, glob, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes12, polish, reel2
import scenes7 as S7
import scenes2 as S2
from reel2 import W, H, FPS, ease, back, lerp, draw_character, CH_X, CH_FEET, INK
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

VID = "28_GTA6_Groesser_als_gedacht"
S7.SCRIPTS7[VID] = [
    "G T A sechs ist viel größer, als du denkst!",
    "Eins: Die Map ist rund doppelt so groß wie in G T A fünf.",
    "Zwei: Fast so groß wie G T A vier, fünf und Red Dead zwei zusammen.",
    "Drei: Vice City allein ist doppelt so groß wie Los Santos.",
    "Vier: Hunderte Innenräume, alle von Hand gebaut.",
    "Fünf: Das Spiel bewertet, wie du spielst, vom Profi bis zum Psycho.",
    "Sechs: Angeblich gibt es zweihundertein Missionen. Aber das ist nur ein Gerücht.",
    "Welcher Fakt schockt dich am meisten? Schreib die Zahl in die Kommentare!",
]
S7.DISPLAY.update({"zweihundertein": "201", "eins": "1"})
S7.COMMENT[VID] = ("WELCHER FAKT?", "Fakt 3 ist krank!")
S7.COVER[VID] = ("GTA 6", "VIEL GRÖSSER")

LIME = (198, 255, 61); VIO = (124, 92, 255); CY = (56, 217, 255); MAG = (255, 74, 163); ORG = (255, 160, 60); RD = (255, 70, 80); WH = (255, 255, 255)
ACC = [(LIME, VIO), (CY, VIO), (MAG, VIO), (MAG, CY), (ORG, MAG), (RD, VIO), (LIME, CY), (LIME, MAG)]
HEAD = [("GTA 6 IST", "VIEL GRÖSSER"), ("DIE MAP:", "2× GTA 5"), ("FAST SO GROSS WIE", "3 SPIELE ZUSAMMEN"), ("VICE CITY =", "2× LOS SANTOS"),
        ("HUNDERTE", "INNENRÄUME"), ("DAS SPIEL", "BEOBACHTET DICH"), ("201 MISSIONEN?", "NUR EIN GERÜCHT"), ("WELCHER FAKT", "SCHOCKT DICH?")]
SRC = [None, "QUELLE: EDGE-MAGAZIN / ROCKSTAR", "QUELLE: EDGE-MAGAZIN / ROCKSTAR", "LAUT ROCKSTAR-ENTWICKLER (BERICHT)", "QUELLE: EDGE-MAGAZIN / ROCKSTAR",
       "LAUT VORAB-BERICHTEN", "NICHT BESTÄTIGT", None]

def _fp(*names):
    for n in names:
        g = glob.glob(f"/usr/share/fonts/**/{n}", recursive=True)
        if g: return g[0]
    return reel2.FONTP
_FB = _fp("InterDisplay-Black.otf", "InterDisplay-ExtraBold.otf", "Inter-Black.otf", "Inter-ExtraBold.otf")
_FM = _fp("InterDisplay-SemiBold.otf", "Inter-SemiBold.otf", "Inter-Bold.otf")
@functools.lru_cache(None)
def FX(n): return ImageFont.truetype(_FB, max(6, int(n)))
@functools.lru_cache(None)
def FS(n): return ImageFont.truetype(_FM, max(6, int(n)))

# ---------------- look ----------------
_yy, _xx = np.mgrid[0:192, 0:108].astype(np.float32)
def aurora(gt, c1, c2):
    a = np.zeros((192, 108, 3), np.float32) + np.array([7, 8, 18], np.float32)
    blobs = [(62 + 34 * math.sin(gt * .5), 56 + 18 * math.cos(gt * .4), 50, c1, .30), (84 + 26 * math.cos(gt * .35 + 1), 128 + 26 * math.sin(gt * .45), 56, c2, .34),
             (12 + 18 * math.sin(gt * .3 + 2), 176, 46, c1, .16), (20 + 10 * math.cos(gt * .6), 20, 40, c2, .22)]
    for bx, by, r, c, k in blobs:
        g = np.exp(-((_xx - bx) ** 2 + (_yy - by) ** 2) / (2 * r * r)) * k
        a += g[..., None] * np.array(c, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)

def _over():
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for x in range(0, W, 90): d.line([(x, 0), (x, H)], fill=(255, 255, 255, 9), width=1)
    for y in range(0, H, 90): d.line([(0, y), (W, y)], fill=(255, 255, 255, 9), width=1)
    v = Image.new("L", (W // 8, H // 8), 0); dv = ImageDraw.Draw(v)
    dv.rectangle([0, 0, W // 8, 26], fill=150); dv.rectangle([0, H // 8 - 60, W // 8, H // 8], fill=190)
    v = v.filter(ImageFilter.GaussianBlur(14)).resize((W, H), Image.BILINEAR)
    dark = Image.new("RGBA", (W, H), (4, 4, 12, 255)); dark.putalpha(v)
    return Image.alpha_composite(o, dark)
OVER = _over()

def atext(im, x, y, txt, font, fill=WH, a=1.0, anchor="mm"):
    if a <= 0.01: return
    d = ImageDraw.Draw(im)
    if a >= 0.99: d.text((x, y), txt, font=font, fill=fill, anchor=anchor); return
    bb = d.textbbox((x, y), txt, font=font, anchor=anchor)
    m = Image.new("L", (int(bb[2] - bb[0]) + 6, int(bb[3] - bb[1]) + 6), 0)
    ImageDraw.Draw(m).text((x - bb[0] + 3, y - bb[1] + 3), txt, font=font, fill=int(255 * a), anchor=anchor)
    im.paste(fill, (int(bb[0]) - 3, int(bb[1]) - 3), m)

def gtext(im, txt, cx, cy, font, c1, c2, a=1.0, glow=True, left=None):
    l, t_, r, b = font.getbbox(txt); w, h = r - l, b - t_
    if w <= 2 or a <= 0.01: return 0
    if left is not None: cx = left + w / 2
    P = 48
    m = Image.new("L", (w + 2 * P, h + 2 * P), 0); ImageDraw.Draw(m).text((P - l, P - t_), txt, font=font, fill=int(255 * a))
    x, y = int(cx - m.width / 2), int(cy - m.height / 2)
    if glow:
        gm = m.resize((m.width // 4, m.height // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(5)).resize(m.size, Image.BILINEAR).point(lambda v: int(v * 0.55))
        im.paste(c1, (x, y), gm)
    k = np.linspace(0, 1, m.width, dtype=np.float32)[None, :, None]
    g = (np.array(c1, np.float32) * (1 - k) + np.array(c2, np.float32) * k).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(g, m.height, 0)), (x, y), m)
    return w

def chip(im, txt, cx, cy, size, bg=LIME, fg=INK, s=1.0, a=255, font=None):
    if s < 0.12: return
    f = (font or FX)(size * s); d = ImageDraw.Draw(im, "RGBA")
    w = d.textlength(txt, font=f); h = size * s * 0.95
    d.rounded_rectangle([cx - w / 2 - h * .7, cy - h, cx + w / 2 + h * .7, cy + h], h, fill=bg + (a,))
    d.text((cx, cy), txt, font=f, fill=fg, anchor="mm")

@functools.lru_cache(None)
def _glow(w, h):
    m = Image.new("L", ((w + 240) // 8, (h + 240) // 8), 0)
    ImageDraw.Draw(m).rounded_rectangle([15, 15, m.width - 15, m.height - 15], 8, fill=255)
    return m.filter(ImageFilter.GaussianBlur(9)).resize((w + 240, h + 240), Image.BILINEAR)

PB = (430, 560, 1010, 1230)
def panel(im, t, c):
    p = ease(t / 0.3); off = int((1 - back(t / 0.42)) * 110)
    x0, y0, x1, y1 = PB[0], PB[1] + off, PB[2], PB[3] + off
    im.paste(c, (x0 - 120, y0 - 120), _glow(x1 - x0, y1 - y0).point(lambda v: int(v * 0.30 * p)))
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([x0, y0, x1, y1], 48, fill=(10, 12, 28, int(205 * p)))
    D.rounded_rectangle([x0, y0, x1, y1], 48, outline=(255, 255, 255, int(70 * p)), width=3)
    D.line([(x0 + 60, y0 + 2), (x1 - 60, y0 + 2)], fill=c + (int(220 * p),), width=4)

def tile(im, box, col, a=1.0, lab=None, fs=34, fill_a=85):
    x0, y0, x1, y1 = [int(v) for v in box]
    if x1 - x0 < 10 or y1 - y0 < 10 or a <= 0.02: return
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([x0, y0, x1, y1], 18, fill=col + (int(fill_a * a),))
    for gx in range(x0 + 34, x1 - 6, 34): D.line([(gx, y0 + 5), (gx, y1 - 5)], fill=(255, 255, 255, int(22 * a)), width=1)
    for gy in range(y0 + 34, y1 - 6, 34): D.line([(x0 + 5, gy), (x1 - 5, gy)], fill=(255, 255, 255, int(22 * a)), width=1)
    D.rounded_rectangle([x0, y0, x1, y1], 18, outline=col + (int(255 * a),), width=4)
    if lab and x1 - x0 > 110: atext(im, (x0 + x1) / 2, (y0 + y1) / 2, lab, FX(fs), WH, a)

# ---------------- scenes ----------------
def h_hook(im, d, t, dur):
    cx, cy = 720, 890; D = ImageDraw.Draw(im, "RGBA")
    g = back((t - 0.75) / 0.6) if t > 0.75 else 0
    if t > 0.95:
        for k in range(3):
            ph = ((t * 0.55 + k / 3) % 1); r = 250 + ph * 260
            D.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], 40, outline=LIME + (int(110 * (1 - ph)),), width=4)
    half = 78 + (275 - 78) * g
    if g > 0.02:
        tile(im, (cx - half, cy - half, cx + half, cy + half), LIME, 1.0)
        atext(im, cx, cy + half - 62, "GTA 6", FX(70), WH, ease((t - 1.0) / 0.3))
    a = ease(t / 0.3)
    for i in range(0, 156, 26):
        for (xa, ya, xb, yb) in [(cx - 78 + i, cy - 78, cx - 78 + i + 14, cy - 78), (cx - 78 + i, cy + 78, cx - 78 + i + 14, cy + 78), (cx - 78, cy - 78 + i, cx - 78, cy - 78 + i + 14), (cx + 78, cy - 78 + i, cx + 78, cy - 78 + i + 14)]:
            D.line([(xa, ya), (xb, yb)], fill=(255, 255, 255, int(255 * a)), width=5)
    atext(im, cx, cy - 112, "DAS DENKST DU", FS(28), WH, a)
    chip(im, "SO GROSS IST ES WIRKLICH", cx, 1235, 34, LIME, INK, back((t - 1.35) / 0.4))
    return (cx, cy)

def h_x2(im, d, t, dur):
    v = 1 + ease((t - 0.35) / 1.0)
    gtext(im, f"{v:.1f}×".replace(".", ","), 720, 690, FX(170), CY, LIME)
    tile(im, (480, 990, 680, 1190), CY, ease((t - 0.1) / 0.3), "GTA 5")
    tile(im, (760, 990, 960, 1190), CY, ease((t - 0.35) / 0.3), None)
    p = ease((t - 0.65) / 0.5)
    if p > 0: tile(im, (760, 990 - 210 * p, 960, 1190 - 210 * p), CY, p, None)
    m = ease((t - 1.25) / 0.3)
    if m > 0:
        ImageDraw.Draw(im, "RGBA").rounded_rectangle([756, 776, 964, 1194], 20, fill=(10, 12, 28, int(255 * m)))
        tile(im, (760, 780, 960, 1190), LIME, m, "GTA 6", 40, 150)
    atext(im, 720, 1090, "→", FX(60), WH, ease((t - 0.3) / 0.3))
    return (860, 985)

def h_sum(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); a = ease(t / 0.3)
    D.rounded_rectangle([480, 660, 960, 1090], 24, outline=LIME + (int(255 * a),), width=5)
    chip(im, "GTA 6", 720, 625, 32, LIME, INK, back(t / 0.3))
    for (box, (dx, dy), t0, col, lab, fs) in [((492, 672, 702, 1078), (-170, 0), 0.25, CY, "GTA 5", 40), ((714, 672, 948, 900), (0, -150), 0.75, MAG, "RED DEAD 2", 28), ((714, 912, 896, 1078), (0, 150), 1.25, VIO, "GTA 4", 34)]:
        if t < t0: continue
        p = back((t - t0) / 0.45); o = 1 - p
        tile(im, (box[0] + dx * o, box[1] + dy * o, box[2] + dx * o, box[3] + dy * o), col, ease((t - t0) / 0.25), lab, fs, 150)
    atext(im, 720, 1140, "GTA 4 + GTA 5 + RED DEAD 2", FS(32), WH, ease((t - 1.6) / 0.3))
    gtext(im, "= FAST GTA 6", 720, 1188, FX(40), LIME, CY, ease((t - 1.8) / 0.3), glow=False)
    return (720, 875)

def skyline(im, x0, x1, base, seed, cols, t, hmax):
    D = ImageDraw.Draw(im, "RGBA"); rng = random.Random(seed); x = x0; i = 0
    while x < x1 - 18:
        w = min(rng.randint(30, 52), x1 - x); h = rng.uniform(.35, 1) * hmax
        g = max(0, back((t - 0.2 - i * 0.05) / 0.5)) if t > 0.2 + i * 0.05 else 0
        hh = h * g
        if hh > 8:
            D.rectangle([x, base - hh, x + w - 4, base], fill=cols[i % len(cols)] + (240,))
            for k in range(int((hh - 14) / 18)):
                wy = base - 14 - k * 18 - 9
                for wx in range(x + 6, x + w - 12, 12):
                    q = (wx * 31 + k * 17 + seed) % 9
                    if q < 5: D.rectangle([wx, wy, wx + 6, wy + 9], fill=(255, 238, 170, 230 if (q + int(t * 2 + wx)) % 5 else 90))
        x += w; i += 1

def h_city(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); base = 1040
    a = ease((t - 0.15) / 0.5)
    if a > 0:
        r = 125; sy = 880 + 60 * (1 - a)
        D.ellipse([815 - r, sy - r, 815 + r, sy + r], fill=ORG + (int(210 * a),))
        for k in range(5): D.rectangle([815 - r, sy + 10 + k * 24, 815 + r, sy + 16 + k * 24 + k * 2], fill=(10, 12, 28, 255))
    skyline(im, 475, 625, base, 3, [(74, 92, 140), (96, 116, 170)], t, 170)
    skyline(im, 665, 965, base, 8, [(214, 62, 150), (116, 86, 236), (58, 176, 226)], t, 320)
    D.line([(460, base), (980, base)], fill=(255, 255, 255, 150), width=4)
    atext(im, 550, 1076, "LOS SANTOS", FS(25), WH, ease((t - 0.5) / 0.3))
    gtext(im, "VICE CITY", 815, 1078, FX(32), MAG, CY, ease((t - 0.7) / 0.3), glow=False)
    b = ease((t - 0.9) / 0.4)
    if b > 0:
        for (xa, xb) in [(475, 625), (665, 965)]:
            xm = (xa + xb) / 2; hw = (xb - xa) / 2 * b
            D.line([(xm - hw, 1118), (xm + hw, 1118)], fill=(255, 255, 255, 200), width=4)
            D.line([(xm - hw, 1106), (xm - hw, 1130)], fill=(255, 255, 255, 200), width=4); D.line([(xm + hw, 1106), (xm + hw, 1130)], fill=(255, 255, 255, 200), width=4)
    chip(im, "1×", 550, 1172, 34, (60, 66, 100), WH, back((t - 1.0) / 0.35))
    chip(im, "2×", 815, 1172, 46, LIME, INK, back((t - 1.2) / 0.35) * (1 + 0.05 * math.sin(t * 8)))
    return (815, 850)

_ORDER = list(range(25)); random.Random(4).shuffle(_ORDER)
def h_int(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); a = ease(t / 0.3)
    D.rounded_rectangle([540, 640, 900, 1120], 14, fill=(28, 32, 60, int(245 * a)), outline=(255, 255, 255, int(90 * a)), width=3)
    D.rectangle([524, 628, 916, 648], fill=(60, 66, 104, int(255 * a)))
    lit = int(25 * ease((t - 0.3) / 1.7))
    for n_, idx in enumerate(_ORDER):
        r, c = divmod(idx, 5); x = 566 + c * 66; y = 672 + r * 66
        if r == 4 and c == 2: continue
        if n_ < lit:
            D.rounded_rectangle([x - 6, y - 6, x + 52, y + 54], 8, fill=(255, 200, 90, 50))
            D.rounded_rectangle([x, y, x + 46, y + 48], 5, fill=(255, 216, 124, 255))
            k = (idx * 7) % 3
            if k == 0: D.rectangle([x + 8, y + 26, x + 22, y + 48], fill=(120, 80, 40, 255))
            elif k == 1: D.ellipse([x + 22, y + 14, x + 36, y + 28], fill=(150, 96, 50, 255)); D.rectangle([x + 20, y + 28, x + 38, y + 48], fill=(150, 96, 50, 255))
        else:
            D.rounded_rectangle([x, y, x + 46, y + 48], 5, fill=(58, 64, 100, int(255 * a)))
    p = ease((t - 0.9) / 0.6)
    D.rectangle([680, 1010, 760, 1120], fill=(255, 216, 124, int(255 * max(p, 0.0))) if p > 0 else (58, 64, 100, int(255 * a)))
    if p > 0: D.polygon([(680, 1120), (760, 1120), (800, 1150), (640, 1150)], fill=(255, 216, 124, int(90 * p)))
    D.rectangle([680, 1010, 680 + 80 * (1 - p * 0.8), 1120], fill=(96, 70, 54, int(255 * a)))
    D.ellipse([680 + 80 * (1 - p * 0.8) - 16, 1062, 680 + 80 * (1 - p * 0.8) - 6, 1072], fill=(240, 200, 90, int(255 * a)))
    chip(im, "ALLE VON HAND GEBAUT", 720, 1185, 30, LIME, INK, back((t - 1.3) / 0.4))
    return (720, 860)

def _bar(w, h):
    k = np.linspace(0, 1, w, dtype=np.float32)
    stops = np.array([CY, LIME, ORG, RD], np.float32); pos = k * 3; i = np.clip(pos.astype(int), 0, 2); f = (pos - i)[:, None]
    row = (stops[i] * (1 - f) + stops[i + 1] * f).astype(np.uint8)
    im = Image.fromarray(np.repeat(row[None], h, 0)); m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=255)
    return im, m, row
_BAR = _bar(460, 34)

def h_profile(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); a = ease(t / 0.3)
    D.ellipse([648, 620, 792, 764], fill=(30, 34, 62, int(255 * a)), outline=RD + (int(255 * a),), width=5)
    D.ellipse([694, 648, 746, 700], fill=(150, 156, 190, int(255 * a))); D.chord([664, 708, 776, 800], 198, 342, fill=(150, 156, 190, int(255 * a)))
    sy = 692 + 56 * math.sin(t * 3.2); hw = math.sqrt(max(0, 70 ** 2 - (sy - 692) ** 2))
    D.line([(720 - hw, sy), (720 + hw, sy)], fill=LIME + (220,), width=4)
    if int(t * 2.5) % 2 == 0: D.ellipse([498, 806, 520, 828], fill=RD + (255,))
    atext(im, 735, 817, "CRIMINAL PROFILE", FX(36), WH, ease((t - 0.2) / 0.3))
    b = ease((t - 0.35) / 0.4)
    if b > 0:
        bi, bm, row = _BAR
        im.paste(bi, (490, 893), bm.point(lambda v: int(v * b)))
        p = 0.5 - 0.45 * math.cos(max(0, t - 0.7) * 1.9); kx = 490 + 460 * p; col = tuple(int(v) for v in row[min(459, int(p * 459))])
        D = ImageDraw.Draw(im, "RGBA")
        D.ellipse([kx - 44, 866, kx + 44, 954], fill=col + (70,))
        D.ellipse([kx - 28, 882, kx + 28, 938], fill=(255, 255, 255, 255), outline=(10, 12, 28, 255), width=6)
        D.ellipse([kx - 10, 900, kx + 10, 920], fill=col + (255,))
    atext(im, 490, 985, "PROFI", FX(32), CY, b, "lm"); atext(im, 950, 985, "PSYCHO", FX(32), RD, b, "rm")
    chip(im, "TRACKT, WIE DU SPIELST", 720, 1085, 30, (255, 255, 255), INK, back((t - 1.1) / 0.4))
    chip(im, "ZU BÖSE? KEIN ZURÜCK!", 720, 1165, 30, RD, WH, back((t - 1.8) / 0.4) * (1 + 0.04 * math.sin(t * 9)))
    return (720, 912)

def h_201(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); q = dur * 0.68
    v = int(201 * ease((t - 0.2) / 1.3)); dim = 1 - 0.55 * ease((t - q) / 0.2)
    gtext(im, str(v), 720, 730, FX(215), LIME, CY, dim, glow=dim > 0.9)
    atext(im, 720, 868, "MISSIONEN", FS(40), WH, ease((t - 0.2) / 0.3) * dim)
    D = ImageDraw.Draw(im, "RGBA")
    for i in range(201):
        r, c = divmod(i, 23); x = 489 + c * 21; y = 930 + r * 22
        D.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(LIME + (int(255 * dim),)) if i < v else (255, 255, 255, 40))
    if t > q:
        e = ease((t - q) / 0.18); s = 1 + 1.3 * (1 - e)
        L = Image.new("RGBA", (560, 190), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
        dl.rounded_rectangle([8, 8, 552, 182], 26, fill=(20, 8, 14, 235), outline=RD, width=12)
        dl.text((280, 95), "GERÜCHT", font=FX(104), fill=RD, anchor="mm")
        L = L.rotate(11, expand=True, resample=Image.BICUBIC)
        L = L.resize((int(L.width * s), int(L.height * s)), Image.BILINEAR)
        if e < 1: L.putalpha(L.split()[3].point(lambda z: int(z * e)))
        sh_ = math.sin(t * 70) * 10 * max(0, 1 - (t - q) / 0.35)
        im.paste(L, (int(720 - L.width / 2 + sh_), int(900 - L.height / 2)), L)
        chip(im, "ROCKSTAR NENNT KEINE ZAHL", 720, 1180, 28, (255, 255, 255), INK, back((t - q - 0.5) / 0.4))
    return (720, 760)

def h_cta(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); act = int(t * 2.4) % 6
    for i in range(6):
        s = back((t - i * 0.07) / 0.3)
        if s < 0.1: continue
        cx = 560 + (i % 3) * 160; cy = 660 + (i // 3) * 150; on = i == act; h = 62 * s * (1.13 if on else 1)
        D.rounded_rectangle([cx - h, cy - h, cx + h, cy + h], 26, fill=(LIME + (255,)) if on else (255, 255, 255, 28), outline=(255, 255, 255, 110), width=3)
        D.text((cx, cy), str(i + 1), font=FX(74 * s), fill=INK if on else WH, anchor="mm")
    return (720, 735)

def comment13(im, ot):
    D = ImageDraw.Draw(im, "RGBA"); q, ans = S7.COMMENT[VID]; s = ease(ot / 0.3); off = (1 - back(ot / 0.4)) * 80
    D.rounded_rectangle([450, 900 + off, 990, 1120 + off], 36, fill=(10, 12, 28, int(225 * s)), outline=(255, 255, 255, int(90 * s)), width=3)
    D.ellipse([480, 930 + off, 548, 998 + off], fill=(60, 160, 95, int(255 * s)))
    atext(im, 566, 948 + off, "du", FS(28), (170, 174, 200), s, "lm")
    n = int(len(ans) * ease((ot - 0.5) / 1.0))
    atext(im, 566, 1000 + off, ans[:n] + ("|" if (int(ot * 3) % 2 == 0 and n < len(ans)) else ""), FX(40), WH, s, "lm")
    if ot > 1.7: scenes12.heart(ImageDraw.Draw(im), 940, 1072, back((ot - 1.7) / 0.3) * (1 + 0.1 * math.sin(ot * 9)), RD)
    b = back((ot - 0.3) / 0.35) * (1 + 0.04 * math.sin(ot * 9))
    if b > 0.12:
        hw, hh = 170 * b, 44 * b
        k = np.linspace(0, 1, int(2 * hw), dtype=np.float32)[None, :, None]
        g = (np.array(LIME, np.float32) * (1 - k) + np.array(CY, np.float32) * k).astype(np.uint8)
        gi = Image.fromarray(np.repeat(g, int(2 * hh), 0)); m = Image.new("L", gi.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, gi.width - 1, gi.height - 1], int(hh), fill=255)
        im.paste(gi, (int(720 - hw), int(1205 - hh)), m)
        ImageDraw.Draw(im).text((720, 1205), "+ FOLGEN", font=FX(42 * b), fill=INK, anchor="mm")
    return (700, 1010)

FACTLBL = "FAKT"; TOP0 = "GTA 6 · 6 FAKTEN"; TOPLAST = "DEINE MEINUNG"; EXTRA = None
RUMOR = 6; COVER_CHIP = "6 FAKTEN IN 30 SEKUNDEN"
SC = [h_hook, h_x2, h_sum, h_city, h_int, h_profile, h_201, h_cta]

# ---------------- captions ----------------
def caption13(fr, words, gt):
    groups = []; cur = []
    for i, (a, b, w) in enumerate(words):
        cur.append(i)
        if len(cur) == 3 or w[-1] in ".!?:": groups.append(cur); cur = []
    if cur: groups.append(cur)
    act = None
    for i, (a, b, w) in enumerate(words):
        if a <= gt < b + 0.05: act = i
    if act is None:
        prev = [i for i, (a, b, w) in enumerate(words) if b <= gt]
        if not prev or gt - words[prev[-1]][1] > 0.35: return
        act = prev[-1]
    g = next(g for g in groups if act in g)
    D = ImageDraw.Draw(fr, "RGBA"); f = FX(62)
    texts = [words[i][2] for i in g]
    widths = [D.textlength(x, font=f) for x in texts]; total = sum(widths) + 22 * (len(texts) - 1)
    if total > 640:
        f = FX(int(62 * 640 / total)); widths = [D.textlength(x, font=f) for x in texts]; total = sum(widths) + 22 * (len(texts) - 1)
    x = 690 - total / 2; y = 1395
    D.rounded_rectangle([x - 34, y - 60, x + total + 34, y + 60], 34, fill=(6, 7, 16, 185), outline=(255, 255, 255, 50), width=2)
    for i, tx, w in zip(g, texts, widths):
        on = i == act
        pop = 1 + 0.14 * (1 - ease((gt - words[i][0]) / 0.15)) if on else 1
        D.text((x + w / 2, y), tx, font=f if pop == 1 else FX(int(f.size * pop)), fill=LIME if on else WH, anchor="mm")
        if on: D.rounded_rectangle([x, y + 40, x + w, y + 46], 3, fill=LIME + (255,))
        x += w + 22

# ---------------- frame ----------------
def fit(font, txt, size, maxw):
    f = font(size); w = f.getlength(txt)
    return f if w <= maxw else font(int(size * maxw / w))

def frame13(vid, idx, t, T, words, cover=False, no_sticker=False):
    R = S2.R[vid]; dur = R[idx][0]; n = len(R); pose0 = R[idx][4]
    gt = sum(s[0] for s in R[:idx]) + t
    c1, c2 = ACC[idx]
    fr = aurora(gt, c1, c2); fr.paste(OVER, (0, 0), OVER)
    D = ImageDraw.Draw(fr, "RGBA")
    for k in range(6): D.ellipse([CH_X - 250 + k * 30, CH_FEET - 44 + k * 6, CH_X + 250 - k * 30, CH_FEET + 56 - k * 6], fill=c1 + (9,))
    tt = t + (0.5 if idx == 0 else 0)
    last = idx == n - 1
    if 0 < idx < n - 1: panel(fr, tt, c1)
    target = SC[idx](fr, ImageDraw.Draw(fr), tt, dur)
    if last and not cover and t > 0.9: target = comment13(fr, t - 0.9)
    pose = pose0
    if pose0 == "wave" and t > 1.2: pose = "point"
    draw_character(fr, t, gt, pose, target)
    # headline
    l1, l2 = HEAD[idx]
    p1 = ease(tt / 0.3); d2 = (dur * 0.68 + 0.1) if idx == RUMOR else 0.14; p2 = ease((tt - d2) / 0.3)
    atext(fr, 64, 300 + (1 - p1) * 50, l1, fit(FX, l1, 76, 950), WH, p1, "lm")
    if p2 > 0: gtext(fr, l2, 0, 412 + (1 - p2) * 50, fit(FX, l2, 112, 950), c1, c2 if idx != RUMOR else ORG, p2, left=64)
    if not cover:
        D = ImageDraw.Draw(fr, "RGBA")
        sw = (W - 120 - (n - 1) * 10) / n
        for i in range(n):
            x0 = 60 + i * (sw + 10)
            D.rounded_rectangle([x0, 118, x0 + sw, 128], 5, fill=(255, 255, 255, 60))
            f_ = 1 if i < idx else (t / dur if i == idx else 0)
            if f_ > 0.03: D.rounded_rectangle([x0, 118, x0 + sw * f_, 128], 5, fill=(255, 255, 255, 240))
        D.ellipse([64, 163, 84, 183], fill=LIME + (255,))
        D.text((96, 173), "ZOCKWISSEN", font=FS(30), fill=(255, 255, 255, 230), anchor="lm")
        D.text((1016, 173), TOP0 if idx == 0 else (TOPLAST if last else f"{FACTLBL} {idx}/{len(SC) - 2}"), font=FS(30), fill=(255, 255, 255, 230), anchor="rm")
        if SRC[idx]:
            s = ease((tt - 0.5) / 0.3)
            if s > 0.02:
                f = FS(25); w = D.textlength(SRC[idx], font=f)
                D.rounded_rectangle([720 - w / 2 - 44, 1262, 720 + w / 2 + 26, 1308], 23, fill=(255, 255, 255, int(26 * s)), outline=(255, 255, 255, int(70 * s)), width=2)
                D.ellipse([720 - w / 2 - 28, 1279, 720 - w / 2 - 16, 1291], fill=(RD if idx == RUMOR else LIME) + (int(255 * s),))
                D.text((720 - w / 2 - 4, 1285), SRC[idx], font=f, fill=(255, 255, 255, int(230 * s)), anchor="lm")
        if EXTRA: EXTRA(fr, idx, t, dur)
        caption13(fr, words, gt)
    else:
        chip(fr, COVER_CHIP, 690, 1400, 40, WH, INK)
    z = 1.0 + 0.05 * ease(t / dur) + (0.10 * (1 - ease(t / 0.35)) if idx > 0 and not cover else 0)
    zw, zh = int(W * z), int(H * z)
    big = fr.resize((zw, zh), Image.BILINEAR); ox = (zw - W) // 2; oy = (zh - H) // 2
    fr = big.crop((ox, oy, ox + W, oy + H))
    if idx > 0 and t < 0.2 and not cover: fr = Image.blend(fr, Image.new("RGB", (W, H), c1), 0.4 * (1 - t / 0.2))
    return Image.blend(fr, Image.merge("RGB", [polish.grain(int(gt * 30))] * 3), 0.035)

_oldf, _oldd, _oldc = S7.frame, S7.defs, S7.make_cover
def _frame(vid, *a, **k): return frame13(vid, *a, **k) if vid == VID else _oldf(vid, *a, **k)
def _defs(vid, durs):
    if vid != VID: return _oldd(vid, durs)
    return [(durs[i], "night", SC[i], [(0, HEAD[i][1], None)], "wave" if i == 0 else "point") for i in range(len(SC))]
def _cover(vid, path):
    if vid != VID: return _oldc(vid, path)
    T = S7.setup(vid); frame13(vid, 0, 2.2, T, [], cover=True).save(path)
S7.frame, S7.defs, S7.make_cover = _frame, _defs, _cover

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.8, 0.9, 0.8, 0.8, 0.8, 0.85, 0.9]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, 0.0, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p13_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
