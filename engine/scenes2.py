from reel2 import *
import wave, struct
import numpy as np

# =============== Reel 06: GTA Geschichte ===============
YEARS = ["1997", "2001", "2002", "2004", "2013", "2026"]
TXS = [440 + i * 104 for i in range(6)]; TLY = 1290

def timeline(d, t, cur, grow=1.0):
    x0, x1 = TXS[0], TXS[0] + (TXS[-1] - TXS[0]) * grow
    d.line([(x0, TLY), (x1, TLY)], fill=INK, width=24)
    d.line([(x0, TLY), (x1, TLY)], fill=(255, 255, 255), width=12)
    if cur >= 0: d.line([(x0, TLY), (TXS[cur], TLY)], fill=YEL, width=12)
    for i, x in enumerate(TXS):
        if x > x1 + 1: break
        r = 16
        if i == cur: r = 24 + 4 * math.sin(t * 8)
        c = YEL if i <= cur else (255, 255, 255)
        d.ellipse([x - r, TLY - r, x + r, TLY + r], fill=c, outline=INK, width=5)
        label(d, YEARS[i], x, TLY + 50, 26 if i != cur else 32, stroke=5)

def g_intro(im, d, t, dur):
    b = main_card(d, (40, 30, 80))
    v = 1997 + int(29 * ease((t - 0.5) / 2.4))
    label(d, str(v), 710, 780, 190, YEL, 10)
    pill(d, "29 JAHRE GTA", 710, 990, 50, PINK, (255, 255, 255), back((t - 0.4) / 0.4))
    sparkle_field(d, t, (450, 580, 980, 700), 8, 4)
    timeline(d, t, -1, ease(t / 1.5))
    return (710, 780)

def g_1997(im, d, t, dur):
    b = main_card(d, (95, 150, 90))
    for y in (700, 960):
        d.rectangle([428, y - 34, 992, y + 34], fill=(80, 80, 90))
        for x in range(440, 990, 70): d.rectangle([x, y - 4, x + 34, y + 4], fill=(240, 220, 120))
    for x in (580, 840):
        d.rectangle([x - 34, 548, x + 34, 1172], fill=(80, 80, 90))
    rnd = random.Random(2)
    for bx0, by0 in [(440, 560), (640, 560), (900, 560), (440, 760), (640, 760), (900, 760), (440, 1010), (640, 1010), (900, 1010)]:
        w = rnd.choice([90, 110, 130]); c = rnd.choice([(200, 120, 90), (120, 140, 200), (220, 200, 140), (170, 110, 170)])
        d.rectangle([bx0, by0, bx0 + w, by0 + 100], fill=c, outline=INK, width=4)
        d.rectangle([bx0 + 14, by0 + 14, bx0 + w - 14, by0 + 86], fill=sh(c, 1.15))
    # car loops: along road y=700 then down x=840
    p = (t * 0.35) % 1
    path = [(460, 700), (840, 700), (840, 960), (460, 960), (460, 700)]
    seg = p * 4; k = int(seg); f = seg - k
    x = lerp(path[k][0], path[k + 1][0], f); y = lerp(path[k][1], path[k + 1][1], f)
    horiz = k in (0, 2)
    w2, h2 = (40, 22) if horiz else (22, 40)
    d.rectangle([x - w2, y - h2, x + w2, y + h2], fill=RED, outline=INK, width=4)
    pill(d, "1997", 520, 590, 40, YEL, INK, back(t / 0.4))
    timeline(d, t, 0)
    return (x, y)

def g_2001(im, d, t, dur):
    b = main_card(d, (150, 200, 240))
    d.rectangle([426, 1000, 994, 1174], fill=(110, 110, 120))
    d.rectangle([426, 1000, 994, 1012], fill=(200, 200, 205))
    rnd = random.Random(5)
    x = 440
    i = 0
    while x < 930:
        w = rnd.randrange(70, 110); hmax = rnd.randrange(160, 380)
        h = hmax * back((t - 0.15 * i) / 0.5)
        if h > 2:
            col = rnd.choice([(120, 130, 160), (160, 140, 170), (110, 150, 170), (170, 160, 140)])
            M.box(d, x, 1000 - h, w, h, 36, col)
            for wy in range(int(1000 - h + 20), 990, 40):
                for wx in range(x + 12, x + w - 16, 26): d.rectangle([wx, wy, wx + 12, wy + 18], fill=(255, 230, 150))
        x += w + 18; i += 1
    pill(d, "2001 · ERSTMALS 3D", 710, 600, 38, YEL, INK, back(t / 0.4))
    timeline(d, t, 1)
    return (710, 820)

