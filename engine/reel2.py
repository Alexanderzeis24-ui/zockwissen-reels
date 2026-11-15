import math, random, subprocess, sys, os, functools
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make as M
import videos as V
import mascot

W, H, FPS = 1080, 1920, 30
OUT = os.path.join(HERE, "teil2")
FONTP = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

@functools.lru_cache(maxsize=512)
def F(n): return ImageFont.truetype(FONTP, max(6, int(n)))
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def sh(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)
def lerp(a, b, p): return a + (b - a) * p
INK = (22, 20, 34)
YEL = (255, 205, 60); PINK = (240, 80, 130); CYAN = (60, 200, 230); GRN = (60, 185, 105); RED = (230, 60, 70)

# ---------------- backgrounds ----------------
THEMES = {
    "purple": ((70, 40, 140), (230, 110, 150), (90, 60, 160)),
    "sky":    ((90, 150, 230), (180, 220, 250), (120, 170, 230)),
    "night":  ((20, 24, 60), (70, 50, 120), (50, 50, 100)),
    "sunset": ((90, 50, 150), (255, 150, 100), (120, 70, 150)),
    "mint":   ((40, 130, 120), (150, 220, 190), (70, 160, 140)),
    "gold":   ((60, 30, 90), (200, 120, 60), (90, 50, 110)),
    "ocean":  ((20, 90, 160), (110, 200, 230), (40, 120, 180)),
}
_bg = {}
def bg(theme):
    if theme in _bg: return _bg[theme]
    a, b, floor = THEMES[theme]
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(x + (z - x) * t) for x, z in zip(a, b)))
    # floor / stage
    d.rectangle([0, 1490, W, H], fill=floor)
    d.rectangle([0, 1490, W, 1506], fill=sh(floor, 1.35))
    for x in range(-200, W + 200, 160):
        d.line([(x, 1506), (x - 260, H)], fill=sh(floor, 0.9), width=4)
    _bg[theme] = im
    return im

def particles(d, gt, theme):
    a, b, _ = THEMES[theme]
    rnd = random.Random(42)
    for i in range(22):
        x = (rnd.randrange(W) + math.sin(gt * 0.6 + i) * 30) % W
        y = (rnd.randrange(1500) - gt * rnd.uniform(15, 40)) % 1480
        r = rnd.randrange(4, 12)
        c = sh(tuple(int(lerp(p, q, y / H)) for p, q in zip(a, b)), 1.35)
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)

# ---------------- UI helpers ----------------
def card(d, b, fill=(255, 255, 255), r=40, sh_off=14):
    x0, y0, x1, y1 = b
    d.rounded_rectangle([x0 + sh_off, y0 + sh_off, x1 + sh_off, y1 + sh_off], r, fill=INK)
    d.rounded_rectangle(b, r, fill=fill, outline=INK, width=6)

def label(d, txt, cx, cy, size, fill=(255, 255, 255), stroke=8, anchor="mm"):
    d.text((cx, cy), txt, font=F(size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=INK)

def pill(d, txt, cx, cy, size, bgc=YEL, fg=INK, s=1.0):
    if s <= 0.05: return
    f = F(size * s); w = d.textlength(txt, font=f)
    h = size * 1.5 * s
    d.rounded_rectangle([cx - w / 2 - 26 * s + 6, cy - h / 2 + 8, cx + w / 2 + 26 * s + 6, cy + h / 2 + 8], int(h / 2), fill=INK)
    d.rounded_rectangle([cx - w / 2 - 26 * s, cy - h / 2, cx + w / 2 + 26 * s, cy + h / 2], int(h / 2), fill=bgc, outline=INK, width=5)
    d.text((cx, cy + 2), txt, font=f, fill=fg, anchor="mm")

def star(d, x, y, r, col=(255, 245, 190)):
    d.polygon([(x, y - r), (x + r * .3, y - r * .3), (x + r, y), (x + r * .3, y + r * .3), (x, y + r), (x - r * .3, y + r * .3), (x - r, y), (x - r * .3, y - r * .3)], fill=col)

def sparkle_field(d, t, box, n=10, seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.randrange(box[0], box[2]); y = rnd.randrange(box[1], box[3])
        a = (math.sin(t * 5 + i * 1.9) + 1) / 2
        star(d, x, y, 6 + 18 * a)

def confetti(d, t, t0, box=(400, 480, 1000, 1400), n=50, seed=3):
    if t < t0: return
    rnd = random.Random(seed)
    for i in range(n):
        x0 = rnd.randrange(box[0], box[2]); sp = rnd.uniform(220, 480)
        y = box[1] - 60 + (t - t0) * sp + rnd.randrange(-250, 0)
        if y < box[1] - 40 or y > box[3]: continue
        a = t * 6 + i; col = rnd.choice([PINK, CYAN, YEL, GRN, (180, 120, 255)])
        x = x0 + math.sin(t * 3 + i) * 20
        d.polygon([(x + 14 * math.cos(a), y + 7 * math.sin(a)), (x - 14 * math.cos(a), y - 7 * math.sin(a)),
                   (x - 10 * math.cos(a) + 5, y + 10), (x + 5, y + 12)], fill=col)

def check_icon(d, cx, cy, s, col=GRN):
    if s <= 0.05: return
    r = 40 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=INK, width=4)
    d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .4), (cx + r * .5, cy - r * .4)], fill="white", width=max(2, int(11 * s)), joint="curve")

