"""Reel 40 – „Klingt erfunden, ist aber echt“. v3-Stil, Hook Sek. 0, Folgen direkt danach, Loop."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
ORIG_COMMENT = S13.comment13
import scenes21 as S21
import scenes14
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, tile, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import stamp, person
from PIL import Image, ImageDraw
import numpy as np

VID = "40_Klingt_erfunden"
S7.SCRIPTS7[VID] = [
    "Diese G T A sechs Fakten klingen erfunden, aber sie sind echt! Folg mir jetzt, sonst verpasst du die nächsten!",
    "Eins: Der zweite Trailer wurde komplett im Spiel aufgenommen, auf einer normalen PS fünf.",
    "Zwei: Zwischen G T A fünf und sechs liegen dreizehn Jahre. Die längste Pause der Serie.",
    "Drei: G T A fünf erschien auf drei Konsolen-Generationen.",
    "Vier: Es gilt als das profitabelste Unterhaltungsprodukt aller Zeiten, mehr als jeder Film.",
    "Fünf: Und der Mitgründer, der die Geschichten schrieb, ist bei G T A sechs nicht mehr dabei.",
    "Welcher Fakt klingt am meisten erfunden? Schreib die Zahl! Und merk dir:",
]
S7.DISPLAY.update({"dreizehn": "13"})
S7.COMMENT[VID] = ("WELCHER FAKT?", "Nummer 1, krass!")
S7.COVER[VID] = ("GTA 6", "ECHT?!")
HEAD = [("KLINGT ERFUNDEN", "IST ABER ECHT!"), ("TRAILER 2", "100% IM SPIEL"), ("13 JAHRE", "LÄNGSTE PAUSE"), ("GTA 5 AUF", "3 GENERATIONEN"),
        ("PROFITABLER", "ALS JEDER FILM"), ("DER STORY-AUTOR", "IST NICHT DABEI")]
HEAD.append(("WELCHER FAKT", "KLINGT ERFUNDEN?"))
SRC = [None, "QUELLE: ROCKSTAR GAMES", "GTA 5: 2013 · GTA 6: 2026", "PS3/360 · PS4/ONE · PS5/SERIES", "LAUT ANALYSEN (2018)", "QUELLE: DAN HOUSER (INTERVIEW)", None]
GRN = (90, 210, 120); GOLD = (255, 205, 70)
ACC = [(GRN, LIME), (CY, VIO), (ORG, MAG), (MAG, CY), (GOLD, ORG), (RD, VIO), (LIME, MAG)]

def k_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    flip = ease((t - 0.7) / 0.35)
    w = 260 * abs(math.cos(flip * math.pi)) if flip < 1 else 260
    fake = flip < 0.5
    col = RD if fake else GRN
    s = back(t / 0.35)
    if s > 0.1:
        hw, hh = w * s, 150 * s
        D.rounded_rectangle([760 - hw, 860 - hh, 760 + hw, 860 + hh], 34, fill=(16, 18, 32, 245), outline=col + (255,), width=8)
        if hw > 60:
            atext(im, 760, 860, "FAKE?" if fake else "ECHT!", FX(int(110 * hw / 260)), col)
    if not fake:
        stamp(im, "100% ECHT", 760, 1090, t - 1.15, GRN, -8, 56)
    q = dur * 0.45
    if t > q:
        S21.f_hook.__globals__  # keep import
        ot = t - q
        _follow(im, ot, 760, 640)
        return (760, 640)
    return (760, 860)

def _follow(im, ot, cx, cy):
    done = ot > 1.9
    b = back(ot / 0.3) * (1 + (0.06 * math.sin(ot * 10) if not done else 0))
    if b < 0.12: return
    hw, hh = 190 * b, 52 * b
    col1, col2 = (LIME, CY) if not done else ((60, 66, 100), (60, 66, 100))
    k = np.linspace(0, 1, int(2 * hw), dtype=np.float32)[None, :, None]
    g = (np.array(col1, np.float32) * (1 - k) + np.array(col2, np.float32) * k).astype(np.uint8)
    gi = Image.fromarray(np.repeat(g, int(2 * hh), 0)); m = Image.new("L", gi.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, gi.width - 1, gi.height - 1], int(hh), fill=255)
    D = ImageDraw.Draw(im, "RGBA")
    if not done:
        for r in range(3):
            ph = (ot * 1.2 + r / 3) % 1; e = 10 + ph * 46
            D.rounded_rectangle([cx - hw - e, cy - hh - e, cx + hw + e, cy + hh + e], int(hh + e), outline=LIME + (int(120 * (1 - ph)),), width=3)
    im.paste(gi, (int(cx - hw), int(cy - hh)), m)
    ImageDraw.Draw(im).text((cx, cy), "+ FOLGEN" if not done else "✓ GEFOLGT", font=FX(46 * b), fill=INK if not done else WH, anchor="mm")
    p = ease((ot - 0.7) / 0.6)
    if p > 0:
        fx, fy = cx + 220 - 120 * p, cy + 140 - 120 * p
        D = ImageDraw.Draw(im, "RGBA"); tap = 1.6 < ot < 1.9
        D.ellipse([fx - 24, fy - 24, fx + 24, fy + 24], fill=(236, 190, 150, 255), outline=(255, 255, 255, 255), width=4)
        if tap: D.ellipse([fx - 46, fy - 46, fx + 46, fy + 46], outline=(255, 255, 255, 160), width=4)

def console(D, cx, yb, h, col=(235, 238, 248), accent=CY):
    w = h * 0.36
    D.rounded_rectangle([cx - w / 2, yb - h, cx + w / 2, yb], int(w * 0.25), fill=col + (255,))
    D.rounded_rectangle([cx - w * 0.12, yb - h + 10, cx + w * 0.12, yb - 10], int(w * 0.1), fill=(30, 32, 46, 255))
    D.line([(cx - w / 2 + 8, yb - h * 0.3), (cx + w / 2 - 8, yb - h * 0.3)], fill=accent + (255,), width=3)

def k_trailer(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s = back(t / 0.4)
    if s > 0.2: console(D, 560, 1120, 330 * s)
    D.rounded_rectangle([660, 650, 980, 860], 18, fill=(20, 24, 40, 255), outline=(255, 255, 255, 120), width=4)
    for i in range(6):
        x = 680 + ((i * 70 + t * 160) % 300)
        D.rectangle([x, 760, x + 40, 840], fill=(70, 90, 150, 255))
    D.ellipse([880, 690, 940, 750], fill=(255, 160, 80, 255))
    if int(t * 3) % 2 == 0:
        D.ellipse([680, 668, 700, 688], fill=RD + (255,))
    atext(im, 740, 678, "REC", FX(24), RD)
    p = ease((t - 0.3) / 0.6)
    D.line([(640, 1010), (640 + 30 * p, 960), (660, 900)], fill=(255, 255, 255, int(150 * p)), width=4)
    chip(im, "KEIN RENDER-TRICK", 820, 950, 26, CY, INK, back((t - 0.9) / 0.35))
    chip(im, "100% IM SPIEL", 720, 1185, 32, LIME, INK, back((t - 1.4) / 0.35))
    return (820, 760)

def k_years(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    p = ease((t - 0.2) / 1.6)
    D.rounded_rectangle([480, 700, 960, 726], 13, fill=(255, 255, 255, 40))
    D.rounded_rectangle([480, 700, 480 + 480 * p, 726], 13, fill=ORG + (255,))
    atext(im, 480, 660, "2013", FX(34), WH, 1, "lm"); atext(im, 960, 660, "2026", FX(34), LIME if p > 0.95 else WH, 1, "rm")
    yr = 2013 + int(13 * p)
    gtext(im, str(yr), 720, 820, FX(96), ORG, MAG)
    b1 = ease((t - 0.8) / 0.5); b2 = ease((t - 1.0) / 0.9)
    D = ImageDraw.Draw(im, "RGBA")
    atext(im, 480, 930, "GTA 4 → 5", FS(28), WH, b1, "lm")
    D.rounded_rectangle([480, 955, 480 + 180 * b1, 990], 12, fill=(120, 126, 160, 255))
    atext(im, 480 + 180 * b1 + 16, 972, "5 J.", FX(28), WH, b1, "lm")
    atext(im, 480, 1040, "GTA 5 → 6", FS(28), WH, b2, "lm")
    D.rounded_rectangle([480, 1065, 480 + 400 * b2, 1100], 12, fill=RD + (255,))
    atext(im, 480 + 400 * b2 + 16, 1082, "13 J.", FX(28), RD, b2, "lm")
    return (720, 820)

def k_gens(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    labels = ["PS3/360", "PS4/ONE", "PS5/SERIES"]
    for i in range(3):
        s = back((t - i * 0.25) / 0.4)
        if s < 0.15: continue
        x = 540 + i * 180
        console(D, x, 1080, (200 + i * 40) * s, (60 + i * 60, 64 + i * 60, 90 + i * 55), [VIO, CY, LIME][i])
        D = ImageDraw.Draw(im, "RGBA")
        atext(im, x, 1120, labels[i], FS(22), WH, min(1, s))
    hop = min(2, max(0, (t - 0.5) / 0.6)); i0 = int(hop); f = hop - i0
    x = 540 + 180 * (i0 + ease(f) if i0 < 2 else 2); y = 760 - 120 * math.sin(math.pi * f if i0 < 2 else 0)
    D.ellipse([x - 46, y - 46, x + 46, y + 46], fill=(220, 225, 240, 255), outline=MAG + (255,), width=6)
    D.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(30, 32, 46, 255))
    atext(im, x, y - 70, "GTA V", FX(28), MAG)
    chip(im, "3 GENERATIONEN", 720, 1185, 30, MAG, WH, back((t - 1.6) / 0.35))
    return (x, y)

def k_profit(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    pods = [(600, 220, "FILM", (150, 156, 190)), (720, 340, "GTA 5", GOLD), (840, 160, "BUCH", (120, 126, 160))]
    for i, (x, h, lab, col) in enumerate(pods):
        p = ease((t - 0.2 - [1, 0, 2][i] * 0.2) / 0.6); hh = h * p
        D.rectangle([x - 55, 1110 - hh, x + 55, 1110], fill=col + (255,))
        if p > 0.5: atext(im, x, 1110 - hh - 30, lab, FX(28), WH)
    if t > 0.9:
        cs = back((t - 0.9) / 0.35); cx, cy = 720, 1110 - 340 - 110
        D.polygon([(cx - 50 * cs, cy + 30 * cs), (cx - 50 * cs, cy - 20 * cs), (cx - 25 * cs, cy + 5 * cs), (cx, cy - 35 * cs), (cx + 25 * cs, cy + 5 * cs), (cx + 50 * cs, cy - 20 * cs), (cx + 50 * cs, cy + 30 * cs)], fill=GOLD + (255,))
    atext(im, 720, 1080, "#1", FX(56), INK, ease((t - 0.8) / 0.3))
    return (720, 800)

def k_writer(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([480, 640, 740, 980], 12, fill=(240, 240, 248, 255))
    n = min(9, int(t * 6))
    for i in range(n):
        D.rounded_rectangle([505, 670 + i * 32, 505 + (200 if i % 3 else 140), 684 + i * 32], 6, fill=(150, 156, 190, 255))
    px = 505 + 200 * ((t * 1.5) % 1); py = 670 + min(8, n) * 32
    D.line([(px, py), (px + 60, py - 90)], fill=GOLD + (255,), width=10)
    p = ease((t - 0.6) / 1.2)
    person(D, 860 + 120 * p, 1110, 300, (150, 156, 190), "down", t, run=0 < p < 1)
    D.rectangle([940, 760, 990, 1110], fill=(60, 50, 40, 255)) if p < 0.2 else None
    chip(im, "AUTOR", 860 + 120 * p, 760, 26, RD, WH, 1 - p * 0.8)
    stamp(im, "NICHT DABEI", 720, 1180, t - 1.6, RD, -6, 50)
    return (610, 800)

SC = [k_hook, k_trailer, k_years, k_gens, k_profit, k_writer, S21.f_end]

def fx(fr, idx, t, dur):
    n = len(SC)
    if idx == 0 and t < 0.25: fr.paste(GRN, (0, 0), Image.new("L", (W, H), int(140 * (1 - t / 0.25))))
    if idx == n - 1 and t > dur - 0.3: fr.paste(GRN, (0, 0), Image.new("L", (W, H), int(140 * (t - (dur - 0.3)) / 0.3)))
    if 1 <= idx <= 5:
        s = back((t - 0.15) / 0.3)
        if s > 0.15:
            L = Image.new("RGBA", (190, 66), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
            dl.rounded_rectangle([4, 4, 186, 62], 20, fill=GRN + (255,), outline=(255, 255, 255, 255), width=4)
            dl.text((95, 33), "✓ ECHT", font=FX(30), fill=INK, anchor="mm")
            L = L.rotate(-8, expand=True, resample=Image.BICUBIC).resize((max(1, int(206 * s)), max(1, int(100 * s))), Image.BILINEAR)
            fr.paste(L, (int(930 - L.width / 2), int(565 - L.height / 2)), L)

S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "KLINGT ERFUNDEN!"; S13.FACTLBL = "FAKT"
S13.TOP0 = "100% ECHT"; S13.TOPLAST = "DEINE MEINUNG"; S13.EXTRA = fx
S13.comment13 = ORIG_COMMENT

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.8, 0.85, 0.85, 0.85, 0.85, 0.8]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.8, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 5, 0.5, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p25_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