def g_2002(im, d, t, dur):
    b = main_card(d, (30, 18, 60))
    # striped sun
    cx, cy, r = 710, 820, 190
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 120, 160))
    d.chord([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(255, 190, 90))
    for k in range(5):
        y = cy + 20 + k * 30
        d.rectangle([cx - r, y, cx + r, y + 8 + k * 2], fill=(30, 18, 60))
    # horizon + grid
    hy = 900
    d.rectangle([426, hy, 994, 1174], fill=(40, 10, 70))
    d.line([(426, hy), (994, hy)], fill=(255, 80, 200), width=6)
    for i in range(-6, 7):
        x0, x1 = 710 + i * 30, 710 + i * 140
        y1 = 1174
        if x1 < 430 or x1 > 990:
            xb = 430 if x1 < 430 else 990
            y1 = hy + (1174 - hy) * (xb - x0) / (x1 - x0); x1 = xb
        d.line([(x0, hy), (x1, y1)], fill=(255, 80, 200), width=3)
    for k in range(6):
        f = ((k + t * 1.2) % 6) / 6
        y = hy + (1174 - hy) * f ** 2
        d.line([(426, y), (994, y)], fill=(80, 220, 255), width=3)
    for px, s in [(470, 0.75), (950, 0.65)]:
        M.palm(d, px, 1150, s, math.sin(t * 2))
    pill(d, "2002", 520, 590, 40, CYAN, INK, back(t / 0.4))
    timeline(d, t, 2)
    return (710, 820)

def g_2004(im, d, t, dur):
    b = main_card(d, (225, 200, 150))
    for mx in (520, 600, 680):
        d.polygon([(mx - 90, 760), (mx, 620), (mx + 90, 760)], fill=(140, 130, 120), outline=INK)
        d.polygon([(mx - 25, 660), (mx, 620), (mx + 25, 660)], fill="white")
    pts = {"LS": (850, 1050), "SF": (520, 900), "LV": (900, 700)}
    order = [("LS", "SF"), ("SF", "LV"), ("LV", "LS")]
    for i, (a, bb) in enumerate(order):
        p = ease((t - 0.6 - i * 0.4) / 0.4)
        if p > 0:
            ax, ay = pts[a]; bx, by = pts[bb]
            d.line([(ax, ay), (lerp(ax, bx, p), lerp(ay, by, p))], fill=(90, 90, 100), width=16)
    for i, (n, (x, y)) in enumerate(pts.items()):
        s = back((t - 0.2 * i) / 0.35)
        if s > 0.05:
            d.ellipse([x - 40 * s, y - 40 * s, x + 40 * s, y + 40 * s], fill=RED, outline=INK, width=5)
            label(d, n, x, y + 2, 34 * s, stroke=4)
    pill(d, "2004 · 3 STÄDTE", 710, 600, 38, YEL, INK, back(t / 0.4))
    timeline(d, t, 3)
    k = min(2, int(max(0, t - 0.2) / 0.5)); return list(pts.values())[k]

def g_2013(im, d, t, dur):
    b = main_card(d, (70, 140, 90))
    V.trophy(d, 710, 840, back(t / 0.5) * 0.95)
    sparkle_field(d, t, (440, 570, 980, 1150), 10, 7)
    v = int(countup(t, 0.6, 2.2, 230))
    pill(d, f"{v} MIO. VERKAUFT", 710, 1100, 40, YEL, INK, back((t - 0.5) / 0.4))
    pill(d, "2013", 520, 590, 40, CYAN, INK, back(t / 0.4))
    timeline(d, t, 4)
    return (710, 840)

def g_2026(im, d, t, dur):
    b = main_card(d, (255, 160, 120))
    s = back(t / 0.5)
    if s > 0.05: M.calendar(d, 710, 850, 0.95 * s, "NOVEMBER", "19")
    confetti(d, t, 0.6, (430, 560, 990, 1170))
    timeline(d, t, 5)
    return (710, 850)

# =============== Reel 07: GTA 5 Rekorde ===============
def r_intro(im, d, t, dur):
    for i, (x, y, s) in enumerate([(500, 1010, 0.5), (920, 1010, 0.5), (710, 800, 0.95)]):
        V.trophy(d, x, y, back((t - 0.25 * i) / 0.45) * s)
    sparkle_field(d, t, (430, 540, 1000, 1200), 14, 2)
    for i in range(5):
        a = t * 1.5 + i * 2 * math.pi / 5
        star(d, 710 + math.cos(a) * 300, 760 + math.sin(a) * 120, 22, YEL)
    return (710, 800)

def r_day1(im, d, t, dur):
    b = main_card(d)
    pill(d, "1. VERKAUFSTAG", 710, 610, 38, YEL, INK, back(t / 0.4))
    v = int(countup(t, 0.3, 2.2, 800))
    label(d, f"{v} Mio. $", 710, 770, 92, GRN, 8)
    rnd = random.Random(4)
    for i in range(14):
        x = rnd.randrange(460, 960); sp = rnd.uniform(120, 220)
        y = 880 + ((t * sp + rnd.randrange(300)) % 280)
        V.bill(d, x + math.sin(t * 3 + i) * 20, y, math.sin(t * 2 + i) * 0.7, 0.9)
    return (710, 780)

def r_3days(im, d, t, dur):
    for i in range(3):
        s = back((t - 0.4 * i) / 0.35)
        if s > 0.05: M.calendar(d, 530 + i * 180, 720, 0.4 * s, "TAG", str(i + 1), (230, 60, 60) if i < 2 else (40, 170, 90))
    p = ease((t - 0.3) / 1.8)
    card(d, (440, 960, 980, 1060), (255, 255, 255), 50)
    if p > 0.02: d.rounded_rectangle([450, 970, 450 + 520 * p, 1050], 42, fill=GRN)
    label(d, f"{p:.0%}".replace("%", " %"), 710, 1010, 44, (255, 255, 255), 6)
    if p >= 0.99:
        pill(d, "1 MILLIARDE $", 710, 1150, 46, YEL, INK, back((t - 2.1) / 0.4))
        check_icon(d, 960, 950, back((t - 2.1) / 0.3) * 1.2)
    k = min(2, int(max(0, t) / 0.4)); return (530 + k * 180, 720) if t < 1.4 else (710, 1010)

def medal(d, cx, cy, s):
    if s <= 0.05: return
    d.polygon([(cx - 90 * s, cy - 300 * s), (cx - 10 * s, cy - 300 * s), (cx + 40 * s, cy - 60 * s), (cx - 40 * s, cy - 60 * s)], fill=(220, 60, 80), outline=INK)
    d.polygon([(cx + 90 * s, cy - 300 * s), (cx + 10 * s, cy - 300 * s), (cx - 40 * s, cy - 60 * s), (cx + 40 * s, cy - 60 * s)], fill=(60, 110, 220), outline=INK)
    r = 140 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 195, 50), outline=INK, width=6)
    d.ellipse([cx - r * .75, cy - r * .75, cx + r * .75, cy + r * .75], fill=(255, 215, 90))
    star(d, cx, cy, r * .55, (230, 160, 30))

