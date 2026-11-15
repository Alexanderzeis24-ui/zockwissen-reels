"""Reel 31 – 6 Dinge, die du vor GTA 6 wissen musst, im festen v3-Stil (scenes13)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes15
import scenes14 as S14
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
import scenes12
from scenes13 import (atext, gtext, chip, tile, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import person, star, stamp, car, dog
from PIL import Image, ImageDraw

VID = "31_GTA6_Vor_dem_Start"
S7.SCRIPTS7[VID] = [
    "Bevor du G T A sechs spielst, musst du diese sechs Dinge wissen!",
    "Eins: Die Story ist riesig. Ein Rockstar-Chef brauchte achtzig Stunden.",
    "Zwei: Stirbst du oder wirst geschnappt, ist dein Bargeld weg. Also ab zur Bank.",
    "Drei: Gestohlene Ware musst du erst bei einem Hehler verkaufen.",
    "Vier: Du kannst nach Schätzen in Schiffswracks tauchen.",
    "Fünf: Hunde kannst du streicheln und mit Leckerlis füttern.",
    "Sechs: Am Drive-in bestellst du Essen, ohne auszusteigen.",
    "Was machst du als Erstes? Schreib die Zahl in die Kommentare!",
]
S7.DISPLAY.update({"achtzig": "80"})
S7.COMMENT[VID] = ("WAS ZUERST?", "Fakt 4, Schätze suchen!")
S7.COVER[VID] = ("GTA 6", "VOR DEM START")
HEAD = [("VOR DEM START", "MUSST DU DAS WISSEN"), ("DIE STORY:", "80 STUNDEN"), ("TOT ODER GESCHNAPPT", "= BARGELD WEG"), ("DIEBESGUT?", "AB ZUM HEHLER"),
        ("TAUCHEN NACH", "SCHÄTZEN"), ("HUNDE", "STREICHELN & FÜTTERN"), ("DRIVE-IN", "OHNE AUSZUSTEIGEN"), ("WAS MACHST DU", "ALS ERSTES?")]
SRC = [None, "QUELLE: ROCKSTAR NORTH (ROB NELSON)", "LAUT MEHREREN VORSCHAUEN", "LAUT MEHREREN VORSCHAUEN", "LAUT VORSCHAUEN & TRAILER", "LAUT VORSCHAUEN", "LAUT VORSCHAUEN", None]
GOLD = (255, 205, 70); GRN = (90, 210, 120)
ACC = [(LIME, VIO), (CY, VIO), (GRN, LIME), (GOLD, ORG), (CY, (40, 120, 255)), (ORG, MAG), (RD, ORG), (LIME, MAG)]

def v_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); s = back(t / 0.4)
    if s > 0.1:
        x0, y0, x1, y1 = 720 - 200 * s, 860 - 270 * s, 720 + 200 * s, 860 + 270 * s
        D.rounded_rectangle([x0, y0, x1, y1], 30, fill=(245, 246, 252, 255))
        D.rounded_rectangle([720 - 80 * s, y0 - 26 * s, 720 + 80 * s, y0 + 26 * s], 14, fill=(150, 156, 190, 255))
        if s > 0.9:
            for i in range(6):
                y = 650 + i * 74
                D.rounded_rectangle([560, y - 22, 604, y + 22], 10, outline=(40, 44, 70, 255), width=4)
                D.rounded_rectangle([624, y - 9, 624 + 220 - (i % 3) * 40, y + 9], 9, fill=(200, 204, 222, 255))
                if t > 0.6 + i * 0.18:
                    p = ease((t - 0.6 - i * 0.18) / 0.15)
                    D.line([(566, y), (578, y + 12 * p)], fill=GRN + (255,), width=8)
                    if p >= 1: D.line([(578, y + 12), (600, y - 16)], fill=GRN + (255,), width=8)
    chip(im, "AB 19.11.", 720, 1190, 38, LIME, INK, back((t - 1.6) / 0.4) * (1 + 0.04 * math.sin(t * 9)))
    return (720, 800)

def v_story(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); cx, cy, R = 720, 820, 170
    D.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(255, 255, 255, 22), outline=(255, 255, 255, 160), width=6)
    for k in range(12):
        a = k * math.pi / 6
        D.line([(cx + (R - 26) * math.cos(a), cy + (R - 26) * math.sin(a)), (cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a))], fill=(255, 255, 255, 200), width=5)
    p = ease((t - 0.2) / 1.5)
    D.pieslice([cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14], -90, -90 + 360 * p, fill=CY + (70,))
    a = -math.pi / 2 + t * 9
    D.line([(cx, cy), (cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a))], fill=LIME + (255,), width=9)
    a2 = -math.pi / 2 + t * 0.9
    D.line([(cx, cy), (cx + (R - 80) * math.cos(a2), cy + (R - 80) * math.sin(a2))], fill=WH + (255,), width=12)
    D.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(240, 240, 250, 255))
    v = int(80 * p)
    gtext(im, f"{v} STUNDEN", 720, 1080, FX(76), CY, LIME)
    chip(im, "STORY + NEBENSACHEN", 720, 1180, 28, WH, INK, back((t - 1.5) / 0.35))
    return (720, 820)

def bill(D, x, y, rot, s=1.0, a=255):
    w, h = 90 * s, 46 * s; c, sn = math.cos(rot), math.sin(rot)
    pts = [(x + px * c - py * sn, y + px * sn + py * c) for px, py in ((-w, -h), (w, -h), (w, h), (-w, h))]
    D.polygon(pts, fill=(110, 200, 120, a), outline=(40, 110, 60, a), width=4)
    D.ellipse([x - 18 * s, y - 18 * s, x + 18 * s, y + 18 * s], outline=(40, 110, 60, a), width=4)

def v_cash(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    p = ease((t - 0.5) / 0.9)
    v = int(25000 * (1 - p))
    col = WH if p < 0.5 else RD
    atext(im, 720, 650, f"$ {v:,}".replace(",", "."), FX(84), col)
    rng = random.Random(7)
    for i in range(9):
        ang = rng.uniform(0, 2 * math.pi); dist = 150 * p
        x = 600 + dist * math.cos(ang) * 1.1; y = 860 + dist * math.sin(ang) - 80 * p
        bill(D, x, y, ang + t * 2 * p, 0.8, int(255 * (1 - p * 0.9)))
    if p > 0.5:
        stamp(im, "WEG!", 600, 860, t - 1.0, RD, 10, 80)
    b = back((t - 1.5) / 0.4)
    if b > 0.1:
        x, y = 870, 960
        D = ImageDraw.Draw(im, "RGBA")
        D.rounded_rectangle([x - 80 * b, y - 150 * b, x + 80 * b, y + 150 * b], 18, fill=(70, 80, 120, 255))
        D.rounded_rectangle([x - 60 * b, y - 125 * b, x + 60 * b, y - 45 * b], 10, fill=CY + (255,))
        for r in range(3):
            for c in range(3): D.rectangle([x - 50 * b + c * 36 * b, y - 20 * b + r * 30 * b, x - 26 * b + c * 36 * b, y + 2 * b + r * 30 * b], fill=(200, 204, 222, 255))
        atext(im, x, y - 85 * b, "ATM", FX(30 * b), INK)
        chip(im, "BANK = SICHER", 720, 1180, 30, GRN, INK, b)
    return (600, 860) if t < 1.5 else (870, 960)

def diamond(D, x, y, s, col=(160, 230, 255)):
    D.polygon([(x - 40 * s, y - 20 * s), (x - 20 * s, y - 42 * s), (x + 20 * s, y - 42 * s), (x + 40 * s, y - 20 * s), (x, y + 40 * s)], fill=col + (255,), outline=(255, 255, 255, 255), width=3)
    D.line([(x - 40 * s, y - 20 * s), (x + 40 * s, y - 20 * s)], fill=(255, 255, 255, 200), width=3)

def v_fence(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s = back((t - 0.1) / 0.4)
    if s > 0.2:
        D.ellipse([480, 840, 680, 1060], fill=(120, 96, 70, 255))
        D.polygon([(540, 850), (620, 850), (650, 800), (510, 800)], fill=(140, 112, 82, 255))
        diamond(D, 580, 780 + 6 * math.sin(t * 4), s * 1.1)
        atext(im, 580, 960, "DIEBESGUT", FX(28), WH, s)
    a = ease((t - 0.6) / 0.4)
    if a > 0:
        D.line([(700, 920), (700 + 80 * a, 920)], fill=WH + (255,), width=8)
        if a > 0.9: D.polygon([(780, 900), (812, 920), (780, 940)], fill=WH + (255,))
    h = back((t - 0.9) / 0.4)
    if h > 0.2:
        person(D, 890, 1100, 300 * h, (150, 156, 190), "down", 0)
        D.rectangle([890 - 40 * h, 1100 - 300 * h + 8 * h, 890 + 40 * h, 1100 - 300 * h + 26 * h], fill=(20, 22, 30, 255))
        chip(im, "HEHLER", 890, 760, 30, GOLD, INK, h)
    if t > 1.5:
        chip(im, "WENIGER GELD, ABER SAUBER", 720, 1180, 26, WH, INK, back((t - 1.5) / 0.35))
    return (580, 900) if t < 0.9 else (890, 950)

def v_dive(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    for k in range(10):
        y0 = 580 + k * 64
        D.rectangle([434, y0, 1006, y0 + 64], fill=(20, 80 - k * 5, 150 - k * 10, 160))
    for k in range(6):
        x = 470 + k * 95 + 20 * math.sin(t * 2 + k)
        D.polygon([(x, 580), (x + 40, 580), (x + 140, 1220), (x + 60, 1220)], fill=(180, 230, 255, 14))
    D.polygon([(470, 1180), (600, 1060), (860, 1060), (960, 1180)], fill=(60, 52, 48, 255))
    D.line([(700, 1060), (690, 900)], fill=(60, 52, 48, 255), width=10)
    D.line([(640, 960), (760, 980)], fill=(60, 52, 48, 255), width=6)
    g = ease((t - 0.8) / 0.4)
    cx, cy = 820, 1100
    if g > 0:
        for r in range(4): D.ellipse([cx - 60 - r * 18, cy - 50 - r * 14, cx + 60 + r * 18, cy + 30 + r * 14], fill=GOLD + (int(30 * g),))
    D.rounded_rectangle([cx - 52, cy - 30, cx + 52, cy + 30], 8, fill=(140, 90, 40, 255), outline=GOLD + (255,), width=4)
    D.rectangle([cx - 52, cy - 46 - 20 * g, cx + 52, cy - 30], fill=(160, 104, 50, 255))
    px = 520 + 230 * ease(t / 1.4); py = 800 + 30 * math.sin(t * 2)
    D.ellipse([px - 26, py - 26, px + 26, py + 26], fill=(30, 34, 50, 255))
    D.rounded_rectangle([px + 10, py - 18, px + 130, py + 18], 18, fill=(30, 34, 50, 255))
    D.rounded_rectangle([px - 10, py - 14, px + 14, py + 4], 6, fill=CY + (255,))
    for k in range(2): D.line([(px + 130, py - 8 + k * 16), (px + 170, py - 16 + k * 32 + 10 * math.sin(t * 9 + k))], fill=(30, 34, 50, 255), width=10)
    for k in range(7):
        ph = (t * 0.5 + k / 7) % 1
        bx = px - 10 + 14 * math.sin(k * 3 + t * 3); by = py - 30 - ph * 220
        r = 5 + k % 3 * 3
        D.ellipse([bx - r, by - r, bx + r, by + r], outline=(220, 240, 255, int(200 * (1 - ph))), width=3)
    chip(im, "SCHATZ GEFUNDEN!", 720, 1180, 30, GOLD, INK, back((t - 1.2) / 0.35))
    return (cx, cy - 20)

def v_dog(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(470, 1100), (970, 1100)], fill=(255, 255, 255, 90), width=3)
    wag = t * 1.2
    dog(D, 640, 1030, 1.6, 0.0, (230, 190, 140))
    D.line([(640 - 66 * 1.6, 1030 - 20 * 1.6), (640 - 110 * 1.6, 1030 - 60 * 1.6 + math.sin(t * 22) * 22)], fill=(230, 190, 140, 255), width=14)
    person(D, 880, 1100, 320, (230, 232, 245), "down", 0)
    hx = 880 - 40 - 60 * ease((t - 0.3) / 0.4)
    D.line([(880 - 20, 1100 - 320 + 90), (hx, 1100 - 320 + 170)], fill=(230, 232, 245, 255), width=16)
    tb = back((t - 0.9) / 0.35)
    if tb > 0.2:
        bx, by = 780, 920
        D.rounded_rectangle([bx - 30 * tb, by - 8 * tb, bx + 30 * tb, by + 8 * tb], 6, fill=(240, 220, 180, 255))
        for sx in (-1, 1):
            for sy in (-1, 1): D.ellipse([bx + sx * 30 * tb - 10 * tb, by + sy * 8 * tb - 10 * tb, bx + sx * 30 * tb + 10 * tb, by + sy * 8 * tb + 10 * tb], fill=(240, 220, 180, 255))
    for k in range(3):
        ht = t - 0.6 - k * 0.35
        if ht > 0:
            ph = (ht % 1.2) / 1.2
            scenes12.heart(ImageDraw.Draw(im), 700 + k * 50, 900 - ph * 220, 0.9 * (1 - ph * 0.5), RD)
    chip(im, "BRAVER HUND!", 720, 1180, 30, ORG, INK, back((t - 1.3) / 0.35))
    return (690, 960)

def v_drive(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.rectangle([700, 700, 990, 1080], fill=(200, 70, 60, 255))
    D.rectangle([690, 680, 1000, 720], fill=(240, 240, 250, 255))
    D.rounded_rectangle([730, 820, 860, 940], 10, fill=(255, 220, 140, 255), outline=(255, 255, 255, 255), width=5)
    blink = int(t * 4) % 2
    D.rounded_rectangle([760, 590, 980, 660], 18, fill=(20, 22, 36, 255), outline=(GOLD if blink else ORG) + (255,), width=5)
    atext(im, 870, 625, "DRIVE-IN", FX(34), GOLD if blink else ORG)
    D.line([(450, 1110), (990, 1110)], fill=(255, 255, 255, 110), width=4)
    p = ease(t / 0.9)
    car(D, 330 + 280 * p, 1040, 0.85, (60, 140, 255))
    sb = back((t - 0.9) / 0.35)
    if sb > 0.2:
        D.rounded_rectangle([520, 700 - 0, 690, 790], 24, fill=(250, 250, 255, 255))
        D.polygon([(600, 790), (630, 790), (610, 820)], fill=(250, 250, 255, 255))
        bx, by, s = 605, 745, sb
        D.chord([bx - 44 * s, by - 34 * s, bx + 44 * s, by + 14 * s], 180, 360, fill=(230, 160, 60, 255))
        D.rectangle([bx - 46 * s, by - 6 * s, bx + 46 * s, by + 4 * s], fill=(110, 200, 90, 255))
        D.rectangle([bx - 44 * s, by + 4 * s, bx + 44 * s, by + 14 * s], fill=(120, 60, 40, 255))
        D.rounded_rectangle([bx - 44 * s, by + 14 * s, bx + 44 * s, by + 28 * s], 6, fill=(230, 160, 60, 255))
    chip(im, "SITZEN BLEIBEN!", 720, 1180, 30, RD, WH, back((t - 1.3) / 0.35))
    return (650, 980)

SC = [v_hook, v_story, v_cash, v_fence, v_dive, v_dog, v_drive, S13.h_cta]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "6 DINGE VOR DEM START"

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.9]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 2, R[2][0] * 0.35, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p16_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
