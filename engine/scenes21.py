"""Zwischen-Reel 36 – 5 Fehler am ersten Tag. Hook in Sek. 0, Folgen-Aufruf am Anfang, Loop-Ende."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
ORIG_COMMENT = S13.comment13
import scenes18 as S18
import scenes17 as S17
import scenes16, scenes14
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import stamp
from PIL import Image, ImageDraw
import numpy as np

VID = "36_Fuenf_Fehler"
S7.SCRIPTS7[VID] = [
    "Mach in G T A sechs bloß nicht diese fünf Fehler! Folg mir, damit du am Release nichts falsch machst.",
    "Fehler eins: Bargeld in der Tasche lassen. Stirbst du, ist es weg.",
    "Fehler zwei: Den Tresor sprengen. Dabei geht Beute kaputt.",
    "Fehler drei: Zu lange im Laden bleiben. Dann umstellt dich die Polizei.",
    "Fehler vier: Im selben Outfit flüchten. Die Polizei erkennt dich wieder.",
    "Fehler fünf: Nachrichten vom Partner ignorieren. Eure Beziehung leidet.",
    "Welchen Fehler hättest du gemacht? Schreib die Zahl in die Kommentare! Und merk dir:",
]
S7.COMMENT[VID] = ("WELCHER FEHLER?", "Nummer 1, sicher!")
S7.COVER[VID] = ("GTA 6", "5 FEHLER")
HEAD = [("MACH BLOSS NICHT", "DIESE 5 FEHLER!"), ("FEHLER 1", "BARGELD BEHALTEN"), ("FEHLER 2", "TRESOR SPRENGEN"), ("FEHLER 3", "ZU LANGE IM LADEN"),
        ("FEHLER 4", "GLEICHES OUTFIT"), ("FEHLER 5", "PARTNER IGNORIEREN"), ("WELCHEN FEHLER", "HÄTTEST DU GEMACHT?")]
SRC = [None, "LAUT MEHREREN VORSCHAUEN", "LAUT VORSCHAU (IGN)", "LAUT VORSCHAU (IGN)", "QUELLE: EDGE-MAGAZIN, VORSCHAU", "LAUT VORSCHAUEN", None]
ACC = [(RD, ORG), (ORG, RD), (RD, MAG), (RD, (60, 120, 255)), (CY, RD), (MAG, RD), (LIME, RD)]
SKIN = (236, 190, 150)

def tri(D, cx, cy, s, fill, outline):
    pts = [(cx, cy - 170 * s), (cx + 190 * s, cy + 150 * s), (cx - 190 * s, cy + 150 * s)]
    D.polygon(pts, fill=fill)
    D.line(pts + [pts[0]], fill=outline, width=max(4, int(16 * s)), joint="curve")

def f_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    # hazard stripes band
    off = (t * 220) % 80
    for x in range(-80, 1160, 80):
        xx = x + off
        D.polygon([(xx, 1090), (xx + 40, 1090), (xx + 80, 1140), (xx + 40, 1140)], fill=(255, 205, 40, 255))
        D.polygon([(xx + 40, 1090), (xx + 80, 1090), (xx + 120, 1140), (xx + 80, 1140)], fill=(20, 20, 26, 255))
    s = back(t / 0.35) * (1 + 0.05 * math.sin(t * 12))
    sh = math.sin(t * 60) * 10 * max(0, 1 - t / 0.5)
    cx, cy = 760 + sh, 840
    for k in range(4):
        r = (1.0 + k * 0.18 + 0.1 * math.sin(t * 6)) * s
        tri(D, cx, cy, r, (0, 0, 0, 0), RD + (int(120 - k * 28),))
    tri(D, cx, cy, s, RD + (255,), (255, 255, 255, 255))
    if s > 0.3:
        D.rounded_rectangle([cx - 18 * s, cy - 90 * s, cx + 18 * s, cy + 40 * s], int(10 * s), fill=WH + (255,))
        D.ellipse([cx - 20 * s, cy + 66 * s, cx + 20 * s, cy + 106 * s], fill=WH + (255,))
    gtext(im, "5 FEHLER", 760, 1210, FX(96 * min(1, back((t - 0.15) / 0.35) + 0.001)), RD, ORG)
    # early follow
    q = dur * 0.5
    if t > q:
        ot = t - q
        done = ot > 1.9
        b = back(ot / 0.3) * (1 + (0.06 * math.sin(ot * 10) if not done else 0))
        if b > 0.12:
            hw, hh = 190 * b, 52 * b
            col1, col2 = (LIME, CY) if not done else ((60, 66, 100), (60, 66, 100))
            k = np.linspace(0, 1, int(2 * hw), dtype=np.float32)[None, :, None]
            g = (np.array(col1, np.float32) * (1 - k) + np.array(col2, np.float32) * k).astype(np.uint8)
            gi = Image.fromarray(np.repeat(g, int(2 * hh), 0)); m = Image.new("L", gi.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, gi.width - 1, gi.height - 1], int(hh), fill=255)
            D = ImageDraw.Draw(im, "RGBA")
            if not done:
                for r in range(3):
                    ph = (ot * 1.2 + r / 3) % 1; e = 10 + ph * 46
                    D.rounded_rectangle([760 - hw - e, 640 - hh - e, 760 + hw + e, 640 + hh + e], int(hh + e), outline=LIME + (int(120 * (1 - ph)),), width=3)
            im.paste(gi, (int(760 - hw), int(640 - hh)), m)
            ImageDraw.Draw(im).text((760, 640), "+ FOLGEN" if not done else "✓ GEFOLGT", font=FX(46 * b), fill=INK if not done else WH, anchor="mm")
            p = ease((ot - 0.7) / 0.6)
            if p > 0:
                fx, fy = 980 - 120 * p, 780 - 120 * p
                D = ImageDraw.Draw(im, "RGBA"); tap = 1.6 < ot < 1.9
                D.ellipse([fx - 24, fy - 24, fx + 24, fy + 24], fill=SKIN + (255,), outline=(255, 255, 255, 255), width=4)
                if tap: D.ellipse([fx - 46, fy - 46, fx + 46, fy + 46], outline=(255, 255, 255, 160), width=4)
        return (760, 640)
    return (cx, cy)

def f_end(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); act = int(t * 2.4) % 5
    for i in range(5):
        s = back((t - i * 0.07) / 0.3)
        if s < 0.1: continue
        cx = 500 + i * 110; cy = 700; on = i == act; h = 46 * s * (1.15 if on else 1)
        D.rounded_rectangle([cx - h, cy - h, cx + h, cy + h], 20, fill=(RD + (255,)) if on else (255, 255, 255, 28), outline=(255, 255, 255, 110), width=3)
        D.text((cx, cy), str(i + 1), font=FX(56 * s), fill=WH, anchor="mm")
    return (720, 700)

def fx(fr, idx, t, dur):
    n = len(SC)
    if 1 <= idx <= 5:
        e = t - 0.15
        if e > 0:
            s = back(e / 0.3)
            if s > 0.15:
                L = Image.new("RGBA", (200, 70), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
                dl.rounded_rectangle([4, 4, 196, 66], 20, fill=RD + (255,), outline=(255, 255, 255, 255), width=4)
                dl.text((100, 35), f"✗ FEHLER {idx}", font=FX(30), fill=WH, anchor="mm")
                L = L.rotate(-8, expand=True, resample=Image.BICUBIC)
                L = L.resize((max(1, int(L.width * s)), max(1, int(L.height * s))), Image.BILINEAR)
                fr.paste(L, (int(930 - L.width / 2), int(565 - L.height / 2)), L)
    if idx == 0 and t < 0.25:
        fr.paste(RD, (0, 0), Image.new("L", (W, H), int(150 * (1 - t / 0.25))))
    if idx == n - 1 and t > dur - 0.3:
        fr.paste(RD, (0, 0), Image.new("L", (W, H), int(150 * (t - (dur - 0.3)) / 0.3)))

SC = [f_hook, scenes16.v_cash, S18.r_boom, S18.r_cops, scenes14.p_heat, S17.c_chat, f_end]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "NICHT MACHEN!"; S13.FACTLBL = "FEHLER"
S13.TOP0 = "VOR DEM RELEASE"; S13.TOPLAST = "DEINE MEINUNG"; S13.EXTRA = fx
S13.comment13 = ORIG_COMMENT

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.8, 0.8, 0.85, 0.85, 0.9, 0.8]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.85, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 0, 0.05, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p21_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
