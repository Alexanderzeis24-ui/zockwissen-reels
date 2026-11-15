"""Reel 23: GTA 6 mini details (Rob Nelson / Guardian, 11.11.2026). Modern look: glass cards, neon glow, lens zoom, liquid sim."""
import sys, os, math, random, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes7 as S7
from scenes7 import *
from PIL import Image, ImageDraw, ImageFilter

VID = "23_Mini_Details"
S7.SCRIPTS7[VID] = ["In GTA 6 schwappt sogar das Bier!", "Jason isst und trinkt gleichzeitig.", "Sogar Hot Dogs!", "Beim Rennen schwappt das Bier im Sixpack.", "Dazu ein Überfall auf einen Juwelier.", "Selbst die Füße der Wachen passen.", "Das verriet Rockstar North.", "Das ganze Interview kommt am 14. November.", "Und in einer Woche kannst du es selbst spielen!", "Welches Detail ist am krassesten? Kommentier!"]
S7.COMMENT[VID] = ("KRASSESTES DETAIL?", "Das Bier, safe 🍺"[:-2])
S7.COVER[VID] = ("SOGAR DAS BIER", "SCHWAPPT IN GTA 6?!")

NEON = (120, 240, 255); NEON2 = (255, 90, 200); AMBER = (255, 190, 60)

# ---------- modern primitives ----------
def glass(im, b, tint=(255, 255, 255), alpha=70, r=44, glow=None):
    """frosted glass card with neon edge glow"""
    x0, y0, x1, y1 = [int(v) for v in b]
    region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(18))
    ov = Image.new("RGB", region.size, tint)
    region = Image.blend(region, ov, alpha / 255)
    m = Image.new("L", region.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, x1 - x0, y1 - y0], r, fill=255)
    if glow:
        g = Image.new("L", (x1 - x0 + 120, y1 - y0 + 120), 0)
        ImageDraw.Draw(g).rounded_rectangle([60, 60, x1 - x0 + 60, y1 - y0 + 60], r, outline=255, width=10)
        g = g.filter(ImageFilter.GaussianBlur(18))
        im.paste(glow, (x0 - 60, y0 - 60), g)
    im.paste(region, (x0, y0), m)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x0, y0, x1, y1], r, outline=(255, 255, 255), width=3)
    d.line([(x0 + r, y0 + 4), (x1 - r, y0 + 4)], fill=(255, 255, 255), width=2)
    return d

@functools.lru_cache(maxsize=64)
def _glow_mask(w, h, r):
    g = Image.new("L", (w, h), 0); ImageDraw.Draw(g).ellipse([w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r], fill=255)
    return g.filter(ImageFilter.GaussianBlur(r * 0.6))

def bloom(im, cx, cy, r, col, k=1.0):
    m = _glow_mask(int(r * 4), int(r * 4), int(r))
    if k < 1: m = m.point(lambda v: int(v * k))
    im.paste(col, (int(cx - r * 2), int(cy - r * 2)), m)

