"""Reel 26 (5 unbekannte GTA-Fakten) + Reel 27 (Fair oder frech?). Engagement-heavy: like nudges, vote buttons, comment CTA."""
import sys, os, math, random, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes11, scenes3
import scenes7 as S7
from scenes11 import *
from PIL import Image, ImageDraw, ImageFilter

V26, V27 = "26_Unbekannte_Fakten", "27_Fair_oder_Frech"
S7.SCRIPTS7[V26] = [
    "Wetten, du kennst keinen einzigen dieser fünf G T A Fakten?",
    "Eins: G T A sollte eigentlich ein Rennspiel werden.",
    "Zwei: Ein Bug machte die Polizei total aggressiv, und genau das wurde zur Spielidee.",
    "Drei: Die Erfinder machten vorher das Knobelspiel Lemmings.",
    "Vier: G T A sechs wurde von einem Teenager gehackt, mit einem Fire TV Stick im Hotelzimmer.",
    "Fünf: Der erste Trailer kam fünfzehn Stunden zu früh, wegen eines Leaks.",
    "Wie viele kanntest du? Schreib die Zahl in die Kommentare! Und wer fünf schreibt, lügt!",
]
S7.SCRIPTS7[V27] = [
    "G T A sechs: fair oder frech? Du entscheidest!",
    "Achtzig Euro für die Standard-Version.",
    "Keine Disc in der Box, nur ein Code.",
    "Zweihundertzwölf Gigabyte Download.",
    "Kein PC zum Start.",
    "Und dreizehn Jahre Wartezeit.",
    "Trotzdem liegen die Vorbestellungen weit über den Erwartungen.",
    "Also: fair oder frech? Schreib ein Wort in die Kommentare! Und folg mir, wenn du es trotzdem holst!",
]
S7.DISPLAY.update({"eins": "1", "fünfzehn": "15", "achtzig": "80", "zweihundertzwölf": "212"})
S7.COMMENT[V26] = ("WIE VIELE?", "Nur 2, krass!")
S7.COMMENT[V27] = ("FAIR ODER FRECH?", "FRECH! Kauf's eh")
S7.COVER[V26] = ("5 GTA-FAKTEN", "DIE FAST NIEMAND KENNT")
S7.COVER[V27] = ("FAIR ODER FRECH?", "GTA 6 – DU ENTSCHEIDEST")

# ---------- engagement overlays ----------
def heart(d, cx, cy, s, col=RED):
    d.ellipse([cx - 30 * s, cy - 26 * s, cx, cy + 4 * s], fill=col); d.ellipse([cx - 2 * s, cy - 26 * s, cx + 28 * s, cy + 4 * s], fill=col)
    d.polygon([(cx - 29 * s, cy - 6 * s), (cx + 27 * s, cy - 6 * s), (cx - 1 * s, cy + 30 * s)], fill=col)

def like_nudge(d, t):
    s = back((t - 0.9) / 0.35)
    if s <= 0.05: return
    pill(d, "DOPPELTIPP, WENN NEU FÜR DICH", 750, 1290, 25, (255, 255, 255), INK, s)
    heart(d, 470, 1288, 1.1 * s * (1 + 0.14 * math.sin(t * 9)))

def vote(d, t):
    s = back((t - 0.5) / 0.35)
    if s <= 0.05: return
    k = int(t * 2.5) % 2
    pill(d, "FAIR", 570, 1285, 54, GRN, (255, 255, 255), s * (1.12 if k == 0 else 0.94))
    pill(d, "FRECH", 850, 1285, 54, RED, (255, 255, 255), s * (1.12 if k == 1 else 0.94))

def with_nudge(fn, n):
    def f(im, d, t, dur):
        tgt = fn(im, d, t, dur); d2 = ImageDraw.Draw(im)
        fact_badge(d2, n, t); like_nudge(d2, t)
        return tgt
    return f

def with_vote(fn):
    def f(im, d, t, dur):
        tgt = fn(im, d, t, dur); vote(ImageDraw.Draw(im), t)
        return tgt
    return f

