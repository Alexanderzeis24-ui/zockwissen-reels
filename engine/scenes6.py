import json
import scenes5
import scenes2 as S2
from scenes5 import *

# ---------- generic icons (all original, no brand logos) ----------
def ic_racket(d, cx, cy, s):
    if s < 0.1: return
    d.ellipse([cx - 40 * s, cy - 60 * s, cx + 40 * s, cy + 30 * s], outline=INK, width=max(2, int(8 * s)), fill=(240, 240, 245))
    for k in range(-2, 3): d.line([(cx + k * 14 * s, cy - 55 * s), (cx + k * 14 * s, cy + 25 * s)], fill=(190, 190, 200), width=2)
    d.line([(cx, cy + 30 * s), (cx, cy + 80 * s)], fill=(120, 80, 50), width=max(2, int(14 * s)))

def ic_hat(d, cx, cy, s):
    if s < 0.1: return
    d.ellipse([cx - 80 * s, cy - 5 * s, cx + 80 * s, cy + 30 * s], fill=(150, 100, 60), outline=INK, width=3)
    d.rounded_rectangle([cx - 42 * s, cy - 60 * s, cx + 42 * s, cy + 12 * s], int(22 * s), fill=(170, 115, 70), outline=INK, width=3)
    d.rectangle([cx - 42 * s, cy - 5 * s, cx + 42 * s, cy + 5 * s], fill=(90, 60, 40))

def ic_palm(d, cx, cy, s):
    if s < 0.1: return
    M.palm(d, cx, cy + 60 * s, 0.32 * s / 0.6, 0)

def ic_cubes(d, cx, cy, s):
    if s < 0.1: return
    for (ox, oy, c) in [(-28, 10, (90, 140, 220)), (28, 10, (240, 150, 60)), (0, -30, (180, 120, 230))]:
        M.box(d, cx + ox * s - 26 * s, cy + oy * s - 10 * s, 52 * s, 44 * s, 30 * s, c)

def ic_blocks(d, cx, cy, s):
    if s < 0.1: return
    u = 26 * s
    for (gx, gy, c) in [(0, 0, CYAN), (1, 0, CYAN), (2, 0, CYAN), (1, -1, CYAN), (-1, 1, PINK), (0, 1, PINK), (1, 1, YEL), (2, 1, YEL)]:
        x = cx + (gx - 0.5) * u - u; y = cy + gy * u
        d.rectangle([x, y, x + u - 2, y + u - 2], fill=c, outline=INK)

ICONS = [ic_blocks, ic_cubes, ic_palm, ic_hat, ic_racket]
RANK = [("Tetris", 520, "*alle Versionen"), ("Minecraft", 425, ""), ("GTA V", 230, ""), ("Red Dead 2", 87, ""), ("Wii Sports", 83, "")]
def rank_scene(cur_rank):
    def f(im, d, t, dur):
        card(d, (420, 520, 1000, 1330), (255, 255, 255))
        label(d, "MIO. VERKAUFT", 710, 570, 30, (120, 120, 135), 0)
        visible = range(cur_rank - 1, 5) if cur_rank else range(0)
        for i in range(0, max(0, cur_rank - 1)):
            y = 640 + i * 140
            d.rounded_rectangle([440, y - 46, 980, y + 46], 22, fill=(238, 238, 244))
            label(d, "?", 710, y, 44, (190, 190, 205), 0)
        for i in visible:
            name, v, note = RANK[i]
            y = 640 + i * 140
            active = (i == cur_rank - 1)
            p = ease((t - 0.2) / 1.2) if active else 1
            if active:
                d.rounded_rectangle([432, y - 58, 988, y + 58], 24, fill=(255, 244, 200))
            ICONS[i](d, 480, y - 6, 0.55)
            label(d, f"#{i + 1}", 540, y - 30, 26, INK, 0)
            bw = 380 * v / 520 * p
            col = [PINK, GRN, YEL, (200, 120, 70), CYAN][i]
            d.rounded_rectangle([540, y - 8, 540 + max(14, bw), y + 30], 18, fill=col, outline=sh(col, 0.6), width=3)
            d.text((580, y - 32), name, font=F(30), fill=INK, anchor="lm")
            d.text((975, y - 32), f"{int(v * p)}", font=F(34), fill=INK, anchor="rm")
            if note and active and t > 1.2: d.text((975, y + 46), note, font=F(22), fill=(120, 120, 135), anchor="rm")
        if cur_rank == 1: confetti(d, t, 1.0, (430, 540, 990, 1320))
        return (700, 640 + (cur_rank - 1) * 140) if cur_rank else (710, 900)
    return f

