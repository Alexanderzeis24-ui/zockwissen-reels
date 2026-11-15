import math, random, subprocess, sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make as M
import mascot
from make import (W, H, FPS, SCENE_H, font, ease, back, shade, box, cloud, palm, person,
                  calendar, xmark, check, car, DAY, SUNSET, NIGHT, grad, ground, word_img, WALL)

OUT = M.OUT
GREEN = (70, 160, 90)

# ---------------- primitives ----------------
def bill_stack(d, x, y, w, h, col=(95, 170, 105)):
    box(d, x, y - h, w, h, 70, col)
    for yy in range(int(y - h + 10), int(y), 14):
        d.line([(x, yy), (x + w, yy)], fill=shade(col, 0.85), width=3)
    d.rectangle([x + w * 0.3, y - h, x + w * 0.42, y], fill=(235, 225, 190))

def bill(d, cx, cy, a, s=1.0):
    w, h = 110 * s, 55 * s
    ca, sa = math.cos(a), math.sin(a)
    pts = [(cx + ca * px - sa * py, cy + sa * px + ca * py) for px, py in [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]]
    d.polygon(pts, fill=(110, 185, 115), outline=(60, 120, 70))
    d.ellipse([cx - 12 * s, cy - 12 * s, cx + 12 * s, cy + 12 * s], fill=(70, 140, 80))

_tag = {}
def tag_img(text, col=(250, 205, 60)):
    k = (text, col)
    if k in _tag: return _tag[k]
    im = Image.new("RGBA", (520, 300), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(120, 20), (500, 20), (500, 280), (120, 280), (20, 150)], fill=col, outline=(40, 40, 40), width=8)
    d.ellipse([70, 130, 110, 170], fill=(0, 0, 0, 0), outline=(40, 40, 40), width=6)
    d.text((310, 150), text, font=font(88), fill=(30, 30, 30), anchor="mm")
    _tag[k] = im
    return im

def paste_rot(im, src, cx, cy, ang, s=1.0):
    if s <= 0.02: return
    r = src.resize((max(1, int(src.width * s)), max(1, int(src.height * s)))).rotate(ang, expand=True, resample=Image.BICUBIC)
    im.paste(r, (int(cx - r.width / 2), int(cy - r.height / 2)), r)

def game_case(d, x, y, w, h, col, label, s=1.0):
    if s <= 0.02: return
    w, h = w * s, h * s
    box(d, x, y - h, w, h, 30, col)
    d.rectangle([x, y - h, x + w, y - h + 40 * s], fill=shade(col, 0.7))
    d.rectangle([x + 25 * s, y - h + 70 * s, x + w - 25 * s, y - 50 * s], fill=shade(col, 1.35))
    d.text((x + w / 2, y - h / 2), label, font=font(max(8, int(58 * s))), fill=(30, 30, 30), anchor="mm")

def phone(d, cx, cy, s, count_text, sub="Aufrufe"):
    if s < 0.1: return
    w, h = 380 * s, 700 * s
    d.rounded_rectangle([cx - w/2, cy - h/2, cx + w/2, cy + h/2], int(50 * s), fill=(25, 25, 30))
    d.rounded_rectangle([cx - w/2 + 18*s, cy - h/2 + 18*s, cx + w/2 - 18*s, cy + h/2 - 18*s], int(36 * s), fill=(235, 238, 245))
    d.rectangle([cx - w/2 + 18*s, cy - h/2 + 90*s, cx + w/2 - 18*s, cy - h/2 + 290*s], fill=(40, 40, 50))
    d.polygon([(cx - 30*s, cy - h/2 + 150*s), (cx - 30*s, cy - h/2 + 230*s), (cx + 40*s, cy - h/2 + 190*s)], fill=(230, 60, 60))
    d.text((cx, cy + 20*s), count_text, font=font(max(8, int(64 * s))), fill=(30, 30, 30), anchor="mm")
    d.text((cx, cy + 90*s), sub, font=font(max(8, int(36 * s))), fill=(110, 110, 120), anchor="mm")
    for k in range(3):
        d.rounded_rectangle([cx - w/2 + 50*s, cy + (160 + k*55)*s, cx + w/2 - 50*s - k*40*s, cy + (190 + k*55)*s], 10, fill=(205, 208, 215))

