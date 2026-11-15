"""Reel 25: Ganze Welt startet GTA 6 - intensive Version. Full-frame space, big planet, orbits, shockwaves."""
import sys, os, math, random, json, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes10
import scenes7 as S7
from scenes10 import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops

VID = "25_Ganze_Welt_v2"
LINES = [
    "Was passiert, wenn die ganze Welt gleichzeitig G T A sechs startet?",
    "Am neunzehnten November ist es so weit.",
    "G T A fünf verkaufte sich am ersten Tag über elf Millionen Mal.",
    "Laden so viele G T A sechs, sind das über zwei Milliarden Gigabyte!",
    "Mit hundert Megabit dauert der Download fast fünf Stunden.",
    "Darum lieber jetzt schon vorladen!",
    "G T A fünf machte am ersten Tag über achthundert Millionen Dollar.",
    "G T A sechs könnte diesen Rekord brechen.",
    "Welches Land zockt zuerst? Schreib dein Land in die Kommentare!",
]
DURS = [3.8, 2.6, 3.6, 3.8, 3.4, 2.6, 3.6, 2.6, 4.0]
S7.SCRIPTS7[VID] = LINES
S7.COMMENT[VID] = ("DEIN LAND?", "Österreich!")
S7.COVER[VID] = ("GANZE WELT ZOCKT", "WAS PASSIERT AM 19.11.?")

# ---------- space ----------
@functools.lru_cache(maxsize=1)
def _space_base():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=(int(6 + 22 * k), int(8 + 8 * k), int(28 + 40 * k)))
    neb = Image.new("RGB", (W, H), (0, 0, 0)); nd = ImageDraw.Draw(neb)
    for (x, y, r, c) in [(860, 480, 380, (120, 30, 140)), (220, 1050, 420, (20, 90, 150)), (700, 1560, 520, (70, 30, 150)), (150, 300, 260, (30, 60, 130))]:
        nd.ellipse([x - r, y - r, x + r, y + r], fill=c)
    neb = neb.filter(ImageFilter.GaussianBlur(190))
    return ImageChops.add(im, neb)

def space(im, t, seed=1):
    im.paste(_space_base(), (0, 0))
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for i in range(170):
        x = (rnd.randrange(W) - t * rnd.uniform(3, 14)) % W; y = rnd.randrange(1650)
        a = 0.5 + 0.5 * math.sin(t * rnd.uniform(2, 5) + i)
        c = int(120 + 135 * a); r = rnd.choice([1, 2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, min(255, c + 25)))
    k = int(t / 1.6); ph = (t % 1.6) / 0.45
    if ph < 1:
        r2 = random.Random(seed * 31 + k)
        x0, y0 = r2.randrange(350, 1050), r2.randrange(150, 650)
        x, y = x0 - ph * 420, y0 + ph * 230
        d.line([(x, y), (x + 130, y - 71)], fill=(255, 255, 255), width=4)
        d.line([(x + 130, y - 71), (x + 230, y - 126)], fill=(140, 150, 200), width=2)
    # hologram platform for the character
    bloom(im, 205, 1530, 110, (60, 200, 255), 0.45)
    d = ImageDraw.Draw(im)
    d.ellipse([205 - 200, 1528 - 44, 205 + 200, 1528 + 44], fill=(16, 26, 66), outline=NEON, width=5)
    pr = 150 + 30 * math.sin(t * 3)
    d.ellipse([205 - pr, 1528 - pr * 0.22, 205 + pr, 1528 + pr * 0.22], outline=(90, 190, 255), width=3)
    return d

def shock(im, cx, cy, p, col, rmax=420):
    if p <= 0 or p >= 1: return
    r = int(rmax * ease(p)); sz = 2 * rmax + 60
    lay = Image.new("L", (sz, sz), 0)
    ImageDraw.Draw(lay).ellipse([sz / 2 - r, sz / 2 - r, sz / 2 + r, sz / 2 + r], outline=int(255 * (1 - p)), width=14)
    im.paste(col, (int(cx - sz / 2), int(cy - sz / 2)), lay.filter(ImageFilter.GaussianBlur(4)))

def orbit(fn, cx, cy, rx, ry, n, t, speed, front, tilt=0.0):
    for i in range(n):
        a = t * speed + i * 2 * math.pi / n; z = math.sin(a)
        if (z > 0) == front:
            x = cx + math.cos(a) * rx; y = cy + z * ry + math.cos(a) * tilt
            fn(x, y, 0.7 + 0.3 * z, i)