def neon_text(im, txt, cx, cy, size, col):
    lay = Image.new("L", (W, H), 0); ImageDraw.Draw(lay).text((cx, cy), txt, font=F(size), fill=255, anchor="mm")
    im.paste(col, (0, 0), lay.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(im).text((cx, cy), txt, font=F(size), fill=(255, 255, 255), anchor="mm")

def bottle(d, cx, cy, s, t, level=0.6, tilt=0.0, slosh=1.0):
    if s < 0.2: return
    w, h = 90 * s, 300 * s
    x0, y0 = cx - w / 2, cy - h / 2
    # liquid with sloshing surface
    top = y0 + 70 * s + (h - 80 * s) * (1 - level)
    pts = [(x0 + 6, y0 + h - 8)]
    for i in range(21):
        x = x0 + 6 + (w - 12) * i / 20
        y = min(y0 + h - 14, max(y0 + 66 * s, top + math.sin(t * 7 + i * 0.6) * 9 * s * slosh + (i - 10) * tilt * 0.5 * s))
        pts.append((x, y))
    pts.append((x0 + w - 6, y0 + h - 8))
    d.rounded_rectangle([x0, y0 + 60 * s, x0 + w, y0 + h], int(26 * s), fill=(150, 90, 30), outline=INK, width=4)
    d.polygon(pts, fill=AMBER)
    d.rounded_rectangle([x0, y0 + 60 * s, x0 + w, y0 + h], int(26 * s), outline=INK, width=4)
    for k in range(6):
        bx = x0 + 15 * s + (k * 23 % max(1, int(w - 30 * s + 1))); by = y0 + h - 20 * s - ((t * 120 * s + k * 40 * s) % (h * 0.55))
        if by > top + 8: d.ellipse([bx - 5 * s, by - 5 * s, bx + 5 * s, by + 5 * s], fill=(255, 235, 170))
    d.rectangle([cx - 20 * s, y0, cx + 20 * s, y0 + 70 * s], fill=(150, 90, 30), outline=INK, width=4)
    d.rectangle([cx - 24 * s, y0 - 12 * s, cx + 24 * s, y0 + 6 * s], fill=(220, 60, 60), outline=INK, width=3)
    d.rounded_rectangle([x0 + 12 * s, y0 + 140 * s, x0 + w - 12 * s, y0 + 210 * s], int(8 * s), fill=(250, 240, 220), outline=INK, width=3)
    d.line([(x0 + 16 * s, y0 + 80 * s), (x0 + 16 * s, y0 + h - 30 * s)], fill=(255, 230, 190), width=max(2, int(6 * s)))

def lens(im, cx, cy, r, src_cx, src_cy, zoom=1.8):
    box = (int(src_cx - r / zoom), int(src_cy - r / zoom), int(src_cx + r / zoom), int(src_cy + r / zoom))
    patch = im.crop(box).resize((2 * r, 2 * r), Image.BICUBIC)
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * r, 2 * r], fill=255)
    im.paste(patch, (int(cx - r), int(cy - r)), m)
    d = ImageDraw.Draw(im)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=8)
    d.ellipse([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6], outline=INK, width=4)
    d.line([(cx + r * 0.72, cy + r * 0.72), (cx + r * 1.25, cy + r * 1.25)], fill=INK, width=26)

def donut(d, cx, cy, r, a):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 160, 90), outline=INK, width=4)
    d.ellipse([cx - r * 0.86, cy - r * 0.86, cx + r * 0.86, cy + r * 0.86], fill=(255, 130, 190))
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32], fill=(40, 30, 60), outline=INK, width=3)
    rnd = random.Random(2)
    for i in range(14):
        aa = a + i * 0.45; rr = r * (0.45 + 0.35 * rnd.random())
        x, y = cx + math.cos(aa) * rr, cy + math.sin(aa) * rr
        d.line([(x - 8, y), (x + 8, y + 3)], fill=[NEON, AMBER, (255, 255, 255), (120, 230, 140)][i % 4], width=6)

def hand(d, cx, cy, s):
    d.ellipse([cx - 45 * s, cy - 35 * s, cx + 45 * s, cy + 45 * s], fill=(232, 190, 152), outline=INK, width=3)

def hotdog(d, cx, cy, s, t):
    d.rounded_rectangle([cx - 190 * s, cy - 40 * s, cx + 190 * s, cy + 60 * s], int(50 * s), fill=(230, 170, 90), outline=INK, width=4)
    d.rounded_rectangle([cx - 210 * s, cy - 30 * s, cx + 210 * s, cy + 20 * s], int(25 * s), fill=(190, 80, 60), outline=INK, width=4)
    p = ease((t - 0.4) / 1.0)
    pts = [(cx - 170 * s + 340 * s * k / 30, cy - 8 * s + math.sin(k * 0.9) * 12 * s) for k in range(int(30 * p) + 1)]
    if len(pts) > 1: d.line(pts, fill=(250, 60, 50), width=max(2, int(12 * s)), joint="curve")
    pts2 = [(cx - 150 * s + 300 * s * k / 30, cy - 2 * s + math.cos(k * 0.9) * 10 * s) for k in range(int(30 * ease((t - 0.8) / 1.0)) + 1)]
    if len(pts2) > 1: d.line(pts2, fill=(255, 210, 40), width=max(2, int(9 * s)), joint="curve")
    for k in range(3):
        x = cx - 80 * s + k * 80 * s; ph = (t * 0.9 + k * 0.33) % 1
        yy = cy - 80 * s - ph * 160 * s
        d.arc([x - 20 * s, yy - 30 * s, x + 20 * s, yy + 30 * s], 270, 90, fill=(255, 255, 255), width=5)
        d.arc([x - 20 * s, yy + 20 * s, x + 20 * s, yy + 80 * s], 90, 270, fill=(255, 255, 255), width=5)