def trophy(d, cx, cy, s):
    if s <= 0.02: return
    g = (245, 195, 50)
    d.chord([cx - 150*s, cy - 200*s, cx + 150*s, cy + 120*s], 0, 180, fill=g)
    d.rectangle([cx - 150*s, cy - 200*s, cx + 150*s, cy - 40*s], fill=g)
    d.ellipse([cx - 220*s, cy - 170*s, cx - 110*s, cy - 40*s], outline=g, width=int(26*s))
    d.ellipse([cx + 110*s, cy - 170*s, cx + 220*s, cy - 40*s], outline=g, width=int(26*s))
    d.rectangle([cx - 30*s, cy + 110*s, cx + 30*s, cy + 200*s], fill=shade(g, 0.85))
    box(d, cx - 120*s, cy + 200*s, 240*s, 70*s, 40*s, (120, 80, 50))
    d.polygon([(cx - 110*s, cy - 180*s), (cx - 60*s, cy - 180*s), (cx - 90*s, cy + 40*s)], fill=shade(g, 1.2))
    d.text((cx, cy - 90*s), "1", font=font(max(8, int(140*s))), fill=shade(g, 0.7), anchor="mm")

def sparkles(d, t, n=14, seed=2, area=(80, 120, 1000, 900)):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.randrange(area[0], area[2]); y = rnd.randrange(area[1], area[3])
        a = (math.sin(t * 5 + i * 1.7) + 1) / 2; r = 6 + 16 * a
        d.polygon([(x, y - r), (x + r*0.3, y - r*0.3), (x + r, y), (x + r*0.3, y + r*0.3), (x, y + r), (x - r*0.3, y + r*0.3), (x - r, y), (x - r*0.3, y - r*0.3)], fill=(255, 245, 190))

def bars(d, t, items, base=950, maxh=560, unit=""):
    n = len(items); bw = 220; gap = (W - n * bw) / (n + 1)
    mx = max(v for _, v, _ in items)
    for i, (lab, v, col) in enumerate(items):
        p = ease((t - 0.25 * i) / 0.9)
        h = maxh * v / mx * p
        x = gap + i * (bw + gap)
        if h > 2: box(d, x, base - h, bw, h, 60, col)
        d.text((x + bw/2, base + 50), lab, font=font(46), fill=(30, 30, 40), anchor="mm")
        if p > 0.05:
            d.text((x + bw/2 + 15, base - h - 70), f"{int(v * p)}{unit}", font=font(60), fill=(30, 30, 40), anchor="mm")

def qmark(d, cx, cy, s, col=(255, 255, 255)):
    if s <= 0.02: return
    d.ellipse([cx - 70*s, cy - 70*s, cx + 70*s, cy + 70*s], fill=(240, 170, 40))
    d.text((cx, cy + 4*s), "?", font=font(max(8, int(110*s))), fill=col, anchor="mm")

FLORIDA = [(80, 330), (560, 300), (640, 340), (720, 330), (790, 420), (850, 560), (900, 700), (930, 830),
           (910, 960), (850, 1020), (790, 990), (730, 900), (660, 780), (620, 640), (590, 520), (520, 450),
           (400, 430), (260, 450), (120, 470), (60, 420)]
REGIONS = [("Mount Kalaga", (430, 360)), ("Ambrosia", (700, 470)), ("Port Gellhorn", (220, 410)),
           ("Grassrivers", (760, 760)), ("Vice City", (880, 860)), ("Leonida Keys", (760, 1080))]