def x_icon(d, cx, cy, s):
    if s <= 0.05: return
    r = 40 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=INK, width=4)
    w = max(2, int(11 * s)); k = r * .4
    d.line([(cx - k, cy - k), (cx + k, cy + k)], fill="white", width=w); d.line([(cx + k, cy - k), (cx - k, cy + k)], fill="white", width=w)

def countup(t, t0, dur, target): return target * ease((t - t0) / dur)

# ---------------- word sticker ----------------
_stk = {}
def sticker(word, col):
    k = (word, col)
    if k in _stk: return _stk[k]
    size = 120
    while True:
        bb = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), word, font=F(size), stroke_width=12)
        if bb[2] - bb[0] <= 860 or size < 50: break
        size -= 4
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 44
    im = Image.new("RGBA", (tw + 2 * pad + 30, th + 2 * pad + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([16, 16, tw + 2 * pad + 16, th + 2 * pad + 16], 34, fill=INK)
    d.rounded_rectangle([0, 0, tw + 2 * pad, th + 2 * pad], 34, fill=col, outline=INK, width=7)
    d.text((pad - bb[0], pad - bb[1]), word, font=F(size), fill="white", stroke_width=12, stroke_fill=INK)
    _stk[k] = im
    return im

# ---------------- character ----------------
SKIN = (232, 190, 152); HOOD = (60, 160, 95); JEANS = (50, 80, 150); HAIR = (60, 40, 28)
CH_X, CH_FEET = 205, 1520
L1, L2 = 170, 155

def _arm(d, sx, sy, a1, a2, finger=False, thumb=False):
    ex, ey = sx + L1 * math.cos(a1), sy + L1 * math.sin(a1)
    hx, hy = ex + L2 * math.cos(a2), ey + L2 * math.sin(a2)
    d.line([(sx, sy), (ex, ey)], fill=HOOD, width=64)
    d.line([(ex, ey), (hx, hy)], fill=HOOD, width=58)
    for (x, y, r, c) in [(sx, sy, 32, HOOD), (ex, ey, 30, HOOD)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=c)
    d.ellipse([hx - 30, hy - 30, hx + 30, hy + 30], fill=sh(HOOD, 0.85))  # cuff
    px, py = hx + 30 * math.cos(a2), hy + 30 * math.sin(a2)
    d.ellipse([px - 38, py - 38, px + 38, py + 38], fill=SKIN)
    if finger:
        fx, fy = px + 70 * math.cos(a2), py + 70 * math.sin(a2)
        d.line([(px, py), (fx, fy)], fill=SKIN, width=26)
        d.ellipse([fx - 13, fy - 13, fx + 13, fy + 13], fill=SKIN)
    if thumb:
        d.rounded_rectangle([px - 13, py - 85, px + 13, py], 13, fill=SKIN)
    return (px, py)

def draw_character(fr, t, gt, pose, target):
    S2 = 2  # supersample
    cw, chh = 1200, 1560
    im = Image.new("RGBA", (cw, chh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    jump = -abs(math.sin(math.pi * min(1, t / 0.4))) * 60 if t < 0.4 else 0
    b = math.sin(gt * 3) * 7 + jump * 0.0
    ox = CH_X - cw / (2 * S2); oy = CH_FEET - 1470 / S2 + jump / S2
    cx = cw / 2
    # legs + shoes
    d.rounded_rectangle([cx - 80, 1000 + b, cx - 10, 1450], 32, fill=JEANS)
    d.rounded_rectangle([cx + 10, 1000 + b, cx + 80, 1450], 32, fill=sh(JEANS, 0.88))
    d.rounded_rectangle([cx - 125, 1405, cx - 5, 1475], 32, fill=(245, 245, 245), outline=(200, 200, 205), width=4)
    d.rounded_rectangle([cx + 5, 1405, cx + 125, 1475], 32, fill=(245, 245, 245), outline=(200, 200, 205), width=4)
    # torso
    d.rounded_rectangle([cx - 140, 640 + b, cx + 140, 1065 + b], 100, fill=HOOD)
    d.rounded_rectangle([cx + 60, 670 + b, cx + 140, 1050 + b], 60, fill=sh(HOOD, 0.88))
    d.rounded_rectangle([cx - 85, 900 + b, cx + 85, 995 + b], 30, fill=sh(HOOD, 0.85))
    d.line([(cx - 35, 680 + b), (cx - 42, 830 + b)], fill=(245, 245, 245), width=12)
    d.line([(cx + 35, 680 + b), (cx + 42, 830 + b)], fill=(245, 245, 245), width=12)
    d.chord([cx - 110, 600 + b, cx + 110, 740 + b], 0, 180, fill=sh(HOOD, 0.7))
    d.rectangle([cx - 30, 590 + b, cx + 30, 650 + b], fill=sh(SKIN, 0.88))
    # head
    hb = b + math.sin(gt * 2.1) * 4
    hx = cx + math.sin(gt * 1.3) * 5
    d.ellipse([hx - 150, 275 + hb, hx + 150, 610 + hb], fill=SKIN)
    d.chord([hx - 160, 250 + hb, hx + 160, 530 + hb], 180, 360, fill=HAIR)
    d.polygon([(hx - 160, 400 + hb), (hx - 90, 345 + hb), (hx, 365 + hb), (hx + 90, 340 + hb), (hx + 160, 400 + hb), (hx + 155, 330 + hb), (hx - 155, 330 + hb)], fill=HAIR)
    d.polygon([(hx - 70, 265 + hb), (hx - 20, 215 + hb), (hx + 20, 262 + hb)], fill=HAIR)
    d.polygon([(hx + 5, 262 + hb), (hx + 55, 210 + hb), (hx + 90, 270 + hb)], fill=HAIR)
    # eyes look at target
    sxw, syw = ox + hx / S2, oy + (450 + hb) / S2
    vx, vy = target[0] - sxw, target[1] - syw; n = math.hypot(vx, vy) or 1
    lx, ly = vx / n * 11, vy / n * 9
    blink = (gt % 3.4) < 0.12
    mouth = mascot.mouth_at(gt)
    for ex in (-58, 58):
        if blink:
            d.line([(hx + ex - 34, 458 + hb), (hx + ex + 34, 458 + hb)], fill=INK, width=10)
        else:
            d.ellipse([hx + ex - 34, 418 + hb, hx + ex + 34, 498 + hb], fill="white")
            d.ellipse([hx + ex - 18 + lx, 440 + hb + ly, hx + ex + 18 + lx, 476 + hb + ly], fill=INK)
            d.ellipse([hx + ex - 6 + lx, 446 + hb + ly, hx + ex + 4 + lx, 456 + hb + ly], fill="white")
        d.line([(hx + ex - 40, 395 + hb - mouth * 4), (hx + ex + 36, 388 + hb - mouth * 4)], fill=HAIR, width=13)
    if mouth == 0:
        d.arc([hx - 55, 500 + hb, hx + 55, 565 + hb], 15, 165, fill=(150, 70, 60), width=11)
    else:
        mh = [0, 28, 50, 70][mouth]
        d.chord([hx - 50, 525 + hb - 6, hx + 50, 525 + hb + mh], 0, 180, fill=(110, 40, 45))
        d.rectangle([hx - 36, 520 + hb, hx + 36, 530 + hb], fill=(250, 250, 250))
    d.ellipse([hx - 165, 420 + hb, hx - 140, 480 + hb], fill=sh(SKIN, 0.9)); d.ellipse([hx + 140, 420 + hb, hx + 165, 480 + hb], fill=sh(SKIN, 0.9))
    # headset
    d.arc([hx - 180, 250 + hb, hx + 180, 620 + hb], 197, 343, fill=(35, 35, 45), width=30)
    for s_ in (-1, 1):
        x0 = hx + s_ * 170
        d.rounded_rectangle([x0 - 35, 395 + hb, x0 + 35, 505 + hb], 26, fill=(35, 35, 45))
        d.rounded_rectangle([x0 - 22, 410 + hb, x0 + 22, 490 + hb], 18, fill=(230, 60, 90))
    d.line([(hx - 170, 495 + hb), (hx - 140, 555 + hb), (hx - 70, 562 + hb)], fill=(35, 35, 45), width=11, joint="curve")
    d.ellipse([hx - 80, 552 + hb, hx - 58, 574 + hb], fill=(35, 35, 45))
    # arms
    shL, shR = (cx - 130, 690 + b), (cx + 130, 690 + b)
    rest = (math.radians(100), math.radians(95))
    restR = (math.radians(80), math.radians(85))
    # pointing angle in world coords
    wsx, wsy = ox + shR[0] / S2, oy + shR[1] / S2
    ang = math.atan2(target[1] - wsy, target[0] - wsx)
    ang = max(math.radians(-85), min(math.radians(50), ang))
    wig = math.sin(gt * 4) * 0.05
    if pose == "wave":
        _arm(d, *shL, *rest)
        _arm(d, *shR, math.radians(-55), math.radians(-100) + math.sin(gt * 11) * 0.45)
    elif pose == "cheer":
        _arm(d, *shL, math.radians(-120) + wig, math.radians(-100) + wig)
        _arm(d, *shR, math.radians(-60) - wig, math.radians(-80) - wig, thumb=True)
    else:
        p = ease((t - 0.15) / 0.35)
        _arm(d, *shL, rest[0] + math.sin(gt * 2) * 0.05, rest[1])
        a1 = lerp(restR[0], ang + 0.22, p) + wig; a2 = lerp(restR[1], ang, p) + wig * 0.5
        _arm(d, *shR, a1, a2, finger=p > 0.5)
    small = im.resize((cw // S2, chh // S2), Image.LANCZOS)
    # shadow
    dd = ImageDraw.Draw(fr)
    sw = 130 * (1 + jump / 300)
    dd.ellipse([CH_X - sw, CH_FEET - 18, CH_X + sw, CH_FEET + 18], fill=(0, 0, 0) if False else sh(fr.getpixel((CH_X, CH_FEET + 30)), 0.7))
    fr.paste(small, (int(ox), int(oy)), small)

# ---------------- map ----------------
def leonida_map(d, t, cx, cy, z, labels=None, land=(110, 175, 95)):
    P = lambda p: (cx + (p[0] - 500) * z, cy + (p[1] - 690) * z)
    pts = [P(p) for p in V.FLORIDA]
    d.polygon([(x + 12, y + 14) for x, y in pts], fill=INK)
    d.polygon(pts, fill=land, outline=INK, width=5)
    for k in range(5):
        x, y = P((700 + k * 32, 1060 + (k % 2) * 16))
        d.ellipse([x - 16 * z * 1.4, y - 8 * z * 1.4, x + 16 * z * 1.4, y + 8 * z * 1.4], fill=(225, 205, 150), outline=INK, width=2)
    return P

# ---------------- outro ----------------
def outro(d, fr, ot, extra=None):
    s = back(ot / 0.4) * (1 + 0.05 * math.sin(ot * 9))
    ps = ease(ot / 0.3)
    if ps > 0.02:
        card(d, (440, 1110 - 170 * ps, 980, 1110 + 170 * ps), (40, 30, 80))
    pill(d, "ZOCKWISSEN", 690, 1040, 46, (255, 255, 255), INK, back((ot - 0.15) / 0.4))
    pill(d, "+ FOLGEN", 690, 1180, 70, PINK, (255, 255, 255), s)
    if ot > 0.9:
        k = (ot - 0.9) % 1.2
        hx, hy = 760 + 40 * (1 - ease(k / 0.4)), 1215 + 40 * (1 - ease(k / 0.4))
        if k > 0.4 and k < 0.8:
            r = 30 + (k - 0.4) * 200
            d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=(255, 255, 255), width=5)
        d.polygon([(hx, hy), (hx, hy + 70), (hx + 18, hy + 54), (hx + 32, hy + 84), (hx + 44, hy + 78), (hx + 30, hy + 50), (hx + 54, hy + 48)], fill="white", outline=INK)
    return (690, 1180)

AREA = (420, 520, 1000, 1340)  # main graphic area
def main_card(d, fill=(255, 255, 255), b=(420, 540, 1000, 1180)):
    card(d, b, fill)
    return b
