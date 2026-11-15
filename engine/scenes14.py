"""Reel 29 – GTA 6 Polizei & Realismus, im festen v3-Stil (scenes13)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, tile, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
import scenes12
from PIL import Image, ImageDraw

VID = "29_GTA6_Polizei"
BLUE = (60, 120, 255)
S7.SCRIPTS7[VID] = [
    "In G T A sechs entkommst du der Polizei nicht mehr so leicht!",
    "Eins: Die Polizei merkt sich dein Aussehen, deine Kleidung und deine Waffen.",
    "Zwei: Klamotten wechseln oder die Waffe wegwerfen macht dich schwerer erkennbar.",
    "Drei: Polizeihunde können dich schnappen und festhalten.",
    "Vier: Nagelbänder siehst du nachts kaum.",
    "Fünf: Teure Autos haben Peilsender, und die Besitzer melden den Diebstahl.",
    "Sechs: Ein Opfer kann erst mitspielen und dich dann von hinten angreifen.",
    "Welcher Fakt ist am krassesten? Schreib die Zahl in die Kommentare!",
]
S7.COMMENT[VID] = ("WELCHER FAKT?", "Fakt 3, die Hunde!")
S7.COVER[VID] = ("GTA 6", "POLIZEI")
HEAD = [("DER POLIZEI", "ENTKOMMST DU KAUM"), ("DIE POLIZEI", "MERKT SICH ALLES"), ("NEUES OUTFIT", "= WENIGER ERKANNT"), ("POLIZEIHUNDE", "SCHNAPPEN DICH"),
        ("NAGELBÄNDER", "NACHTS KAUM ZU SEHEN"), ("TEURE AUTOS", "HABEN PEILSENDER"), ("OPFER", "SCHLAGEN ZURÜCK"), ("WELCHER FAKT", "IST AM KRASSESTEN?")]
SRC = [None] + ["QUELLE: EDGE-MAGAZIN, VORSCHAU"] * 6 + [None]
ACC = [(RD, BLUE), (CY, BLUE), (LIME, CY), (ORG, RD), (VIO, CY), (MAG, VIO), (RD, ORG), (LIME, MAG)]

def star(D, cx, cy, r, fill, outline=None, w=4):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5; rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    D.polygon(pts, fill=fill, outline=outline, width=w)

def person(D, x, yf, h, col, arms="down", t=0.0, run=False, a=255):
    if h < 20: return
    r = h * 0.12; c = col + (a,)
    D.ellipse([x - r, yf - h, x + r, yf - h + 2 * r], fill=c)
    bt, bb = yf - h + 2.25 * r, yf - h * 0.42
    D.rounded_rectangle([x - r * 1.15, bt, x + r * 1.15, bb], int(r * 0.8), fill=c)
    sw = math.sin(t * 14) * (0.5 if run else 0)
    lw = max(4, int(r * 0.55))
    for s in (-1, 1):
        D.line([(x + s * r * 0.5, bb - 4), (x + s * r * 0.5 + math.sin(sw * s) * h * 0.3, yf)], fill=c, width=lw)
        if arms == "up":
            D.line([(x + s * r * 1.05, bt + r * 0.4), (x + s * r * 1.9, bt - r * 1.6)], fill=c, width=lw)
        else:
            D.line([(x + s * r * 1.05, bt + r * 0.4), (x + s * r * 1.5 - math.sin(sw * s) * h * 0.15, bb + r * 0.2)], fill=c, width=lw)

def stamp(im, txt, cx, cy, t, col=RD, rot=10, size=96):
    if t <= 0: return
    e = ease(t / 0.18); s = 1 + 1.2 * (1 - e)
    f = FX(size); w = int(f.getlength(txt)) + 70
    L = Image.new("RGBA", (w, int(size * 1.7)), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.rounded_rectangle([6, 6, w - 6, L.height - 6], 24, fill=(20, 8, 14, 235), outline=col, width=10)
    dl.text((w / 2, L.height / 2), txt, font=f, fill=col, anchor="mm")
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    L = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s))), Image.BILINEAR)
    if e < 1: L.putalpha(L.split()[3].point(lambda z: int(z * e)))
    sh = math.sin(t * 70) * 10 * max(0, 1 - t / 0.35)
    im.paste(L, (int(cx - L.width / 2 + sh), int(cy - L.height / 2)), L)

# ---------- scenes ----------
def p_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    k = int(t * 6) % 2
    for side, col in ((-1, RD), (1, BLUE)):
        on = (k == 0) == (side < 0)
        a = 120 if on else 30
        for rr in range(5):
            R = 330 - rr * 55
            D.ellipse([720 + side * 210 - R, 700 - R * 0.6, 720 + side * 210 + R, 700 + R * 0.6], fill=col + (int(a * 0.18),))
    D.rounded_rectangle([500, 660, 940, 740], 30, fill=(18, 20, 36, 255), outline=(255, 255, 255, 90), width=3)
    D.rounded_rectangle([515, 672, 712, 728], 22, fill=RD + (255 if k == 0 else 70,))
    D.rounded_rectangle([728, 672, 925, 728], 22, fill=BLUE + (255 if k == 1 else 70,))
    for i in range(5):
        s = back((t - 0.1 - i * 0.16) / 0.3)
        cx = 535 + i * 92
        star(D, cx, 900, 40, (255, 255, 255, 30), (255, 255, 255, 90), 3)
        if s > 0.1:
            pulse = 1 + 0.08 * math.sin(t * 10 + i)
            star(D, cx, 900, 40 * s * pulse, (255, 214, 64, 255))
    chip(im, "KEINE CHANCE MEHR?", 720, 1060, 38, RD, WH, back((t - 1.1) / 0.4) * (1 + 0.04 * math.sin(t * 9)))
    return (720, 900)

def _icon(D, kind, cx, cy, col):
    c = col + (255,)
    if kind == 0:
        D.ellipse([cx - 22, cy - 26, cx + 22, cy + 22], outline=c, width=5)
        D.ellipse([cx - 11, cy - 8, cx - 3, cy], fill=c); D.ellipse([cx + 3, cy - 8, cx + 11, cy], fill=c)
        D.arc([cx - 12, cy - 4, cx + 12, cy + 12], 20, 160, fill=c, width=4)
    elif kind == 1:
        D.polygon([(cx - 28, cy - 18), (cx - 12, cy - 26), (cx - 6, cy - 18), (cx + 6, cy - 18), (cx + 12, cy - 26), (cx + 28, cy - 18), (cx + 22, cy - 2), (cx + 15, cy - 6), (cx + 15, cy + 26), (cx - 15, cy + 26), (cx - 15, cy - 6), (cx - 22, cy - 2)], fill=c)
    elif kind == 2:
        D.rectangle([cx - 30, cy - 14, cx + 26, cy - 2], fill=c); D.polygon([(cx + 4, cy - 2), (cx + 18, cy - 2), (cx + 12, cy + 24), (cx - 2, cy + 24)], fill=c)
        D.rectangle([cx - 34, cy - 18, cx - 24, cy - 10], fill=c)
    else:
        D.rounded_rectangle([cx - 26, cy - 14, cx + 18, cy + 12], 6, fill=c); D.polygon([(cx + 18, cy - 8), (cx + 32, cy - 16), (cx + 32, cy + 14), (cx + 18, cy + 6)], fill=c)
        D.line([(cx - 4, cy - 14), (cx - 14, cy - 28)], fill=c, width=5)

def p_heat(im, d, t, dur):
    labels = ["AUSSEHEN", "KLEIDUNG", "WAFFEN", "KAMERAS"]
    tgt = (720, 700)
    for i, lab in enumerate(labels):
        y = 680 + i * 120; t0 = 0.25 + i * 0.32
        s = ease((t - t0) / 0.3)
        if s <= 0.02: continue
        hit = t > t0 + 0.45
        D = ImageDraw.Draw(im, "RGBA")
        off = (1 - s) * 60
        D.rounded_rectangle([470 + off, y - 46, 970 + off, y + 46], 22, fill=(255, 255, 255, int(20 * s)), outline=((RD if hit else WH) + (int(120 * s),)), width=3)
        D.rounded_rectangle([484 + off, y - 34, 552 + off, y + 34], 16, fill=(RD if hit else (60, 66, 100)) + (int(255 * s),))
        _icon(D, i, 518 + off, y, WH)
        atext(im, 576 + off, y, lab, FX(36), WH, s, "lm")
        if hit:
            p = back((t - t0 - 0.45) / 0.3)
            chip(im, "ERFASST", 900, y, 24, RD, WH, p)
            tgt = (720, y)
    if t > 1.0:
        D = ImageDraw.Draw(im, "RGBA")
        for i in range(5):
            on = i < min(5, int((t - 1.0) * 3) + 1)
            star(D, 560 + i * 80, 1170, 26, (255, 214, 64, 255) if on else (255, 255, 255, 40))
    return tgt

def p_clothes(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    cols = [RD, (255, 200, 60), CY]
    ci = min(2, int(max(0, t - 0.4) / 0.6))
    fl = ((t - 0.4) % 0.6) < 0.1 and t > 0.4 and ci < 3
    D.ellipse([495, 1080, 705, 1120], fill=(0, 0, 0, 90))
    person(D, 600, 1100, 400, cols[ci], "down", t)
    if fl:
        D.ellipse([480, 680, 720, 1110], fill=(255, 255, 255, 60))
    # dropped weapon
    g = ease((t - 0.9) / 0.5)
    if g > 0:
        gx, gy = 700 + 60 * g, 900 + 190 * g
        D.rectangle([gx - 26, gy - 8, gx + 22, gy + 2], fill=(200, 205, 220, 255)); D.polygon([(gx + 2, gy + 2), (gx + 14, gy + 2), (gx + 9, gy + 22), (gx - 3, gy + 22)], fill=(200, 205, 220, 255))
    # meter
    p = ease((t - 0.3) / 1.8); val = int(100 - 75 * p)
    x0, y0, y1 = 880, 660, 1100
    D.rounded_rectangle([x0, y0, x0 + 56, y1], 28, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=3)
    hh = (y1 - y0 - 12) * val / 100
    mc = tuple(int(RD[i] * p * 0 + (RD[i] * (val / 100) + LIME[i] * (1 - val / 100))) for i in range(3))
    D.rounded_rectangle([x0 + 6, y1 - 6 - hh, x0 + 50, y1 - 6], 22, fill=mc + (255,))
    atext(im, x0 + 28, y1 + 40, f"{val}%", FX(40), WH)
    atext(im, x0 + 28, y0 - 30, "ERKANNT", FS(24), WH)
    return (600, 860)

def dog(D, x, y, s, t, col=(230, 235, 245)):
    c = col + (255,)
    D.ellipse([x - 70 * s, y - 32 * s, x + 50 * s, y + 18 * s], fill=c)
    D.ellipse([x + 32 * s, y - 62 * s, x + 86 * s, y - 14 * s], fill=c)
    D.polygon([(x + 70 * s, y - 50 * s), (x + 104 * s, y - 36 * s), (x + 74 * s, y - 24 * s)], fill=c)
    D.polygon([(x + 40 * s, y - 56 * s), (x + 50 * s, y - 86 * s), (x + 60 * s, y - 58 * s)], fill=c)
    D.line([(x - 66 * s, y - 20 * s), (x - 100 * s, y - 44 * s + math.sin(t * 20) * 8 * s)], fill=c, width=max(3, int(9 * s)))
    for k, lx in enumerate((-50, -26, 18, 38)):
        sw = math.sin(t * 22 + k * 1.7) * 26 * s
        D.line([(x + lx * s, y + 8 * s), (x + lx * s + sw, y + 52 * s)], fill=c, width=max(3, int(10 * s)))
    D.rounded_rectangle([x + 14 * s, y - 20 * s, x + 46 * s, y - 8 * s], 4, fill=CY + (255,))

def p_dog(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(460, 1080), (980, 1080)], fill=(255, 255, 255, 110), width=4)
    for i in range(8):
        x = 460 + ((i * 70 - t * 520) % 520)
        D.line([(x, 1100), (x + 30, 1100)], fill=(255, 255, 255, 50), width=3)
    catch = 1.5
    p = ease(t / catch)
    if t < catch:
        px = 900; person(D, px, 1080, 300, (150, 156, 190), "down", t, run=True)
        dx = 470 + (px - 120 - 470) * p
        dog(D, dx, 1020, 1.25, t)
    else:
        D.rounded_rectangle([780, 1030, 980, 1078], 22, fill=(150, 156, 190, 255))
        D.ellipse([930, 1000, 990, 1060], fill=(150, 156, 190, 255))
        dog(D, 850, 1000, 1.25, 0.0)
        stamp(im, "GESCHNAPPT!", 720, 800, t - catch, RD, 8, 74)
    chip(im, "K-9", 540, 690, 36, CY, INK, back((t - 0.2) / 0.3))
    return (760, 980)

def p_spike(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    hz = 720
    D.polygon([(690, hz), (750, hz), (980, 1200), (460, 1200)], fill=(26, 28, 40, 255))
    for i in range(7):
        z = ((i / 7) + t * 0.6) % 1; y = hz + (1200 - hz) * z ** 1.8; w = 3 + 14 * z ** 1.8; h_ = 6 + 40 * z ** 1.8
        D.rectangle([720 - w / 2, y, 720 + w / 2, y + h_], fill=(255, 220, 120, int(160 * z)))
    D.polygon([(640, 1200), (800, 1200), (750, hz + 20), (690, hz + 20)], fill=(255, 245, 200, 18))
    yb = 1010; rev = ease((t - 0.9) / 0.4)
    xl, xr = 470 + (720 - 470) * (hz - yb) / (hz - 1200) * 0, 970
    xl = 720 - (720 - 460) * (yb - hz) / (1200 - hz); xr = 720 + (980 - 720) * (yb - hz) / (1200 - hz)
    D.rectangle([xl + 6, yb - 6, xr - 6, yb + 6], fill=(40, 42, 52, 255))
    for x in range(int(xl + 14), int(xr - 10), 22):
        c = (int(60 + 140 * rev), int(62 + 193 * rev * 0.78), int(70 + 0 * rev))
        D.polygon([(x - 7, yb - 4), (x, yb - 22), (x + 7, yb - 4)], fill=(LIME if rev > 0.5 else (70, 72, 84)) + (255,))
    if rev > 0:
        D.rounded_rectangle([xl - 10, yb - 40, xr + 10, yb + 24], 18, outline=LIME + (int(255 * rev),), width=4)
        chip(im, "KAUM ZU SEHEN", 720, 1150, 30, LIME, INK, back((t - 1.1) / 0.35))
    # moon
    D.ellipse([880, 600, 940, 660], fill=(230, 232, 255, 220)); D.ellipse([898, 592, 958, 652], fill=(14, 16, 32, 255))
    return (720, yb)

def car(D, cx, cy, s, col):
    c = col + (255,)
    D.rounded_rectangle([cx - 190 * s, cy - 30 * s, cx + 190 * s, cy + 40 * s], int(30 * s), fill=c)
    D.polygon([(cx - 100 * s, cy - 28 * s), (cx - 50 * s, cy - 82 * s), (cx + 70 * s, cy - 82 * s), (cx + 130 * s, cy - 28 * s)], fill=c)
    D.polygon([(cx - 80 * s, cy - 30 * s), (cx - 42 * s, cy - 70 * s), (cx + 6 * s, cy - 70 * s), (cx + 6 * s, cy - 30 * s)], fill=(20, 24, 44, 255))
    D.polygon([(cx + 16 * s, cy - 30 * s), (cx + 16 * s, cy - 70 * s), (cx + 62 * s, cy - 70 * s), (cx + 106 * s, cy - 30 * s)], fill=(20, 24, 44, 255))
    for wx in (-115, 115):
        D.ellipse([cx + (wx - 40) * s, cy + 2 * s, cx + (wx + 40) * s, cy + 82 * s], fill=(16, 16, 22, 255))
        D.ellipse([cx + (wx - 18) * s, cy + 24 * s, cx + (wx + 18) * s, cy + 60 * s], fill=(190, 194, 210, 255))
    D.rectangle([cx + 170 * s, cy - 18 * s, cx + 190 * s, cy - 2 * s], fill=(255, 240, 180, 255))

def p_tracker(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    cy = 880
    for k in range(3):
        ph = (t * 0.7 + k / 3) % 1; r = 60 + ph * 260
        D.ellipse([720 - r, cy - 40 - r * 0.7, 720 + r, cy - 40 + r * 0.7], outline=MAG + (int(160 * (1 - ph)),), width=4)
    car(D, 720, cy, 1.15, (236, 90, 150))
    p = back((t - 0.3) / 0.4)
    if p > 0.1:
        px, py = 720, cy - 160 - 10 * math.sin(t * 4)
        D.ellipse([px - 34 * p, py - 34 * p, px + 34 * p, py + 34 * p], fill=LIME + (255,))
        D.polygon([(px - 24 * p, py + 22 * p), (px + 24 * p, py + 22 * p), (px, py + 64 * p)], fill=LIME + (255,))
        D.ellipse([px - 13 * p, py - 13 * p, px + 13 * p, py + 13 * p], fill=(14, 16, 32, 255))
        atext(im, 720, cy - 250, "GPS", FX(30), LIME, ease((t - 0.5) / 0.3))
    n = ease((t - 1.1) / 0.4); off = (1 - n) * 120
    if n > 0.02:
        D = ImageDraw.Draw(im, "RGBA")
        D.rounded_rectangle([470, 1060 + off, 970, 1180 + off], 28, fill=(250, 250, 255, int(240 * n)))
        D.ellipse([494, 1090 + off, 554, 1150 + off], fill=RD + (int(255 * n),))
        atext(im, 524, 1120 + off, "!", FX(40), WH, n)
        atext(im, 576, 1098 + off, "BESITZER", FS(24), (110, 112, 130), n, "lm")
        atext(im, 576, 1140 + off, "DIEBSTAHL GEMELDET", FX(32), INK, n, "lm")
    return (720, cy)

def p_victim(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    q = dur * 0.5
    D.line([(470, 1120), (970, 1120)], fill=(255, 255, 255, 90), width=3)
    turned = t > q
    person(D, 840, 1120, 330, (120, 126, 160), "down", 0)
    vc = RD if turned else (230, 232, 245)
    lean = ease((t - q) / 0.25) * 70 if turned else 0
    person(D, 590 + lean, 1120, 330, vc, "down" if turned else "up", 0)
    if not turned:
        chip(im, "ERGIBT SICH …", 600, 700, 30, WH, INK, back((t - 0.3) / 0.35))
    else:
        f = 1 + 0.15 * math.sin(t * 14)
        atext(im, 590 + lean, 720, "!", FX(120 * f), RD)
        stamp(im, "ANGRIFF!", 760, 1000, t - q - 0.15, RD, -8, 80)
    return (650, 900)

SC = [p_hook, p_heat, p_clothes, p_dog, p_spike, p_tracker, p_victim, S13.h_cta]

S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "6 POLIZEI-FAKTEN"

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.8, 0.9]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 6, R[6][0] * 0.3, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p14_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