def leonida(d, t, show=6, zoom=1.0):
    def P(p): return (540 + (p[0] - 540) * zoom, 640 + (p[1] - 640) * zoom)
    pts = [P(p) for p in FLORIDA]
    d.polygon([(x + 18, y + 22) for x, y in pts], fill=(40, 90, 130))
    d.polygon(pts, fill=(110, 175, 95), outline=(60, 120, 60), width=6)
    for k in range(5):
        x, y = P((700 + k * 32, 1060 + (k % 2) * 16))
        d.ellipse([x - 20, y - 10, x + 20, y + 10], fill=(225, 205, 150))
    for i, (name, p) in enumerate(REGIONS[:show]):
        s = back((t - 0.35 * i) / 0.3)
        if s <= 0.02: continue
        x, y = P(p)
        d.ellipse([x - 22*s, y - 22*s, x + 22*s, y + 22*s], fill=(230, 60, 60), outline="white", width=5)
        tw = d.textlength(name, font=font(40))
        lx = min(max(x, tw/2 + 30), W - tw/2 - 30)
        d.rounded_rectangle([lx - tw/2 - 14, y - 82, lx + tw/2 + 14, y - 34], 14, fill=(255, 255, 255))
        d.text((lx, y - 58), name, font=font(40), fill=(30, 30, 30), anchor="mm")

SEA = grad((90, 170, 215), (40, 110, 170))

def alligator(d, x, y, s=1.0, jaw=0.0):
    c = (125, 165, 70)
    d.polygon([(x, y), (x + 120*s, y - 40*s), (x + 420*s, y - 45*s), (x + 520*s, y - 25*s), (x + 520*s, y + 5*s), (x + 120*s, y + 15*s)], fill=c)
    d.polygon([(x + 420*s, y - 45*s), (x + 640*s, y - 40*s - jaw*40*s), (x + 640*s, y - 20*s - jaw*30*s), (x + 520*s, y - 10*s)], fill=shade(c, 1.1))
    d.polygon([(x + 520*s, y - 5*s), (x + 640*s, y - 5*s + jaw*20*s), (x + 640*s, y + 10*s + jaw*20*s), (x + 520*s, y + 10*s)], fill=shade(c, 0.85))
    for k in range(8):
        bx = x + 150*s + k * 40*s
        d.polygon([(bx, y - 42*s), (bx + 15*s, y - 62*s), (bx + 30*s, y - 42*s)], fill=shade(c, 0.8))
    d.ellipse([x + 450*s, y - 70*s, x + 485*s, y - 40*s], fill=(230, 210, 60))
    d.ellipse([x + 462*s, y - 62*s, x + 474*s, y - 48*s], fill=(20, 20, 20))

# ---------------- scenes ----------------
def S(fn): return fn

# ===== Video 2: Preis =====
def p_tag(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im)
    cloud(d, 100 + t * 15, 170); cloud(d, 780 - t * 12, 250, 0.8); ground(d, 980)

    ang = math.sin(t * 3) * 12 * (1 - min(1, t / 3)) + math.sin(t * 2) * 3
    paste_rot(im, tag_img("79,99 €"), 540, 560, -8 + ang, 1.3 * back(t / 0.4))
    sparkles(d, t, 10, 5)
    return im

def p_standard(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 980)
    game_case(d, 330, 980, 380, 520, (40, 120, 200), "STANDARD", back(t / 0.45))
    paste_rot(im, tag_img("79,99 €"), 820, 460, 18 + math.sin(t * 3) * 4, 0.6 * back((t - 0.6) / 0.4))
    return im

def p_ultimate(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im); ground(d, 980, (200, 190, 200))
    bill_stack(d, 90, 980, 180, 120 * ease(t / 0.8)); bill_stack(d, 820, 980, 170, 200 * ease((t - 0.2) / 0.8))
    game_case(d, 350, 980, 380, 520, (235, 185, 50), "ULTIMATE", back(t / 0.45))
    paste_rot(im, tag_img("99,99 €", (255, 120, 120)), 760, 360, 15 + math.sin(t * 3) * 4, 0.6 * back((t - 0.6) / 0.4))
    sparkles(d, t, 12, 9)
    return im