def rk_intro(im, d, t, dur):
    rays(d, 710, 880, t, (95, 55, 170), (120, 70, 190))
    V.trophy(d, 710, 880, back(t / 0.5) * 1.25)
    for i, fn in enumerate(ICONS):
        a = t * 1.2 + i * 2 * math.pi / 5
        fn(d, 710 + math.cos(a) * 250, 860 + math.sin(a) * 300, 0.6 * back((t - 0.3 - 0.1 * i) / 0.3))
    return (710, 880)

def rk_outro(im, d, t, dur):
    card(d, (420, 540, 1000, 960), (40, 30, 80))
    label(d, "2x", 600, 750, 150, YEL, 9)
    label(d, "IN DEN TOP 5", 820, 750, 44, (255, 255, 255), 6)
    return (710, 750)

# ---------- Rockstar ----------
def rs_intro(im, d, t, dur):
    rays(d, 710, 860, t, (40, 40, 70), (60, 55, 95))
    s = back(t / 0.45)
    if s > 0.05:
        star(d, 710, 860, 260 * s, YEL)
        star(d, 710, 860, 150 * s, (255, 235, 140))
    sparkle_field(d, t, (430, 520, 1000, 1300), 14, 21)
    pill(d, "STUDIO-FAKTEN", 710, 1180, 44, PINK, (255, 255, 255), back((t - 0.4) / 0.4))
    return (710, 860)

def rs_ny(im, d, t, dur):
    card(d, (420, 540, 1000, 1200), (120, 160, 210))
    skyline(d, 432, 990, 1170, 9, [(70, 80, 110), (90, 100, 130), (60, 70, 100)], (255, 220, 150))
    s = back((t - 0.3) / 0.4)
    if s > 0.05: M.calendar(d, 710, 760, 0.55 * s, "DEZEMBER", "1998", (230, 60, 60))
    pill(d, "NEW YORK", 710, 1130, 40, YEL, INK, back((t - 0.8) / 0.4))
    return (710, 760)

def rs_brothers(im, d, t, dur):
    person_card(d, 570, 800, back(t / 0.45) * 0.95, "SAM", CYAN, False)
    person_card(d, 850, 800, back((t - 0.25) / 0.45) * 0.95, "DAN", PINK, False)
    pill(d, "BRÜDER HOUSER", 710, 1130, 42, YEL, INK, back((t - 0.6) / 0.4))
    return (710, 800)

def rs_older(im, d, t, dur):
    card(d, (420, 600, 1000, 1150), (255, 255, 255))
    d.line([(470, 900), (950, 900)], fill=INK, width=10)
    for i, (yr, lab, col, x) in enumerate([("1997", "ERSTES GTA", GRN, 540), ("1998", "ROCKSTAR", PINK, 880)]):
        s = back((t - 0.3 - 0.6 * i) / 0.35)
        if s > 0.05:
            d.ellipse([x - 28 * s, 900 - 28 * s, x + 28 * s, 900 + 28 * s], fill=col, outline=INK, width=5)
            label(d, yr, x, 820, 60 * s, col, 6)
            d.text((x, 980), lab, font=F(30 * s), fill=INK, anchor="mm")
    if t > 1.6: V.qmark(d, 710, 700, back((t - 1.6) / 0.3))
    return (540, 900) if t < 0.9 else (880, 900)

def scot_flag(d, x0, y0, x1, y1, t):
    pts = []
    card(d, (x0, y0, x1, y1), (0, 94, 184))
    d.line([(x0 + 10, y0 + 10), (x1 - 10, y1 - 10)], fill="white", width=34)
    d.line([(x1 - 10, y0 + 10), (x0 + 10, y1 - 10)], fill="white", width=34)

def castle(d, cx, cy, s):
    c = (150, 140, 130)
    d.rectangle([cx - 160 * s, cy - 80 * s, cx + 160 * s, cy + 80 * s], fill=c, outline=INK, width=4)
    for k in range(-2, 3): d.rectangle([cx + k * 64 * s - 18 * s, cy - 110 * s, cx + k * 64 * s + 18 * s, cy - 80 * s], fill=c, outline=INK, width=3)
    d.rectangle([cx - 60 * s, cy - 200 * s, cx + 60 * s, cy - 80 * s], fill=sh(c, 1.1), outline=INK, width=4)
    d.chord([cx - 30 * s, cy + 10 * s, cx + 30 * s, cy + 110 * s], 180, 360, fill=INK)

