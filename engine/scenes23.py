"""Reel 38 – Glow-Sketch-Stil: Neon-Linien zeichnen sich selbst. Thema: Rekorde von GTA 6."""
import sys, os, math, random, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
from scenes13 import FX, FS, ease, back, W, H
from reel2 import draw_character
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

VID = "38_Rekorde_Glow"
S7.SCRIPTS7[VID] = [
    "G T A sechs hat schon Rekorde gebrochen, bevor es überhaupt draußen ist! Folg mir für mehr!",
    "Eins: Der erste Trailer hatte über neunzig Millionen Aufrufe in vierundzwanzig Stunden.",
    "Zwei: Der zweite Trailer sogar vierhundertfünfundsiebzig Millionen, über alle Plattformen.",
    "Drei: Das Spiel wurde zweimal verschoben. Jetzt kommt es am neunzehnten November.",
    "Vier: Der Vorgänger G T A fünf hat sich über zweihundertfünfundzwanzig Millionen Mal verkauft.",
    "Fünf: Und die Vorbestellungen liegen weit über den Erwartungen.",
    "Welcher Rekord ist am krassesten? Schreib die Zahl! Und merk dir:",
]
S7.DISPLAY.update({"neunzig": "90", "vierundzwanzig": "24", "vierhundertfünfundsiebzig": "475", "neunzehnten": "19.", "zweihundertfünfundzwanzig": "225"})
S7.COMMENT[VID] = ("WELCHER REKORD?", "475 Millionen?!")
S7.COVER[VID] = ("GTA 6", "REKORDE")
CYAN = (60, 230, 255); PINK = (255, 70, 200); LIME = (190, 255, 70); GOLD = (255, 200, 60); WHITE = (235, 245, 255); RED = (255, 70, 90)
HEAD = [("SCHON VOR RELEASE", "REKORDE!"), ("TRAILER 1", "90 MIO IN 24H"), ("TRAILER 2", "475 MIO IN 24H"), ("2× VERSCHOBEN", "JETZT: 19.11."),
        ("GTA 5", "225 MIO VERKAUFT"), ("VORBESTELLUNGEN", "ÜBER ERWARTUNG"), ("WELCHER REKORD", "IST AM KRASSESTEN?")]
COLS = [PINK, CYAN, PINK, GOLD, LIME, CYAN, LIME]
SRC = [None, "Quelle: Medienberichte (YouTube)", "Quelle: Rockstar Games", "Quelle: Rockstar Games", "Quelle: Take-Two", "Laut Berichten", None]

# ---------------- sketch primitives ----------------
def seg_pts(pts, n=6):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for k in range(n): out.append((x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n))
    out.append(pts[-1]); return out
def rect(x0, y0, x1, y1, r=0): return seg_pts([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], 10)
def circ(cx, cy, r, a0=0, a1=360, n=48): return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
def line(x0, y0, x1, y1): return seg_pts([(x0, y0), (x1, y1)], 8)

def jit(pts, gt, seed, amp=2.2):
    fr = int(gt * 8)
    rr = random.Random(seed * 1000 + fr)
    return [(x + rr.uniform(-amp, amp), y + rr.uniform(-amp, amp)) for x, y in pts]

def stroke(d, pts, p, col, gt, seed=0, w=5, double=True):
    if p <= 0 or len(pts) < 2: return
    L = [0.0]
    for a, b in zip(pts, pts[1:]): L.append(L[-1] + math.dist(a, b))
    tgt = L[-1] * min(1, p); out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= tgt: out.append(pts[i])
        else:
            a, b = pts[i - 1], pts[i]; f = (tgt - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)); break
    if len(out) < 2: return
    d.line(jit(out, gt, seed), fill=col, width=w, joint="curve")
    if double: d.line(jit(out, gt, seed + 77, 3.0), fill=tuple(int(c * 0.55) for c in col), width=max(2, w - 2), joint="curve")