def p_nodisc(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 980)
    # open box
    box(d, 330, 760, 420, 220, 160, (190, 140, 90))
    lid = ease(t / 0.5)
    d.polygon([(330, 760), (750, 760), (750 - 40 * lid, 760 - 200 * lid), (330 + 40 * lid, 760 - 200 * lid)], fill=(210, 160, 105))
    # disc flying out with X
    s = back((t - 0.5) / 0.4)
    if s > 0.02:
        cx, cy, r = 280, 430, 130 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(215, 220, 230), outline=(160, 165, 180), width=6)
        d.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18], fill=(110, 150, 200))
        xmark(d, cx, cy, 110, ease((t - 1.0) / 0.4))
    # code card with check
    s2 = back((t - 1.6) / 0.4)
    if s2 > 0.02:
        cx, cy = 770, 430
        d.rounded_rectangle([cx - 170*s2, cy - 100*s2, cx + 170*s2, cy + 100*s2], 20, fill=(255, 255, 255), outline=(40, 40, 40), width=5)
        d.text((cx, cy - 25*s2), "CODE", font=font(max(8, int(56*s2))), fill=(40, 40, 40), anchor="mm")
        d.text((cx, cy + 40*s2), "XXXX-XXXX", font=font(max(8, int(34*s2))), fill=(120, 120, 130), anchor="mm")
        check(d, cx + 150, cy - 110, ease((t - 2.1) / 0.3), back((t - 2.1) / 0.3))
    return im

def p_bonus(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im)
    d.rectangle([0, 860, W, SCENE_H], fill=(238, 205, 150))
    # garage
    box(d, 560, 480, 420, 380, 120, (240, 230, 220))
    d.rectangle([600, 600, 940, 860], fill=(70, 70, 80))
    op = ease(t / 0.8)
    d.rectangle([600, 600, 940, 600 + 260 * (1 - op)], fill=(200, 200, 205))
    for yy in range(600, int(600 + 260 * (1 - op)), 26): d.line([(600, yy), (940, yy)], fill=(170, 170, 178), width=3)
    palm(d, 120, 900, 1.0, math.sin(t * 2))
    cx = 1200 - ease((t - 0.6) / 1.2) * 1020
    car(d, cx * 1.0 - 100, 1010, (60, 190, 180))
    sparkles(d, t, 8, 4, (100, 150, 1000, 450))
    return im

def p_think(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 900)
    person(d, 540, 1110, (60, 140, 90), (50, 80, 150), (70, 50, 30), bob=math.sin(t * 4) * 4)
    for i, (x, y) in enumerate([(330, 380), (760, 330), (560, 230)]):
        qmark(d, x, y + math.sin(t * 4 + i) * 10, back((t - 0.3 * i) / 0.3))
    return im

# ===== Video 3: Trailer-Rekord =====
def r_trophy(t, dur):
    im = NIGHT.copy(); d = ImageDraw.Draw(im); ground(d, 960, (60, 64, 90))
    for i in range(6):
        a = t * 0.6 + i * math.pi / 3
        d.polygon([(540, 560), (540 + math.cos(a) * 900, 560 + math.sin(a) * 900), (540 + math.cos(a + 0.25) * 900, 560 + math.sin(a + 0.25) * 900)], fill=(45, 60, 110))
    trophy(d, 540, 580, back(t / 0.5) * 1.3)
    sparkles(d, t, 16, 3)
    return im

def r_count(t, dur, target=475, start=0.2, total=2.6):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 1000)
    v = int(target * ease((t - start) / total))
    phone(d, 540, 600, 1.1 * back(t / 0.4), f"{v} Mio.")
    for i in range(5):
        y = 900 - ((t * 260 + i * 160) % 800)
        x = 160 + (i * 197) % 760 if i % 2 else 880 - (i * 131) % 200
        d.polygon([(x, y), (x + 22, y - 20), (x + 44, y), (x + 22, y + 26)], fill=(230, 60, 90))
        d.ellipse([x - 2, y - 24, x + 24, y + 4], fill=(230, 60, 90)); d.ellipse([x + 20, y - 24, x + 46, y + 4], fill=(230, 60, 90))
    return im