def rs_scotland(im, d, t, dur):
    scot_flag(d, 460, 580, 960, 880, t)
    castle(d, 710, 1080, back((t - 0.4) / 0.45))
    pill(d, "EHEMALS DMA DESIGN", 710, 1230, 34, YEL, INK, back((t - 1.2) / 0.4))
    return (710, 1000)

def people_grid(d, t, n_on, total=40, col=GRN, t0=0.2, dur=2.0, x0=450, y0=600, cols=8, cell=66):
    k = int(total * ease((t - t0) / dur))
    for i in range(total):
        r, c = divmod(i, cols)
        x = x0 + c * cell + 30; y = y0 + r * (cell + 18) + 30
        on = i < k
        colr = col if (i < n_on and on) else ((210, 210, 220) if not on else (150, 150, 165))
        d.ellipse([x - 12, y - 30, x + 12, y - 6], fill=colr)
        d.chord([x - 22, y - 4, x + 22, y + 40], 180, 360, fill=colr)

def rs_people(im, d, t, dur):
    card(d, (420, 560, 1000, 1180), (255, 255, 255))
    people_grid(d, t, 40, 40, GRN, 0.2, 1.6, 450, 580)
    v = int(countup(t, 0.2, 1.8, 4700))
    pill(d, f"{v:,} MENSCHEN".replace(",", "."), 710, 1120, 40, YEL, INK, 1)
    pill(d, "12 STUDIOS", 710, 1240, 40, PINK, (255, 255, 255), back((t - 1.8) / 0.4))
    return (710, 850)

def rs_outro(im, d, t, dur):
    card(d, (420, 540, 1000, 960), (40, 30, 80))
    M.box(d, 600, 600, 220, 320, 80, (90, 100, 140))
    for yy in range(630, 900, 50):
        for xx in range(620, 800, 45): d.rectangle([xx, yy, xx + 24, yy + 30], fill=(255, 220, 140))
    label(d, "TAKE-TWO", 710, 640, 40, (255, 255, 255), 6)
    return (710, 760)

# ---------- GTA Online ----------
def go_intro(im, d, t, dur):
    rays(d, 710, 860, t, (20, 70, 50), (30, 95, 65))
    for i in range(24):
        rnd = random.Random(i)
        x = rnd.randrange(440, 990); y = (rnd.randrange(-600, 0) + t * rnd.uniform(250, 420)) % 900 + 480
        V.bill(d, x, y, math.sin(t * 2 + i) * 0.8, 0.8)
    pill(d, "GTA ONLINE", 710, 860, 80, GRN, (255, 255, 255), back(t / 0.45) * (1 + 0.04 * math.sin(t * 8)))
    return (710, 860)

def go_5bn(im, d, t, dur):
    for i in range(6):
        h = (130 + i * 75) * ease((t - 0.12 * i) / 0.6)
        if h > 3: V.bill_stack(d, 450 + i * 90, 1220, 70, h)
    v = countup(t, 0.2, 1.8, 5.0)
    label(d, f"{v:.1f}".replace(".", ",") + " MRD. $", 710, 640, 96, (255, 255, 255), 9)
    stamp(im, "LEAK", 710, 1300, t, 2.0, -8, 1.0, YEL)
    return (710, 900)

def go_2020(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (255, 255, 255))
    for i, (yr, v, col) in enumerate([("2020", 744, GRN), ("2025", 400, (160, 165, 180))]):
        x = 540 + i * 280; p = ease((t - 0.2 - 0.3 * i) / 1.0)
        h = 480 * v / 744 * p
        if h > 2: M.box(d, x - 80, 1150 - h, 160, h, 40, col)
        d.text((x, 1190), yr, font=F(40), fill=INK, anchor="mm")
        if p > 0.1: label(d, f"{int(v * p)} Mio. $", x, 1110 - h, 34, INK, 0)
    if t > 1.4: star(d, 540, 600, 40 * back((t - 1.4) / 0.3), YEL)
    return (540, 900)

def donut(d, cx, cy, r, p, frac, col1, col2):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col2, outline=INK, width=5)
    if p > 0.01:
        d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac * p, fill=col1, outline=INK, width=5)
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55], fill=(255, 255, 255), outline=INK, width=5)

