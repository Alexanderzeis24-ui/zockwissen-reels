"""Reel 30 – GTA 6 Realismus-Details, im festen v3-Stil (scenes13)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes14 as S14
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, tile, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import person, star, stamp, car
from PIL import Image, ImageDraw

VID = "30_GTA6_Realismus"
S7.SCRIPTS7[VID] = [
    "G T A sechs ist so realistisch, dass es fast unheimlich ist!",
    "Eins: Über sechshunderttausend Animationen. G T A fünf hatte nur fünfundfünfzigtausend.",
    "Zwei: Passanten reagieren sogar auf schlechten Geruch.",
    "Drei: Kaffee gibt dir Ausdauer, ein Proteinshake Gesundheit.",
    "Vier: Jedes Fahrzeug hat eine Tankanzeige.",
    "Fünf: Busse und Züge fahren wirklich.",
    "Sechs: Bei Sturm suchen die Passanten Schutz.",
    "Welches Detail feierst du am meisten? Schreib die Zahl in die Kommentare!",
]
S7.DISPLAY.update({"sechshunderttausend": "600.000", "fünfundfünfzigtausend": "55.000"})
S7.COMMENT[VID] = ("WELCHES DETAIL?", "Fakt 2, der Geruch!")
S7.COVER[VID] = ("GTA 6", "REALISTISCH")
HEAD = [("SO REALISTISCH", "WIE NIE ZUVOR"), ("600.000", "ANIMATIONEN"), ("PASSANTEN", "RIECHEN DICH"), ("KAFFEE & SHAKE", "= POWER-UPS"),
        ("JEDES AUTO", "HAT EINE TANKANZEIGE"), ("BUSSE & ZÜGE", "FAHREN WIRKLICH"), ("BEI STURM", "FLÜCHTEN ALLE"), ("WELCHES DETAIL", "FEIERST DU?")]
SRC = [None, "QUELLE: ROCKSTAR / NEW YORK TIMES"] + ["QUELLE: EDGE-MAGAZIN, VORSCHAU"] * 5 + [None]
ACC = [(CY, VIO), (LIME, CY), ((120, 220, 90), LIME), (ORG, RD), (RD, ORG), ((255, 200, 60), ORG), (CY, (60, 120, 255)), (LIME, MAG)]
GRN = (120, 220, 90)

def r_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); cx, cy = 720, 860
    o = back(t / 0.45)
    blink = 1.0
    for bt in (1.6, 3.2):
        if bt < t < bt + 0.22: blink = abs((t - bt) / 0.11 - 1)
    w, h = 250 * o, 140 * o * max(0.05, blink)
    if w > 10:
        for k in range(4):
            r = w + 40 + k * 34 + 10 * math.sin(t * 4 + k)
            D.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], outline=CY + (60 - k * 12,), width=3)
        D.ellipse([cx - w, cy - h, cx + w, cy + h], fill=(240, 244, 255, 255))
        lx = cx + 50 * math.sin(t * 1.6)
        ir = min(h, 105 * o)
        if ir > 8:
            for k in range(6):
                rr = ir * (1 - k / 7)
                c = tuple(int(CY[i] * (1 - k / 6) + VIO[i] * k / 6) for i in range(3))
                D.ellipse([lx - rr, cy - rr, lx + rr, cy + rr], fill=c + (255,))
            pr = ir * 0.42
            D.ellipse([lx - pr, cy - pr, lx + pr, cy + pr], fill=(8, 10, 22, 255))
            D.ellipse([lx - pr * 0.9 + ir * 0.35, cy - ir * 0.55, lx - pr * 0.9 + ir * 0.6, cy - ir * 0.3], fill=(255, 255, 255, 230))
        sy = cy - 150 + ((t * 160) % 300)
        D.line([(cx - w - 30, sy), (cx + w + 30, sy)], fill=LIME + (150,), width=3)
    v = min(99, int(99 * ease((t - 0.4) / 1.4)))
    atext(im, cx, 1080, f"REALISMUS {v}%", FX(44), WH, ease((t - 0.3) / 0.3))
    chip(im, "FAST UNHEIMLICH", cx, 1170, 34, CY, INK, back((t - 1.3) / 0.4))
    return (cx - 120, cy)

def r_anim(im, d, t, dur):
    v = int(600000 * ease((t - 0.2) / 1.2))
    gtext(im, f"{v:,}".replace(",", "."), 720, 650, FX(118), LIME, CY)
    atext(im, 720, 735, "GTA 6", FS(30), WH, ease((t - 0.2) / 0.3))
    D = ImageDraw.Draw(im, "RGBA")
    for i in range(10):
        s = back((t - 0.3 - i * 0.07) / 0.3)
        if s < 0.2: continue
        x = 500 + (i % 5) * 110; yf = 920 + (i // 5) * 150
        mode = i % 3
        person(D, x, yf, 120 * s, (230, 235, 250) if i % 2 else LIME, "up" if (mode == 1 and int(t * 3 + i) % 2) else "down", t + i, run=mode != 1)
    b = ease((t - 1.3) / 0.4)
    if b > 0:
        D = ImageDraw.Draw(im, "RGBA")
        D.rounded_rectangle([490, 1130, 950, 1200], 22, fill=(255, 255, 255, int(28 * b)), outline=(255, 255, 255, int(80 * b)), width=2)
        atext(im, 520, 1165, "GTA 5:", FS(30), (190, 194, 220), b, "lm")
        atext(im, 920, 1165, "NUR 55.000", FX(36), RD, b, "rm")
    return (720, 650)

def trash(D, x, yb, s=1.0):
    D.rounded_rectangle([x - 60 * s, yb - 150 * s, x + 60 * s, yb], int(12 * s), fill=(80, 90, 110, 255))
    D.rounded_rectangle([x - 72 * s, yb - 172 * s, x + 72 * s, yb - 148 * s], int(10 * s), fill=(100, 112, 136, 255))
    for k in (-30, 0, 30): D.line([(x + k * s, yb - 130 * s), (x + k * s, yb - 20 * s)], fill=(60, 68, 86, 255), width=6)

def r_smell(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(470, 1110), (970, 1110)], fill=(255, 255, 255, 90), width=3)
    trash(D, 560, 1110)
    for k in range(5):
        ph = (t * 0.6 + k / 5) % 1
        pts = []
        for j in range(16):
            yy = 930 - j * 14 - ph * 120
            xx = 540 + k * 12 + 18 * math.sin(j * 0.7 + t * 5 + k) + ph * 220
            pts.append((xx, yy))
        D.line(pts, fill=GRN + (int(220 * (1 - ph)),), width=7)
    turned = t > 1.0
    px = 860 + (40 * ease((t - 1.0) / 0.4) if turned else 0)
    person(D, px, 1110, 330, (230, 232, 245), "down", 0)
    if turned:
        D.line([(px - 22, 1110 - 330 + 50), (px - 54, 1110 - 330 + 66)], fill=(230, 232, 245, 255), width=14)
        chip(im, "IGITT!", 860, 700, 40, GRN, INK, back((t - 1.0) / 0.35) * (1 + 0.05 * math.sin(t * 10)))
    else:
        atext(im, 860, 720, "?", FX(80), WH, ease((t - 0.4) / 0.3))
    return (600, 880)

def cup(D, x, yb, s):
    D.polygon([(x - 50 * s, yb - 130 * s), (x + 50 * s, yb - 130 * s), (x + 38 * s, yb), (x - 38 * s, yb)], fill=(245, 245, 250, 255))
    D.rectangle([x - 47 * s, yb - 95 * s, x + 44 * s, yb - 60 * s], fill=(160, 100, 60, 255))
    D.rounded_rectangle([x - 58 * s, yb - 150 * s, x + 58 * s, yb - 128 * s], int(8 * s), fill=(60, 40, 30, 255))

def shake(D, x, yb, s):
    D.rounded_rectangle([x - 42 * s, yb - 150 * s, x + 42 * s, yb], int(18 * s), fill=(250, 120, 170, 255))
    D.rounded_rectangle([x - 46 * s, yb - 175 * s, x + 46 * s, yb - 145 * s], int(10 * s), fill=(240, 240, 250, 255))
    D.line([(x + 12 * s, yb - 175 * s), (x + 30 * s, yb - 230 * s)], fill=(255, 220, 90, 255), width=max(3, int(10 * s)))
    D.rectangle([x - 42 * s, yb - 100 * s, x + 42 * s, yb - 60 * s], fill=(255, 255, 255, 200))

def bar(im, x0, y, w, p, col, label, a):
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([x0, y - 16, x0 + w, y + 16], 16, fill=(255, 255, 255, int(35 * a)))
    if p > 0.05: D.rounded_rectangle([x0, y - 16, x0 + w * p, y + 16], 16, fill=col + (int(255 * a),))
    atext(im, x0 + w / 2, y - 42, label, FS(24), WH, a)

def r_food(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s1 = back((t - 0.1) / 0.4); s2 = back((t - 0.6) / 0.4)
    if s1 > 0.2:
        cup(D, 600, 940, s1)
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            D.line([(580 + k * 20 + 8 * math.sin(ph * 9 + k), 790 - ph * 90), (580 + k * 20 + 8 * math.sin(ph * 9 + 2 + k), 760 - ph * 90)], fill=(255, 255, 255, int(160 * (1 - ph))), width=5)
        bar(im, 500, 1080, 200, ease((t - 0.5) / 0.8), LIME, "AUSDAUER", ease((t - 0.3) / 0.3))
    if s2 > 0.2:
        shake(D, 840, 940, s2)
        bar(im, 740, 1080, 200, ease((t - 1.0) / 0.8), RD, "GESUNDHEIT", ease((t - 0.8) / 0.3))
    if t > 1.6:
        chip(im, "+ BOOST", 720, 1170, 32, ORG, INK, back((t - 1.6) / 0.35))
    return (600 if t < 0.8 else 840, 860)

def r_fuel(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); cx, cy, R = 720, 1000, 230
    D.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=(255, 255, 255, 18))
    D.arc([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=(255, 255, 255, 90), width=6)
    D.arc([cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14], 180, 210, fill=RD + (255,), width=18)
    for k in range(9):
        a = math.radians(180 + k * 22.5)
        D.line([(cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a)), (cx + (R - 10) * math.cos(a), cy + (R - 10) * math.sin(a))], fill=(255, 255, 255, 200), width=5)
    atext(im, cx - R + 50, cy - 30, "E", FX(44), RD); atext(im, cx + R - 50, cy - 30, "F", FX(44), WH)
    p = 1 - ease((t - 0.3) / 1.4) * 0.92
    a = math.radians(180 + 180 * p)
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(cx, cy), (cx + (R - 50) * math.cos(a), cy + (R - 50) * math.sin(a))], fill=ORG + (255,), width=10)
    D.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(240, 240, 250, 255))
    # pump icon
    ic = RD if (p < 0.2 and int(t * 4) % 2 == 0) else (200, 204, 220)
    D.rounded_rectangle([cx - 30, cy - 130, cx + 14, cy - 70], 6, fill=ic + (255,))
    D.rectangle([cx - 22, cy - 122, cx + 6, cy - 104], fill=(14, 16, 32, 255))
    D.line([(cx + 14, cy - 120), (cx + 32, cy - 108), (cx + 32, cy - 80)], fill=ic + (255,), width=5)
    if p < 0.2:
        chip(im, "TANK LEER!", cx, 1130, 34, RD, WH, back((t - 1.7) / 0.35) * (1 + 0.05 * math.sin(t * 10)))
    car(D, 720, 700, 0.62, (236, 90, 150))
    return (cx, cy - 60)

def r_transit(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    # rail
    D.line([(450, 830), (990, 830)], fill=(255, 255, 255, 120), width=5)
    for x in range(450, 990, 30): D.line([(x, 822), (x + 12, 838)], fill=(255, 255, 255, 50), width=3)
    tx = 1000 - ((t * 330) % 900)
    for k in range(3):
        x0 = tx + k * 170
        if x0 > 1000 or x0 + 160 < 440: continue
        D.rounded_rectangle([max(440, x0), 700, min(1000, x0 + 160), 818], 20, fill=(200, 210, 230, 255))
        for wx in range(int(x0) + 16, int(x0) + 150, 36):
            if 445 < wx < 990: D.rectangle([wx, 722, min(wx + 24, 995), 758], fill=(40, 60, 110, 255))
        if 445 < x0 + 10 < 990: D.rectangle([max(445, x0), 776, min(995, x0 + 160), 786], fill=(255, 200, 60, 255))
    # road + bus
    D.line([(450, 1110), (990, 1110)], fill=(255, 255, 255, 120), width=5)
    bp = ease(t / 1.2); bx = 400 + 330 * bp
    D.rounded_rectangle([bx - 150, 960, bx + 150, 1090], 22, fill=(255, 200, 60, 255))
    for wx in range(int(bx) - 130, int(bx) + 110, 52): D.rounded_rectangle([wx, 980, wx + 40, 1024], 6, fill=(40, 50, 80, 255))
    for wx in (-90, 90): D.ellipse([bx + wx - 28, 1070, bx + wx + 28, 1126], fill=(16, 16, 22, 255))
    # stop sign
    D.line([(930, 1110), (930, 960)], fill=(220, 224, 240, 255), width=8)
    D.ellipse([892, 900, 968, 976], fill=GRN + (255,), outline=(255, 255, 255, 255), width=5)
    atext(im, 930, 938, "H", FX(44), INK)
    chip(im, "WIRKLICH NUTZBAR", 720, 1180, 30, (255, 200, 60), INK, back((t - 1.2) / 0.35))
    return (bx, 1000)

def r_storm(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    fl = any(bt < t < bt + 0.12 for bt in (0.9, 1.05, 2.4))
    if fl: D.rounded_rectangle([432, 562, 1008, 1228], 46, fill=(220, 230, 255, 60))
    rng = random.Random(5)
    for i in range(60):
        x = 450 + rng.random() * 540; y0 = 600 + ((rng.random() * 600 + t * 900) % 600)
        D.line([(x, y0), (x - 10, y0 + 34)], fill=(170, 200, 255, 120), width=3)
    for k, (cx, cy, r) in enumerate([(560, 650, 70), (650, 630, 90), (760, 650, 80), (860, 640, 70)]):
        ox = 14 * math.sin(t * 1.4 + k)
        D.ellipse([cx - r + ox, cy - r * 0.7, cx + r + ox, cy + r * 0.7], fill=(70, 78, 100, 255))
    if fl:
        D.line([(720, 690), (690, 780), (730, 780), (680, 900)], fill=(255, 240, 150, 255), width=8)
    # shelter
    D.polygon([(800, 940), (990, 940), (990, 960), (780, 960)], fill=CY + (255,))
    D.line([(820, 960), (820, 1110)], fill=(220, 224, 240, 255), width=6); D.line([(970, 960), (970, 1110)], fill=(220, 224, 240, 255), width=6)
    D.line([(450, 1110), (990, 1110)], fill=(255, 255, 255, 110), width=3)
    for i, (x0, dl) in enumerate([(500, 0.2), (580, 0.45), (460, 0.7)]):
        p = ease((t - dl) / 1.3); x = x0 + (860 + i * 40 - x0) * p
        person(D, x, 1110, 170, (230, 232, 245), "up" if p < 1 else "down", t + i, run=p < 1)
    chip(im, "ALLE SUCHEN SCHUTZ", 720, 1180, 30, CY, INK, back((t - 1.5) / 0.35))
    return (700, 900)

SC = [r_hook, r_anim, r_smell, r_food, r_fuel, r_transit, r_storm, S13.h_cta]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "6 KRASSE DETAILS"

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.5, 0.9]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 2, R[2][0] * 0.3, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p15_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