def r_bars(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 950)
    bars(d, t, [("GTA 6", 475, (230, 70, 110)), ("Kino-Hit", 365, (90, 120, 200))], unit=" Mio.")
    return im

def r_trailer1(t, dur):
    return r_count(t, dur, 93, 0.2, 2.0)

def r_globe(t, dur):
    im = NIGHT.copy(); d = ImageDraw.Draw(im)
    rnd = random.Random(1)
    for _ in range(50):
        x, y = rnd.randrange(W), rnd.randrange(SCENE_H); d.ellipse([x, y, x + 4, y + 4], fill=(200, 200, 220))
    g = Image.new("RGB", (640, 640), (50, 120, 200)); gd = ImageDraw.Draw(g)
    off = (t * 120) % 640
    rr = random.Random(8)
    blobs = [(rr.randrange(640), rr.randrange(80, 560), rr.randrange(60, 140)) for _ in range(9)]
    for bx, by, r in blobs:
        for o in (-640, 0, 640):
            gd.ellipse([bx + o - off - r, by - r * 0.7, bx + o - off + r, by + r * 0.7], fill=(90, 170, 90))
    mask = Image.new("L", (640, 640)); ImageDraw.Draw(mask).ellipse([0, 0, 640, 640], fill=255)
    s = back(t / 0.5)
    if s > 0.05:
        sz = int(640 * s)
        im.paste(g.resize((sz, sz)), (540 - sz // 2, 560 - sz // 2), mask.resize((sz, sz)))
    for i, (x, y) in enumerate([(380, 420), (620, 380), (700, 640), (450, 700), (560, 520)]):
        ps = back((t - 0.6 - 0.25 * i) / 0.3)
        if ps > 0.05:
            d.ellipse([x - 20*ps, y - 60*ps, x + 20*ps, y - 20*ps], fill=(230, 60, 60))
            d.polygon([(x - 18*ps, y - 40*ps), (x + 18*ps, y - 40*ps), (x, y)], fill=(230, 60, 60))
    return im

def r_watch(t, dur):
    im = NIGHT.copy(); d = ImageDraw.Draw(im); ground(d, 900, (70, 74, 96))
    box(d, 560, 420, 440, 280, 30, (30, 30, 36))
    flick = (int(t * 6) % 3)
    d.rectangle([580, 440, 980, 680], fill=[(230, 120, 160), (120, 90, 190), (255, 170, 110)][flick])
    d.polygon([(750, 510), (750, 610), (830, 560)], fill="white")
    d.rectangle([770, 700, 790, 900], fill=(40, 40, 46))
    person(d, 280, 1110, (230, 120, 60), (40, 60, 120), (40, 28, 22), bob=math.sin(t * 8) * 3)
    for i in range(3):
        y = 330 - ((t * 120 + i * 60) % 160)
        d.text((330 + i * 50, y), "!", font=font(80), fill=(255, 220, 80), anchor="mm")
    return im

# ===== Video 4: Map =====
def m_map(t, dur, show=0, zoom=1.0):
    im = SEA.copy(); d = ImageDraw.Draw(im)
    for k in range(10):
        y = 120 + k * 110; off = (t * 40 + k * 70) % 240
        for x in range(-240, W, 240): d.line([(x + off, y), (x + off + 60, y)], fill=(130, 195, 230), width=4)
    leonida(d, t, show, zoom * (0.85 + 0.15 * back(t / 0.5)))
    return im

def m_map_full(t, dur): return m_map(t, dur, 0)
def m_map_regions(t, dur): return m_map(t, dur, 6)

def m_keys(t, dur):
    im = SEA.copy(); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 330], fill=(140, 195, 235)); cloud(d, 150 + t * 10, 150, 0.8)
    d.line([(0, 600), (W, 560)], fill=(220, 220, 225), width=26)
    for x in range(40, W, 120): d.line([(x, 590 - x * 0.037), (x, 700)], fill=(180, 180, 190), width=10)
    for cx, cy, r in [(220, 800, 170), (760, 880, 210)]:
        d.ellipse([cx - r, cy - r * 0.35, cx + r, cy + r * 0.35], fill=(235, 210, 150))
        palm(d, cx - 30, cy, 0.75, math.sin(t * 2)); palm(d, cx + 60, cy + 5, 0.6, -math.sin(t * 2))
    bx = -200 + (t * 300) % (W + 400)
    d.polygon([(bx, 1030), (bx + 200, 1030), (bx + 240, 990), (bx - 20, 990)], fill=(250, 250, 250))
    d.rectangle([bx + 60, 950, bx + 150, 990], fill=(60, 120, 200))
    for k in range(4): d.line([(bx - 40 - k * 50, 1020 + k * 6), (bx - 80 - k * 50, 1020 + k * 6)], fill=(220, 240, 250), width=5)
    return im