def r_record(im, d, t, dur):
    medal(d, 710, 880, back(t / 0.5) * 1.2)
    confetti(d, t, 0.5)
    pill(d, "SCHNELLSTE MILLIARDE", 710, 1150, 40, YEL, INK, back((t - 0.6) / 0.4))
    return (710, 880)

def r_sales(im, d, t, dur):
    n = int(ease(t / 3.0) * 15)
    cols = [(40, 120, 200), (230, 70, 110), (60, 170, 110)]
    for i in range(n):
        row, cl = divmod(i, 5)
        V.game_case(d, 450 + cl * 108 + (row % 2) * 20, 1230 - row * 175, 92, 150, cols[i % 3], "V")
    v = int(countup(t, 0, 3.0, 230))
    label(d, f"{v} Mio.", 710, 620, 120, (255, 255, 255), 10)
    return (710, 1230 - max(0, (n - 1) // 5) * 175 - 80)

def r_years(im, d, t, dur):
    b = main_card(d)
    d.rectangle([426, 546, 994, 680], fill=(230, 60, 60))
    label(d, "GTA 5 IST SCHON", 710, 615, 44, (255, 255, 255), 6)
    y = 2013 + int(13 * ease((t - 0.3) / 2.2))
    label(d, str(y), 710, 860, 170, INK, 0)
    pill(d, "13 JAHRE ALT", 710, 1080, 46, YEL, INK, back((t - 2.4) / 0.4))
    return (710, 860)

def r_outro(im, d, t, dur):
    b = main_card(d, (40, 30, 80), (420, 540, 1000, 960))
    label(d, "GTA 6?", 710, 750, 150, YEL, 10)
    return (710, 750)

# =============== Reel 08: Echt vs. Spiel ===============
def e_intro(im, d, t, dur):
    for i, (txt, col, x) in enumerate([("ECHT", CYAN, 560), ("SPIEL", PINK, 860)]):
        s = back((t - 0.25 * i) / 0.4)
        if s > 0.05:
            card(d, (x - 130 * s, 830 - 160 * s, x + 130 * s, 830 + 160 * s), col)
            label(d, txt, x, 830, 54 * s, (255, 255, 255), 7)
    s = 1 + 0.15 * math.sin(t * 6)
    label(d, "≈", 710, 830, 120 * s, YEL, 8)
    V.qmark(d, 560, 600 + math.sin(t * 4) * 10, back((t - 0.8) / 0.3)); V.qmark(d, 860, 600 + math.cos(t * 4) * 10, back((t - 1.0) / 0.3))
    return (710, 760)

def e_florida(im, d, t, dur):
    b = main_card(d, (90, 170, 215))
    leonida_map(d, t, 720, 870, 0.62 * (0.85 + 0.15 * back(t / 0.5)))
    pill(d, "FLORIDA  =  LEONIDA", 710, 1110, 40, YEL, INK, back((t - 0.6) / 0.4))
    return (720, 850)

def skyline(d, x0, x1, base, seed, cols, win=(255, 225, 150)):
    rnd = random.Random(seed); x = x0
    while x < x1 - 40:
        w = rnd.randrange(50, 90); h = rnd.randrange(150, 330)
        w = min(w, x1 - x); c = rnd.choice(cols)
        d.rectangle([x, base - h, x + w, base], fill=c, outline=INK, width=3)
        for wy in range(base - h + 16, base - 20, 34):
            for wx in range(x + 10, x + w - 12, 22): d.rectangle([wx, wy, wx + 10, wy + 16], fill=win)
        x += w + 8

def two_panel(d, t, left, right, lname, rname):
    card(d, (420, 540, 1000, 1180), (255, 255, 255))
    d.rectangle([426, 546, 707, 1174], fill=left); d.rectangle([713, 546, 994, 1174], fill=right)
    d.line([(710, 546), (710, 1174)], fill=INK, width=6)
    pill(d, lname, 566, 1110, 34, (255, 255, 255), INK, back((t - 0.3) / 0.4))
    pill(d, rname, 853, 1110, 34, YEL, INK, back((t - 0.6) / 0.4))
    a = ease((t - 0.9) / 0.4)
    if a > 0:
        d.ellipse([710 - 42 * a, 600 - 42 * a, 710 + 42 * a, 600 + 42 * a], fill=PINK, outline=INK, width=4)
        d.polygon([(690, 600 - 16 * a), (690 + 0, 600 + 16 * a), (690 + 0, 600 + 16 * a)], fill="white"); d.line([(688 - 18 * a, 600), (720 + 10 * a, 600)], fill="white", width=max(1, int(9 * a))); d.polygon([(735 * 1 + 0 * a, 600), (712, 600 - 16 * a), (712, 600 + 16 * a)], fill="white")

def e_miami(im, d, t, dur):
    two_panel(d, t, (130, 190, 240), (120, 60, 140), "MIAMI", "VICE CITY")
    d.ellipse([500, 620, 580, 700], fill=(255, 230, 120))
    d.ellipse([800, 640, 900, 740], fill=(255, 170, 110))
    skyline(d, 432, 702, 1060, 3, [(150, 160, 190), (120, 140, 170), (180, 180, 200)])
    skyline(d, 718, 990, 1060, 3, [(170, 90, 170), (130, 70, 150), (200, 110, 170)])
    M.palm(d, 690, 1070, 0.45, math.sin(t * 2)); M.palm(d, 975, 1070, 0.45, -math.sin(t * 2))
    return (710, 850)

def e_swamp(im, d, t, dur):
    b = main_card(d, (150, 190, 160))
    d.rectangle([426, 840, 994, 1174], fill=(70, 110, 80))
    for k in range(6):
        y = 870 + k * 50; off = (t * 30 + k * 40) % 160
        for x in range(400, 1000, 160):
            if 430 < x + off < 930: d.line([(x + off, y), (x + off + 60, y)], fill=(100, 140, 105), width=4)
    for x in range(440, 990, 45): d.line([(x, 850), (x + math.sin(t * 2 + x) * 8, 780 + (x * 37) % 50)], fill=(80, 120, 60), width=6)
    ax = 990 - ease(t / 2.2) * 560
    jaw = max(0, math.sin((t - 2.3) * 6)) if t > 2.3 else 0
    V.alligator(d, max(440, ax), 1000, 0.85, jaw)
    pill(d, "EVERGLADES = GRASSRIVERS", 710, 610, 30, YEL, INK, back((t - 0.3) / 0.4))
    return (max(430, ax) + 300, 960)

def e_keys(im, d, t, dur):
    b = main_card(d, (70, 160, 210))
    d.rectangle([426, 546, 994, 700], fill=(160, 210, 240))
    d.line([(426, 840), (994, 800)], fill=(230, 230, 235), width=16)
    for x in range(450, 990, 70): d.line([(x, 838 - (x - 426) * 0.07), (x, 900)], fill=(190, 190, 200), width=7)
    for cx, cy, r in [(520, 1000, 70), (680, 960, 90), (870, 1010, 100)]:
        d.ellipse([cx - r, cy - r * .35, cx + r, cy + r * .35], fill=(235, 210, 150), outline=INK, width=3)
        M.palm(d, cx, cy, 0.4, math.sin(t * 2 + cx))
    bx = 430 + (t * 160) % 520
    d.polygon([(bx, 1110), (bx + 90, 1110), (bx + 110, 1090), (bx - 10, 1090)], fill=(250, 250, 250), outline=INK)
    pill(d, "KEYS = LEONIDA KEYS", 710, 610, 34, YEL, INK, back((t - 0.3) / 0.4))
    return (680, 960)

def laugh_face(d, cx, cy, s):
    if s <= 0.05: return
    r = 120 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 210, 70), outline=INK, width=6)
    for ex in (-0.4, 0.4):
        d.arc([cx + ex * r - 30 * s, cy - 50 * s, cx + ex * r + 30 * s, cy - 10 * s], 200, 340, fill=INK, width=max(2, int(10 * s)))
    d.chord([cx - 70 * s, cy - 10 * s, cx + 70 * s, cy + 90 * s], 0, 180, fill=(120, 40, 50), outline=INK)
    d.ellipse([cx - r * .95, cy - 25 * s, cx - r * .7, cy + 20 * s], fill=(120, 200, 255))