# ---------- Reel 26 ----------
def f_hook(im, d, t, dur):
    rays(d, 710, 840, t, (95, 55, 170), (120, 70, 190))
    s = back(t / 0.4) * (1 + 0.05 * math.sin(t * 9))
    if s > 0.05:
        burst(d, 710, 820, 270 * s, YEL, 16)
        label(d, "5", 710, 800, 300 * s, PINK, 14)
    for i in range(5):
        cs = back((t - 0.3 - 0.1 * i) / 0.3)
        if cs > 0.05:
            x = 510 + i * 100; y = 1150 + math.sin(t * 4 + i) * 8
            card(d, (x - 40 * cs, y - 52 * cs, x + 40 * cs, y + 52 * cs), [CYAN, PINK, GRN, YEL, (180, 120, 255)][i], 14, 6)
            label(d, "?", x, y, 56 * cs, (255, 255, 255), 5)
    return (710, 820)

def topcar(d, x, y, col, s=1.0, police=False, t=0):
    d.rounded_rectangle([x - 62 * s, y - 32 * s, x + 62 * s, y + 32 * s], int(16 * s), fill=col, outline=INK, width=4)
    d.rounded_rectangle([x - 20 * s, y - 24 * s, x + 28 * s, y + 24 * s], int(8 * s), fill=(150, 200, 235), outline=INK, width=3)
    if police:
        on = int(t * 8) % 2
        d.rectangle([x - 6 * s, y - 22 * s, x + 6 * s, y - 2 * s], fill=RED if on else (90, 30, 30))
        d.rectangle([x - 6 * s, y + 2 * s, x + 6 * s, y + 22 * s], fill=(60, 120, 255) if not on else (30, 40, 90))

def f_race(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (120, 200, 140), 80, 44, NEON)
    cx, cy, rx, ry = 710, 900, 220, 170
    d.ellipse([cx - rx - 50, cy - ry - 50, cx + rx + 50, cy + ry + 50], fill=(70, 70, 82), outline=INK, width=5)
    d.ellipse([cx - rx + 50, cy - ry + 50, cx + rx - 50, cy + ry - 50], fill=(80, 150, 95), outline=(255, 255, 255), width=5)
    for k, col in enumerate([RED, CYAN, YEL]):
        a = t * (2.4 - 0.25 * k) + k * 0.7
        d.ellipse([cx + math.cos(a) * rx - 26, cy + math.sin(a) * ry - 26, cx + math.cos(a) * rx + 26, cy + math.sin(a) * ry + 26], fill=col, outline=INK, width=4)
    flag(d, 860, 610, t, 0.8)
    pill(d, "ARBEITSTITEL: RACE'N'CHASE", 710, 1170, 28, YEL, INK, back((t - 0.5) / 0.4))
    return (cx + math.cos(t * 2.4) * rx, cy + math.sin(t * 2.4) * ry)

def beetle(d, cx, cy, s, t):
    for k in (-1, 0, 1):
        w = math.sin(t * 12 + k) * 8
        d.line([(cx - 30 * s, cy + k * 22 * s), (cx - 62 * s, cy + k * 34 * s + w)], fill=INK, width=6)
        d.line([(cx + 30 * s, cy + k * 22 * s), (cx + 62 * s, cy + k * 34 * s - w)], fill=INK, width=6)
    d.ellipse([cx - 36 * s, cy - 46 * s, cx + 36 * s, cy + 46 * s], fill=(70, 190, 110), outline=INK, width=4)
    d.line([(cx, cy - 40 * s), (cx, cy + 44 * s)], fill=INK, width=4)
    d.ellipse([cx - 20 * s, cy - 66 * s, cx + 20 * s, cy - 34 * s], fill=(40, 60, 50), outline=INK, width=3)

def f_bug(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (30, 30, 60), 150, 44, NEON2)
    d.rectangle([436, 820, 984, 1010], fill=(62, 62, 76))
    for x in range(440, 990, 110):
        xx = 436 + ((x - t * 420) % 548)
        d.rectangle([xx, 910, min(984, xx + 55), 920], fill=(230, 220, 130))
    xr = 800 + 30 * math.sin(t * 3)
    hit = abs(math.sin(t * 7))
    xp = xr - 175 + 55 * hit
    topcar(d, xp, 915, (245, 245, 250), 1.0, True, t)
    topcar(d, xr + (10 if hit > 0.9 else 0), 915 + (6 * math.sin(t * 40) if hit > 0.9 else 0), RED)
    if hit > 0.88:
        burst(d, xr - 66, 915, 52, YEL, 9); label(d, "!", xr - 66, 915, 40, INK, 0)
    beetle(d, 600, 690 + math.sin(t * 5) * 10, back((t - 0.3) / 0.4), t)
    pill(d, "BUG", 760, 690, 44, GRN, (255, 255, 255), back((t - 0.5) / 0.35))
    if int(t * 6) % 4 == 0: glitch(d, t, (440, 600, 980, 800))
    pill(d, "TESTER LIEBTEN ES", 710, 1140, 32, YEL, INK, back((t - 1.6) / 0.4))
    return (xr - 66, 915)