def m_swamp(t, dur):
    im = grad((150, 190, 160), (200, 215, 180)); d = ImageDraw.Draw(im)
    d.rectangle([0, 700, W, SCENE_H], fill=(60, 95, 70))
    for k in range(9):
        y = 740 + k * 50; off = (t * 30 + k * 40) % 200
        for x in range(-200, W, 200): d.line([(x + off, y), (x + off + 70, y)], fill=(90, 130, 95), width=4)
    rnd = random.Random(5)
    for _ in range(26):
        x = rnd.randrange(W); h = rnd.randrange(80, 200); yb = rnd.choice([710, 720, 1150, 1160])
        d.line([(x, yb), (x + math.sin(t * 2 + x) * 10, yb - h)], fill=(80, 120, 60), width=7)
    for x in (80, 960):
        d.rectangle([x, 300, x + 30, 720], fill=(90, 70, 50))
        d.ellipse([x - 140, 180, x + 170, 380], fill=(70, 115, 70))
    ax = 1100 - ease(t / 2.5) * 1000
    jaw = max(0, math.sin((t - 2.5) * 6)) if t > 2.5 else 0
    alligator(d, ax, 950, 1.25, jaw)
    return im

def m_mountain(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); cloud(d, 120 + t * 12, 150, 0.8)
    d.polygon([(-50, 800), (300, 300), (650, 800)], fill=(110, 120, 140)); d.polygon([(300, 300), (650, 800), (420, 800)], fill=(85, 95, 115))
    d.polygon([(300, 300), (360, 390), (330, 380), (300, 410), (260, 380), (240, 390)], fill=(245, 245, 250))
    d.polygon([(400, 800), (760, 220), (1150, 800)], fill=(120, 132, 150)); d.polygon([(760, 220), (1150, 800), (900, 800)], fill=(92, 104, 122))
    d.polygon([(760, 220), (830, 330), (790, 315), (760, 350), (720, 320), (690, 330)], fill=(245, 245, 250))
    d.rectangle([0, 800, W, SCENE_H], fill=(90, 150, 80))
    for x in range(20, W, 110):
        h = 140 + (x * 37) % 60
        d.polygon([(x, 830 - h), (x - 45, 830), (x + 45, 830)], fill=(40, 105, 60))
    d.ellipse([200, 930, 880, 1120], fill=(70, 140, 200))
    ph = (t * 1.2) % 1.6
    if ph < 1:
        fx = 420 + ph * 220; fy = 1010 - math.sin(ph * math.pi) * 200
        d.ellipse([fx - 40, fy - 16, fx + 40, fy + 16], fill=(240, 160, 70))
        d.polygon([(fx - 40, fy), (fx - 70, fy - 22), (fx - 70, fy + 22)], fill=(240, 160, 70))
    return im