def e_parody(im, d, t, dur):
    b = main_card(d)
    for i, (txt, ok) in enumerate([("1:1 KOPIE", False), ("PARODIE", True)]):
        y = 640 + i * 150
        label(d, txt, 640, y, 56, INK if ok else (150, 150, 160), 0)
        s = back((t - 0.6 - 0.6 * i) / 0.3)
        (check_icon if ok else x_icon)(d, 900, y, s * 1.2)
    laugh_face(d, 710, 1040, back((t - 1.6) / 0.4) * (1 + 0.05 * math.sin(t * 12)))
    return (900, 790) if t > 1.2 else (900, 640)

def e_outro(im, d, t, dur):
    b = main_card(d, (90, 170, 215), (420, 540, 1000, 960))
    P = leonida_map(d, t, 710, 760, 0.38)
    for i, (n, p) in enumerate(V.REGIONS):
        x, y = P(p); s = back((t - 0.15 * i) / 0.3)
        if s > 0.05: d.ellipse([x - 14 * s, y - 14 * s, x + 14 * s, y + 14 * s], fill=RED, outline="white", width=3)
    return (710, 760)

# =============== Reel 09: Checkliste ===============
ROWS = ["Release 19.11.", "Preload läuft!", "PS5 & Xbox Series", "Preis 79,99 €", "Code statt Disc"]
def clipboard(d, t, done, cur, cur_t, slide=1.0):
    off = (1 - slide) * 700
    x0, y0, x1, y1 = 420 + off, 520, 1000 + off, 1360
    card(d, (x0, y0, x1, y1), (150, 105, 70))
    d.rounded_rectangle([x0 + 26, y0 + 60, x1 - 26, y1 - 26], 20, fill=(252, 250, 245))
    d.rounded_rectangle([x0 + 190, y0 - 26, x1 - 190, y0 + 60], 18, fill=(150, 150, 160), outline=INK, width=5)
    for i, txt in enumerate(ROWS):
        y = y0 + 160 + i * 150
        if i == cur:
            hp = ease(cur_t / 0.4)
            d.rounded_rectangle([x0 + 40, y - 52, x0 + 40 + (x1 - x0 - 80) * hp, y + 52], 20, fill=(255, 235, 150))
        d.rounded_rectangle([x0 + 50, y - 30, x0 + 110, y + 30], 12, outline=INK, width=6, fill="white")
        if i < done or (i == cur and cur_t > 0.6):
            s = back((cur_t - 0.6) / 0.3) if i == cur else 1
            if s > 0.05:
                d.line([(x0 + 58, y), (x0 + 78, y + 22), (x0 + 125, y - 40)], fill=GRN, width=max(2, int(14 * s)), joint="curve")
        col = INK if (i < done or i == cur) else (175, 175, 185)
        d.text((x0 + 140, y), txt, font=F(40), fill=col, anchor="lm")
    return (x0 + 300, y0 + 160 + max(0, cur) * 150)

