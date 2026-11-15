import scenes2 as S2
from scenes2 import *

# ---------------- new primitives ----------------
def console(d, cx, cy, s):
    if s <= 0.05: return
    M.box(d, cx - 160 * s, cy - 50 * s, 320 * s, 100 * s, 90 * s, (240, 240, 245))
    d.rectangle([cx - 140 * s, cy - 20 * s, cx - 60 * s, cy - 10 * s], fill=(60, 140, 255))

def dl_bar(d, x0, y, x1, p, txt=None, col=GRN):
    card(d, (x0, y - 40, x1, y + 40), (255, 255, 255), 40, 8)
    if p > 0.01: d.rounded_rectangle([x0 + 8, y - 32, x0 + 8 + (x1 - x0 - 16) * p, y + 32], 32, fill=col)
    label(d, txt if txt else f"{int(p * 100)} %", (x0 + x1) / 2, y, 36, (255, 255, 255), 6)

def ssd(d, cx, cy, s, p):
    if s <= 0.05: return
    w, h = 420 * s, 220 * s
    card(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), (45, 45, 60), int(30 * s), int(10 * s))
    d.rectangle([cx - w / 2 + 30 * s, cy - h / 2 + 30 * s, cx - w / 2 + 120 * s, cy - h / 2 + 70 * s], fill=YEL)
    for k in range(4): d.rectangle([cx + w / 2 - 40 * s - k * 30 * s, cy + h / 2 - 22 * s, cx + w / 2 - 25 * s - k * 30 * s, cy + h / 2 - 2 * s], fill=(200, 170, 60))
    bx0, bx1 = cx - w / 2 + 30 * s, cx + w / 2 - 30 * s
    d.rounded_rectangle([bx0, cy + 10 * s, bx1, cy + 50 * s], int(18 * s), fill=(80, 80, 100))
    if p > 0.01: d.rounded_rectangle([bx0, cy + 10 * s, bx0 + (bx1 - bx0) * p, cy + 50 * s], int(18 * s), fill=PINK if p > 0.85 else CYAN)

def padlock(d, cx, cy, s, open_p=0.0):
    if s <= 0.05: return
    lift = 60 * s * open_p
    d.arc([cx - 90 * s, cy - 190 * s - lift, cx + 90 * s, cy - 10 * s - lift], 180, 360, fill=(170, 170, 185), width=int(36 * s))
    d.line([(cx - 72 * s, cy - 100 * s - lift), (cx - 72 * s, cy - 40 * s)], fill=(170, 170, 185), width=int(36 * s))
    d.line([(cx + 72 * s, cy - 100 * s - lift), (cx + 72 * s, cy - 40 * s + (0 if open_p < 0.5 else -60 * s))], fill=(170, 170, 185), width=int(36 * s))
    card(d, (cx - 140 * s, cy - 60 * s, cx + 140 * s, cy + 160 * s), YEL, int(30 * s), int(10 * s))
    d.ellipse([cx - 25 * s, cy + 15 * s, cx + 25 * s, cy + 65 * s], fill=INK)
    d.rectangle([cx - 10 * s, cy + 50 * s, cx + 10 * s, cy + 110 * s], fill=INK)

def trash(d, cx, cy, s, lid=0.0):
    d.polygon([(cx - 70 * s, cy - 60 * s), (cx + 70 * s, cy - 60 * s), (cx + 55 * s, cy + 100 * s), (cx - 55 * s, cy + 100 * s)], fill=(150, 160, 175), outline=INK)
    for k in (-30, 0, 30): d.line([(cx + k * s, cy - 40 * s), (cx + k * s * 0.85, cy + 85 * s)], fill=INK, width=max(1, int(6 * s)))
    a = -lid * 0.9
    p0 = (cx - 80 * s, cy - 70 * s)
    pts = [(0, 0), (160, 0), (160, -18), (0, -18)]
    rp = [(p0[0] + (x * math.cos(a) - y * math.sin(a)) * s, p0[1] + (x * math.sin(a) + y * math.cos(a)) * s) for x, y in pts]
    d.polygon(rp, fill=(130, 140, 155), outline=INK)

def rocket(d, cx, cy, s, t):
    fl = 1 + 0.25 * math.sin(t * 40)
    d.polygon([(cx - 40 * s, cy + 110 * s), (cx + 40 * s, cy + 110 * s), (cx, cy + (110 + 140 * fl) * s)], fill=(255, 150, 50))
    d.polygon([(cx - 22 * s, cy + 110 * s), (cx + 22 * s, cy + 110 * s), (cx, cy + (110 + 80 * fl) * s)], fill=(255, 235, 120))
    d.polygon([(cx - 60 * s, cy + 40 * s), (cx - 110 * s, cy + 130 * s), (cx - 50 * s, cy + 110 * s)], fill=RED, outline=INK)
    d.polygon([(cx + 60 * s, cy + 40 * s), (cx + 110 * s, cy + 130 * s), (cx + 50 * s, cy + 110 * s)], fill=RED, outline=INK)
    d.rounded_rectangle([cx - 60 * s, cy - 120 * s, cx + 60 * s, cy + 120 * s], int(50 * s), fill=(245, 245, 250), outline=INK, width=5)
    d.polygon([(cx - 58 * s, cy - 90 * s), (cx, cy - 210 * s), (cx + 58 * s, cy - 90 * s)], fill=RED, outline=INK)
    d.ellipse([cx - 30 * s, cy - 50 * s, cx + 30 * s, cy + 10 * s], fill=CYAN, outline=INK, width=5)