# ===== Video 5: Kosten =====
def k_rain(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im); ground(d, 980, (200, 190, 200))
    bill_stack(d, 380, 980, 320, 380 * ease(t / 2.5))
    rnd = random.Random(11)
    for i in range(30):
        x = rnd.randrange(W); sp = rnd.uniform(250, 420)
        y = (rnd.randrange(-900, 0) + t * sp) % 1300 - 120
        bill(d, x + math.sin(t * 3 + i) * 30, y, math.sin(t * 2 + i) * 0.8, 0.9)
    return im

def k_stacks(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 1000)
    for i in range(5):
        h = (120 + i * 90) * ease((t - 0.3 * i) / 0.7)
        if h > 3: bill_stack(d, 70 + i * 195, 1000, 150, h)
    d.text((540, 230), "$ 1.500.000.000", font=font(78), fill=(40, 120, 60), anchor="mm")
    return im

def k_question(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 980)
    box(d, 330, 520, 420, 460, 150, (110, 115, 125))
    d.ellipse([480, 680, 600, 800], outline=(60, 60, 70), width=14)
    d.text((540, 600), "GEHEIM", font=font(50), fill=(230, 230, 235), anchor="mm")
    mx = 540 + math.sin(t * 2) * 200; my = 430 + math.cos(t * 2) * 60
    d.ellipse([mx - 90, my - 90, mx + 90, my + 90], outline=(60, 60, 70), width=20)
    d.line([(mx + 60, my + 60), (mx + 150, my + 150)], fill=(60, 60, 70), width=30)
    qmark(d, 860, 320, back((t - 0.5) / 0.3)); qmark(d, 220, 360, back((t - 0.8) / 0.3))
    return im

def k_compare(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 950)
    bars(d, t, [("GTA 5", 265, (90, 150, 210)), ("GTA 6 (geschätzt)", 1500, (230, 70, 110))], unit=" Mio. $")
    return im

def k_sales(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 1000)
    n = int(ease(t / 3.0) * 18)
    cols = [(40, 120, 200), (230, 70, 110), (60, 170, 110)]
    for i in range(n):
        row, colm = divmod(i, 6)
        x = 90 + colm * 150 + (row % 2) * 30; y = 1000 - row * 190
        game_case(d, x, y, 120, 180, cols[i % 3], "V", 1.0)
    v = int(230 * ease(t / 3.0))
    d.text((540, 230), f"{v} Mio.", font=font(110), fill=(30, 30, 40), anchor="mm")
    return im

def k_up(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im); ground(d, 1000)
    pts = [(120, 900), (300, 820), (450, 860), (620, 640), (780, 680), (950, 380)]
    p = ease(t / 1.5) * (len(pts) - 1)
    k = int(p); f = p - k
    path = pts[:k + 1] + ([(pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f)] if k < len(pts) - 1 else [])
    if len(path) > 1: d.line(path, fill=(40, 170, 90), width=30, joint="curve")
    if p >= len(pts) - 1.01:
        d.polygon([(950, 300), (1010, 420), (890, 420)], fill=(40, 170, 90))
    sparkles(d, t, 8, 6)
    return im