def walker(d, x, y, s, ph, col):
    a = math.sin(ph) * 10 * s
    d.line([(x - 5 * s, y - 14 * s), (x - 5 * s - a, y)], fill=INK, width=max(2, int(7 * s)))
    d.line([(x + 5 * s, y - 14 * s), (x + 5 * s + a, y)], fill=INK, width=max(2, int(7 * s)))
    d.rounded_rectangle([x - 15 * s, y - 50 * s, x + 15 * s, y - 12 * s], int(8 * s), fill=col, outline=INK, width=3)
    d.ellipse([x - 16 * s, y - 80 * s, x + 16 * s, y - 48 * s], fill=(240, 205, 170), outline=INK, width=3)

def f_lem(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (200, 220, 255), 80, 44, NEON)
    d.rectangle([436, 1000, 770, 1060], fill=(130, 95, 70), outline=INK, width=4)
    d.rectangle([436, 990, 770, 1004], fill=(90, 170, 90))
    for i in range(8):
        u = (t * 130 + i * 72) % 576
        x = 440 + u
        col = [(110, 150, 230), (230, 120, 150), (120, 200, 150), (240, 190, 80)][i % 4]
        if x < 775:
            walker(d, x, 990, 1.25, t * 12 + i, col)
        else:
            tf = (x - 775) / 130
            y = 990 + 620 * tf * tf
            if y < 1200: walker(d, 775 + (x - 775) * 0.45, y, 1.25, t * 20 + i, col)
    pill(d, "DMA DESIGN · 1991", 710, 660, 34, YEL, INK, back((t - 0.4) / 0.4))
    pill(d, "ERST KNOBELN, DANN GANGSTER", 710, 1150, 27, NEON, INK, back((t - 1.2) / 0.4))
    return (775, 990)

def f_hack(im, d, t, dur):
    glass(im, (430, 580, 990, 1220), (12, 14, 34), 205, 44, NEON2)
    neon_text(im, "HOTEL", 560, 630, 48, NEON2)
    bloom(im, 968, 835, 46, (120, 255, 160), 0.8)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([480, 690, 930, 980], 18, fill=(18, 20, 30), outline=(200, 205, 220), width=6)
    rnd = random.Random(5)
    for k in range(14):
        y = 708 + ((k * 30 - t * 90) % 250)
        w = rnd.randrange(80, 400)
        d.rectangle([500, y, 500 + w, y + 12], fill=(90, 255, 140) if k % 4 else (255, 255, 255))
    d.rectangle([690, 980, 720, 1030], fill=(200, 205, 220)); d.rectangle([610, 1030, 800, 1044], fill=(200, 205, 220))
    d.rounded_rectangle([930, 815, 990, 855], 8, fill=(15, 15, 18), outline=(255, 255, 255), width=3)
    d.ellipse([972, 829, 984, 841], fill=(120, 255, 160) if int(t * 6) % 2 else (40, 90, 60))
    stamp(im, "GEHACKT", 705, 835, t, 1.3, -10, 1.0, RED)
    d = ImageDraw.Draw(im)
    pill(d, "TEENAGER · FIRE TV STICK · 2022", 710, 1140, 26, YEL, INK, back((t - 0.6) / 0.4))
    return (955, 835)