def stock_chart(d, b, t, t0=0.3, dur=2.0, pts=None, col=GRN):
    x0, y0, x1, y1 = b
    card(d, b, (255, 255, 255))
    for k in range(1, 4):
        y = y0 + (y1 - y0) * k / 4; d.line([(x0 + 20, y), (x1 - 20, y)], fill=(225, 228, 235), width=3)
    pts = pts or [0.25, 0.3, 0.22, 0.35, 0.3, 0.42, 0.38, 0.85]
    P = [(x0 + 40 + (x1 - x0 - 80) * i / (len(pts) - 1), y1 - 40 - (y1 - y0 - 80) * v) for i, v in enumerate(pts)]
    p = ease((t - t0) / dur) * (len(P) - 1)
    k = int(p); f = p - k
    path = P[:k + 1]
    if k < len(P) - 1: path.append((lerp(P[k][0], P[k + 1][0], f), lerp(P[k][1], P[k + 1][1], f)))
    if len(path) > 1:
        d.polygon(path + [(path[-1][0], y1 - 20), (path[0][0], y1 - 20)], fill=(210, 245, 220))
        d.line(path, fill=col, width=14, joint="curve")
        hx, hy = path[-1]; d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=col, outline=INK, width=4)
        return path[-1]
    return P[0]

def gold_disc(d, cx, cy, r, t):
    d.ellipse([cx - r + 12, cy - r + 14, cx + r + 12, cy + r + 14], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 190, 50), outline=INK, width=6)
    for k in (0.85, 0.7, 0.55): d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], outline=(250, 215, 110), width=4)
    a = t * 3
    d.pieslice([cx - r * .95, cy - r * .95, cx + r * .95, cy + r * .95], math.degrees(a), math.degrees(a) + 35, fill=(255, 240, 180))
    d.pieslice([cx - r * .95, cy - r * .95, cx + r * .95, cy + r * .95], math.degrees(a) + 180, math.degrees(a) + 205, fill=(255, 240, 180))
    d.ellipse([cx - r * .18, cy - r * .18, cx + r * .18, cy + r * .18], fill=(60, 50, 80), outline=INK, width=4)