def runner(d, cx, cy, s, t):
    if s < 0.25: return
    ph = t * 10
    c = (35, 40, 70)
    d.ellipse([cx - 30 * s, cy - 210 * s, cx + 30 * s, cy - 150 * s], fill=c)
    d.line([(cx, cy - 150 * s), (cx + 10 * s, cy - 40 * s)], fill=c, width=int(38 * s))
    for sg in (1, -1):
        a = math.sin(ph) * 0.8 * sg
        kx, ky = cx + 10 * s + math.sin(a) * 60 * s, cy - 40 * s + 60 * s
        d.line([(cx + 10 * s, cy - 40 * s), (kx, ky), (kx - math.sin(a) * 30 * s, ky + 70 * s)], fill=c, width=int(26 * s), joint="curve")
    d.line([(cx, cy - 130 * s), (cx + 40 * s + math.sin(ph) * 40 * s, cy - 60 * s)], fill=c, width=int(22 * s))
    # six-pack tucked under other arm
    bx, by = cx - 70 * s, cy - 110 * s
    d.rounded_rectangle([bx - 50 * s, by, bx + 50 * s, by + 70 * s], int(8 * s), fill=(200, 150, 90), outline=INK, width=3)
    for k in range(3):
        d.rectangle([bx - 40 * s + k * 30 * s, by - 50 * s, bx - 20 * s + k * 30 * s, by], fill=(150, 90, 30), outline=INK, width=2)
        lvl = by - 30 * s + math.sin(t * 14 + k) * 8 * s
        d.rectangle([bx - 38 * s + k * 30 * s, min(lvl, by - 3), bx - 22 * s + k * 30 * s, by - 2], fill=AMBER)
    d.line([(cx, cy - 130 * s), (bx + 30 * s, by + 20 * s)], fill=c, width=int(22 * s))
    for k in range(5):
        y = cy - 180 * s + k * 40 * s; x = cx - 160 * s - (t * 600 + k * 60) % 120
        d.line([(x, y), (x - 80 * s, y)], fill=(255, 255, 255), width=4)

def diamond(d, cx, cy, s, t):
    pts = [(cx, cy - 120 * s), (cx + 120 * s, cy - 30 * s), (cx, cy + 140 * s), (cx - 120 * s, cy - 30 * s)]
    d.polygon(pts, fill=(170, 230, 255), outline=INK)
    d.polygon([(cx - 120 * s, cy - 30 * s), (cx + 120 * s, cy - 30 * s), (cx, cy + 140 * s)], fill=(120, 200, 245), outline=INK)
    d.polygon([(cx - 60 * s, cy - 30 * s), (cx, cy - 120 * s), (cx + 60 * s, cy - 30 * s), (cx, cy + 140 * s)], fill=(200, 245, 255), outline=INK)
    for i in range(4):
        a = t * 3 + i * math.pi / 2
        star(d, cx + math.cos(a) * 170 * s, cy + math.sin(a) * 140 * s, 22 * s, (255, 255, 255))

def crack(d, cx, cy, p, seed=3):
    rnd = random.Random(seed)
    for i in range(8):
        a = i * math.pi / 4 + rnd.uniform(-0.3, 0.3); x, y = cx, cy
        L = 260 * p
        for k in range(4):
            nx = x + math.cos(a) * L / 4 + rnd.uniform(-15, 15); ny = y + math.sin(a) * L / 4 + rnd.uniform(-15, 15)
            d.line([(x, y), (nx, ny)], fill=(255, 255, 255), width=4); x, y = nx, ny