def f_trailer(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (255, 255, 255), 70, 44, NEON)
    s = back(t / 0.4) * (1 + 0.06 * math.sin(t * 8)); r = 135 * s
    if s > 0.05:
        bloom(im, 610, 840, 150, (255, 80, 90), 0.5); d = ImageDraw.Draw(im)
        d.ellipse([610 - r, 840 - r, 610 + r, 840 + r], fill=RED, outline=INK, width=6)
        d.polygon([(585 - 30 * s, 840 - 62 * s), (585 - 30 * s, 840 + 62 * s), (585 + 75 * s, 840)], fill="white")
    cs = back((t - 0.4) / 0.4)
    if cs > 0.05: clock(d, 870, 720, int(95 * cs), -t * 1.5)
    pill(d, "15 STD. ZU FRÜH", 710, 1060, 46, PINK, (255, 255, 255), back((t - 0.8) / 0.4))
    stamp(im, "LEAK", 870, 900, t, 1.4, -12, 0.9, YEL)
    return (610, 840)

def f_cta(im, d, t, dur):
    d = ImageDraw.Draw(im)
    for n in range(6):
        x = 470 + n * 96; act = int(t * 5) % 6 == n
        r = 46 if act else 38
        d.ellipse([x - r + 5, 700 - r + 7, x + r + 5, 700 + r + 7], fill=INK)
        d.ellipse([x - r, 700 - r, x + r, 700 + r], fill=YEL if act else (255, 255, 255), outline=INK, width=5)
        label(d, str(n), x, 700, 50 if act else 42, INK, 0)
    return (710, 700)

# ---------- Reel 27 ----------
def q_hook(im, d, t, dur):
    card(d, (420, 580, 1000, 1200), (255, 255, 255))
    d.rectangle([426, 586, 707, 1194], fill=(50, 170, 100)); d.rectangle([713, 586, 994, 1194], fill=(220, 60, 70))
    label(d, "FAIR", 566, 690, 70, (255, 255, 255), 7); label(d, "FRECH", 853, 690, 70, (255, 255, 255), 7)
    k = int(t * 3) % 2
    check_icon(d, 566, 930, back(t / 0.4) * (2.6 if k == 0 else 2.2), (30, 120, 70))
    x_icon(d, 853, 930, back((t - 0.2) / 0.4) * (2.6 if k == 1 else 2.2))
    burst(d, 710, 890, 95 * back((t - 0.3) / 0.4) * (1 + 0.1 * math.sin(t * 8)), YEL, 12)
    label(d, "?", 710, 890, 90 * back((t - 0.3) / 0.4), INK, 0)
    return (710, 890)

def q_price(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (255, 240, 200), 80, 44, AMBER)
    rnd = random.Random(3)
    for i in range(12):
        x = rnd.randrange(460, 960); y = 600 + ((rnd.randrange(600) + t * rnd.uniform(200, 340)) % 600)
        d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=(250, 200, 60), outline=INK, width=3)
        d.text((x, y), "€", font=F(28), fill=INK, anchor="mm")
    V.paste_rot(im, V.tag_img("79,99 €"), 710, 850, -8 + math.sin(t * 3) * 6, 1.25 * back(t / 0.4))
    d = ImageDraw.Draw(im)
    pill(d, "STANDARD EDITION", 710, 1130, 34, (255, 255, 255), INK, back((t - 0.5) / 0.4))
    return (710, 850)

def q_code(im, d, t, dur): return scenes3._nodisc(d, t)
def q_gb(im, d, t, dur): return scenes3.d_intro(im, d, t, dur)

def q_pc(im, d, t, dur):
    d = glass(im, (430, 580, 990, 1220), (200, 220, 255), 70, 44, NEON)
    s = back(t / 0.4)
    if s > 0.05:
        d.rounded_rectangle([520, 660, 900, 920], 16, fill=(30, 32, 44), outline=INK, width=5)
        d.rectangle([540, 680, 880, 900], fill=(90, 110, 150))
        label(d, "PC", 710, 790, 120, (255, 255, 255), 8)
        d.rectangle([690, 920, 730, 970], fill=(60, 62, 74)); d.rounded_rectangle([610, 970, 810, 990], 8, fill=(60, 62, 74))
        d.rounded_rectangle([560, 1030, 860, 1075], 10, fill=(220, 224, 235), outline=INK, width=4)
    x_icon(d, 880, 680, back((t - 0.6) / 0.3) * 2.4)
    pill(d, "ZUM START NICHT DABEI", 710, 1150, 32, RED, (255, 255, 255), back((t - 0.8) / 0.4))
    return (710, 790)