def c_scene(i):
    def f(im, d, t, dur):
        if i == 0:
            return clipboard(d, t, 0, -1, 0, ease(t / 0.7))
        if i == 6:
            return clipboard(d, t, 5, -1, 0)
        return clipboard(d, t, i - 1, i - 1, t)
    return f

# =============== Reel 10: Lucia & Jason ===============
def silhouette(d, cx, cy, s, long_hair=False, col=INK):
    if s <= 0.05: return
    if long_hair:
        d.rounded_rectangle([cx - 85 * s, cy - 120 * s, cx + 85 * s, cy + 60 * s], int(60 * s), fill=col)
    d.ellipse([cx - 70 * s, cy - 130 * s, cx + 70 * s, cy + 20 * s], fill=col)
    d.chord([cx - 150 * s, cy + 30 * s, cx + 150 * s, cy + 330 * s], 180, 360, fill=col)
    d.rectangle([cx - 30 * s, cy, cx + 30 * s, cy + 60 * s], fill=col)

def person_card(d, cx, cy, s, name, col, long_hair):
    if s <= 0.05: return
    card(d, (cx - 140 * s, cy - 210 * s, cx + 140 * s, cy + 210 * s), col)
    silhouette(d, cx, cy - 20 * s, s, long_hair, sh(col, 0.45))
    d.rectangle([cx - 134 * s, cy + 130 * s, cx + 134 * s, cy + 204 * s], fill=INK)
    label(d, name, cx, cy + 168 * s, 44 * s, (255, 255, 255), 0)