def disco_ball(d, cx, cy, r, t):
    for i in range(6):
        a = t * 1.2 + i * math.pi / 3
        col = [PINK, CYAN, YEL, GRN, (180, 120, 255), RED][i]
        d.polygon([(cx, cy), (cx + math.cos(a) * 260, 1160), (cx + math.cos(a + 0.25) * 260, 1160)], fill=sh(col, 0.75))
    d.line([(cx, 546), (cx, cy - r)], fill=(200, 200, 210), width=5)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 195, 210), outline=INK, width=5)
    off = (t * 60) % 30
    for yy in range(int(cy - r) + 10, int(cy + r), 26):
        hw = math.sqrt(max(0, r * r - (yy - cy) ** 2))
        for xx in range(int(cx - hw - 30 + off), int(cx + hw), 30):
            if cx - hw + 4 < xx < cx + hw - 20:
                c = 255 if ((xx // 30 + yy // 26) % 3 == 0) else 215
                d.rectangle([xx, yy, xx + 22, yy + 18], fill=(c, c, min(255, c + 15)))

def yacht(d, x, y, s):
    d.polygon([(x, y), (x + 460 * s, y), (x + 520 * s, y - 70 * s), (x - 20 * s, y - 70 * s)], fill=(250, 250, 252), outline=INK)
    d.rectangle([x + 60 * s, y - 70 * s, x + 470 * s, y - 64 * s], fill=CYAN)
    d.polygon([(x + 80 * s, y - 70 * s), (x + 360 * s, y - 70 * s), (x + 320 * s, y - 140 * s), (x + 110 * s, y - 140 * s)], fill=(240, 240, 245), outline=INK)
    d.polygon([(x + 140 * s, y - 140 * s), (x + 290 * s, y - 140 * s), (x + 260 * s, y - 190 * s), (x + 160 * s, y - 190 * s)], fill=(235, 235, 240), outline=INK)
    for k in range(5): d.rectangle([x + 110 * s + k * 45 * s, y - 120 * s, x + 140 * s + k * 45 * s, y - 95 * s], fill=(60, 70, 100))

def flag(d, x, y, t, s=1.0):
    d.line([(x, y), (x, y + 300 * s)], fill=(90, 90, 100), width=int(10 * s))
    cw = 28 * s
    for i in range(6):
        for j in range(4):
            wy = math.sin(t * 6 - i * 0.7) * 10 * s * (i / 5)
            c = INK if (i + j) % 2 == 0 else (255, 255, 255)
            d.rectangle([x + i * cw, y + j * cw + wy, x + (i + 1) * cw, y + (j + 1) * cw + wy], fill=c)

def film_strip(d, y, t, x0=426, x1=994):
    d.rectangle([x0, y - 60, x1, y + 60], fill=INK)
    off = (t * 200) % 120
    for x in range(int(x0 - 120 + off), x1, 120):
        if max(x0, x + 10) < min(x1, x + 100):
            d.rectangle([max(x0, x + 10), y - 40, min(x1, x + 100), y + 40], fill=[(230, 120, 160), (120, 90, 190), (255, 170, 110)][int(x // 120) % 3])
        for hx in (x + 20, x + 60, x + 100):
            if x0 < hx < x1 - 16:
                d.rectangle([hx, y - 56, hx + 16, y - 46], fill="white"); d.rectangle([hx, y + 46, hx + 16, y + 56], fill="white")

def flip_clock(d, cx, cy, n, t, s=1.0):
    for k, ch in enumerate(n):
        x = cx + (k - (len(n) - 1) / 2) * 200 * s
        card(d, (x - 90 * s, cy - 130 * s, x + 90 * s, cy + 130 * s), (40, 40, 55), int(24 * s), int(10 * s))
        d.line([(x - 90 * s, cy), (x + 90 * s, cy)], fill=INK, width=6)
        label(d, ch, x, cy, 190 * s, (255, 255, 255), 0)

def folded_map(d, cx, cy, s):
    if s <= 0.05: return
    w = 110 * s
    for i in range(4):
        x = cx - 2 * w + i * w
        up = 20 * s if i % 2 == 0 else -20 * s
        col = (130, 190, 110) if i % 2 == 0 else (110, 170, 95)
        d.polygon([(x, cy - 150 * s + up), (x + w, cy - 150 * s - up), (x + w, cy + 150 * s - up), (x, cy + 150 * s + up)], fill=col, outline=INK)
        d.line([(x + 15 * s, cy - 50 * s), (x + w - 15 * s, cy + 30 * s)], fill=(90, 150, 210), width=max(1, int(10 * s)))
        d.ellipse([x + w / 2 - 12 * s, cy + 60 * s, x + w / 2 + 12 * s, cy + 84 * s], fill=RED)

def gift(d, cx, cy, s, open_p=0.0):
    if s <= 0.05: return
    card(d, (cx - 130 * s, cy - 60 * s, cx + 130 * s, cy + 150 * s), PINK, int(18 * s), int(10 * s))
    d.rectangle([cx - 20 * s, cy - 60 * s, cx + 20 * s, cy + 150 * s], fill=YEL)
    ly = cy - 60 * s - 120 * s * ease(open_p); lx = cx + 60 * s * ease(open_p)
    card(d, (lx - 150 * s, ly - 50 * s, lx + 150 * s, ly + 10 * s), sh(PINK, 1.1), int(14 * s), int(8 * s))
    d.rectangle([lx - 20 * s, ly - 50 * s, lx + 20 * s, ly + 10 * s], fill=YEL)

def siren_scene(d, t):
    b = main_card(d, (25, 25, 45))
    d.rectangle([426, 1000, 994, 1174], fill=(55, 55, 70))
    for x in range(440, 990, 120): d.rectangle([x, 1080, x + 60, 1090], fill=(200, 200, 120))
    on = int(t * 6) % 2
    for k, col in enumerate([(255, 60, 60), (60, 120, 255)]):
        bright = col if (k == on) else sh(col, 0.35)
        cx = 650 + k * 120
        if k == on:
            d.polygon([(cx, 800), (cx - 150 + k * 300, 570), (cx - 60 + k * 120, 570)], fill=sh(col, 0.55))
        d.rounded_rectangle([cx - 50, 790, cx + 50, 830], 16, fill=bright, outline=INK, width=4)
    M.box(d, 520, 840, 380, 170, 60, (40, 45, 60))
    d.rectangle([540, 860, 640, 930], fill=(120, 150, 190)); d.rectangle([660, 860, 760, 930], fill=(120, 150, 190))
    label(d, "SWAT", 820, 950, 48, (255, 255, 255), 0)
    for wx in (580, 830): d.ellipse([wx - 45, 965, wx + 45, 1055], fill=(20, 20, 25))
    return (710, 900)

# ---------------- Reel 11: 212 GB ----------------
def d_intro(im, d, t, dur):
    b = main_card(d, (40, 30, 80))
    v = int(countup(t, 0.3, 2.0, 212))
    label(d, f"{v} GB", 710, 720, 150, YEL, 10)
    ssd(d, 710, 980, back((t - 0.3) / 0.45) * 0.9 * (1 + 0.04 * math.sin(t * 10)), v / 230)
    return (710, 720)

def d_preload(im, d, t, dur):
    b = main_card(d, (30, 30, 50))
    console(d, 710, 980, back(t / 0.4) * 1.3)
    ay = 640 + (t * 120) % 120
    d.polygon([(680, ay), (740, ay), (740, ay + 60), (775, ay + 60), (710, ay + 120), (645, ay + 60), (680, ay + 60)], fill=CYAN, outline=INK)
    dl_bar(d, 470, 1110, 950, ease(t / 4.0))
    pill(d, "PRELOAD AKTIV", 710, 600, 36, GRN, (255, 255, 255), back((t - 0.3) / 0.4) * (1 + 0.05 * math.sin(t * 8)))
    return (710, 900)

def d_earlier(im, d, t, dur):
    s1 = back(t / 0.4)
    if s1 > 0.05: M.calendar(d, 560, 800, 0.5 * s1, "NOV", "12", (150, 150, 160))
    if t > 0.8: x_icon(d, 560, 820, back((t - 0.8) / 0.3) * 1.6)
    s2 = back((t - 1.3) / 0.4)
    if s2 > 0.05: M.calendar(d, 860, 800, 0.6 * s2, "NOV", "10", (40, 170, 90))
    if t > 1.9: check_icon(d, 950, 660, back((t - 1.9) / 0.3) * 1.3)
    a = ease((t - 1.0) / 0.4)
    if a > 0:
        d.line([(640, 1080), (640 + 140 * a, 1080)], fill=YEL, width=16)
        d.polygon([(640 + 140 * a + 30, 1080), (640 + 140 * a, 1060), (640 + 140 * a, 1100)], fill=YEL)
    pill(d, "-2 TAGE", 710, 1160, 44, PINK, (255, 255, 255), back((t - 2.0) / 0.4))
    return (560, 800) if t < 1.3 else (860, 800)

def d_box(im, d, t, dur):
    V.game_case(d, 470, 1150, 260, 380, (40, 120, 200), "BOX", back(t / 0.45))
    s = back((t - 0.6) / 0.4)
    if s > 0.05:
        card(d, (780 - 150 * s, 760 - 90 * s, 780 + 150 * s, 760 + 90 * s), (255, 255, 255))
        label(d, "CODE", 780, 735, 54 * s, INK, 0)
        d.text((780, 795), "XXXX-XXXX", font=F(30 * s), fill=(130, 130, 140), anchor="mm")
    if t > 1.2:
        s2 = back((t - 1.2) / 0.4)
        if s2 > 0.05: M.calendar(d, 820, 1060, 0.38 * s2, "NOV", "12", (230, 60, 60))
    return (780, 760) if t < 1.6 else (820, 1060)

def d_space(im, d, t, dur):
    b = main_card(d)
    label(d, "SPEICHER", 710, 600, 44, INK, 0)
    x0, x1, y0, y1 = 460, 960, 660, 740
    d.rounded_rectangle([x0, y0, x1, y1], 20, fill=(230, 232, 240), outline=INK, width=5)
    blocks = [(0.22, PINK), (0.2, CYAN), (0.18, (180, 120, 255)), (0.15, YEL)]
    x = x0 + 6
    for i, (w, col) in enumerate(blocks):
        gone = ease((t - 0.6 - 0.4 * i) / 0.35)
        ww = (x1 - x0 - 12) * w * (1 - gone)
        if ww > 2: d.rectangle([x, y0 + 6, x + ww, y1 - 6], fill=col)
        x += ww
    free = 1 - sum(w * (1 - ease((t - 0.6 - 0.4 * i) / 0.35)) for i, (w, _) in enumerate(blocks))
    trash(d, 600, 960, 1.1, max(0, math.sin(t * 6)) if 0.5 < t < 2.4 else 0)
    p = ease((t - 2.4) / 0.6)
    if p > 0:
        d.rounded_rectangle([x1 - (x1 - x0 - 12) * 0.62 * p - 6, y0 + 6, x1 - 6, y1 - 6], 14, fill=GRN)
        label(d, "212 GB", x1 - 160, (y0 + y1) / 2, 34, (255, 255, 255), 5)
    pill(d, f"FREI: {int(free * 100)} %", 830, 960, 38, GRN, (255, 255, 255), back((t - 0.5) / 0.4))
    return (600, 960) if t < 2.4 else (800, 700)

def d_lock(im, d, t, dur):
    b = main_card(d, (40, 30, 80))
    padlock(d, 710, 840, back(t / 0.45) * 1.2, ease((t - 2.6) / 0.4))
    pill(d, "AB 19.11.", 710, 1110, 48, YEL, INK, back((t - 0.6) / 0.4))
    return (710, 840)

def d_outro(im, d, t, dur):
    b = main_card(d, (30, 30, 50), (420, 540, 1000, 960))
    console(d, 710, 800, 1.1)
    dl_bar(d, 470, 650, 950, 1.0, "100 %")
    return (710, 760)

# ---------------- Reel 12: Vorbestellungen ----------------
def p_rocket(im, d, t, dur):
    y = 1150 - ease((t - 0.4) / 2.5) * 420 + math.sin(t * 30) * 3
    for i in range(10):
        lx = 450 + (i * 61) % 520; ly = (y + 200 + (t * 900 + i * 97) % 500)
        if ly < 1300: d.line([(lx, ly), (lx, ly + 60)], fill=(255, 255, 255), width=4)
    rocket(d, 710, y, 1.0, t)
    for k in range(5):
        r = 40 + k * 15; cyy = 1240 + math.sin(t * 3 + k) * 5
        if t < 1.5: d.ellipse([710 - r * 2 + k * 30 - 60, cyy - r * 0.6, 710 - r + k * 30 + 60, cyy + r * 0.6], fill=(230, 230, 240))
    return (710, y)

def p_expect(im, d, t, dur):
    b = main_card(d)
    base = 1110
    h1 = 300 * ease(t / 0.8)
    M.box(d, 500, base - h1, 150, h1, 40, (160, 165, 180)) if h1 > 2 else None
    label(d, "ERWARTUNG", 575, base + 40, 30, INK, 0)
    h2 = 600 * ease((t - 0.6) / 1.4)
    top = base - h2
    if h2 > 2:
        M.box(d, 770, max(560, top), 150, base - max(560, top), 40, GRN)
    label(d, "REALITÄT", 845, base + 40, 30, INK, 0)
    if top < 560:
        burst(d, 845, 560, 80 + 10 * math.sin(t * 10))
        label(d, "!!!", 845, 560, 44, INK, 0)
    return (845, max(560, top))

def p_gold(im, d, t, dur):
    gold_disc(d, 710, 820, 230 * back(t / 0.5), t)
    pill(d, "FERTIG ENTWICKELT", 710, 1130, 40, YEL, INK, back((t - 0.6) / 0.4))
    if t > 1.0: check_icon(d, 900, 640, back((t - 1.0) / 0.3) * 1.5)
    sparkle_field(d, t, (440, 560, 990, 1100), 10, 8)
    return (710, 820)

def p_stock(im, d, t, dur):
    tip = stock_chart(d, (420, 560, 1000, 1180), t)
    pill(d, "TAKE-TWO AKTIE", 600, 610, 30, (240, 240, 245), INK, 1)
    s = back((t - 2.1) / 0.4)
    pill(d, "+8 %", 880, 640, 52, GRN, (255, 255, 255), s)
    return tip

def p_8bn(im, d, t, dur):
    for i in range(6):
        h = (110 + i * 60) * ease((t - 0.2 * i) / 0.6)
        if h > 3: V.bill_stack(d, 440 + i * 92, 1180, 70, h)
    v = countup(t, 0.3, 2.2, 8.0)
    label(d, f"{v:.1f}".replace(".", ",") + " MRD. $", 710, 640, 92, (255, 255, 255), 9)
    pill(d, "GESCHÄFTSJAHR-PROGNOSE", 710, 760, 30, YEL, INK, back((t - 0.4) / 0.4))
    return (710, 900)

def p_estimate(im, d, t, dur):
    b = main_card(d)
    v = int(countup(t, 0.3, 2.0, 730))
    label(d, f"~{v} MIO. $", 710, 760, 78, GRN, 6)
    mx = 710 + math.sin(t * 2) * 180; my = 960 + math.cos(t * 2) * 40
    d.ellipse([mx - 80, my - 80, mx + 80, my + 80], outline=INK, width=18)
    d.ellipse([mx - 66, my - 66, mx + 66, my + 66], outline=CYAN, width=6)
    d.line([(mx + 56, my + 56), (mx + 130, my + 130)], fill=INK, width=26)
    s = back((t - 1.6) / 0.35)
    if s > 0.05:
        pill(d, "SCHÄTZUNG", 710, 620, 40, RED, (255, 255, 255), s)
    return (710, 760)

def p_outro(im, d, t, dur):
    b = main_card(d, (40, 30, 80), (420, 540, 1000, 960))
    rocket(d, 710, 760 + math.sin(t * 4) * 8, 0.7, t)
    return (710, 760)

# ---------------- Reel 13: Neuer Trailer ----------------
def n_intro(im, d, t, dur):
    b = main_card(d, (30, 30, 50))
    film_strip(d, 1080, t)
    s = back(t / 0.45) * (1 + 0.06 * math.sin(t * 8))
    r = 120 * s
    d.ellipse([710 - r, 800 - r, 710 + r, 800 + r], fill=RED, outline=INK, width=6)
    d.polygon([(690 - 30 * s, 800 - 55 * s), (690 - 30 * s, 800 + 55 * s), (690 + 65 * s, 800)], fill="white")
    pill(d, "NEU", 900, 610, 44, YEL, INK, back((t - 0.5) / 0.3))
    return (710, 800)

def n_chars(im, d, t, dur):
    cols = [PINK, CYAN, YEL, GRN]
    for i in range(4):
        s = back((t - 0.25 * i) / 0.35)
        x = 500 + (i % 2) * 290; y = 700 + (i // 2) * 330
        if s > 0.05:
            card(d, (x - 120 * s, y - 140 * s, x + 120 * s, y + 140 * s), cols[i])
            silhouette(d, x, y - 10 * s, 0.75 * s, i % 2 == 0, sh(cols[i], 0.45))
            V.qmark(d, x + 90 * s, y - 120 * s, 0.6 * s)
    k = min(3, int(t / 0.5))
    return (500 + (k % 2) * 290, 700 + (k // 2) * 330)

def n_swat(im, d, t, dur): return siren_scene(d, t)

def n_club(im, d, t, dur):
    b = main_card(d, (25, 15, 45))
    disco_ball(d, 710, 700, 95 * back(t / 0.4), t)
    for i in range(8):
        for j in range(3):
            on = (i + j + int(t * 5)) % 3 == 0
            col = [PINK, CYAN, YEL][(i + j) % 3]
            d.rectangle([430 + i * 70, 1000 + j * 58, 495 + i * 70, 1052 + j * 58], fill=col if on else sh(col, 0.35))
    return (710, 700)

def n_yacht(im, d, t, dur):
    b = main_card(d, (60, 150, 210))
    d.rectangle([426, 546, 994, 820], fill=(255, 180, 140))
    d.ellipse([780, 600, 900, 720], fill=(255, 225, 120))
    bob = math.sin(t * 3) * 8
    yacht(d, 470, 1000 + bob, 0.9)
    for k in range(5):
        y = 1040 + k * 26; off = (t * 80 + k * 50) % 160
        for x in range(380, 1000, 160):
            if 430 < x + off < 930: d.line([(x + off, y), (x + off + 60, y)], fill=(160, 210, 240), width=5)
    confetti(d, t, 0.4, (430, 560, 990, 980), 30, 6)
    return (680, 900 + bob)

def n_race(im, d, t, dur):
    b = main_card(d, (90, 160, 90))
    cx, cy, rx, ry = 710, 900, 230, 170
    d.ellipse([cx - rx - 40, cy - ry - 40, cx + rx + 40, cy + ry + 40], fill=(70, 70, 80), outline=INK, width=5)
    d.ellipse([cx - rx + 40, cy - ry + 40, cx + rx - 40, cy + ry - 40], fill=(90, 160, 90), outline=(255, 255, 255), width=5)
    for k, col in enumerate([RED, CYAN, YEL]):
        a = t * 1.8 + k * 0.5
        x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=col, outline=INK, width=4)
    flag(d, 830, 620, t, 0.8)
    return (cx + math.cos(t * 1.8) * rx, cy + math.sin(t * 1.8) * ry)

def n_count(im, d, t, dur):
    b = main_card(d, (40, 30, 80), (420, 540, 1000, 960))
    flip_clock(d, 710, 740, "8", t, 1.0)
    pill(d, "TAGE", 710, 900, 40, YEL, INK, back((t - 0.3) / 0.3))
    return (710, 740)

# ---------------- Reel 14: Box & Map ----------------
def b_intro(im, d, t, dur):
    sh_ = math.sin(t * 25) * 10 if t < 1.5 else 0
    V.game_case(d, 560 + sh_, 1150, 300, 440, (40, 120, 200), "?", back(t / 0.45))
    for i, (x, y) in enumerate([(880, 640), (930, 860), (840, 1050)]):
        V.qmark(d, x, y + math.sin(t * 4 + i) * 10, back((t - 0.4 - 0.2 * i) / 0.3))
    return (710, 900)

def b_code(im, d, t, dur):
    return V.p_nodisc.__wrapped__(im, d, t, dur) if hasattr(V.p_nodisc, "__wrapped__") else _nodisc(d, t)

def _nodisc(d, t):
    M.box(d, 470, 1000, 380, 180, 130, (190, 140, 90))
    lid = ease(t / 0.5)
    d.polygon([(470, 1000), (850, 1000), (850 - 40 * lid, 1000 - 180 * lid), (470 + 40 * lid, 1000 - 180 * lid)], fill=(210, 160, 105), outline=INK)
    s = back((t - 0.5) / 0.4)
    if s > 0.05:
        cx, cy, r = 560, 700, 110 * s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(215, 220, 230), outline=INK, width=5)
        d.ellipse([cx - r * .18, cy - r * .18, cx + r * .18, cy + r * .18], fill=(110, 150, 200))
        x_icon(d, cx + 80, cy - 80, back((t - 1.0) / 0.3) * 1.2)
    s2 = back((t - 1.5) / 0.4)
    if s2 > 0.05:
        card(d, (860 - 130 * s2, 700 - 80 * s2, 860 + 130 * s2, 700 + 80 * s2))
        label(d, "CODE", 860, 700, 50 * s2, INK, 0)
        check_icon(d, 960, 620, back((t - 2.0) / 0.3) * 1.2)
    return (560, 700) if t < 1.5 else (860, 700)

def b_nomap(im, d, t, dur):
    folded_map(d, 710, 830, back(t / 0.45) * 1.3)
    if t > 0.9: x_icon(d, 900, 640, back((t - 0.9) / 0.3) * 1.6)
    pill(d, "NICHT IN DER BOX", 710, 1110, 40, RED, (255, 255, 255), back((t - 1.2) / 0.4))
    return (710, 830)

def b_price(im, d, t, dur):
    s = back(t / 0.45)
    if s > 0.05:
        card(d, (470, 600, 950, 1060), (130, 190, 110))
        d.line([(500, 700), (920, 980)], fill=(90, 150, 210), width=18)
        for x, y in [(560, 760), (760, 900), (880, 700)]: d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=RED, outline=INK, width=3)
        label(d, "POSTER-KARTE", 710, 640, 32, (255, 255, 255), 5)
    V.paste_rot(im, V.tag_img("0,99 $"), 850, 1080, 12 + math.sin(t * 3) * 5, 0.7 * back((t - 0.6) / 0.4))
    return (850, 1080)

def b_free(im, d, t, dur):
    gift(d, 710, 950, back(t / 0.45) * 1.4, (t - 1.0) / 0.6)
    if t > 1.4:
        folded_map(d, 710, 700 - ease((t - 1.4) / 0.5) * 60, back((t - 1.4) / 0.4) * 0.6)
    confetti(d, t, 1.5)
    pill(d, "GRATIS ZUR BESTELLUNG", 710, 1210, 32, GRN, (255, 255, 255), back((t - 1.8) / 0.4))
    return (710, 950)

def b_digital(im, d, t, dur):
    V.phone(d, 710, 860, 0.9 * back(t / 0.45), "GRATIS", "Download am 19.11.")
    ay = 560 + (t * 100) % 80
    if t > 0.6: d.polygon([(870, ay), (920, ay), (920, ay + 50), (950, ay + 50), (895, ay + 100), (840, ay + 50), (870, ay + 50)], fill=GRN, outline=INK)
    pill(d, "KARTE + POSTER", 710, 1230, 38, YEL, INK, back((t - 0.6) / 0.4))
    return (710, 860)

def b_outro(im, d, t, dur):
    b = main_card(d, (40, 30, 80), (420, 540, 1000, 960))
    folded_map(d, 710, 750, 0.9)
    return (710, 750)

# ---------------- Reel 15: GTA 6 in Zahlen ----------------
TILES = [("19.11.", "RELEASE", PINK), ("212 GB", "DOWNLOAD", CYAN), ("79,99 €", "PREIS", YEL),
         ("475 MIO.", "TRAILER-VIEWS", GRN), ("8 MRD. $", "PROGNOSE", (180, 120, 255)), ("?", "DEINE ZAHL", RED)]
def tile_pos(i):
    return (565 + (i % 2) * 290, 640 + (i // 2) * 250)

def draw_tile(d, i, cx, cy, s, t):
    if s <= 0.05: return
    v, lab, col = TILES[i]
    card(d, (cx - 130 * s, cy - 105 * s, cx + 130 * s, cy + 105 * s), col, int(28 * s), int(10 * s))
    label(d, v, cx, cy - 15 * s, 56 * s, (255, 255, 255), max(1, int(6 * s)))
    d.text((cx, cy + 60 * s), lab, font=F(24 * s), fill=INK, anchor="mm")

def dash(cur):
    def f(im, d, t, dur):
        for i in range(6):
            if cur == -1:
                s = back((t - 0.12 * i) / 0.35)
                draw_tile(d, i, *tile_pos(i), s * 0.92, t)
                continue
            if i < cur: draw_tile(d, i, *tile_pos(i), 0.92, t)
            elif i > cur and cur < 6:
                x, y = tile_pos(i); d.rounded_rectangle([x - 120, y - 96, x + 120, y + 96], 26, outline=(255, 255, 255), width=4)
        if 0 <= cur < 6:
            big = ease(t / 0.4) * (1 - ease((t - 2.6) / 0.5))
            x0, y0 = tile_pos(cur)
            cx, cy = lerp(x0, 710, big), lerp(y0, 880, big)
            s = 0.92 + 0.9 * big
            if big > 0.3: card(d, (430, 540, 990, 1340), (40, 30, 80))
            draw_tile(d, cur, cx, cy, s, t)
            if big > 0.6: sparkle_field(d, t, (440, 600, 980, 1200), 8, cur + 3)
            return (cx, cy)
        if cur == 6:
            for i in range(6): draw_tile(d, i, *tile_pos(i), 0.92 * (1 + 0.04 * math.sin(t * 6 + i)), t)
            return (710, 900)
        return (710, 900)
    return f

R3 = {
"11_Download_212GB": [
    (4.0, "purple", d_intro, [(0, "212 GB", PINK)], "wave"),
    (4.5, "night", d_preload, [(0, "SCHON JETZT", GRN)], "point"),
    (4.5, "sky", d_earlier, [(0, "2 TAGE FRÜHER", CYAN)], "point"),
    (4.5, "mint", d_box, [(0, "BOX-VERSION", PINK)], "point"),
    (4.5, "sunset", d_space, [(0, "PLATZ SCHAFFEN", PINK)], "point"),
    (4.0, "night", d_lock, [(0, "KEIN EARLY ACCESS", CYAN)], "point"),
    (4.0, "purple", d_outro, [(0, "SCHON GELADEN?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"12_Vorbestellungen": [
    (4.0, "sky", p_rocket, [(0, "REKORD-HYPE", PINK)], "wave"),
    (4.5, "mint", p_expect, [(0, "WEIT ÜBER PLAN", GRN)], "point"),
    (4.5, "gold", p_gold, [(0, "FERTIG!", PINK)], "cheer"),
    (4.5, "sky", p_stock, [(0, "AKTIE +8 %", GRN)], "point"),
    (4.5, "purple", p_8bn, [(0, "8 MILLIARDEN", CYAN)], "point"),
    (4.0, "sunset", p_estimate, [(0, "GESCHÄTZT", PINK)], "point"),
    (4.0, "night", p_outro, [(0, "VORBESTELLT?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"13_Neuer_Trailer": [
    (4.0, "purple", n_intro, [(0, "NEUER TRAILER", PINK)], "wave"),
    (4.5, "sunset", n_chars, [(0, "NEUE FIGUREN", CYAN)], "point"),
    (4.5, "night", n_swat, [(0, "SWAT-EINSATZ", CYAN)], "point"),
    (4.0, "purple", n_club, [(0, "NACHTCLUB", PINK)], "point"),
    (4.0, "ocean", n_yacht, [(0, "YACHT-PARTY", CYAN)], "cheer"),
    (4.5, "mint", n_race, [(0, "RENNSTRECKE", GRN)], "point"),
    (4.5, "night", n_count, [(0, "NOCH 8 TAGE", PINK), (2.0, "FOLGT FÜR MEHR", PINK)], "point"),
],
"14_Box_und_Karte": [
    (4.0, "purple", b_intro, [(0, "WAS IST IN DER BOX?", PINK)], "wave"),
    (4.5, "sky", lambda im, d, t, dur: _nodisc(d, t), [(0, "NUR EIN CODE", CYAN)], "point"),
    (4.5, "sunset", b_nomap, [(0, "KEINE KARTE", PINK)], "point"),
    (4.5, "mint", b_price, [(0, "0,99 $", GRN)], "point"),
    (4.5, "gold", b_free, [(0, "ODER GRATIS", PINK)], "cheer"),
    (4.0, "ocean", b_digital, [(0, "DIGITAL GRATIS", CYAN)], "point"),
    (4.0, "night", b_outro, [(0, "HOLST DU SIE?", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
],
"15_GTA6_in_Zahlen": [
    (4.0, "purple", dash(-1), [(0, "GTA 6 IN ZAHLEN", PINK)], "wave"),
    (4.0, "sunset", dash(0), [(0, "RELEASE", PINK)], "point"),
    (4.0, "ocean", dash(1), [(0, "DOWNLOAD", CYAN)], "point"),
    (4.0, "gold", dash(2), [(0, "PREIS", PINK)], "point"),
    (4.5, "mint", dash(3), [(0, "TRAILER-REKORD", GRN)], "point"),
    (4.5, "purple", dash(4), [(0, "PROGNOSE", CYAN)], "point"),
    (5.0, "night", dash(6), [(0, "DEINE ZAHL?", PINK), (2.2, "FOLGT FÜR MEHR", PINK)], "cheer"),
],
}
S2.R.update(R3)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        vid = sys.argv[2]
        ims = [S2.frame(vid, i, S2.R[vid][i][0] * (0.9 if i == 6 else 0.55)).resize((270, 480)) for i in range(7)]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(HERE, f"p3_{vid}.png"))
    elif cmd == "render":
        S2.render(sys.argv[2], int(sys.argv[3]))
    elif cmd == "jobs":
        for v in R3:
            for i in range(7): print(v, i)