def go_shark(im, d, t, dur):
    card(d, (420, 560, 1000, 1260), (255, 255, 255))
    p = ease((t - 0.2) / 1.4)
    donut(d, 710, 860, 230, p, 0.74, CYAN, (230, 232, 240))
    label(d, f"{int(74 * p)} %", 710, 860, 80, INK, 0)
    pill(d, "SHARK CARDS", 600, 1170, 32, CYAN, INK, back((t - 1.2) / 0.4))
    pill(d, "GTA+", 880, 1170, 32, (230, 232, 240), INK, back((t - 1.4) / 0.4))
    return (710, 860)

def go_4pct(im, d, t, dur):
    card(d, (420, 560, 1000, 1260), (255, 255, 255))
    total = 50; on = 2
    for i in range(total):
        r, c = divmod(i, 10)
        x = 470 + c * 52; y = 640 + r * 105
        colr = PINK if (i < on and t > 1.2) else (200, 200, 212)
        s = back((t - 0.02 * i) / 0.3)
        if s > 0.05:
            d.ellipse([x - 12 * s, y - 30 * s, x + 12 * s, y - 6 * s], fill=colr)
            d.chord([x - 20 * s, y - 4 * s, x + 20 * s, y + 36 * s], 180, 360, fill=colr)
    pill(d, "NUR 4 % ZAHLEN", 710, 1200, 40, PINK, (255, 255, 255), back((t - 1.3) / 0.4))
    return (500, 650)

def xmas_tree(d, cx, cy, s, t):
    for k in range(3):
        w = (220 - k * 50) * s; y = cy - k * 110 * s
        d.polygon([(cx, y - 170 * s), (cx - w, y), (cx + w, y)], fill=(40, 140, 70), outline=INK)
    d.rectangle([cx - 25 * s, cy, cx + 25 * s, cy + 60 * s], fill=(120, 80, 50))
    star(d, cx, cy - 390 * s, 40 * s, YEL)
    rnd = random.Random(3)
    for i in range(10):
        x = cx + rnd.randrange(-140, 140) * s; y = cy - rnd.randrange(20, 300) * s
        on = int(t * 4 + i) % 2
        d.ellipse([x - 10 * s, y - 10 * s, x + 10 * s, y + 10 * s], fill=[RED, YEL, CYAN][i % 3] if on else (250, 250, 250))

def go_xmas(im, d, t, dur):
    xmas_tree(d, 600, 1100, back(t / 0.45) * 1.0, t)
    s = back((t - 0.4) / 0.4)
    if s > 0.05: M.calendar(d, 870, 760, 0.4 * s, "DEZ", "25", (230, 60, 60))
    v = countup(t, 0.6, 1.6, 8.5)
    pill(d, f"{v:.1f}".replace(".", ",") + " MIO. $", 860, 1020, 40, GRN, (255, 255, 255), back((t - 0.6) / 0.3))
    return (600, 900)

def go_outro(im, d, t, dur):
    card(d, (420, 540, 1000, 960), (40, 30, 80))
    stamp(im, "NICHT OFFIZIELL", 710, 750, t, 0.2, -8, 0.9)
    return (710, 750)

# ---------- GTA 5 vs GTA 6 ----------
def vs_card(d, t, left_col=(70, 110, 170), right_col=(200, 80, 150)):
    card(d, (420, 540, 1000, 1240), (255, 255, 255))
    d.rectangle([426, 546, 707, 1234], fill=left_col); d.rectangle([713, 546, 994, 1234], fill=right_col)
    d.line([(710, 546), (710, 1234)], fill=INK, width=6)
    label(d, "GTA 5", 566, 610, 50, (255, 255, 255), 6); label(d, "GTA 6", 853, 610, 50, (255, 255, 255), 6)

def vs_intro(im, d, t, dur):
    vs_card(d, t)
    s = 1 + 0.15 * math.sin(t * 7)
    burst(d, 710, 880, 110 * back(t / 0.4) * s, YEL, 12)
    label(d, "VS", 710, 880, 80 * back(t / 0.4), INK, 0)
    return (710, 880)

def vs_years(im, d, t, dur):
    vs_card(d, t)
    label(d, "2013", 566, 880, 90, (255, 255, 255), 8)
    v = 2013 + int(13 * ease((t - 0.3) / 1.6))
    label(d, str(v), 853, 880, 90, YEL, 8)
    pill(d, "+13 JAHRE", 710, 1120, 44, YEL, INK, back((t - 1.8) / 0.4))
    return (853, 880)