def foot(d, x, y, s, a):
    ca, sa = math.cos(a), math.sin(a)
    pts = [(-22, -60), (22, -60), (26, 40), (-26, 40)]
    P = [(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts]
    d.polygon(P, fill=(30, 30, 40), outline=(255, 255, 255))

# ---------- scenes ----------
def m_hook(im, d, t, dur):
    bloom(im, 710, 880, 260, (255, 170, 60), 0.8)
    d = ImageDraw.Draw(im)
    tilt = math.sin(t * 2.6) * 8
    bottle(d, 710, 880, 1.6 * back(t / 0.4), t, 0.62, tilt, 1.6)
    if t > 0.7:
        lens(im, 900, 660, 120, 710, 886, 2.0)
    return (710, 820)

def m_both(im, d, t, dur):
    glass(im, (430, 570, 990, 1230), (255, 255, 255), 60, 44, NEON)
    d = ImageDraw.Draw(im)
    sw = math.sin(t * 3)
    donut(d, 580, 820 + sw * 14, 110 * back(t / 0.4), t * 1.2)
    hand(d, 580, 950 + sw * 14, 1.0 * back(t / 0.4))
    bottle(d, 850, 840 - sw * 14, 0.85 * back((t - 0.25) / 0.4), t, 0.6, sw * 6, 1.2)
    hand(d, 850, 990 - sw * 14, 1.0 * back((t - 0.25) / 0.4))
    pill(d, "GLEICHZEITIG", 710, 1160, 38, NEON, INK, back((t - 0.7) / 0.4))
    return (580, 820)

def m_hotdog(im, d, t, dur):
    glass(im, (430, 600, 990, 1200), (255, 230, 200), 70, 44, AMBER)
    d = ImageDraw.Draw(im)
    s = back(t / 0.45)
    if s > 0.05: hotdog(d, 710, 920, 1.25 * s, t)
    # bite marks
    if t > 1.4:
        for k in range(3): d.ellipse([860 + k * 26, 860, 900 + k * 26, 900], fill=(30, 25, 50))
    return (710, 920)

def m_run(im, d, t, dur):
    glass(im, (430, 570, 990, 1230), (200, 240, 255), 60, 44, NEON)
    d = ImageDraw.Draw(im)
    for k in range(8):
        x = 440 + ((k * 90 - t * 500) % 560)
        d.line([(x, 1150), (x + 50, 1150)], fill=(255, 255, 255), width=6)
    runner(d, 760, 1120, 1.5 * back(t / 0.4), t)
    if t > 1.2: lens(im, 560, 700, 110, 655, 950, 2.0)
    return (655, 950)

def m_jewel(im, d, t, dur):
    on = int(t * 5) % 2
    bloom(im, 520, 640, 90, (255, 40, 60) if on else (40, 80, 255), 0.9)
    bloom(im, 900, 640, 90, (40, 80, 255) if on else (255, 40, 60), 0.9)
    d = glass(im, (440, 700, 980, 1220), (180, 220, 255), 50, 30, NEON2)
    diamond(d, 710, 940, back(t / 0.45), t)
    if t > 1.0: crack(d, 710, 940, ease((t - 1.0) / 0.4))
    pill(d, "JUWELIER-ÜBERFALL", 710, 640, 34, NEON2, (255, 255, 255), back((t - 0.3) / 0.4))
    return (710, 940)

def m_feet(im, d, t, dur):
    d = glass(im, (430, 570, 990, 1230), (220, 220, 240), 55, 44, NEON)
    for i, (x, y, a) in enumerate([(620, 1050, -0.25), (790, 1050, 0.25)]):
        s = back((t - 0.2 - 0.25 * i) / 0.3)
        if s > 0.05: foot(d, x, y, 1.6 * s, a)
    # scan line
    sy = 640 + ((t * 300) % 560)
    d.line([(440, sy), (980, sy)], fill=NEON, width=4)
    bloom(im, 710, sy, 40, NEON, 0.4)
    d = ImageDraw.Draw(im)
    if t > 1.0: lens(im, 710, 760, 120, 625, 1040, 1.8)
    pill(d, "DURCHDACHT", 710, 1180, 36, NEON, INK, back((t - 1.2) / 0.4))
    return (705, 1040)

def m_source(im, d, t, dur):
    d = glass(im, (430, 600, 990, 1180), (255, 255, 255), 85, 36, NEON2)
    d.rectangle([450, 620, 970, 700], fill=INK)
    neon_text(im, "INTERVIEW", 710, 660, 44, NEON2)
    d = ImageDraw.Draw(im)
    silhouette(d, 560, 880, 0.75 * back((t - 0.2) / 0.4), False, (60, 60, 90))
    for k in range(5):
        p = ease((t - 0.4 - 0.12 * k) / 0.35)
        d.rounded_rectangle([660, 780 + k * 55, 660 + 280 * p * (0.9 - 0.12 * (k % 2)), 800 + k * 55], 10, fill=(170, 175, 195))
    pill(d, "ROCKSTAR NORTH", 710, 1120, 34, YEL, INK, back((t - 0.8) / 0.4))
    return (710, 900)

def m_paper(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (255, 255, 255), 80, 36, NEON)
    for k in range(6):
        p = ease((t - 0.2 - 0.1 * k) / 0.35)
        d.rounded_rectangle([470, 640 + k * 60, 470 + 300 * p * (0.95 - 0.1 * (k % 2)), 664 + k * 60], 10, fill=(170, 175, 195))
    s = back((t - 0.4) / 0.45)
    if s > 0.05: M.calendar(d, 860, 900, 0.42 * s, "NOV", "14", (60, 120, 220))
    pill(d, "GANZES INTERVIEW", 710, 1150, 34, NEON, INK, back((t - 0.8) / 0.4))
    return (860, 900)

def m_week(im, d, t, dur):
    bloom(im, 710, 820, 220, NEON2, 0.6)
    d = ImageDraw.Draw(im)
    s = back(t / 0.45)
    if s > 0.05: M.calendar(d, 710, 800, 0.75 * s, "NOVEMBER", "19", (230, 60, 60))
    v = 7 - int(min(6, max(0, (t - 0.6) * 0)))
    pill(d, "NOCH 7 TAGE", 710, 1130, 48, NEON2, (255, 255, 255), back((t - 0.6) / 0.4) * (1 + 0.05 * math.sin(t * 8)))
    confetti(d, t, 1.0, (430, 540, 990, 1250))
    return (710, 800)

def m_cta(im, d, t, dur):
    bloom(im, 710, 760, 200, (255, 170, 60), 0.5)
    d = ImageDraw.Draw(im)
    icons = [lambda x, y: bottle(d, x, y, 0.45, t, 0.6, math.sin(t * 3) * 5, 1.2), lambda x, y: donut(d, x, y, 55, t),
             lambda x, y: hotdog(d, x, y, 0.42, t + 3), lambda x, y: diamond(d, x, y, 0.5, t)]
    for i, fn in enumerate(icons):
        a = t * 1.1 + i * math.pi / 2
        fn(710 + math.cos(a) * 200, 760 + math.sin(a) * 120)
    return (710, 760)

_old = S7.defs
def defs(vid, durs):
    if vid != VID: return _old(vid, durs)
    sc = [m_hook, m_both, m_hotdog, m_run, m_jewel, m_feet, m_source, m_paper, m_week, m_cta]
    w = [("BIER SCHWAPPT?!", PINK), ("ESSEN + TRINKEN", CYAN), ("HOT DOG", YEL), ("SIXPACK-SPRINT", CYAN), ("JUWELIER", PINK), ("FUSSSTELLUNG", GRN), ("ROCKSTAR NORTH", CYAN), ("AM 14. NOVEMBER", GRN), ("NOCH 7 TAGE", PINK), ("KRASSESTES DETAIL?", PINK)]
    th = ["night", "purple", "sunset", "ocean", "night", "purple", "night", "sky", "sunset", "purple"]
    poses = ["wave"] + ["point"] * 7 + ["cheer", "point"]
    return [(durs[i], th[i], sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(10)]
S7.defs = defs

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        T = S7.setup(VID); words = S7.word_times(VID, T); R = S2.R[VID]
        ims = [S7.frame(VID, 0, 0.0, T, words).resize((270, 480))] + [S7.frame(VID, i, R[i][0] * (0.9 if i == 7 else 0.65), T, words).resize((270, 480)) for i in range(8)]
        S7.make_cover(VID, os.path.join(HERE, "cov23.png")); ims.append(Image.open(os.path.join(HERE, "cov23.png")).resize((270, 480)))
        shp = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(ims[:10]): shp.paste(im, ((i % 5) * 270, (i // 5) * 480))
        shp.save(os.path.join(HERE, "p9.png"))
    elif cmd == "render":
        S7.render(VID, int(sys.argv[2]))
