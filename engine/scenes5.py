import json
import scenes4
import scenes2 as S2
from scenes4 import *

def rays(d, cx, cy, t, col1, col2, n=14, r=900):
    for i in range(n):
        a = t * 0.8 + i * 2 * math.pi / n
        d.polygon([(cx, cy), (cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + math.pi / n) * r, cy + math.sin(a + math.pi / n) * r)], fill=col1 if i % 2 else col2)

def k_intro(im, d, t, dur):
    rays(d, 710, 850, t, (95, 55, 170), (120, 70, 190))
    s = back(t / 0.45) * (1 + 0.05 * math.sin(t * 9))
    sx = math.sin(t * 50) * 8 if t < 0.5 else 0
    if s > 0.05:
        burst(d, 710 + sx, 850, 300 * s, YEL, 16)
        label(d, "6", 710 + sx, 830, 330 * s, PINK, 14)
    pill(d, "KRASSE FAKTEN", 710, 1160, 46, CYAN, INK, back((t - 0.5) / 0.4))
    sparkle_field(d, t, (430, 520, 1000, 1300), 16, 11)
    return (710, 850)

def fact_badge(d, n, t):
    s = back(t / 0.35)
    if s > 0.05:
        r = 46 * s
        d.ellipse([440 - r, 560 - r, 440 + r, 560 + r], fill=YEL, outline=INK, width=5)
        label(d, f"#{n}", 440, 560, 40 * s, INK, 0)

def wrap(fn, n):
    def f(im, d, t, dur):
        tgt = fn(im, d, t, dur)
        fact_badge(d, n, t)
        return tgt
    return f

def k_billion(im, d, t, dur):
    for i in range(6):
        h = (120 + i * 70) * ease((t - 0.15 * i) / 0.6)
        if h > 3: V.bill_stack(d, 450 + i * 90, 1200, 70, h)
    v = countup(t, 0.2, 1.8, 1.5)
    label(d, f"{v:.1f}".replace(".", ",") + " MRD. $", 710, 660, 96, (255, 255, 255), 9)
    stamp(im, "GESCHÄTZT", 760, 800, t, 3.85, -10, 0.8)
    return (710, 900)

def k_views(im, d, t, dur):
    v = int(countup(t, 0.2, min(2.5, dur * 0.6), 475))
    V.phone(d, 700, 880, 1.0 * back(t / 0.4), f"{v} Mio.", "Aufrufe in 24 h")
    for i in range(7):
        y = 1250 - ((t * 300 + i * 140) % 700); x = 470 + (i * 83) % 520
        d.ellipse([x - 16, y - 16, x, y], fill=PINK); d.ellipse([x - 2, y - 16, x + 14, y], fill=PINK)
        d.polygon([(x - 16, y - 8), (x + 14, y - 8), (x - 1, y + 14)], fill=PINK)
    return (700, 880)

def k_last(im, d, t, dur):
    return p_8bn(im, d, t, dur)

cfg = json.load(open(os.path.join(HERE, "k_timing.json"))) if os.path.exists(os.path.join(HERE, "k_timing.json")) else None
D = cfg["durs"] if cfg else [4.2, 3.6, 5.2, 4.0, 3.6, 5.0, 5.4]
FOL = cfg["follow"] if cfg else 3.8
R5 = {"17_Krasse_Fakten": [
    (D[0], "night", k_intro, [(0, "KRASSE FAKTEN", PINK)], "wave"),
    (D[1], "purple", wrap(d_intro, 1), [(0, "212 GB", CYAN)], "point"),
    (D[2], "mint", wrap(k_views, 2), [(0, "475 MIO. VIEWS", PINK)], "point"),
    (D[3], "gold", wrap(r_3days, 3), [(0, "1 MRD. IN 3 TAGEN", GRN)], "cheer"),
    (D[4], "sky", wrap(r_sales, 4), [(0, "230 MILLIONEN", CYAN)], "point"),
    (D[5], "sunset", wrap(k_billion, 5), [(0, "1,5 MRD. $", PINK)], "point"),
    (D[6], "purple", wrap(k_last, 6), [(0, "8 MILLIARDEN", CYAN), (FOL, "FOLGT FÜR MEHR", PINK)], "point"),
]}
S2.R.update(R5)

if __name__ == "__main__":
    cmd = sys.argv[1]; vid = "17_Krasse_Fakten"
    if cmd == "preview":
        ims = [S2.frame(vid, i, S2.R[vid][i][0] * (0.95 if i == 6 else 0.7)).resize((270, 480)) for i in range(7)]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(HERE, "p5.png"))
    elif cmd == "render":
        S2.render(vid, int(sys.argv[2]))