# ---------------- video definitions ----------------
# each scene: (duration, fn, [(start_sec, WORD), ...])
VIDEOS = {
    "02_Preis": [
        (4.0, p_tag, [(0, "SO TEUER")]),
        (4.5, p_standard, [(0, "79,99 EURO")]),
        (4.5, p_ultimate, [(0, "ULTIMATE")]),
        (5.0, p_nodisc, [(0, "KEINE DISC")]),
        (4.5, p_bonus, [(0, "BONUS")]),
        (3.5, p_think, [(0, "LOHNT SICH?")]),
        (4.0, M.sc_outro, [(0, "FOLGT FÜR MEHR")]),
    ],
    "03_Trailer_Rekord": [
        (4.0, r_trophy, [(0, "WELTREKORD")]),
        (5.0, r_count, [(0, "475 MILLIONEN")]),
        (5.0, r_bars, [(0, "MEHR ALS KINO")]),
        (4.5, r_trailer1, [(0, "TRAILER 1")]),
        (4.5, r_globe, [(0, "WELTWEIT")]),
        (4.0, r_watch, [(0, "DU AUCH?")]),
        (3.0, M.sc_outro, [(0, "FOLGT FÜR MEHR")]),
    ],
    "04_Map_Leonida": [
        (3.5, m_map_full, [(0, "LEONIDA")]),
        (4.5, m_map_regions, [(0, "6 REGIONEN")]),
        (4.0, M.sc_city, [(0, "VICE CITY")]),
        (4.0, m_keys, [(0, "LEONIDA KEYS")]),
        (4.5, m_swamp, [(0, "ALLIGATOREN")]),
        (4.5, m_mountain, [(0, "MOUNT KALAGA")]),
        (5.0, M.sc_outro, [(0, "UND NOCH MEHR"), (2.5, "FOLGT FÜR MEHR")]),
    ],
    "05_Kosten": [
        (4.0, k_rain, [(0, "TEUERSTES SPIEL")]),
        (5.0, k_stacks, [(0, "1,5 MILLIARDEN")]),
        (4.5, k_question, [(0, "NUR GESCHÄTZT")]),
        (5.0, k_compare, [(0, "GTA 5")]),
        (4.5, k_sales, [(0, "230 MILLIONEN")]),
        (3.5, k_up, [(0, "LOHNT SICH")]),
        (3.5, M.sc_outro, [(0, "FOLGT FÜR MEHR")]),
    ],
}

def frame(vid, idx, t):
    dur, fn, words = VIDEOS[vid][idx]
    fr = Image.new("RGB", (W, H))
    sc = fn(t, dur)
    z = 1.0 + 0.05 * (t / dur)
    zw, zh = int(W * z), int(SCENE_H * z)
    if z > 1.001:
        sc = sc.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - SCENE_H) // 2, (zw - W) // 2 + W, (zh - SCENE_H) // 2 + SCENE_H))
    fr.paste(sc, (0, 0)); fr.paste(WALL, (0, SCENE_H))
    cur = [w for w in words if w[0] <= t][-1]
    wimg = word_img(cur[1]); s = back((t - cur[0]) / 0.22)
    if s > 0.02:
        ww, wh = max(1, int(wimg.width * s)), max(1, int(wimg.height * s))
        wi = wimg.resize((ww, wh), Image.BILINEAR)
        fr.paste(wi, ((W - ww) // 2, SCENE_H + 40 - wh // 2), wi)
    gt = sum(sc_[0] for sc_ in VIDEOS[vid][:idx]) + t
    ot = (t - words[-1][0]) if (idx == len(VIDEOS[vid]) - 1 and t >= words[-1][0]) else None
    fr = mascot.overlay(fr, gt, ot)
    if t < 0.08 and idx > 0:
        fr = Image.blend(fr, Image.new("RGB", (W, H), "white"), 0.6 * (1 - t / 0.08))
    return fr

def render(vid, idx):
    dur = VIDEOS[vid][idx][0]; n = int(round(dur * FPS))
    os.makedirs(os.path.join(OUT, vid), exist_ok=True)
    tmp = os.path.join(OUT, vid, f"s{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(vid, idx, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(OUT, vid, f"s{idx}.mp4"))

if __name__ == "__main__":
    vid = sys.argv[2]
    if sys.argv[1] == "preview":
        ims = [frame(vid, i, VIDEOS[vid][i][0] * 0.8).resize((270, 480)) for i in range(len(VIDEOS[vid]))]
        sh = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): sh.paste(im, ((i % 4) * 270, (i // 4) * 480))
        sh.save(os.path.join(OUT, f"prev_{vid}.png"))
    else:
        render(vid, int(sys.argv[3]))
