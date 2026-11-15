"""Reel 24: Was passiert, wenn die ganze Welt GTA 6 startet? Planet + data visuals. Fixed 30 s timing for CapCut TTS."""
import sys, os, math, random, json, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes9
import scenes7 as S7
from scenes9 import *
from PIL import Image, ImageDraw, ImageFilter, ImageChops

VID = "24_Ganze_Welt"
LINES = [
    "Was passiert, wenn die ganze Welt GTA sechs startet?",
    "Am neunzehnten November ist es so weit.",
    "GTA fünf verkaufte sich am ersten Tag elf Millionen Mal.",
    "Laden so viele GTA sechs, sind das über zwei Milliarden Gigabyte!",
    "Mit hundert Megabit dauert der Download fast fünf Stunden.",
    "Darum lieber jetzt vorladen!",
    "GTA fünf machte am ersten Tag über achthundert Millionen Dollar.",
    "GTA sechs könnte das locker schlagen.",
    "Welches Land zockt zuerst? Schreib dein Land in die Kommentare!",
]
DURS = [3.4, 2.8, 3.4, 3.8, 3.4, 2.6, 3.6, 2.8, 4.2]
S7.SCRIPTS7[VID] = LINES
S7.DISPLAY.update({"elf": "11", "hundert": "100", "achthundert": "800", "zwei": "2", "neunzehnten": "19.", "Megabit": "Mbit"})
S7.COMMENT[VID] = ("DEIN LAND?", "Österreich!")
S7.COVER[VID] = ("GANZE WELT ZOCKT", "WAS PASSIERT AM 19.11.?")

# ---------- planet ----------
PR = 300
@functools.lru_cache(maxsize=1)
def _earth_tex():
    """equirectangular-ish texture 2R x R (wraps horizontally)"""
    tw, th = 1200, 600
    tex = Image.new("RGB", (tw, th), (30, 90, 170)); d = ImageDraw.Draw(tex)
    rnd = random.Random(7)
    for _ in range(26):
        cx, cy = rnd.randrange(tw), rnd.randrange(80, th - 80)
        for k in range(rnd.randrange(5, 12)):
            r = rnd.randrange(25, 85)
            x, y = cx + rnd.randrange(-90, 90), cy + rnd.randrange(-60, 60)
            col = rnd.choice([(70, 160, 90), (90, 170, 80), (150, 150, 90), (60, 140, 80)])
            for o in (-tw, 0, tw): d.ellipse([x + o - r, y - r * 0.7, x + o + r, y + r * 0.7], fill=col)
    d.rectangle([0, 0, tw, 40], fill=(235, 240, 250)); d.rectangle([0, th - 40, tw, th], fill=(235, 240, 250))
    lights = Image.new("L", (tw, th), 0); ld = ImageDraw.Draw(lights)
    px = tex.load()
    for _ in range(2600):
        x, y = rnd.randrange(tw), rnd.randrange(60, th - 60)
        if px[x, y][2] < 120: ld.ellipse([x - 2, y - 2, x + 2, y + 2], fill=255)
    return tex, lights

@functools.lru_cache(maxsize=4)
def _sphere_maps(R):
    """per-pixel texture lookup (u,v) and lambert shade for a sphere of radius R"""
    import numpy as np
    yy, xx = np.mgrid[-R:R, -R:R].astype("float32") + 0.5
    rr = np.sqrt(xx ** 2 + yy ** 2) / R
    mask = rr <= 1
    z = np.sqrt(np.clip(1 - rr ** 2, 0, 1))
    lon = np.arctan2(xx / R, z); lat = np.arcsin(np.clip(yy / R, -1, 1))
    lx, ly, lz = -0.55, -0.45, 0.70
    shade = np.clip((xx / R) * lx + (yy / R) * ly + z * lz, 0, 1)
    return lon, lat, mask, shade