def vs_heroes(im, d, t, dur):
    vs_card(d, t)
    for i in range(3):
        silhouette(d, 500 + i * 66, 880, 0.42 * back((t - 0.15 * i) / 0.3), False, (30, 40, 70))
    for i in range(2):
        silhouette(d, 800 + i * 110, 880, 0.55 * back((t - 0.6 - 0.15 * i) / 0.3), i == 0, (80, 20, 60))
    pill(d, "TRIO", 566, 1120, 40, (255, 255, 255), INK, back((t - 0.4) / 0.3))
    pill(d, "DUO", 853, 1120, 40, YEL, INK, back((t - 0.9) / 0.3))
    return (853, 880)

def vs_map(im, d, t, dur):
    vs_card(d, t, (190, 170, 130), (80, 170, 210))
    for (x, h) in [(470, 160), (530, 230), (590, 190), (650, 140)]:
        d.rectangle([x, 1000 - h, x + 50, 1000], fill=(110, 110, 130), outline=INK, width=3)
    d.polygon([(440, 1000), (520, 820), (600, 1000)], fill=(140, 120, 90))
    P = leonida_map(d, t, 853, 880, 0.3)
    M.palm(d, 960, 1120, 0.35, math.sin(t * 2))
    pill(d, "LOS SANTOS", 566, 1120, 30, (255, 255, 255), INK, back((t - 0.3) / 0.3))
    pill(d, "LEONIDA", 853, 1160, 30, YEL, INK, back((t - 0.7) / 0.3))
    return (853, 880)

def vs_console(im, d, t, dur):
    vs_card(d, t, (60, 60, 75), (40, 120, 200))
    M.box(d, 480, 830, 170, 60, 50, (30, 30, 35))
    pill(d, "PS3", 566, 1000, 36, (255, 255, 255), INK, back((t - 0.3) / 0.3))
    console(d, 853, 860, back((t - 0.6) / 0.4) * 0.8)
    pill(d, "PS5 + XBOX SERIES", 853, 1000, 28, YEL, INK, back((t - 0.9) / 0.3))
    return (853, 860)

def vs_price(im, d, t, dur):
    vs_card(d, t, (90, 120, 90), (200, 80, 150))
    V.paste_rot(im, V.tag_img("60 $", (230, 230, 235)), 566, 880, 10 + math.sin(t * 3) * 4, 0.45 * back((t - 0.2) / 0.4))
    V.paste_rot(im, V.tag_img("80 $"), 853, 880, -10 + math.sin(t * 3) * 4, 0.55 * back((t - 0.7) / 0.4))
    pill(d, "+20 $", 710, 1120, 50, RED, (255, 255, 255), back((t - 1.3) / 0.4))
    return (853, 880)

def vs_outro(im, d, t, dur):
    vs_card(d, t)
    for i, x in enumerate((566, 853)):
        V.qmark(d, x, 880 + math.sin(t * 4 + i) * 10, back((t - 0.2 * i) / 0.3) * 1.3)
    return (710, 880)

# ---------- timing ----------
SCRIPTS = {
"18_Meistverkaufte_Spiele": ["Das sind die meistverkauften Spiele aller Zeiten!", "Platz fünf: Wii Sports, mit rund dreiundachtzig Millionen.", "Platz vier: Red Dead Redemption zwei, mit siebenundachtzig Millionen.", "Platz drei: G T A fünf, mit fast zweihundertdreißig Millionen.", "Platz zwei: Minecraft, mit unfassbaren vierhundertfünfundzwanzig Millionen.", "Und Platz eins: Tetris, mit über fünfhundert Millionen, über alle Versionen zusammen.", "Rockstar hat damit zwei Spiele in den Top fünf! Folgt für mehr!"],
"19_Rockstar_Games": ["Krasse Fakten über Rockstar Games!", "Gegründet wurde Rockstar im Dezember neunzehnhundertachtundneunzig, in New York.", "Zu den Gründern gehören die Brüder Sam und Dan Houser.", "Das allererste G T A kam schon neunzehnhundertsiebenundneunzig, also bevor es Rockstar überhaupt gab.", "Das Hauptstudio Rockstar North sitzt in Schottland und hieß früher DMA Design.", "Heute arbeiten rund viertausendsiebenhundert Menschen in zwölf Studios.", "Und alle gehören zu Take-Two. Folgt für mehr!"],
"20_GTA_Online_Geld": ["So viel Geld macht G T A Online wirklich!", "Laut geleakten Daten hat es seit zweitausenddreizehn über fünf Milliarden Dollar eingebracht.", "Das beste Jahr war zweitausendzwanzig, mit rund siebenhundertvierzig Millionen.", "Fast drei Viertel davon kommen von Shark Cards, also virtuellem Geld.", "Dabei zahlen nur rund vier Prozent der Spieler überhaupt etwas.", "An einem einzigen Weihnachtstag kamen über acht Millionen Dollar rein.", "Aber Achtung: Rockstar hat diese Zahlen nie bestätigt. Folgt für mehr!"],
"21_GTA5_vs_GTA6": ["G T A fünf gegen G T A sechs: Das hat sich geändert!", "Zwischen den beiden Spielen liegen dreizehn Jahre.", "Statt drei Hauptfiguren gibt es jetzt ein Duo.", "Statt Los Santos geht es nach Vice City, im Bundesstaat Leonida.", "G T A fünf kam zuerst für PS drei, G T A sechs nur für PS fünf und Xbox Series.", "Und der Preis steigt von sechzig auf achtzig Dollar.", "Welches wird besser? Folgt für mehr!"],
}
def est_durs(lines):
    raw = [len(l) / 15.5 + 0.4 for l in lines]
    k = 29.4 / sum(raw)
    d = [r * k for r in raw]
    d[-1] += 30 - sum(d)
    return [round(x, 2) for x in d]