def l_intro(im, d, t, dur):
    person_card(d, 565, 800, back(t / 0.45), "LUCIA", PINK, True)
    person_card(d, 855, 800, back((t - 0.25) / 0.45), "JASON", CYAN, False)
    for x, k in ((565, 0), (855, 1)):
        V.qmark(d, x, 560 + math.sin(t * 4 + k) * 12, back((t - 0.8 - 0.2 * k) / 0.3))
    return (710, 800)

def glove(d, cx, cy, s, flip=1):
    r = 95 * s
    d.ellipse([cx - r, cy - r * 0.85, cx + r, cy + r * 0.85], fill=RED, outline=INK, width=6)
    d.ellipse([cx - flip * r * 0.9 - 40 * s, cy - 20 * s, cx - flip * r * 0.9 + 40 * s, cy + 60 * s], fill=sh(RED, 0.9), outline=INK, width=5)
    d.rounded_rectangle([cx + flip * r * 0.6 - (0 if flip > 0 else 90 * s), cy - 55 * s, cx + flip * r * 0.6 + (90 * s if flip > 0 else 0), cy + 55 * s], 20, fill=(250, 250, 250), outline=INK, width=5)

def burst(d, cx, cy, r, col=YEL, n=12):
    pts = []
    for i in range(n * 2):
        a = i * math.pi / n; rr = r if i % 2 == 0 else r * 0.55
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=col, outline=INK)

def l_fighter(im, d, t, dur):
    person_card(d, 830, 800, 0.85, "LUCIA", PINK, True)
    ph = (t * 1.6) % 1
    px = 520 + 140 * math.sin(ph * math.pi) ** 2
    if t > 0.3:
        glove(d, px, 760, 1.15, -1)
        if 0.35 < ph < 0.65: burst(d, px + 120, 720, 70); label(d, "POW", px + 120, 720, 30, INK, 0)
    pill(d, "KAMPFTRAINING", 710, 1130, 40, YEL, INK, back((t - 0.4) / 0.4))
    return (px, 760)

def l_prison(im, d, t, dur):
    person_card(d, 710, 820, 1.1, "LUCIA", PINK, True)
    down = ease((t - 0.4) / 0.6); up = ease((t - 3.2) / 0.6)
    yb = 820 - 230 * 1.1 - 330 + 330 * down - 420 * up
    for x in range(560, 880, 52):
        d.rectangle([x, yb, x + 18, yb + 470], fill=(120, 125, 135), outline=INK, width=3)
    d.rectangle([550, yb + 40, 880, yb + 66], fill=(120, 125, 135), outline=INK, width=3)
    pill(d, "GEFÄNGNIS" if t < 3.2 else "FREI!", 710, 1150, 42, YEL if t < 3.2 else GRN, INK, back((t - 0.6) / 0.4))
    return (710, 820)

def helmet(d, cx, cy, s):
    if s <= 0.05: return
    c = (95, 115, 70)
    d.chord([cx - 150 * s, cy - 140 * s, cx + 150 * s, cy + 140 * s], 180, 360, fill=c, outline=INK, width=6)
    d.rounded_rectangle([cx - 180 * s, cy - 10 * s, cx + 180 * s, cy + 30 * s], 16, fill=sh(c, 0.85), outline=INK, width=5)
    for k in range(4):
        d.ellipse([cx - 90 * s + k * 55 * s, cy - 90 * s + (k % 2) * 30 * s, cx - 60 * s + k * 55 * s, cy - 60 * s + (k % 2) * 30 * s], fill=sh(c, 0.75))

def l_army(im, d, t, dur):
    person_card(d, 860, 820, 0.8, "JASON", CYAN, False)
    helmet(d, 560, 760 + math.sin(t * 3) * 8, back((t - 0.3) / 0.45))
    medal(d, 560, 1040, back((t - 1.0) / 0.45) * 0.5)
    pill(d, "ARMEE", 560, 610, 40, YEL, INK, back((t - 0.2) / 0.4))
    return (560, 760)

def l_keys(im, d, t, dur):
    b = main_card(d, (70, 160, 210))
    d.rectangle([426, 546, 994, 700], fill=(255, 190, 140))
    for cx, cy, r in [(560, 820, 110), (860, 880, 90)]:
        d.ellipse([cx - r, cy - r * .35, cx + r, cy + r * .35], fill=(235, 210, 150), outline=INK, width=3)
        M.palm(d, cx, cy, 0.45, math.sin(t * 2 + cx))
    bx = 990 - (t * 200) % 600
    d.polygon([(bx, 1060), (bx + 150, 1060), (bx + 120, 1100), (bx + 10, 1100)], fill=(250, 250, 250), outline=INK)
    d.rectangle([bx + 50, 1025, bx + 100, 1060], fill=(40, 40, 50))
    for k in range(4): d.line([(bx + 160 + k * 40, 1080 + k * 5), (bx + 190 + k * 40, 1080 + k * 5)], fill=(220, 240, 255), width=5)
    pill(d, "JASON · DIE KEYS", 710, 610, 36, YEL, INK, back((t - 0.3) / 0.4))
    return (bx + 75, 1060)