def arc_net(im, pts, t, col):
    lay = Image.new("L", (W, H), 0); ld = ImageDraw.Draw(lay)
    for k in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[k], pts[k + 1]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - 90
        prev = None
        for j in range(17):
            u = j / 16
            x = (1 - u) ** 2 * x0 + 2 * u * (1 - u) * mx + u * u * x1; y = (1 - u) ** 2 * y0 + 2 * u * (1 - u) * my + u * u * y1
            if prev: ld.line([prev, (x, y)], fill=230, width=5)
            prev = (x, y)
        u = (t * 0.9 + k * 0.23) % 1
        x = (1 - u) ** 2 * x0 + 2 * u * (1 - u) * mx + u * u * x1; y = (1 - u) ** 2 * y0 + 2 * u * (1 - u) * my + u * u * y1
        ld.ellipse([x - 12, y - 12, x + 12, y + 12], fill=255)
    box = (380, 560, 1040, 1320)
    crop = lay.crop(box)
    im.paste(col, box[:2], crop.filter(ImageFilter.GaussianBlur(7)))
    im.paste((255, 255, 255), box[:2], crop.point(lambda v: v // 2))

def visible_pins(cx, cy, R, rot, n=12):
    out = []
    for (la, lo) in PINS[:n]:
        x, y, z = latlon_xy(cx, cy, R, la, lo, rot)
        if z > 0.25: out.append((x, y))
    return out

def flash(im, k):
    if k > 0: im.paste(Image.blend(im, Image.new("RGB", im.size, (255, 255, 255)), min(1, k)), (0, 0))

# ---------- scenes ----------
def e_hook(im, d, t, dur):
    d = space(im, t, 1)
    R = max(70, int(330 * back(t / 0.55)))
    rot = t * 0.07
    for k in range(3): shock(im, 700, 900, ((t - 0.25 - k * 0.9) / 1.1), NEON2 if k % 2 == 0 else NEON, 470)
    d = planet(im, 700, 900, R, rot, lights_on=min(1, t / 1.2))
    d = pins(d, im, 700, 900, R, rot, t, 12, 0.35)
    flash(im, 0.7 * (1 - t / 0.15))
    return (700, 880)

def e_date(im, d, t, dur):
    d = space(im, t, 2)
    cx, cy, R = 850, 1120, 170
    d.ellipse([cx - 290, cy - 90, cx + 290, cy + 90], outline=(120, 200, 255), width=3)
    a = t * 1.6
    mx, my, mz = cx + math.cos(a) * 290, cy + math.sin(a) * 90, math.sin(a)
    if mz <= 0: d.ellipse([mx - 22, my - 22, mx + 22, my + 22], fill=(200, 205, 220), outline=INK, width=2)
    d = planet(im, cx, cy, R, t * 0.06 + 0.3, lights_on=0.7)
    if mz > 0: d.ellipse([mx - 26, my - 26, mx + 26, my + 26], fill=(225, 228, 240), outline=INK, width=2)
    shock(im, 640, 800, (t - 0.1) / 0.7, NEON, 330)
    d = ImageDraw.Draw(im)
    s = back(t / 0.4)
    if s > 0.05: M.calendar(d, 640, 790, 0.72 * s, "NOVEMBER", "19", (230, 60, 60))
    pill(d, "RELEASE", 640, 1010, 40, NEON2, (255, 255, 255), back((t - 0.5) / 0.35) * (1 + 0.05 * math.sin(t * 9)))
    return (640, 790)

def e_sales(im, d, t, dur):
    d = space(im, t, 3)
    cx, cy, R = 710, 980, 200
    cols = [(40, 120, 200), (230, 70, 110), (60, 170, 110)]
    n = max(1, int(16 * ease(t / 1.6)))
    def case(x, y, s, i):
        if i < n: V.game_case(ImageDraw.Draw(im), x - 42 * s, y + 62 * s, 84, 124, cols[i % 3], "V", s)
    orbit(case, cx, cy, 345, 120, 16, t, 1.3, False, 40)
    planet(im, cx, cy, R, t * 0.06 + 0.9, lights_on=0.85)
    orbit(case, cx, cy, 345, 120, 16, t, 1.3, True, 40)
    v = countup(t, 0.1, 2.0, 11.2)
    neon_text(im, f"{v:.1f}".replace(".", ",") + " MIO.", 710, 640, 104, NEON)
    d = ImageDraw.Draw(im)
    pill(d, "GTA 5 · TAG 1", 710, 745, 32, YEL, INK, back((t - 0.3) / 0.4))
    return (710, 640)

def e_data(im, d, t, dur):
    d = space(im, t, 4)
    cx, cy, R = 710, 1010, 235
    rot = t * 0.06 + 0.5
    planet(im, cx, cy, R, rot, lights_on=0.9)
    vp = visible_pins(cx, cy, R, rot)
    if len(vp) > 1: arc_net(im, vp, t, NEON)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.42
        sx, sy = cx + math.cos(a) * 370, cy + math.sin(a) * 370 + math.sin(t * 2 + k) * 6
        if t > 0.1 * k:
            beam(im, sx, sy, cx + math.cos(a) * (R + 4), cy + math.sin(a) * (R + 4), t, NEON2 if k % 2 else NEON, k)
            satellite(ImageDraw.Draw(im), sx, sy, 0.75, a)
    v = countup(t, 0.2, 2.2, 2.4)
    neon_text(im, f"{v:.1f}".replace(".", ",") + " MRD. GB", 710, 610, 84, NEON2)
    d = ImageDraw.Draw(im)
    pill(d, "RECHENBEISPIEL: 11,2 MIO. × 212 GB", 710, 1300, 24, (255, 255, 255), INK, back((t - 0.9) / 0.4))
    return (710, 1000)

def gauge(im, cx, cy, r, p):
    d = ImageDraw.Draw(im)
    d.arc([cx - r, cy - r, cx + r, cy + r], 150, 390, fill=(60, 66, 110), width=34)
    if p > 0.01:
        lay = Image.new("L", (2 * r + 120, 2 * r + 120), 0)
        ImageDraw.Draw(lay).arc([60, 60, 2 * r + 60, 2 * r + 60], 150, 150 + 240 * p, fill=255, width=34)
        im.paste(NEON, (int(cx - r - 60), int(cy - r - 60)), lay.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(im)
        d.arc([cx - r, cy - r, cx + r, cy + r], 150, 150 + 240 * p, fill=NEON, width=34)
    for k in range(11):
        a = math.radians(150 + 24 * k)
        d.line([(cx + math.cos(a) * (r - 60), cy + math.sin(a) * (r - 60)), (cx + math.cos(a) * (r - 34), cy + math.sin(a) * (r - 34))], fill=(255, 255, 255), width=5)
    a = math.radians(150 + 240 * p)
    d.line([(cx, cy), (cx + math.cos(a) * (r - 50), cy + math.sin(a) * (r - 50))], fill=NEON2, width=14)
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 255, 255), outline=INK, width=4)
    return d

def e_time(im, d, t, dur):
    d = space(im, t, 5)
    planet(im, 930, 1260, 150, t * 0.06 + 1.3, lights_on=0.8)
    p = back(min(1, t / 0.9)) if t < 0.9 else 1 + 0.015 * math.sin(t * 30)
    d = gauge(im, 710, 800, 210, max(0, min(1.04, p)) * 0.96)
    label(d, f"{int(100 * min(1, ease(t / 0.9)))}", 710, 890, 90, (255, 255, 255), 8)
    label(d, "MBIT/S", 710, 965, 30, NEON, 5)
    q = ease((t - 0.5) / 2.4)
    dl_bar(d, 470, 1110, 950, q, f"{int(q * 212)} / 212 GB", CYAN)
    hrs = 4.71 * q; hh = int(hrs); mm = int((hrs - hh) * 60)
    neon_text(im, f"{hh} STD. {mm:02d} MIN.", 710, 1210, 56, NEON2)
    return (710, 800)

def e_preload(im, d, t, dur):
    d = space(im, t, 6)
    px, py = 880, 690
    planet(im, px, py, 125, t * 0.07 + 2.0, lights_on=1.0)
    d = ImageDraw.Draw(im)
    for j in range(12):
        u = (t * 1.3 + j / 12) % 1
        x = lerp(px - 60, 700, u) + math.sin(u * math.pi) * -70; y = lerp(py + 90, 960, u)
        r = 6 + 6 * u
        d.ellipse([x - r, y - r, x + r, y + r], fill=(140, 255, 190))
    bloom(im, 690, 1010, 190, (80, 255, 160), 0.55)
    d = ImageDraw.Draw(im)
    console(d, 690, 1030, back(t / 0.35) * 1.45)
    shock(im, 690, 1010, ((t - 0.5) % 1.2) / 1.0, (80, 255, 160), 330)
    d = ImageDraw.Draw(im)
    check_icon(d, 860, 900, back((t - 0.5) / 0.3) * 2.0)
    pill(d, "JETZT VORLADEN", 700, 1230, 44, GRN, (255, 255, 255), back((t - 0.3) / 0.35) * (1 + 0.06 * math.sin(t * 10)))
    return (690, 1010)

def e_money(im, d, t, dur):
    d = space(im, t, 7)
    cx, cy, R = 710, 990, 200
    def bill_(x, y, s, i): V.bill(ImageDraw.Draw(im), x, y, math.sin(t * 3 + i) * 0.6, 1.1 * s)
    orbit(bill_, cx, cy, 340, 115, 18, t, 1.6, False, -50)
    orbit(bill_, cx, cy, 300, 150, 12, t, -1.1, False, 60)
    planet(im, cx, cy, R, t * 0.06 + 2.6, lights_on=0.9)
    orbit(bill_, cx, cy, 340, 115, 18, t, 1.6, True, -50)
    orbit(bill_, cx, cy, 300, 150, 12, t, -1.1, True, 60)
    v = int(countup(t, 0.15, 2.0, 815))
    neon_text(im, f"{v} MIO. $", 710, 640, 112, (120, 255, 160))
    d = ImageDraw.Draw(im)
    pill(d, "GTA 5 · TAG 1", 710, 750, 32, YEL, INK, back((t - 0.3) / 0.4))
    return (710, 640)

def e_record(im, d, t, dur):
    d = space(im, t, 8)
    planet(im, 930, 1290, 140, t * 0.06 + 3.1, lights_on=0.9)
    d = ImageDraw.Draw(im)
    base = 1240
    h5 = 300 * ease(t / 0.5)
    if h5 > 3: M.box(d, 500, base - h5, 150, h5, 46, (90, 150, 220))
    label(d, "GTA 5", 575, base + 45, 36, (255, 255, 255), 6)
    if h5 > 280: label(d, "815", 590, base - h5 - 50, 44, (255, 255, 255), 6)
    g = ease((t - 0.4) / 1.6)
    h6 = 470 * g + (8 * math.sin(t * 40) if g < 1 else 0)
    if h6 > 3:
        bloom(im, 880, base - h6, 120, NEON2, 0.5); d = ImageDraw.Draw(im)
        M.box(d, 790, base - h6, 150, h6, 46, NEON2)
        rocket(d, 880, base - h6 - 150, 0.55, t)
    label(d, "GTA 6", 865, base + 45, 36, (255, 255, 255), 6)
    V.qmark(d, 865, base - max(120, h6 / 2) + math.sin(t * 5) * 8, back((t - 1.2) / 0.3) * 1.1)
    return (880, max(700, base - h6 - 120))

def e_cta(im, d, t, dur):
    d = space(im, t, 9)
    rot = t * 0.07 + 1.6
    shock(im, 710, 740, (t % 1.3) / 1.2, NEON2, 300)
    d = planet(im, 710, 740, 180, rot, lights_on=1.0)
    d = pins(d, im, 710, 740, 180, rot, t, 12, 0.0)
    return (710, 740)

_old = S7.defs
def defs(vid, durs):
    if vid != VID: return _old(vid, durs)
    sc = [e_hook, e_date, e_sales, e_data, e_time, e_preload, e_money, e_record, e_cta]
    w = [("GANZE WELT ZOCKT?!", PINK), ("19. NOVEMBER", CYAN), ("11 MIO. AM 1. TAG", GRN), ("2 MRD. GIGABYTE", PINK), ("FAST 5 STUNDEN", CYAN),
         ("JETZT VORLADEN", GRN), ("815 MIO. $", GRN), ("NEUER REKORD?", PINK), ("DEIN LAND?", PINK)]
    poses = ["wave", "point", "point", "point", "point", "cheer", "point", "point", "point"]
    return [(durs[i], "night", sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(9)]
S7.defs = defs

def set_timing():
    segs = []; t = 0
    for dd in DURS: segs.append((t + 0.1, t + dd - 0.3)); t += dd
    T = S7.load_timing(); T[VID] = {"durs": DURS, "segs": segs, "total": 30.0}
    json.dump(T, open(S7.TF, "w"), indent=1)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        if VID not in S7.load_timing(): set_timing()
        T = S7.setup(VID); words = S7.word_times(VID, T); R = S2.R[VID]
        ims = [S7.frame(VID, 0, 0.0, T, words).resize((270, 480))] + [S7.frame(VID, i, R[i][0] * (0.9 if i == 8 else 0.7), T, words).resize((270, 480)) for i in range(9)]
        shp = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(ims[:10]): shp.paste(im, ((i % 5) * 270, (i // 5) * 480))
        shp.save(os.path.join(HERE, "p11.png"))
    elif cmd == "render":
        S7.render(VID, int(sys.argv[2]))