TIMING_FILE = os.path.join(HERE, "timing6.json")
TIMING = json.load(open(TIMING_FILE)) if os.path.exists(TIMING_FILE) else {}
def durs(vid):
    if vid in TIMING: return TIMING[vid]["durs"], TIMING[vid]["follow"]
    d = est_durs(SCRIPTS[vid]); return d, max(1.2, d[-1] - 2.0)

def build(vid, scenes, words, poses, themes):
    d, fol = durs(vid)
    out = []
    for i in range(7):
        w = [(0, words[i][0], words[i][1])]
        if i == 6: w.append((fol, "FOLGT FÜR MEHR", PINK))
        out.append((d[i], themes[i], scenes[i], w, poses[i]))
    return out

R6 = {
"18_Meistverkaufte_Spiele": build("18_Meistverkaufte_Spiele",
    [rk_intro, rank_scene(5), rank_scene(4), rank_scene(3), rank_scene(2), rank_scene(1), rk_outro],
    [("BESTSELLER", PINK), ("PLATZ 5", CYAN), ("PLATZ 4", PINK), ("PLATZ 3", GRN), ("PLATZ 2", CYAN), ("PLATZ 1", PINK), ("2X ROCKSTAR", GRN)],
    ["wave", "point", "point", "point", "point", "cheer", "point"],
    ["gold", "sky", "sunset", "mint", "ocean", "purple", "night"]),
"19_Rockstar_Games": build("19_Rockstar_Games",
    [rs_intro, rs_ny, rs_brothers, rs_older, rs_scotland, rs_people, rs_outro],
    [("ROCKSTAR FAKTEN", PINK), ("SEIT 1998", CYAN), ("DIE GRÜNDER", PINK), ("ÄLTER ALS ROCKSTAR", GRN), ("SCHOTTLAND", CYAN), ("4.700 LEUTE", PINK), ("TAKE-TWO", CYAN)],
    ["wave", "point", "point", "point", "point", "cheer", "point"],
    ["night", "sky", "sunset", "mint", "ocean", "gold", "purple"]),
"20_GTA_Online_Geld": build("20_GTA_Online_Geld",
    [go_intro, go_5bn, go_2020, go_shark, go_4pct, go_xmas, go_outro],
    [("GTA ONLINE", GRN), ("5 MILLIARDEN $", PINK), ("REKORDJAHR 2020", CYAN), ("SHARK CARDS", CYAN), ("NUR 4 %", PINK), ("8,5 MIO. AN 1 TAG", GRN), ("NICHT BESTÄTIGT", PINK)],
    ["wave", "point", "point", "point", "point", "cheer", "point"],
    ["mint", "gold", "sky", "ocean", "purple", "night", "sunset"]),
"21_GTA5_vs_GTA6": build("21_GTA5_vs_GTA6",
    [vs_intro, vs_years, vs_heroes, vs_map, vs_console, vs_price, vs_outro],
    [("GTA 5 VS GTA 6", PINK), ("13 JAHRE", CYAN), ("DUO STATT TRIO", PINK), ("NEUE MAP", GRN), ("NUR NEXT-GEN", CYAN), ("+20 $", PINK), ("WELCHES IST BESSER?", CYAN)],
    ["wave", "point", "point", "point", "point", "point", "point"],
    ["purple", "sky", "sunset", "ocean", "night", "gold", "purple"]),
}
S2.R.update(R6)