def l_duo(im, d, t, dur):
    p = ease(t / 0.8)
    person_card(d, lerp(450, 575, p), 820, 0.9, "LUCIA", PINK, True)
    person_card(d, lerp(980, 855, p), 820, 0.9, "JASON", CYAN, False)
    if t > 0.8:
        s = 1 + 0.2 * math.sin(t * 14)
        d.polygon([(715, 620), (680, 760), (720, 760), (690, 900), (760, 720), (720, 720), (750, 620)], fill=YEL, outline=INK)
    pill(d, "EIN TEAM", 715, 1130, 46, YEL, INK, back((t - 0.9) / 0.4))
    return (715, 760)

def l_outro(im, d, t, dur):
    person_card(d, 565, 760, 0.7, "LUCIA", PINK, True)
    person_card(d, 855, 760, 0.7, "JASON", CYAN, False)
    label(d, "VS", 710, 760, 70 * (1 + 0.1 * math.sin(t * 8)), YEL, 8)
    return (710, 760)

# =============== definitions ===============
# scene: (dur, theme, fn, [(t, word, color)], pose_intro)
R = {
"06_GTA_Geschichte": [
    (4.0, "purple", g_intro, [(0, "SEIT 1997", PINK)], "wave"),
    (4.5, "sky", g_1997, [(0, "1997", CYAN)], "point"),
    (4.0, "sky", g_2001, [(0, "ERSTMALS 3D", PINK)], "point"),
    (4.5, "night", g_2002, [(0, "VICE CITY", PINK)], "point"),
    (4.5, "sunset", g_2004, [(0, "SAN ANDREAS", CYAN)], "point"),
    (4.0, "mint", g_2013, [(0, "GTA 5", PINK)], "point"),
    (4.5, "sunset", g_2026, [(0, "GTA 6", PINK), (2.3, "FOLGT FÜR MEHR", PINK)], "cheer"),
],
"07_GTA5_Rekorde": [
    (4.0, "gold", r_intro, [(0, "REKORDE", PINK)], "wave"),
    (4.5, "mint", r_day1, [(0, "800 MIO. $", GRN)], "point"),
    (4.5, "sky", r_3days, [(0, "3 TAGE", CYAN)], "point"),
    (4.5, "gold", r_record, [(0, "WELTREKORD", PINK)], "cheer"),
    (4.5, "purple", r_sales, [(0, "230 MILLIONEN", CYAN)], "point"),
    (4.0, "sky", r_years, [(0, "13 JAHRE", PINK)], "point"),
    (4.0, "night", r_outro, [(0, "UND GTA 6?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"08_Echt_vs_Spiel": [
    (4.0, "purple", e_intro, [(0, "ECHTES VORBILD", PINK)], "wave"),
    (4.0, "ocean", e_florida, [(0, "FLORIDA", CYAN)], "point"),
    (4.0, "sunset", e_miami, [(0, "MIAMI", PINK)], "point"),
    (5.0, "mint", e_swamp, [(0, "EVERGLADES", GRN)], "point"),
    (4.5, "ocean", e_keys, [(0, "FLORIDA KEYS", CYAN)], "point"),
    (4.5, "gold", e_parody, [(0, "PARODIE", PINK)], "point"),
    (4.0, "night", e_outro, [(0, "WOHIN ZUERST?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"09_Release_Checkliste": [
    (4.0, "purple", c_scene(0), [(0, "CHECKLISTE", PINK)], "wave"),
    (4.0, "sky", c_scene(1), [(0, "19. NOVEMBER", CYAN)], "point"),
    (4.0, "mint", c_scene(2), [(0, "PRELOAD", GRN)], "point"),
    (5.0, "night", c_scene(3), [(0, "PS5 & XBOX", CYAN)], "point"),
    (4.5, "gold", c_scene(4), [(0, "79,99 €", PINK)], "point"),
    (4.5, "sunset", c_scene(5), [(0, "NUR CODE", PINK)], "point"),
    (4.0, "purple", c_scene(6), [(0, "SPEICHERN!", CYAN), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"10_Lucia_und_Jason": [
    (4.0, "purple", l_intro, [(0, "LUCIA & JASON", PINK)], "wave"),
    (4.5, "sunset", l_fighter, [(0, "KÄMPFERIN", PINK)], "point"),
    (5.0, "night", l_prison, [(0, "GEFÄNGNIS", CYAN)], "point"),
    (4.5, "mint", l_army, [(0, "ARMEE", GRN)], "point"),
    (4.0, "ocean", l_keys, [(0, "DIE KEYS", CYAN)], "point"),
    (4.0, "gold", l_duo, [(0, "EIN DUO", PINK)], "cheer"),
    (4.0, "night", l_outro, [(0, "DEIN FAVORIT?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
}

def frame(vid, idx, t):
    dur, theme, fn, words, pose0 = R[vid][idx]
    gt = sum(s[0] for s in R[vid][:idx]) + t
    fr = bg(theme).copy(); d = ImageDraw.Draw(fr)
    particles(d, gt, theme)
    target = fn(fr, d, t, dur)
    last = idx == len(R[vid]) - 1
    cur = [w for w in words if w[0] <= t][-1]
    ot = (t - cur[0]) if (last and cur[1] == "FOLGT FÜR MEHR") else None
    if ot is not None:
        # dim the main graphic a bit and show follow button
        target = outro(d, fr, ot)
    pose = pose0
    if pose0 == "wave" and t > 1.6: pose = "point"
    if pose0 == "cheer" and ot is not None: pose = "point"
    draw_character(fr, t, gt, pose, target)
    # word sticker
    st = sticker(cur[1], cur[2])
    s = back((t - cur[0]) / 0.25)
    if s > 0.03:
        ang = -3 + 4 * (1 - ease((t - cur[0]) / 0.35)) + math.sin(gt * 2) * 1.2
        r = st.resize((max(1, int(st.width * s)), max(1, int(st.height * s))), Image.BILINEAR).rotate(ang, expand=True, resample=Image.BICUBIC)
        fr.paste(r, (int(W / 2 - r.width / 2), int(380 - r.height / 2)), r)
    # transition wipe
    if idx > 0 and t < 0.3:
        p = t / 0.3
        x = -300 + p * (W + 600)
        d = ImageDraw.Draw(fr)
        d.polygon([(x - 260, 0), (x + 120, 0), (x - 120, H), (x - 500, H)], fill=YEL)
        d.polygon([(x - 380, 0), (x - 260, 0), (x - 500, H), (x - 620, H)], fill=PINK)
    return fr

def render(vid, idx):
    dur = R[vid][idx][0]; n = int(round(dur * FPS))
    od = os.path.join(OUT, "_scenes", vid); os.makedirs(od, exist_ok=True)
    tmp = os.path.join(od, f"s{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(vid, idx, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(od, f"s{idx}.mp4"))

# ---------------- sound effects ----------------
SR = 44100
def sfx(vid):
    total = max(30.0, sum(x[0] for x in R[vid]) + 1.0) if vid in R else 30.0; a = np.zeros(int(SR * total))
    rng = np.random.default_rng(1)
    def add(sig, t0):
        i = int(t0 * SR); j = min(len(a), i + len(sig))
        if j > i: a[i:j] += sig[: j - i]
    # whoosh
    n = int(0.35 * SR); tt = np.arange(n) / SR
    noise = rng.standard_normal(n)
    k = 30; sm = np.convolve(noise, np.ones(k) / k, mode="same")
    env = np.sin(np.pi * np.clip(tt / 0.35, 0, 1)) ** 2
    whoosh = (sm * env) * 0.9
    # pop
    m = int(0.12 * SR); tp = np.arange(m) / SR
    freq = 900 * np.exp(-tp * 18) + 250
    pop = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tp * 30) * 0.5
    # ding
    q = int(0.7 * SR); tq = np.arange(q) / SR
    ding = (np.sin(2 * np.pi * 1320 * tq) + 0.6 * np.sin(2 * np.pi * 1980 * tq)) * np.exp(-tq * 5) * 0.3
    t0 = 0
    for i, (dur, _, _, words, _) in enumerate(R[vid]):
        if i > 0: add(whoosh, t0)
        for (wt, w, _) in words:
            add(pop, t0 + wt + 0.03)
            if w == "FOLGT FÜR MEHR": add(ding, t0 + wt + 0.3)
        t0 += dur
    a = np.clip(a * 0.55, -1, 1)
    st = (np.stack([a, a], axis=1) * 32767).astype(np.int16)
    path = os.path.join(OUT, "_scenes", vid, "sfx.wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    return path

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        vid = sys.argv[2]
        ims = [frame(vid, i, R[vid][i][0] * (0.9 if i == len(R[vid]) - 1 else 0.6)).resize((270, 480)) for i in range(len(R[vid]))]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(HERE, f"p2_{vid}.png"))
    elif cmd == "render":
        render(sys.argv[2], int(sys.argv[3]))
    elif cmd == "jobs":
        for v in R:
            for i in range(len(R[v])): print(v, i)
    elif cmd == "sfx":
        print(sfx(sys.argv[2]))