def planet(im, cx, cy, R, rot, night=0.0, lights_on=0.0):
    import numpy as np
    tex, lights = _earth_tex()
    lon, lat, mask, shade = _sphere_maps(R)
    T = np.asarray(tex); Lg = np.asarray(lights)
    th, tw = T.shape[:2]
    u = ((lon / (2 * math.pi) + 0.5 + rot) % 1.0) * (tw - 1)
    v = (lat / math.pi + 0.5) * (th - 1)
    ui, vi = u.astype("int32"), v.astype("int32")
    col = T[vi, ui].astype("float32")
    lit = 0.25 + 0.75 * shade[..., None]
    col = col * lit
    dark = (1 - shade[..., None]) ** 2
    glow = Lg[vi, ui].astype("float32")[..., None] / 255 * lights_on * dark
    col = col + glow * np.array([255, 210, 120], dtype="float32")
    col = np.clip(col, 0, 255).astype("uint8")
    sph = Image.fromarray(col)
    m = Image.fromarray((mask * 255).astype("uint8"))
    # atmosphere glow
    g = Image.new("L", (2 * R + 160, 2 * R + 160), 0)
    ImageDraw.Draw(g).ellipse([80 - 10, 80 - 10, 2 * R + 90, 2 * R + 90], fill=200)
    g = g.filter(ImageFilter.GaussianBlur(30))
    im.paste((110, 200, 255), (int(cx - R - 80), int(cy - R - 80)), g)
    im.paste(sph, (int(cx - R), int(cy - R)), m)
    d = ImageDraw.Draw(im)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(170, 225, 255), width=4)
    return d

def latlon_xy(cx, cy, R, lat, lon, rot):
    a = lon + (-rot) * 2 * math.pi
    x = math.sin(a) * math.cos(lat); y = math.sin(lat); z = math.cos(a) * math.cos(lat)
    return cx + x * R, cy + y * R, z

PINS = [(-0.6, 0.3), (-0.75, 1.4), (-0.85, -1.5), (-0.5, -1.0), (0.3, 0.6), (-0.2, 2.2), (0.55, 2.5), (-0.95, 0.1), (-0.65, -0.4), (0.2, -0.9), (-0.4, 1.9), (0.6, -1.2)]
def pins(d, im, cx, cy, R, rot, t, n, t0=0.0):
    for i, (la, lo) in enumerate(PINS[:n]):
        x, y, z = latlon_xy(cx, cy, R, la, lo, rot)
        if z < 0.05: continue
        s = back((t - t0 - 0.12 * i) / 0.3) * (0.5 + 0.5 * z)
        if s < 0.05: continue
        pr = 26 * s * (1 + 0.15 * math.sin(t * 6 + i))
        bloom(im, x, y - 10 * s, 30 * s, (255, 120, 200), 0.7)
        d = ImageDraw.Draw(im)
        d.ellipse([x - pr * 0.6, y - 40 * s - pr * 0.6, x + pr * 0.6, y - 40 * s + pr * 0.6], fill=NEON2, outline=INK, width=3)
        d.polygon([(x - 12 * s, y - 34 * s), (x + 12 * s, y - 34 * s), (x, y)], fill=NEON2, outline=INK)
        # tiny controller
        d.rounded_rectangle([x - 10 * s, y - 46 * s, x + 10 * s, y - 36 * s], 4, fill=(255, 255, 255))
    return ImageDraw.Draw(im)

def stars_bg(d, t, seed=11):
    rnd = random.Random(seed)
    for i in range(70):
        x, y = rnd.randrange(430, 990), rnd.randrange(560, 1240)
        a = 0.5 + 0.5 * math.sin(t * 3 + i)
        c = int(150 + 105 * a); r = rnd.choice([2, 2, 3])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, min(255, c + 20)))

def space_card(im, b=(430, 560, 990, 1240)):
    d = glass(im, b, (10, 14, 40), 200, 44, NEON)
    return d

def satellite(d, x, y, s, a):
    d.rectangle([x - 18 * s, y - 14 * s, x + 18 * s, y + 14 * s], fill=(220, 220, 230), outline=INK, width=3)
    for sg in (-1, 1):
        xa, xb = sorted([x + sg * 22 * s, x + sg * 70 * s])
        d.rectangle([xa, y - 10 * s, xb, y + 10 * s], fill=(60, 110, 200), outline=INK, width=2)