def ntext(d, xy, txt, size, col, p=1.0, hollow=False, anchor="mm"):
    if p <= 0.02: return
    f = FX(size)
    c = tuple(int(v * min(1, p)) for v in col)
    if hollow: d.text(xy, txt, font=f, fill=(0, 0, 0), stroke_width=max(2, size // 22), stroke_fill=c, anchor=anchor)
    else: d.text(xy, txt, font=f, fill=c, anchor=anchor)

# ---------------- background ----------------
def _bg():
    im = Image.new("RGB", (W, H), (6, 8, 18)); d = ImageDraw.Draw(im)
    for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(14, 18, 34), width=1)
    for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(14, 18, 34), width=1)
    v = Image.new("L", (W // 8, H // 8), 0); ImageDraw.Draw(v).ellipse([-30, -10, W // 8 + 30, H // 8 + 10], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(20)).resize((W, H))
    return Image.composite(im, Image.new("RGB", (W, H), (2, 2, 6)), v)
BG = _bg()

def glow(base, light):
    small = light.resize((W // 4, H // 4), Image.BILINEAR).filter(ImageFilter.GaussianBlur(7)).resize((W, H), Image.BILINEAR)
    small = small.point(lambda v: min(255, int(v * 1.7)))
    out = ImageChops.screen(base, small)
    return ImageChops.screen(out, light)

# ---------------- scenes (draw on light layer) ----------------
def s_hook(d, t, dur, gt):
    p = ease(t / 0.9)
    # trophy
    cx, cy = 720, 860; c = GOLD
    stroke(d, seg_pts([(cx - 120, cy - 150), (cx + 120, cy - 150), (cx + 100, cy - 20), (cx + 40, cy + 40), (cx - 40, cy + 40), (cx - 100, cy - 20), (cx - 120, cy - 150)], 8), p, c, gt, 1, 7)
    stroke(d, circ(cx - 130, cy - 90, 50, 90, 270), ease((t - 0.3) / 0.5), c, gt, 2, 6)
    stroke(d, circ(cx + 130, cy - 90, 50, -90, 90), ease((t - 0.3) / 0.5), c, gt, 3, 6)
    stroke(d, line(cx, cy + 40, cx, cy + 110), ease((t - 0.5) / 0.3), c, gt, 4, 7)
    stroke(d, rect(cx - 90, cy + 110, cx + 90, cy + 150), ease((t - 0.6) / 0.4), c, gt, 5, 7)
    ntext(d, (cx, cy - 75), "#1", 90, GOLD, ease((t - 0.7) / 0.3), True)
    for k in range(8):
        a = k * math.pi / 4 + t * 0.6; r0 = 230; r1 = 230 + 40 * (0.5 + 0.5 * math.sin(t * 6 + k))
        stroke(d, line(cx + r0 * math.cos(a), cy - 40 + r0 * math.sin(a), cx + r1 * math.cos(a), cy - 40 + r1 * math.sin(a)), ease((t - 0.8) / 0.3), PINK, gt, 10 + k, 4, False)
    return (cx, cy)

def screen_icon(d, cx, cy, w, h, p, col, gt, seed):
    stroke(d, rect(cx - w, cy - h, cx + w, cy + h), p, col, gt, seed, 6)
    stroke(d, seg_pts([(cx - 25, cy - 35), (cx + 40, cy), (cx - 25, cy + 35), (cx - 25, cy - 35)], 6), ease((p - 0.6) / 0.4), col, gt, seed + 1, 6)

def counter(d, val, p, xy, size, col, suffix=" MIO"):
    v = int(val * ease(p))
    ntext(d, xy, f"{v}{suffix}", size, col, min(1, p * 3), True)

def s_t1(d, t, dur, gt):
    screen_icon(d, 720, 800, 220, 130, ease(t / 0.8), CYAN, gt, 20)
    counter(d, 90, (t - 0.3) / 1.4, (720, 1030), 110, CYAN)
    # clock 24h
    p = ease((t - 0.8) / 0.6)
    stroke(d, circ(930, 610, 58), p, PINK, gt, 21, 5)
    a = -math.pi / 2 + t * 6
    stroke(d, line(930, 610, 930 + 40 * math.cos(a), 610 + 40 * math.sin(a)), p, PINK, gt, 22, 5, False)
    ntext(d, (930, 700), "24H", 34, PINK, p)
    return (720, 800)

def s_t2(d, t, dur, gt):
    for i, (dx, dy) in enumerate([(-170, -60), (170, -60), (-170, 140), (170, 140)]):
        screen_icon(d, 720 + dx, 760 + dy, 120, 72, ease((t - i * 0.15) / 0.7), [PINK, CYAN, LIME, GOLD][i], gt, 30 + i)
    counter(d, 475, (t - 0.4) / 1.5, (720, 1080), 120, PINK)
    ntext(d, (720, 1180), "x5 MEHR ALS TRAILER 1", 34, WHITE, ease((t - 1.6) / 0.3))
    return (720, 800)

def s_delay(d, t, dur, gt):
    items = [("2025", 620), ("26.05.2026", 790), ("19.11.2026", 960)]
    for i, (txt, y) in enumerate(items):
        p = ease((t - i * 0.35) / 0.5)
        stroke(d, rect(500, y - 60, 940, y + 60), p, GOLD if i < 2 else LIME, gt, 40 + i, 5)
        ntext(d, (720, y), txt, 64, WHITE if i < 2 else LIME, p)
        if i < 2:
            q = ease((t - 0.5 - i * 0.35) / 0.3)
            stroke(d, line(510, y - 50, 930, y + 50), q, RED, gt, 50 + i, 8, False)
            stroke(d, line(510, y + 50, 930, y - 50), ease((q - 0.5) * 2), RED, gt, 52 + i, 8, False)
        else:
            q = ease((t - 1.4) / 0.6)
            stroke(d, circ(720, y, 280, -200, 160), q, LIME, gt, 55, 6)
    return (720, 960 if t > 1.3 else 700)

def s_gta5(d, t, dur, gt):
    for i in range(6):
        p = ease((t - i * 0.12) / 0.4)
        x = 560 + (i % 3) * 160; y = 900 - (i // 3) * 210
        stroke(d, rect(x - 60, y - 90, x + 60, y + 90), p, LIME, gt, 60 + i, 5)
        ntext(d, (x, y), "V", 70, LIME, p, True)
    counter(d, 225, (t - 0.5) / 1.4, (720, 1110), 120, LIME)
    return (720, 800)

def s_pre(d, t, dur, gt):
    stroke(d, line(500, 1060, 960, 1060), ease(t / 0.4), WHITE, gt, 70, 5)
    stroke(d, line(500, 1060, 500, 600), ease(t / 0.4), WHITE, gt, 71, 5)
    ey = 820
    stroke(d, seg_pts([(500, ey), (960, ey)], 30), ease((t - 0.3) / 0.5), GOLD, gt, 72, 4, False)
    ntext(d, (930, ey - 30), "ERWARTUNG", 26, GOLD, ease((t - 0.5) / 0.3), anchor="rm")
    for i, h in enumerate([120, 170, 230, 330, 420]):
        p = ease((t - 0.5 - i * 0.12) / 0.4); hh = h * p
        x = 540 + i * 85
        stroke(d, rect(x, 1060 - hh, x + 55, 1060), 1 if p > 0 else 0, CYAN if i < 4 else LIME, gt, 73 + i, 5)
    pa = ease((t - 1.3) / 0.5)
    stroke(d, seg_pts([(560, 1000), (700, 860), (780, 900), (930, 660)], 10), pa, LIME, gt, 80, 7)
    stroke(d, seg_pts([(890, 660), (930, 660), (930, 700)], 6), ease((pa - 0.8) * 5), LIME, gt, 81, 7, False)
    return (900, 700)

def s_end(d, t, dur, gt):
    act = int(t * 2.4) % 5
    for i in range(5):
        p = ease((t - i * 0.08) / 0.4); x = 500 + i * 110
        col = LIME if i == act else WHITE
        stroke(d, rect(x - 42, 660, x + 42, 744), p, col, gt, 90 + i, 5)
        ntext(d, (x, 702), str(i + 1), 52, col, p)
    if t > 0.8:
        ot = t - 0.8; p = ease(ot / 0.5)
        stroke(d, rect(470, 820, 970, 990), p, CYAN, gt, 99, 5)
        ans = S7.COMMENT[VID][1]; n = int(len(ans) * ease((ot - 0.4) / 1.0))
        ntext(d, (500, 870), "du:", 28, (150, 160, 190), p, anchor="lm")
        ntext(d, (500, 930), ans[:n], 44, WHITE, p, anchor="lm")
    return (720, 700)

SC = [s_hook, s_t1, s_t2, s_delay, s_gta5, s_pre, s_end]

def follow_sketch(d, ot, gt):
    done = ot > 1.9
    p = ease(ot / 0.5)
    col = LIME if not done else (120, 130, 160)
    s = 1 + (0.05 * math.sin(ot * 10) if not done else 0)
    w, h = 210 * s, 56 * s; cx, cy = 720, 1160
    stroke(d, rect(cx - w, cy - h, cx + w, cy + h), p, col, gt, 200, 7)
    ntext(d, (cx, cy), "+ FOLGEN" if not done else "GEFOLGT", 54, col, p)
    if done: stroke(d, seg_pts([(cx + 140, cy), (cx + 165, cy + 25), (cx + 205, cy - 30)], 6), ease((ot - 1.9) / 0.3), LIME, gt, 201, 8, False)
    pf = ease((ot - 0.7) / 0.6)
    if pf > 0:
        fx, fy = cx + 280 - 120 * pf, cy + 160 - 140 * pf
        stroke(d, circ(fx, fy, 22), 1, WHITE, gt, 202, 5)
        if 1.6 < ot < 1.9: stroke(d, circ(fx, fy, 46), 1, WHITE, gt, 203, 3, False)

def mascot_glow(light, t, gt, target, col=CYAN):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_character(layer, t, gt, "point", target)
    a = layer.split()[3]
    gray = layer.convert("L")
    e1 = a.filter(ImageFilter.FIND_EDGES).point(lambda v: 255 if v > 60 else 0)
    e2 = gray.filter(ImageFilter.FIND_EDGES).point(lambda v: 200 if v > 40 else 0)
    e = ImageChops.lighter(e1, e2).filter(ImageFilter.MaxFilter(3))
    light.paste(col, (0, 0), e)
    light.paste((10, 30, 40), (0, 0), a.point(lambda v: 60 if v > 128 else 0))

def captions(d, words, gt):
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
    f = FX(64); txts = [words[i][2] for i in g]; ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 24 * (len(ws) - 1)
    if tot > 660: f = FX(int(64 * 660 / tot)); ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 24 * (len(ws) - 1)
    x = 690 - tot / 2
    for i, tx, w in zip(g, txts, ws):
        on = i == act
        d.text((x + w / 2, 1395), tx, font=f, fill=LIME if on else WHITE, anchor="mm")
        if on: d.line([(x, 1440), (x + w, 1440)], fill=LIME, width=5)
        x += w + 24

def frame23(vid, idx, t, T, words, cover=False, no_sticker=False):
    R = S2.R[vid]; dur = R[idx][0]; n = len(R)
    gt = sum(s[0] for s in R[:idx]) + t
    light = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(light)
    col = COLS[idx]
    tt = t + (0.6 if idx == 0 else 0) + (2.0 if cover else 0)
    target = SC[idx](d, tt, dur, gt)
    if idx == 0 and not cover and t > dur * 0.5:
        follow_sketch(d, t - dur * 0.5, gt); target = (720, 1160)
    # headline
    l1, l2 = HEAD[idx]
    ntext(d, (64, 300), l1, 70 if len(l1) < 16 else 60, WHITE, ease(tt / 0.3), anchor="lm")
    f2 = S13.fit(FX, l2, 112, 950)
    ntext(d, (64, 420), l2, f2.size, col, ease((tt - 0.15) / 0.3), True, anchor="lm")
    w2 = f2.getlength(l2)
    stroke(d, seg_pts([(64, 492), (64 + w2 * 0.5, 500), (64 + w2, 488)], 12), ease((tt - 0.35) / 0.5), col, gt, 300 + idx, 6, False)
    # top
    d.text((64, 173), "ZOCKWISSEN", font=FS(30), fill=LIME, anchor="lm")
    d.text((1016, 173), ("GLOW FACTS" if idx == 0 else (f"REKORD {idx}/5" if idx < n - 1 else "DEINE MEINUNG")), font=FS(30), fill=WHITE, anchor="rm")
    if not cover:
        sw = (W - 120 - (n - 1) * 10) / n
        for i in range(n):
            x0 = 60 + i * (sw + 10)
            d.rectangle([x0, 120, x0 + sw, 126], fill=(40, 50, 70))
            f_ = 1 if i < idx else (t / dur if i == idx else 0)
            if f_ > 0.02: d.rectangle([x0, 120, x0 + sw * f_, 126], fill=WHITE)
        if SRC[idx]:
            sa = ease((t - 0.5) / 0.3)
            if sa > 0.02:
                fs = FS(26); w_ = d.textlength(SRC[idx], font=fs)
                stroke(d, rect(720 - w_ / 2 - 26, 1262, 720 + w_ / 2 + 26, 1306), sa, (90, 100, 130), gt, 400, 3, False)
                d.text((720, 1284), SRC[idx], font=fs, fill=tuple(int(v * sa) for v in (200, 210, 230)), anchor="mm")
        captions(d, words, gt)
    else:
        ntext(d, (690, 1400), "VOR DEM RELEASE!", 64, LIME, 1)
    mascot_glow(light, t if not cover else 2.0, gt, target)
    im = glow(BG, light)
    z = 1.0 + 0.04 * ease(t / dur) + (0.08 * (1 - ease(t / 0.3)) if idx > 0 and not cover else 0)
    zw, zh = int(W * z), int(H * z); big = im.resize((zw, zh), Image.BILINEAR); ox, oy = (zw - W) // 2, (zh - H) // 2
    im = big.crop((ox, oy, ox + W, oy + H))
    if not cover:
        if idx == 0 and t < 0.2: im = Image.blend(im, Image.new("RGB", (W, H), col), 0.5 * (1 - t / 0.2))
        if idx == n - 1 and t > dur - 0.2: im = Image.blend(im, Image.new("RGB", (W, H), COLS[0]), 0.5 * (t - (dur - 0.2)) / 0.2)
        if 0 < idx and t < 0.12: im = Image.blend(im, Image.new("RGB", (W, H), col), 0.25 * (1 - t / 0.12))
    return im

_oldf, _oldd, _oldc = S7.frame, S7.defs, S7.make_cover
def _frame(vid, *a, **k): return frame23(vid, *a, **k) if vid == VID else _oldf(vid, *a, **k)
def _defs(vid, durs):
    if vid != VID: return _oldd(vid, durs)
    return [(durs[i], "night", None, [(0, "", None)], "point") for i in range(len(S7.SCRIPTS7[VID]))]
def _cover(vid, path):
    if vid != VID: return _oldc(vid, path)
    T = S7.setup(vid); frame23(vid, 0, 1.0, T, [], cover=True).save(path)
S7.frame, S7.defs, S7.make_cover = _frame, _defs, _cover

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.75, 0.8, 0.8, 0.8, 0.85, 0.85]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.8, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 1, 0.3, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p23_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
