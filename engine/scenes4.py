import scenes3
import scenes2 as S2
from scenes3 import *

_stamp = {}
def stamp_img(txt, col=RED):
    k = (txt, col)
    if k in _stamp: return _stamp[k]
    f = F(64); w = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(txt, font=f))
    im = Image.new("RGBA", (w + 80, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, w + 76, 126], 18, outline=col, width=10)
    d.text((w / 2 + 40, 65), txt, font=f, fill=col, anchor="mm")
    _stamp[k] = im
    return im

def stamp(im, txt, cx, cy, t, t0, ang=-12, scale=1.0, col=RED):
    p = (t - t0) / 0.25
    if p <= 0: return
    s = scale * (1 + 1.2 * (1 - ease(p)))
    V.paste_rot(im, stamp_img(txt, col), cx, cy, ang, s)

def doc(d, x0, y0, x1, y1, title, rows=6):
    card(d, (x0, y0, x1, y1), (250, 248, 240))
    d.rectangle([x0 + 6, y0 + 6, x1 - 6, y0 + 80], fill=(40, 30, 80))
    label(d, title, (x0 + x1) / 2, y0 + 44, 36, (255, 255, 255), 0)
    for i in range(rows):
        y = y0 + 120 + i * 60
        d.rounded_rectangle([x0 + 40, y, x0 + 40 + (x1 - x0 - 80) * (0.9 - 0.1 * (i % 3)), y + 24], 12, fill=(200, 200, 210))

def icon_shield(d, cx, cy, s):
    d.polygon([(cx, cy - 70 * s), (cx + 60 * s, cy - 45 * s), (cx + 50 * s, cy + 30 * s), (cx, cy + 75 * s), (cx - 50 * s, cy + 30 * s), (cx - 60 * s, cy - 45 * s)], fill=CYAN, outline=INK)
    star(d, cx, cy, 30 * s, (255, 255, 255))

def icon_plane(d, cx, cy, s):
    d.rounded_rectangle([cx - 80 * s, cy - 14 * s, cx + 80 * s, cy + 14 * s], int(14 * s), fill=(240, 240, 245), outline=INK, width=3)
    d.polygon([(cx - 10 * s, cy), (cx + 20 * s, cy - 70 * s), (cx + 40 * s, cy - 70 * s), (cx + 30 * s, cy)], fill=YEL, outline=INK)
    d.polygon([(cx - 10 * s, cy), (cx + 20 * s, cy + 70 * s), (cx + 40 * s, cy + 70 * s), (cx + 30 * s, cy)], fill=YEL, outline=INK)
    d.polygon([(cx - 80 * s, cy), (cx - 95 * s, cy - 35 * s), (cx - 70 * s, cy - 10 * s)], fill=YEL, outline=INK)

def icon_bolt(d, cx, cy, s):
    d.polygon([(cx + 10 * s, cy - 80 * s), (cx - 45 * s, cy + 10 * s), (cx, cy + 10 * s), (cx - 15 * s, cy + 80 * s), (cx + 45 * s, cy - 15 * s), (cx, cy - 15 * s)], fill=YEL, outline=INK)

def icon_car(d, cx, cy, s):
    d.rounded_rectangle([cx - 80 * s, cy - 10 * s, cx + 80 * s, cy + 35 * s], int(14 * s), fill=PINK, outline=INK, width=3)
    d.polygon([(cx - 45 * s, cy - 10 * s), (cx - 25 * s, cy - 45 * s), (cx + 30 * s, cy - 45 * s), (cx + 50 * s, cy - 10 * s)], fill=PINK, outline=INK)
    for wx in (-45, 45): d.ellipse([cx + wx * s - 20 * s, cy + 20 * s, cx + wx * s + 20 * s, cy + 60 * s], fill=INK)

def glitch(d, t, box):
    rnd = random.Random(int(t * 12))
    for _ in range(5):
        y = rnd.randrange(box[1], box[3]); h = rnd.randrange(6, 20); x = rnd.randrange(box[0], box[2] - 120)
        d.rectangle([x, y, x + rnd.randrange(60, 200), y + h], fill=rnd.choice([CYAN, PINK, (255, 255, 255)]))

# ---- scenes ----
def c_intro(im, d, t, dur):
    s = back(t / 0.45)
    x0 = 470 + (1 - s) * 400
    doc(d, x0, 600, x0 + 460, 1100, "GTA 6 CHEATS?")
    if 0.5 < t < 3.0 and int(t * 8) % 3 == 0: glitch(d, t, (440, 600, 990, 1100))
    for i, (x, y) in enumerate([(470, 580), (960, 700)]):
        V.qmark(d, x, y + math.sin(t * 4 + i) * 10, back((t - 0.6 - 0.2 * i) / 0.3))
    stamp(im, "LEAK?", 700, 870, t, 1.2, -10, 1.1)
    return (700, 850)

def c_viral(im, d, t, dur):
    V.phone(d, 600, 860, 0.85 * back(t / 0.4), "VIRAL", "Cheat-Liste")
    icons = [(icon_shield, 880, 640), (icon_car, 880, 840), (icon_plane, 880, 1030), (icon_bolt, 880, 1210)]
    for i, (fn, x, y) in enumerate(icons):
        s = back((t - 0.6 - 0.35 * i) / 0.3)
        if s > 0.05: fn(d, x, y + math.sin(t * 3 + i) * 6, 0.8 * s)
    for i in range(6):
        y = 1150 - ((t * 240 + i * 120) % 600); x = 470 + (i * 53) % 120
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=PINK)
    k = min(3, int(max(0, t - 0.6) / 0.35))
    return (880, icons[k][2]) if t > 0.6 else (600, 860)