# ---------- scenes ----------
def w_hook(im, d, t, dur):
    d = space_card(im); stars_bg(d, t)
    rot = t * 0.06
    s = back(t / 0.5)
    R = int(240 * max(0.3, s))
    d = planet(im, 710, 900, R, rot, lights_on=min(1, t / 1.5))
    d = pins(d, im, 710, 900, R, rot, t, 12, 0.4)
    return (710, 900)

def w_date(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 3)
    d = planet(im, 850, 1070, 150, t * 0.05 + 0.3, lights_on=0.6)
    s = back(t / 0.45)
    if s > 0.05: M.calendar(d, 620, 820, 0.6 * s, "NOVEMBER", "19", (230, 60, 60))
    return (620, 820)

def w_gta5(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 5)
    n = int(ease(t / 2.4) * 15)
    cols = [(40, 120, 200), (230, 70, 110), (60, 170, 110)]
    for i in range(n):
        row, cl = divmod(i, 5)
        V.game_case(d, 460 + cl * 104 + (row % 2) * 18, 1210 - row * 160, 88, 140, cols[i % 3], "V")
    v = countup(t, 0.1, 2.4, 11.2)
    neon_text(im, f"{v:.1f}".replace(".", ",") + " MIO.", 710, 680, 92, NEON)
    d = ImageDraw.Draw(im)
    pill(d, "GTA 5 · TAG 1", 710, 790, 32, YEL, INK, back((t - 0.3) / 0.4))
    return (710, 680)

def beam(im, x0, y0, x1, y1, t, col, k=0):
    d = ImageDraw.Draw(im)
    for j in range(6):
        p = ((t * 1.4 + j / 6 + k * 0.13) % 1)
        x = lerp(x0, x1, p); y = lerp(y0, y1, p)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=col)
    lay = Image.new("L", (W, H), 0); ImageDraw.Draw(lay).line([(x0, y0), (x1, y1)], fill=160, width=10)
    im.paste(col, (0, 0), lay.filter(ImageFilter.GaussianBlur(8)))

def w_data(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 7)
    rot = t * 0.05 + 0.6
    d = planet(im, 710, 1020, 210, rot, lights_on=0.8)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * 0.5
        sx, sy = 710 + math.cos(a) * 330, 1020 + math.sin(a) * 330
        beam(im, sx, sy, 710 + math.cos(a) * 205, 1020 + math.sin(a) * 205, t, NEON, k)
        satellite(ImageDraw.Draw(im), sx, sy, 0.7, a)
    v = countup(t, 0.2, 2.6, 2.4)
    neon_text(im, f"{v:.1f}".replace(".", ",") + " MRD. GB", 710, 640, 74, NEON2)
    d = ImageDraw.Draw(im)
    pill(d, "RECHENBEISPIEL", 710, 730, 26, (255, 255, 255), INK, back((t - 1.0) / 0.4))
    return (710, 1020)

def clock(d, cx, cy, r, t):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=6)
    for k in range(12):
        a = k * math.pi / 6
        d.line([(cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82), (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)], fill=INK, width=5)
    a1 = t * 8 - math.pi / 2; a2 = t * 0.7 - math.pi / 2
    d.line([(cx, cy), (cx + math.cos(a1) * r * 0.75, cy + math.sin(a1) * r * 0.75)], fill=INK, width=8)
    d.line([(cx, cy), (cx + math.cos(a2) * r * 0.5, cy + math.sin(a2) * r * 0.5)], fill=RED, width=12)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=INK)

def w_time(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 9)
    clock(d, 710, 820, int(170 * back(t / 0.4)) or 1, t)
    p = ease((t - 0.3) / 2.8)
    dl_bar(d, 470, 1080, 950, p, f"{int(p * 212)} / 212 GB", CYAN)
    pill(d, "~4 STD. 43 MIN. BEI 100 MBIT", 710, 1180, 28, YEL, INK, back((t - 0.6) / 0.4))
    return (710, 820)