def q_wait(im, d, t, dur):
    glass(im, (430, 580, 990, 1220), (20, 20, 50), 190, 44, NEON2)
    y = 2013 + int(13 * ease((t - 0.2) / 1.4))
    neon_text(im, str(y), 710, 800, 170, NEON)
    d = ImageDraw.Draw(im)
    p = ease((t - 0.2) / 1.4)
    d.rounded_rectangle([490, 950, 930, 980], 15, fill=(60, 66, 110))
    d.rounded_rectangle([490, 950, 490 + 440 * max(0.04, p), 980], 15, fill=NEON2)
    d.text((490, 1010), "2013", font=F(30), fill=(255, 255, 255), anchor="lm"); d.text((930, 1010), "2026", font=F(30), fill=(255, 255, 255), anchor="rm")
    pill(d, "13 JAHRE", 710, 1110, 50, YEL, INK, back((t - 1.3) / 0.4))
    return (710, 800)

def q_pre(im, d, t, dur): return p_expect(im, d, t, dur)

def q_cta(im, d, t, dur):
    d = ImageDraw.Draw(im)
    k = int(t * 3) % 2
    pill(d, "FAIR", 560, 720, 70, GRN, (255, 255, 255), 1.1 if k == 0 else 0.9)
    pill(d, "FRECH", 860, 720, 70, RED, (255, 255, 255), 1.1 if k == 1 else 0.9)
    return (710, 720)

def draw_caption2(fr, words, gt):
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
    d = ImageDraw.Draw(fr); f = F(62)
    texts = [words[i][2] for i in g]
    widths = [d.textlength(x, font=f) for x in texts]; total = sum(widths) + 22 * (len(texts) - 1)
    if total > 600:
        f = F(int(62 * 600 / total)); widths = [d.textlength(x, font=f) for x in texts]; total = sum(widths) + 22 * (len(texts) - 1)
    x = 690 - total / 2; y = 1395
    for i, tx, w in zip(g, texts, widths):
        on = i == act
        pop = 1 + 0.12 * (1 - ease((gt - words[i][0]) / 0.15)) if on else 1
        if on: d.rounded_rectangle([x - 10, y - 44 * pop, x + w + 10, y + 44 * pop], 16, fill=YEL)
        d.text((x + w / 2, y), tx, font=f if pop == 1 else F(int(f.size * pop)), fill=INK if on else (255, 255, 255), anchor="mm", stroke_width=0 if on else 8, stroke_fill=INK)
        x += w + 22
S7.draw_caption = draw_caption2

_old = S7.defs
def defs(vid, durs):
    if vid == V26:
        sc = [f_hook, with_nudge(f_race, 1), with_nudge(f_bug, 2), with_nudge(f_lem, 3), with_nudge(f_hack, 4), with_nudge(f_trailer, 5), f_cta]
        w = [("KENNST DU KEINEN!", PINK), ("RENNSPIEL?!", CYAN), ("EIN BUG!", PINK), ("LEMMINGS?!", GRN), ("FIRE-STICK-HACK", PINK), ("15 STD. ZU FRÜH", CYAN), ("WER 5 SCHREIBT, LÜGT", PINK)]
        th = ["purple", "mint", "night", "sky", "night", "sunset", "purple"]
        poses = ["wave", "point", "point", "point", "point", "point", "point"]
    elif vid == V27:
        sc = [q_hook, with_vote(q_price), with_vote(q_code), with_vote(q_gb), with_vote(q_pc), with_vote(q_wait), with_vote(q_pre), q_cta]
        w = [("FAIR ODER FRECH?", PINK), ("80 EURO", GRN), ("NUR EIN CODE", CYAN), ("212 GB", PINK), ("KEIN PC", CYAN), ("13 JAHRE WARTEN", PINK), ("TROTZDEM HYPE", GRN), ("FAIR ODER FRECH?", PINK)]
        th = ["night", "gold", "sky", "purple", "ocean", "night", "mint", "purple"]
        poses = ["wave"] + ["point"] * 7
    else:
        return _old(vid, durs)
    return [(durs[i], th[i], sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(len(sc))]
S7.defs = defs

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        ims = [S7.frame(vid, i, R[i][0] * (0.9 if i == n - 1 else 0.7), T, words).resize((270, 480)) for i in range(n)]
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((270, 480)))
        shp = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(ims[:10]): shp.paste(im, ((i % 5) * 270, (i // 5) * 480))
        shp.save(os.path.join(HERE, f"p12_{vid}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