ROWS4 = ["Unsterblichkeit", "Alle Waffen", "Super-Sprung", "Fahrzeuge", "Zeitlupe"]
def c_unconf(im, d, t, dur):
    card(d, (420, 540, 1000, 1300), (250, 248, 240))
    for i, r in enumerate(ROWS4):
        y = 620 + i * 140
        d.text((460, y), r, font=F(40), fill=INK, anchor="lm")
        stamp(im, "UNBESTÄTIGT", 880, y, t, 0.4 + 0.45 * i, -8, 0.36)
    k = min(4, int(max(0, t - 0.4) / 0.45))
    return (880, 620 + k * 140)

PAIRS = ["PAINKILLER", "TURTLE", "SLOWMO", "SNOWDAY"]
def c_gta5(im, d, t, dur):
    card(d, (420, 540, 1000, 1300), (255, 255, 255))
    label(d, "GTA 5", 560, 600, 40, CYAN, 6); label(d, "\"LEAK\"", 860, 600, 40, PINK, 6)
    d.line([(710, 650), (710, 1270)], fill=(220, 220, 230), width=4)
    for i, c in enumerate(PAIRS):
        y = 720 + i * 145
        s1 = back((t - 0.3 - 0.4 * i) / 0.3); s2 = back((t - 0.5 - 0.4 * i) / 0.3)
        pill(d, c, 560, y, 30, (230, 245, 255), INK, s1)
        pill(d, c, 860, y, 30, (255, 230, 240), INK, s2)
        if t > 0.7 + 0.4 * i:
            label(d, "=", 710, y, 50 * back((t - 0.7 - 0.4 * i) / 0.3), GRN, 5)
    if t > 2.6: stamp(im, "KOPIERT!", 710, 1000, t, 2.6, -14, 1.2)
    k = min(3, int(max(0, t - 0.3) / 0.4))
    return (710, 720 + k * 145) if t < 2.6 else (710, 1000)

def c_silent(im, d, t, dur):
    b = main_card(d, (40, 30, 80))
    s = back(t / 0.45)
    if s > 0.05:
        d.rounded_rectangle([710 - 220 * s, 780 - 120 * s, 710 + 220 * s, 780 + 120 * s], int(60 * s), fill=(255, 255, 255), outline=INK, width=6)
        d.polygon([(620, 780 + 115 * s), (600, 780 + 190 * s), (680, 780 + 115 * s)], fill=(255, 255, 255), outline=INK)
        for k in range(3):
            on = int(t * 3) % 4 > k
            r = 22 * s
            d.ellipse([650 + k * 60 - r, 780 - r, 650 + k * 60 + r, 780 + r], fill=INK if on else (200, 200, 210))
    v = 0
    pill(d, "0 BESTÄTIGT", 710, 1080, 52, RED, (255, 255, 255), back((t - 0.8) / 0.4))
    return (710, 780)

def c_wait(im, d, t, dur):
    s = back(t / 0.45)
    if s > 0.05: M.calendar(d, 710, 840, 0.85 * s, "NOVEMBER", "19")
    mx = 710 + math.sin(t * 2.5) * 200; my = 1130
    d.ellipse([mx - 60, my - 60, mx + 60, my + 60], outline=INK, width=16)
    d.line([(mx + 42, my + 42), (mx + 100, my + 100)], fill=INK, width=22)
    return (710, 840)

def c_outro(im, d, t, dur):
    b = main_card(d, (40, 30, 80), (420, 540, 1000, 960))
    stamp(im, "FAKE?", 710, 750, t, 0.2, -10, 1.3)
    return (710, 750)

R4 = {"16_Cheat_Leak_Faktencheck": [
    (4.0, "night", c_intro, [(0, "CHEATS GELEAKT?", PINK)], "wave"),
    (4.5, "purple", c_viral, [(0, "GEHT VIRAL", CYAN)], "point"),
    (4.5, "sunset", c_unconf, [(0, "UNBESTÄTIGT", PINK)], "point"),
    (5.0, "sky", c_gta5, [(0, "GTA-5-CODES", CYAN)], "point"),
    (4.5, "night", c_silent, [(0, "ROCKSTAR SCHWEIGT", PINK)], "point"),
    (3.5, "mint", c_wait, [(0, "ERST AB 19.11.", GRN)], "point"),
    (4.0, "purple", c_outro, [(0, "FAKE-CHECK", PINK), (1.6, "FOLGT FÜR MEHR", PINK)], "point"),
]}
S2.R.update(R4)

if __name__ == "__main__":
    cmd = sys.argv[1]; vid = "16_Cheat_Leak_Faktencheck"
    if cmd == "preview":
        ims = [S2.frame(vid, i, S2.R[vid][i][0] * (0.9 if i == 6 else 0.75)).resize((270, 480)) for i in range(7)]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(HERE, "p4.png"))
    elif cmd == "render":
        S2.render(vid, int(sys.argv[2]))