def w_preload(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 13)
    bloom(im, 710, 900, 160, (80, 255, 160), 0.5)
    d = ImageDraw.Draw(im)
    console(d, 710, 950, back(t / 0.4) * 1.3)
    check_icon(d, 860, 760, back((t - 0.5) / 0.3) * 2.0)
    pill(d, "JETZT VORLADEN", 710, 1150, 40, GRN, (255, 255, 255), back((t - 0.4) / 0.4) * (1 + 0.05 * math.sin(t * 9)))
    return (710, 950)

def w_money(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 15)
    for i in range(22):
        rnd = random.Random(i)
        x = rnd.randrange(450, 970); y = (rnd.randrange(-500, 0) + t * rnd.uniform(220, 380)) % 700 + 560
        V.bill(d, x, y, math.sin(t * 2 + i) * 0.8, 0.75)
    v = int(countup(t, 0.2, 2.2, 815))
    neon_text(im, f"{v} MIO. $", 710, 860, 110, (120, 255, 160))
    d = ImageDraw.Draw(im)
    pill(d, "GTA 5 · TAG 1", 710, 980, 32, YEL, INK, back((t - 0.3) / 0.4))
    return (710, 860)

def w_beat(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 17)
    rot = t * 0.08 + 1.1
    d = planet(im, 710, 900, 190, rot, lights_on=0.9)
    a = t * 2.2
    rx, ry = 710 + math.cos(a) * 300, 900 + math.sin(a) * 160
    for k in range(10):
        b = a - k * 0.08
        tx, ty = 710 + math.cos(b) * 300, 900 + math.sin(b) * 160
        r = 10 - k * 0.8
        if r > 1: d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(255, 190, 90))
    rocket(d, rx, ry, 0.45, t)
    V.qmark(d, 900, 640, back((t - 0.6) / 0.3))
    return (rx, ry)

def w_cta(im, d, t, dur):
    d = space_card(im); stars_bg(d, t, 19)
    rot = t * 0.06 + 1.6
    d = planet(im, 710, 760, 170, rot, lights_on=1.0)
    d = pins(d, im, 710, 760, 170, rot, t, 12, 0.0)
    return (710, 760)

_old = S7.defs
def defs(vid, durs):
    if vid != VID: return _old(vid, durs)
    sc = [w_hook, w_date, w_gta5, w_data, w_time, w_preload, w_money, w_beat, w_cta]
    w = [("GANZE WELT ZOCKT?!", PINK), ("19. NOVEMBER", CYAN), ("11 MIO. AM 1. TAG", GRN), ("2 MRD. GIGABYTE", PINK), ("FAST 5 STUNDEN", CYAN), ("JETZT VORLADEN", GRN), ("815 MIO. $", GRN), ("NEUER REKORD?", PINK), ("DEIN LAND?", PINK)]
    th = ["night"] * 9
    poses = ["wave", "point", "point", "point", "point", "cheer", "point", "point", "point"]
    return [(durs[i], th[i], sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(9)]
S7.defs = defs

def set_timing():
    segs = []; t = 0
    for dd in DURS: segs.append((t + 0.1, t + dd - 0.3)); t += dd
    T = S7.load_timing(); T[VID] = {"durs": DURS, "segs": segs, "total": 30.0}
    json.dump(T, open(S7.TF, "w"), indent=1)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        set_timing(); T = S7.setup(VID); words = S7.word_times(VID, T); R = S2.R[VID]
        ims = [S7.frame(VID, 0, 0.0, T, words).resize((270, 480))] + [S7.frame(VID, i, R[i][0] * (0.9 if i == 8 else 0.7), T, words).resize((270, 480)) for i in range(9)]
        shp = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(ims[:10]): shp.paste(im, ((i % 5) * 270, (i // 5) * 480))
        shp.save(os.path.join(HERE, "p10.png"))
    elif cmd == "render":
        S7.render(VID, int(sys.argv[2]))
