"""Reel 32 – Countdown Teil 1: Dein Handy in GTA 6. v3-Stil + Follow-Cliffhanger."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes16
import scenes14 as S14
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
import scenes12
from scenes13 import (atext, gtext, chip, tile, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import person, star, stamp, car
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

VID = "32_Countdown_Teil1_Handy"
S7.SCRIPTS7[VID] = [
    "Noch sechs Tage bis G T A sechs! Teil eins: Dein Handy wird komplett neu!",
    "Eins: Das Handy ist ein echtes Objekt in deiner Hand, kein Overlay mehr.",
    "Zwei: Snapmatic ist zurück, das Instagram von G T A.",
    "Drei: Jason und Lucia dürfen nichts posten. Sie sind auf der Flucht.",
    "Vier: Im Feed entdeckst du, was gerade in der Stadt passiert.",
    "Fünf: Mit der App Ryde Me reist du blitzschnell durch die Map.",
    "Sechs: Ignorierst du die Nachrichten deines Partners, leidet eure Beziehung.",
    "Morgen in Teil zwei: So raubst du in G T A sechs richtig ab. Folg mir, sonst verpasst du es!",
]
S7.COMMENT[VID] = ("", "")
S7.COVER[VID] = ("GTA 6", "COUNTDOWN")
HEAD = [("NOCH 6 TAGE", "BIS GTA 6!"), ("DEIN HANDY IST", "ECHT IN DER HAND"), ("SNAPMATIC", "IST ZURÜCK"), ("POSTEN?", "VERBOTEN!"),
        ("DER FEED ZEIGT", "WAS GERADE PASSIERT"), ("RYDE ME", "= SCHNELLREISE"), ("NACHRICHTEN IGNORIEREN", "= BEZIEHUNG LEIDET"), ("MORGEN TEIL 2", "NICHT VERPASSEN!")]
SRC = [None, "QUELLE: ROCKSTAR / EXTENDED LOOK", "QUELLE: ROCKSTAR", "QUELLE: ROCKSTAR (INTERVIEW)", "QUELLE: ROCKSTAR", "LAUT MEHREREN VORSCHAUEN", "LAUT VORSCHAUEN", None]
GOLD = (255, 205, 70); GRN = (90, 210, 120); SKIN = (236, 190, 150)
ACC = [(RD, MAG), (CY, VIO), (MAG, ORG), (RD, VIO), (CY, LIME), (GOLD, ORG), (MAG, RD), (LIME, CY)]

def phone(D, cx, cy, h, a=255):
    w = h * 0.5
    D.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], int(h * 0.09), fill=(24, 26, 40, a), outline=(140, 146, 180, a), width=5)
    sx0, sy0, sx1, sy1 = cx - w / 2 + 12, cy - h / 2 + 14, cx + w / 2 - 12, cy + h / 2 - 14
    D.rounded_rectangle([sx0, sy0, sx1, sy1], int(h * 0.07), fill=(244, 245, 252, a))
    D.rounded_rectangle([cx - w * 0.16, sy0 + 8, cx + w * 0.16, sy0 + 26], 9, fill=(24, 26, 40, a))
    return sx0, sy0, sx1, sy1

def appbar(im, D, box, title, col):
    sx0, sy0, sx1, sy1 = box
    D.rectangle([sx0, sy0 + 34, sx1, sy0 + 84], fill=col + (255,))
    atext(im, (sx0 + sx1) / 2, sy0 + 59, title, FX(26), WH)

# ---------- scenes ----------
def c_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    rem = max(0, 23 * 3600 + 59 * 60 + 59 - int(t * 7))
    vals = ["06", f"{rem // 3600:02d}", f"{rem // 60 % 60:02d}", f"{rem % 60:02d}"]
    labs = ["TAGE", "STD", "MIN", "SEK"]
    for i, (v, l) in enumerate(zip(vals, labs)):
        s = back((t - i * 0.1) / 0.35)
        if s < 0.15: continue
        cx = 520 + i * 135; cy = 830
        hw, hh = 58 * s, 80 * s
        D.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 18, fill=(255, 255, 255, 24), outline=(RD if i == 0 else (255, 255, 255)) + (160,), width=3)
        D.line([(cx - hw, cy), (cx + hw, cy)], fill=(0, 0, 0, 90), width=3)
        if i == 0: gtext(im, v, cx, cy, FX(84 * s), RD, MAG)
        else: atext(im, cx, cy, v, FX(70 * s), WH)
        atext(im, cx, cy + 112, l, FS(24), (200, 204, 225), s)
        D = ImageDraw.Draw(im, "RGBA")
    if int(t * 2) % 2 == 0: D.ellipse([706, 790, 718, 802], fill=(255, 255, 255, 0))
    chip(im, "TEIL 1: DEIN HANDY", 720, 1060, 36, LIME, INK, back((t - 1.0) / 0.4))
    chip(im, "COUNTDOWN-SERIE", 720, 1150, 26, (255, 255, 255), INK, back((t - 1.3) / 0.4))
    return (520, 830)

def c_object(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s = 0.75 + 0.25 * ease((t - 0.1) / 0.8)
    cy = 880 + 60 * (1 - ease(t / 0.6))
    box = phone(D, 720, cy, 520 * s)
    appbar(im, D, box, "HOME", VIO)
    sx0, sy0, sx1, sy1 = box
    for r in range(3):
        for c in range(3):
            x = sx0 + 26 + c * (sx1 - sx0 - 40) / 3; y = sy0 + 110 + r * 90
            q = back((t - 0.4 - (r * 3 + c) * 0.05) / 0.3)
            if q > 0.2:
                col = [CY, MAG, LIME, ORG, VIO, RD, GOLD, GRN, (60, 120, 255)][r * 3 + c]
                D.rounded_rectangle([x, y, x + 56 * q, y + 56 * q], 14, fill=col + (255,))
    # thumbs / hand
    hx = 720 + 130 * s; hy = cy + 120 * s
    D.rounded_rectangle([hx - 40, hy - 150, hx + 50, hy + 120], 40, fill=SKIN + (255,))
    D.rounded_rectangle([hx - 120, hy + 40, hx + 30, hy + 100], 30, fill=SKIN + (255,))
    D.rounded_rectangle([720 - 130 * s - 50, cy - 40, 720 - 130 * s + 20, cy + 180], 30, fill=SKIN + (255,))
    chip(im, "KEIN HUD MEHR", 720, 1185, 30, RD, WH, back((t - 1.2) / 0.35))
    return (720, cy)

def feedpost(im, D, x0, y0, x1, h, seed, t, likes=True):
    rng = random.Random(seed)
    c1 = rng.choice([CY, MAG, ORG, VIO, LIME]); c2 = rng.choice([VIO, (60, 120, 255), RD])
    D.ellipse([x0, y0, x0 + 30, y0 + 30], fill=c1 + (255,))
    D.rounded_rectangle([x0 + 40, y0 + 8, x0 + 40 + rng.randint(60, 120), y0 + 22], 7, fill=(170, 174, 196, 255))
    w = x1 - x0
    k = np.linspace(0, 1, int(w), dtype=np.float32)[None, :, None]
    g = (np.array(c1, np.float32) * (1 - k) + np.array(c2, np.float32) * k).astype(np.uint8)
    im.paste(Image.fromarray(np.repeat(g, int(h), 0)), (int(x0), int(y0 + 40)))

def c_snap(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = phone(D, 720, 890, 600)
    sx0, sy0, sx1, sy1 = box
    appbar(im, D, box, "SNAPMATIC", MAG)
    top = int(sy0 + 86); scr = Image.new("RGB", (int(sx1 - sx0), int(sy1 - top)), (244, 245, 252)); ds = ImageDraw.Draw(scr, "RGBA")
    off = -((t * 90) % 230); base = int((t * 90) // 230)
    for i in range(-1, 4):
        y = 12 + i * 230 + off
        feedpost(scr, ds, 16, y, scr.width - 16, 130, i + base, t)
        ds = ImageDraw.Draw(scr, "RGBA")
        scenes12.heart(ImageDraw.Draw(scr), 34, y + 192, 0.55, RD)
    m = Image.new("L", scr.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, -40, scr.width - 1, scr.height - 1], 30, fill=255)
    im.paste(scr, (int(sx0), top), m)
    for k in range(3):
        ht = t - 0.5 - k * 0.4
        if ht > 0:
            ph = (ht % 1.2) / 1.2
            scenes12.heart(ImageDraw.Draw(im), 900 + k * 25, 1050 - ph * 300, 1.0 * (1 - ph * 0.4), RD)
    return (720, 890)

def c_nopost(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = phone(D, 720, 890, 600)
    sx0, sy0, sx1, sy1 = box
    appbar(im, D, box, "NEUER POST", (60, 66, 100))
    D.rounded_rectangle([sx0 + 20, sy0 + 110, sx1 - 20, sy0 + 330], 18, fill=(210, 214, 230, 255))
    person(D, (sx0 + sx1) / 2, sy0 + 320, 190, (150, 156, 190), "up", 0)
    tap = t > 0.8
    bc = RD if tap and int(t * 6) % 2 else (60, 120, 255)
    D.rounded_rectangle([sx0 + 30, sy1 - 110, sx1 - 30, sy1 - 40], 30, fill=bc + (255,))
    atext(im, (sx0 + sx1) / 2, sy1 - 75, "POSTEN", FX(32), WH)
    if not tap:
        p = ease(t / 0.8)
        fx, fy = 900 - 100 * p, 1300 - 230 * p
        D.ellipse([fx - 22, fy - 22, fx + 22, fy + 22], fill=SKIN + (255,))
    stamp(im, "AUF DER FLUCHT", 720, 870, t - 1.0, RD, -9, 56)
    return (720, sy1 - 75)

def c_feed(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = phone(D, 640, 890, 580)
    sx0, sy0, sx1, sy1 = box
    appbar(im, D, box, "FEED", (60, 120, 255))
    D.rounded_rectangle([sx0 + 14, sy0 + 100, sx1 - 14, sy0 + 320], 16, fill=(30, 34, 52, 255))
    rng = random.Random(3)
    for i in range(9):
        x = sx0 + 30 + i * 22; hh = rng.randint(30, 90)
        D.rectangle([x, sy0 + 300 - hh, x + 16, sy0 + 300], fill=(90, 100, 140, 255))
    fl = 0.5 + 0.5 * math.sin(t * 12)
    D.ellipse([sx0 + 100, sy0 + 170, sx0 + 170, sy0 + 240], fill=(255, 140, 40, int(160 + 90 * fl)))
    lv = int(t * 3) % 2
    D.rounded_rectangle([sx0 + 26, sy0 + 114, sx0 + 106, sy0 + 146], 8, fill=RD + (255 if lv else 170,))
    atext(im, sx0 + 66, sy0 + 130, "LIVE", FX(22), WH)
    D.rounded_rectangle([sx0 + 20, sy0 + 340, sx1 - 40, sy0 + 362], 10, fill=(170, 174, 196, 255))
    D.rounded_rectangle([sx0 + 20, sy0 + 376, sx1 - 90, sy0 + 398], 10, fill=(200, 204, 222, 255))
    p = back((t - 0.8) / 0.4)
    if p > 0.2:
        mx, my = 880, 880
        D.rounded_rectangle([mx - 90 * p, my - 120 * p, mx + 90 * p, my + 120 * p], 22, fill=(40, 60, 70, 255), outline=(255, 255, 255, 120), width=3)
        D.line([(mx - 80 * p, my + 30 * p), (mx + 80 * p, my - 50 * p)], fill=(90, 110, 120, 255), width=10)
        for r in range(3):
            ph = (t * 0.8 + r / 3) % 1; rr = 10 + ph * 60 * p
            D.ellipse([mx - rr, my - rr, mx + rr, my + rr], outline=CY + (int(220 * (1 - ph)),), width=3)
        D.ellipse([mx - 18, my - 18, mx + 18, my + 18], fill=CY + (255,))
    chip(im, "HINFAHREN!", 720, 1180, 30, CY, INK, back((t - 1.3) / 0.35))
    return (640, 900) if t < 0.8 else (880, 880)

def c_ryde(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = phone(D, 720, 890, 600)
    sx0, sy0, sx1, sy1 = box
    appbar(im, D, box, "RYDE ME", GOLD)
    D.rectangle([sx0, sy0 + 84, sx1, sy1 - 120], fill=(226, 232, 222, 255))
    for k in range(6):
        D.line([(sx0, sy0 + 120 + k * 70), (sx1, sy0 + 150 + k * 60)], fill=(255, 255, 255, 255), width=10)
        D.line([(sx0 + 30 + k * 48, sy0 + 84), (sx0 + 10 + k * 52, sy1 - 120)], fill=(255, 255, 255, 255), width=8)
    pts = [(sx0 + 40, sy1 - 160), (sx0 + 90, sy0 + 330), (sx0 + 190, sy0 + 300), (sx1 - 40, sy0 + 130)]
    p = ease((t - 0.2) / 1.4)
    segs = []; L = 0
    for a, b in zip(pts, pts[1:]): l = math.dist(a, b); segs.append((a, b, l)); L += l
    dd = p * L; cur = pts[0]; drawn = [pts[0]]
    for a, b, l in segs:
        if dd >= l: drawn.append(b); dd -= l; cur = b
        else:
            cur = (a[0] + (b[0] - a[0]) * dd / l, a[1] + (b[1] - a[1]) * dd / l); drawn.append(cur); break
    if len(drawn) > 1: D.line(drawn, fill=(60, 120, 255, 255), width=8)
    D.ellipse([pts[-1][0] - 14, pts[-1][1] - 14, pts[-1][0] + 14, pts[-1][1] + 14], fill=RD + (255,))
    D.ellipse([cur[0] - 16, cur[1] - 16, cur[0] + 16, cur[1] + 16], fill=GOLD + (255,), outline=(20, 22, 30, 255), width=4)
    D.rectangle([sx0, sy1 - 120, sx1, sy1], fill=(250, 250, 255, 255))
    eta = max(0, int(9 * (1 - p)))
    atext(im, (sx0 + sx1) / 2, sy1 - 82, f"ANKUNFT IN {eta} MIN", FX(24), INK)
    D.rounded_rectangle([sx0 + 30, sy1 - 56, sx1 - 30, sy1 - 18], 19, fill=INK + (255,))
    atext(im, (sx0 + sx1) / 2, sy1 - 37, "FAHRT BUCHEN", FX(20), GOLD)
    return (cur[0], cur[1])

def heartcrack(D, cx, cy, s, crack):
    r = 46 * s
    D.ellipse([cx - 2 * r, cy - r, cx, cy + r * 0.9], fill=RD + (255,))
    D.ellipse([cx, cy - r, cx + 2 * r, cy + r * 0.9], fill=RD + (255,))
    D.polygon([(cx - 1.95 * r, cy + 0.2 * r), (cx + 1.95 * r, cy + 0.2 * r), (cx, cy + 2.2 * r)], fill=RD + (255,))
    if crack > 0:
        pts = [(cx, cy - r * 0.6), (cx - 18 * s, cy), (cx + 14 * s, cy + 0.6 * r), (cx - 10 * s, cy + 1.3 * r), (cx, cy + 1.9 * r)]
        n = max(2, int(len(pts) * crack))
        D.line(pts[:n], fill=(14, 16, 30, 255), width=max(4, int(10 * s)))

def c_chat(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = phone(D, 660, 890, 600)
    sx0, sy0, sx1, sy1 = box
    appbar(im, D, box, "PARTNER", (60, 66, 100))
    msgs = ["Wo bist du?", "Hallo??", "Antworte mir!", "OK. Danke."]
    for i, m in enumerate(msgs):
        s = back((t - 0.15 - i * 0.35) / 0.3)
        if s < 0.2: continue
        y = sy0 + 110 + i * 90
        f = FX(24); w = f.getlength(m) + 40
        D.rounded_rectangle([sx0 + 16, y, sx0 + 16 + w * s, y + 60], 22, fill=((230, 232, 245) if i < 3 else (255, 210, 210)) + (255,))
        if s > 0.8: atext(im, sx0 + 36, y + 30, m, f, INK, 1, "lm")
        D = ImageDraw.Draw(im, "RGBA")
    n = min(4, int(max(0, t - 0.15) / 0.35) + 1)
    D.ellipse([sx1 - 60, sy0 + 40, sx1 - 20, sy0 + 80], fill=RD + (255,))
    atext(im, sx1 - 40, sy0 + 60, str(n), FX(22), WH)
    crack = ease((t - 1.5) / 0.4)
    heartcrack(D, 900, 760, 1.0, crack)
    D = ImageDraw.Draw(im, "RGBA")
    bw = 160; v = 1 - 0.7 * ease((t - 0.4) / 1.4)
    D.rounded_rectangle([820, 880, 820 + bw, 906], 13, fill=(255, 255, 255, 40))
    D.rounded_rectangle([820, 880, 820 + bw * v, 906], 13, fill=(RD if v < 0.5 else GRN) + (255,))
    atext(im, 900, 940, "BEZIEHUNG", FS(22), WH)
    return (660, 900)

def c_end(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s = back(t / 0.4)
    if s > 0.2:
        x0, y0, x1, y1 = 720 - 250 * s, 840 - 220 * s, 720 + 250 * s, 840 + 220 * s
        k = np.linspace(0, 1, int(x1 - x0), dtype=np.float32)[None, :, None]
        g = (np.array((60, 20, 40), np.float32) * (1 - k) + np.array((20, 20, 60), np.float32) * k).astype(np.uint8)
        card = Image.fromarray(np.repeat(g, int(y1 - y0), 0))
        dc = ImageDraw.Draw(card)
        dc.text((card.width / 2, card.height / 2 - 30), "TEIL 2", font=FX(110 * s), fill=GOLD, anchor="mm")
        dc.text((card.width / 2, card.height / 2 + 70), "RICHTIG ABRAUBEN", font=FX(44 * s), fill=WH, anchor="mm")
        rev = ease((t - 0.5) / 1.2)
        card = card.filter(ImageFilter.GaussianBlur(14 * (1 - rev * 0.55)))
        m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], 30, fill=255)
        im.paste(card, (int(x0), int(y0)), m)
        D = ImageDraw.Draw(im, "RGBA")
        D.rounded_rectangle([x0, y0, x1, y1], 30, outline=GOLD + (200,), width=4)
        lx, ly = 720, 840 - 10 + 6 * math.sin(t * 5)
        D.rounded_rectangle([lx - 46, ly - 10, lx + 46, ly + 64], 12, fill=(250, 250, 255, 235))
        D.arc([lx - 32, ly - 60, lx + 32, ly + 10], 180, 360, fill=(250, 250, 255, 235), width=12)
        D.ellipse([lx - 9, ly + 18, lx + 9, ly + 36], fill=INK + (255,))
    chip(im, "MORGEN", 720, 600, 30, RD, WH, back((t - 0.3) / 0.35) * (1 + 0.05 * math.sin(t * 9)))
    return (720, 840)

def end_overlay(im, ot):
    D = ImageDraw.Draw(im, "RGBA")
    done = ot > 3.2
    b = back(ot / 0.35) * (1 + (0.06 * math.sin(ot * 10) if not done else 0))
    if b < 0.12: return (720, 1180)
    hw, hh = 210 * b, 56 * b
    col1, col2 = (LIME, CY) if not done else ((60, 66, 100), (60, 66, 100))
    k = np.linspace(0, 1, int(2 * hw), dtype=np.float32)[None, :, None]
    g = (np.array(col1, np.float32) * (1 - k) + np.array(col2, np.float32) * k).astype(np.uint8)
    gi = Image.fromarray(np.repeat(g, int(2 * hh), 0)); m = Image.new("L", gi.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, gi.width - 1, gi.height - 1], int(hh), fill=255)
    if not done:
        for r in range(3):
            ph = (ot * 1.2 + r / 3) % 1; e = 12 + ph * 50
            D.rounded_rectangle([720 - hw - e, 1180 - hh - e, 720 + hw + e, 1180 + hh + e], int(hh + e), outline=LIME + (int(120 * (1 - ph)),), width=3)
    im.paste(gi, (int(720 - hw), int(1180 - hh)), m)
    ImageDraw.Draw(im).text((720, 1180), "+ FOLGEN" if not done else "✓ GEFOLGT", font=FX(52 * b), fill=INK if not done else WH, anchor="mm")
    p = ease((ot - 2.0) / 0.8)
    if p > 0:
        fx, fy = 900 - 150 * min(1, p), 1350 - 150 * min(1, p)
        tap = 2.9 < ot < 3.2
        r = 26 if not tap else 22
        D = ImageDraw.Draw(im, "RGBA")
        D.ellipse([fx - r, fy - r, fx + r, fy + r], fill=SKIN + (255,), outline=(255, 255, 255, 255), width=4)
        if tap: D.ellipse([fx - 50, fy - 50, fx + 50, fy + 50], outline=(255, 255, 255, 160), width=4)
    return (720, 1180)

def nudge(fr, idx, t, dur):
    if idx not in (3, 4, 5): return
    a = ease(t / 0.3) if idx == 3 else 1.0
    pulse = 1 + 0.04 * math.sin((t + idx) * 7)
    chip(fr, "TEIL 2 KOMMT MORGEN · JETZT FOLGEN", 690, 1505, 25 * pulse, GOLD, INK, a)

SC = [c_hook, c_object, c_snap, c_nopost, c_feed, c_ryde, c_chat, c_end]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "TEIL 1: DEIN HANDY"
S13.TOP0 = "COUNTDOWN · TEIL 1"; S13.TOPLAST = "TEIL 2 MORGEN"; S13.EXTRA = nudge
S13.comment13 = end_overlay

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.85, 0.9, 0.45]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 7, min(R[7][0] - 0.1, 4.4), T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p17_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
