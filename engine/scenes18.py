"""Reel 33 – Countdown Teil 2: Richtig abrauben. Gleicher Stil wie Teil 1 (scenes17)."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes17 as S17
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import person, stamp, car
from scenes16 import bill
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

VID = "33_Countdown_Teil2_Raub"
DAYS = "05"; PART = 2
NEXT_T, NEXT_SUB = "TEIL 3", "6 REGIONEN VON LEONIDA"
S7.SCRIPTS7[VID] = [
    "Noch fünf Tage bis G T A sechs! Teil zwei: So raubst du richtig ab!",
    "Eins: Du kannst fast jeden Laden ausrauben, sogar Tankstellen und Handyläden.",
    "Zwei: Das echte Geld liegt im Tresor, und dafür brauchst du den Code.",
    "Drei: Ein Hehler kann dir den Code vorher per SMS schicken.",
    "Vier: Sprengen geht schneller, zerstört aber einen Teil der Beute.",
    "Fünf: Suchst du zu lange, umstellt dich die Polizei.",
    "Sechs: Mitarbeiter und Passanten können dich aufhalten.",
    "Morgen in Teil drei: Die sechs Regionen von Leonida. Folg mir, sonst verpasst du es!",
]
S7.COMMENT[VID] = ("", "")
S7.COVER[VID] = ("GTA 6", "COUNTDOWN")
HEAD = [("NOCH 5 TAGE", "BIS GTA 6!"), ("FAST JEDER LADEN", "IST AUSRAUBBAR"), ("DAS ECHTE GELD", "LIEGT IM TRESOR"), ("DER HEHLER", "SCHICKT DEN CODE"),
        ("SPRENGEN", "= WENIGER BEUTE"), ("ZU LANGSAM?", "POLIZEI UMSTELLT DICH"), ("PASSANTEN", "WEHREN SICH"), ("MORGEN TEIL 3", "NICHT VERPASSEN!")]
SRC = [None, "LAUT VORSCHAU BEI ROCKSTAR NORTH", "LAUT MEHREREN VORSCHAUEN", "LAUT VORSCHAU (TGG)", "LAUT VORSCHAU (IGN)", "LAUT VORSCHAU (IGN)", "LAUT MEHREREN VORSCHAUEN", None]
GOLD = (255, 205, 70); GRN = (90, 210, 120); BLUE = (60, 120, 255); SKIN = (236, 190, 150)
ACC = [(RD, MAG), (GOLD, ORG), (CY, VIO), (MAG, VIO), (ORG, RD), (RD, BLUE), (LIME, CY), (LIME, CY)]

def d_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    rem = max(0, 23 * 3600 + 59 * 60 + 59 - int(t * 7))
    vals = [DAYS, f"{rem // 3600:02d}", f"{rem // 60 % 60:02d}", f"{rem % 60:02d}"]
    for i, (v, l) in enumerate(zip(vals, ["TAGE", "STD", "MIN", "SEK"])):
        s = back((t - i * 0.1) / 0.35)
        if s < 0.15: continue
        cx = 520 + i * 135; cy = 830; hw, hh = 58 * s, 80 * s
        D.rounded_rectangle([cx - hw, cy - hh, cx + hw, cy + hh], 18, fill=(255, 255, 255, 24), outline=(RD if i == 0 else (255, 255, 255)) + (160,), width=3)
        D.line([(cx - hw, cy), (cx + hw, cy)], fill=(0, 0, 0, 90), width=3)
        if i == 0: gtext(im, v, cx, cy, FX(84 * s), RD, MAG)
        else: atext(im, cx, cy, v, FX(70 * s), WH)
        atext(im, cx, cy + 112, l, FS(24), (200, 204, 225), s)
        D = ImageDraw.Draw(im, "RGBA")
    chip(im, "TEIL 2: RICHTIG ABRAUBEN", 720, 1060, 34, GOLD, INK, back((t - 1.0) / 0.4))
    chip(im, "COUNTDOWN-SERIE", 720, 1150, 26, (255, 255, 255), INK, back((t - 1.3) / 0.4))
    return (520, 830)

def shop(D, im, x, w, label, col, s):
    yb = 1100; h = 300 * s
    if h < 20: return
    D.rectangle([x, yb - h, x + w, yb], fill=(44, 48, 72, 255))
    for k in range(6):
        D.rectangle([x + k * w / 6, yb - h, x + (k + 1) * w / 6, yb - h + 40 * s], fill=(col if k % 2 == 0 else (240, 240, 250)) + (255,))
    D.rectangle([x + 14, yb - h + 60 * s, x + w - 60, yb - 40], fill=(120, 170, 220, 200))
    D.rectangle([x + w - 50, yb - 150 * s, x + w - 12, yb], fill=(30, 32, 50, 255))
    atext(im, x + w / 2, yb - h - 26, label, FX(26 * s), WH, min(1, s))

def r_shops(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(450, 1100), (990, 1100)], fill=(255, 255, 255, 110), width=4)
    data = [(462, "TANKE", ORG), (642, "HANDY", CY), (822, "SHOP", MAG)]
    tgt = (720, 950)
    for i, (x, lab, col) in enumerate(data):
        s = back((t - 0.1 - i * 0.15) / 0.4)
        shop(D, im, x, 160, lab, col, s)
        D = ImageDraw.Draw(im, "RGBA")
        t0 = 0.8 + i * 0.35
        if t > t0:
            p = ease((t - t0) / 0.25); cx = x + 80; cy = 950
            for r in (70, 45):
                rr = r * (1.6 - 0.6 * p)
                D.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=RD + (int(230 * p),), width=5)
            D.line([(cx - 90, cy), (cx + 90, cy)], fill=RD + (int(200 * p),), width=3); D.line([(cx, cy - 90), (cx, cy + 90)], fill=RD + (int(200 * p),), width=3)
            tgt = (cx, cy)
    chip(im, "FAST ÜBERALL", 720, 1180, 32, GOLD, INK, back((t - 1.9) / 0.35))
    return tgt

def safe(D, im, cx, cy, s, dial_rot=0.0, open_p=0.0):
    w = 190 * s
    D.rounded_rectangle([cx - w, cy - w, cx + w, cy + w], int(24 * s), fill=(90, 96, 120, 255), outline=(40, 44, 60, 255), width=8)
    D.rounded_rectangle([cx - w + 22 * s, cy - w + 22 * s, cx + w - 22 * s, cy + w - 22 * s], int(16 * s), fill=(20, 22, 32, 255))
    if open_p > 0:
        for k in range(3):
            D.rounded_rectangle([cx - 120 * s, cy + 60 * s - k * 50 * s, cx + 120 * s, cy + 100 * s - k * 50 * s], 8, fill=GOLD + (255,), outline=(180, 130, 30, 255), width=3)
        dw = (2 * w - 44 * s) * (1 - open_p)
        D.rounded_rectangle([cx - w + 22 * s, cy - w + 22 * s, cx - w + 22 * s + dw, cy + w - 22 * s], int(16 * s), fill=(110, 116, 142, 255))
    else:
        D.rounded_rectangle([cx - w + 22 * s, cy - w + 22 * s, cx + w - 22 * s, cy + w - 22 * s], int(16 * s), fill=(110, 116, 142, 255))
        r = 80 * s
        D.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 64, 84, 255), outline=(200, 204, 222, 255), width=6)
        for k in range(12):
            a = dial_rot + k * math.pi / 6
            D.line([(cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a)), (cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a))], fill=(220, 224, 240, 255), width=4)
        D.line([(cx, cy), (cx + r * 0.6 * math.cos(dial_rot), cy + r * 0.6 * math.sin(dial_rot))], fill=RD + (255,), width=8)
        D.rectangle([cx + w - 60 * s, cy - 60 * s, cx + w - 40 * s, cy + 60 * s], fill=(200, 204, 222, 255))

def r_safe(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    op = ease((t - 1.7) / 0.5)
    if op > 0:
        for r in range(5): D.ellipse([720 - 230 - r * 20, 860 - 230 - r * 20, 720 + 230 + r * 20, 860 + 230 + r * 20], fill=GOLD + (int(18 * op),))
    safe(D, im, 720, 860, 1.0, t * 3.2, op)
    code = "4719"; n = min(4, int(max(0, t - 0.4) / 0.32))
    txt = " ".join(code[i] if i < n else "_" for i in range(4))
    atext(im, 720, 1150, txt, FX(56), LIME if n == 4 else WH)
    return (720, 860)

def r_sms(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    box = S17.phone(D, 640, 890, 600)
    sx0, sy0, sx1, sy1 = box
    S17.appbar(im, D, box, "HEHLER", (60, 66, 100))
    msgs = [("Hab was für dich.", 0.3), ("Tresor-Code:", 0.8), ("4 - 7 - 1 - 9", 1.2)]
    for i, (m, t0) in enumerate(msgs):
        s = back((t - t0) / 0.3)
        if s < 0.2: continue
        y = sy0 + 110 + i * 90
        f = FX(26 if i < 2 else 34); w = f.getlength(m) + 40
        D.rounded_rectangle([sx0 + 16, y, sx0 + 16 + w * s, y + 64], 22, fill=((230, 232, 245) if i < 2 else LIME) + (255,))
        if s > 0.8: atext(im, sx0 + 36, y + 32, m, f, INK, 1, "lm")
        D = ImageDraw.Draw(im, "RGBA")
    if t > 0.3 and t < 1.2 and int(t * 6) % 2 == 0:
        D.ellipse([sx1 - 60, sy0 + 40, sx1 - 20, sy0 + 80], fill=RD + (255,))
    s2 = back((t - 1.5) / 0.4)
    if s2 > 0.2:
        safe(D, im, 890, 1000, 0.42 * s2, 0.0, 0)
        D = ImageDraw.Draw(im, "RGBA")
        D.ellipse([850, 900, 930, 980], fill=GRN + (230,)); D.line([(868, 942), (886, 958), (914, 922)], fill=WH + (255,), width=8)
    return (640, sy0 + 300)

def boom(D, cx, cy, r, a):
    pts = []
    for k in range(18):
        ang = k * math.pi / 9; rr = r if k % 2 == 0 else r * 0.55
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    D.polygon(pts, fill=ORG + (int(255 * a),))
    pts2 = [(cx + (p[0] - cx) * 0.6, cy + (p[1] - cy) * 0.6) for p in pts]
    D.polygon(pts2, fill=GOLD + (int(255 * a),))

def r_boom(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); tb = 1.0
    sh = math.sin(t * 60) * 12 * max(0, 1 - (t - tb) / 0.4) if t > tb else 0
    safe(D, im, 720 + sh, 860, 0.9, 0.0, ease((t - tb) / 0.2))
    if t < tb:
        for k in range(3):
            x = 640 + k * 50
            D.rounded_rectangle([x - 16, 640, x + 16, 760], 8, fill=RD + (255,))
        fx = 690 + 40 * (t / tb); D.line([(690, 640), (690, 600), (fx, 590)], fill=(230, 220, 200, 255), width=4)
        if int(t * 12) % 2: D.ellipse([fx - 10, 580, fx + 10, 600], fill=GOLD + (255,))
    else:
        a = max(0, 1 - (t - tb) / 0.6)
        if a > 0: boom(D, 720, 860, 160 + 300 * (1 - a), a)
        rng = random.Random(3)
        for i in range(8):
            p = ease((t - tb) / 0.8); ang = rng.uniform(-math.pi, 0)
            x = 720 + math.cos(ang) * 230 * p; y = 820 + math.sin(ang) * 180 * p + 260 * p * p
            bill(D, x, y, ang + t * 3, 0.55, int(255 * (1 - p * 0.6)))
            if p > 0.3: D.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(30, 30, 30, int(200 * p)))
    v = 1 - 0.45 * ease((t - tb) / 0.6)
    D = ImageDraw.Draw(im, "RGBA")
    D.rounded_rectangle([500, 1140, 940, 1172], 16, fill=(255, 255, 255, 40))
    D.rounded_rectangle([500, 1140, 500 + 440 * v, 1172], 16, fill=(GOLD if v > 0.8 else RD) + (255,))
    atext(im, 720, 1112, "BEUTE", FS(24), WH)
    return (720, 860)

def r_cops(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); cx, cy = 720, 880
    D.rounded_rectangle([cx - 70, cy - 70, cx + 70, cy + 70], 12, fill=(70, 76, 110, 255), outline=(255, 255, 255, 160), width=4)
    atext(im, cx, cy, "LADEN", FX(26), WH)
    p = ease((t - 0.2) / 1.6); R = 270 - 120 * p
    fl = int(t * 6) % 2
    for k in range(8):
        a = k * math.pi / 4 + t * 0.4 * (1 - p)
        x = cx + R * math.cos(a); y = cy + R * 0.85 * math.sin(a)
        D.rounded_rectangle([x - 30, y - 18, x + 30, y + 18], 8, fill=(240, 240, 250, 255))
        D.rectangle([x - 12, y - 16, x - 2, y - 8], fill=(RD if fl else BLUE) + (255,)); D.rectangle([x + 2, y - 16, x + 12, y - 8], fill=(BLUE if fl else RD) + (255,))
    D.ellipse([cx - R - 40, cy - R * 0.85 - 40, cx + R + 40, cy + R * 0.85 + 40], outline=(RD if fl else BLUE) + (90,), width=4)
    sec = max(0, 30 - int(t * 9))
    atext(im, 720, 620, f"00:{sec:02d}", FX(56), RD if sec < 10 else WH)
    chip(im, "UMSTELLT!", 720, 1180, 32, RD, WH, back((t - 1.8) / 0.35) * (1 + 0.05 * math.sin(t * 10)))
    return (cx, cy)

def r_people(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    D.line([(450, 1110), (990, 1110)], fill=(255, 255, 255, 100), width=3)
    person(D, 890, 1110, 320, (120, 124, 150), "down", 0)
    D.rounded_rectangle([858, 790, 922, 812], 8, fill=(20, 20, 26, 255))
    p = ease((t - 0.3) / 1.0)
    person(D, 520 + 180 * p, 1110, 300, (230, 232, 245), "down", t, run=p < 1)
    p2 = ease((t - 0.6) / 1.0)
    person(D, 470 + 130 * p2, 1110, 280, GOLD, "down", t + 1, run=p2 < 1)
    stamp(im, "STOPP!", 720, 760, t - 1.5, RD, -8, 84)
    return (700, 900)

def d_end(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    s = back(t / 0.4)
    if s > 0.2:
        x0, y0, x1, y1 = 720 - 250 * s, 840 - 220 * s, 720 + 250 * s, 840 + 220 * s
        k = np.linspace(0, 1, int(x1 - x0), dtype=np.float32)[None, :, None]
        g = (np.array((20, 40, 60), np.float32) * (1 - k) + np.array((20, 20, 60), np.float32) * k).astype(np.uint8)
        card = Image.fromarray(np.repeat(g, int(y1 - y0), 0)); dc = ImageDraw.Draw(card)
        dc.text((card.width / 2, card.height / 2 - 30), NEXT_T, font=FX(110 * s), fill=GOLD, anchor="mm")
        dc.text((card.width / 2, card.height / 2 + 70), NEXT_SUB, font=S13.fit(FX, NEXT_SUB, 44 * s, 440 * s), fill=WH, anchor="mm")
        rev = ease((t - 0.5) / 1.2)
        card = card.filter(ImageFilter.GaussianBlur(14 * (1 - rev * 0.55)))
        m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, card.width - 1, card.height - 1], 30, fill=255)
        im.paste(card, (int(x0), int(y0)), m)
        D = ImageDraw.Draw(im, "RGBA")
        D.rounded_rectangle([x0, y0, x1, y1], 30, outline=GOLD + (200,), width=4)
        lx, ly = 720, 830 + 6 * math.sin(t * 5)
        D.rounded_rectangle([lx - 46, ly - 10, lx + 46, ly + 64], 12, fill=(250, 250, 255, 235))
        D.arc([lx - 32, ly - 60, lx + 32, ly + 10], 180, 360, fill=(250, 250, 255, 235), width=12)
        D.ellipse([lx - 9, ly + 18, lx + 9, ly + 36], fill=INK + (255,))
    chip(im, "MORGEN", 720, 600, 30, RD, WH, back((t - 0.3) / 0.35) * (1 + 0.05 * math.sin(t * 9)))
    return (720, 840)

def nudge(fr, idx, t, dur):
    if idx not in (3, 4, 5): return
    a = ease(t / 0.3) if idx == 3 else 1.0
    chip(fr, f"TEIL {PART + 1} KOMMT MORGEN · JETZT FOLGEN", 690, 1505, 25 * (1 + 0.04 * math.sin((t + idx) * 7)), GOLD, INK, a)

SC = [d_hook, r_shops, r_safe, r_sms, r_boom, r_cops, r_people, d_end]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "TEIL 2: RICHTIG ABRAUBEN"
S13.TOP0 = "COUNTDOWN · TEIL 2"; S13.TOPLAST = "TEIL 3 MORGEN"; S13.EXTRA = nudge
S13.comment13 = S17.end_overlay

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.7, 0.85, 0.9, 0.45]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 4, 0.6, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p18_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
