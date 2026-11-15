import math, random, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import mascot

W, H, FPS = 1080, 1920, 30
SCENE_H = 1180          # upper 3D scene area
OUT = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

def font(s): return ImageFont.truetype(FONT, s)

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def shade(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

def box(d, x, y, w, h, dep, col):
    dx, dy = dep * 0.55, dep * 0.45
    d.polygon([(x, y), (x + w, y), (x + w + dx, y - dy), (x + dx, y - dy)], fill=shade(col, 1.18))
    d.polygon([(x + w, y), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h)], fill=shade(col, 0.72))
    d.rectangle([x, y, x + w, y + h], fill=col)

def grad(top, bot, h=SCENE_H):
    im = Image.new("RGB", (W, h)); d = ImageDraw.Draw(im)
    for yy in range(h):
        t = yy / h
        d.line([(0, yy), (W, yy)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    return im

def cloud(d, x, y, s=1.0):
    for ox, oy, r in [(0, 0, 60), (60, -25, 70), (130, 0, 55), (60, 20, 60)]:
        d.ellipse([x + ox * s - r * s, y + oy * s - r * s, x + ox * s + r * s, y + oy * s + r * s], fill=(245, 247, 250))

def palm(d, x, y, s=1.0, sway=0.0):
    trunk = (120, 84, 52)
    pts = []
    for i in range(7):
        t = i / 6
        pts.append((x + math.sin(t * 1.6) * 35 * s + sway * t * 10, y - t * 300 * s))
    for i in range(6):
        d.line([pts[i], pts[i + 1]], fill=shade(trunk, 1 - i * 0.03), width=int(22 * s))
    tx, ty = pts[-1]
    for k, ang in enumerate([-160, -125, -90, -55, -20, 200]):
        a = math.radians(ang + sway * 6)
        ex, ey = tx + math.cos(a) * 150 * s, ty + math.sin(a) * 60 * s + 55 * s
        mx, my = tx + math.cos(a) * 75 * s, ty + math.sin(a) * 60 * s - 25 * s
        g = (52, 150, 72) if k % 2 else (40, 125, 60)
        d.polygon([(tx, ty), (mx, my - 18 * s), (ex, ey), (mx, my + 14 * s)], fill=g)

def person(d, x, y, shirt, pants, hair, skin=(222, 184, 150), long_hair=False, bob=0):
    y = y + bob
    d.rounded_rectangle([x - 40, y - 230, x - 6, y], 16, fill=pants)
    d.rounded_rectangle([x + 6, y - 230, x + 40, y], 16, fill=shade(pants, 0.85))
    d.rounded_rectangle([x - 52, y + -10, x - 2, y + 14], 10, fill=(240, 240, 240))
    d.rounded_rectangle([x + 2, y - 10, x + 52, y + 14], 10, fill=(240, 240, 240))
    d.rounded_rectangle([x - 58, y - 420, x + 58, y - 215], 30, fill=shirt)
    d.rounded_rectangle([x - 82, y - 405, x - 52, y - 260], 15, fill=shade(shirt, 0.85))
    d.rounded_rectangle([x + 52, y - 405, x + 82, y - 260], 15, fill=shade(shirt, 0.75))
    d.ellipse([x - 82, y - 272, x - 52, y - 242], fill=skin)
    d.ellipse([x + 52, y - 272, x + 82, y - 242], fill=skin)
    d.rectangle([x - 14, y - 445, x + 14, y - 415], fill=shade(skin, 0.9))
    d.ellipse([x - 48, y - 545, x + 48, y - 435], fill=skin)
    if long_hair:
        d.rounded_rectangle([x - 54, y - 530, x + 54, y - 400], 30, fill=hair)
        d.ellipse([x - 44, y - 520, x + 44, y - 440], fill=skin)
    d.chord([x - 52, y - 552, x + 52, y - 455], 180, 360, fill=hair)

# ---------- static bottom wall (like the reference) ----------
def make_wall():
    h = H - SCENE_H
    im = Image.new("RGB", (W, h), (150, 128, 92)); d = ImageDraw.Draw(im)
    rnd = random.Random(3)
    for _ in range(9000):
        x, y = rnd.randrange(W), rnd.randrange(h); r = rnd.choice([2, 3, 4])
        c = rnd.choice([(170, 148, 110), (128, 108, 76), (160, 138, 100)])
        d.ellipse([x, y, x + r, y + r], fill=c)
    bh = 190
    for row in range(h // bh + 1):
        y = row * bh
        d.rectangle([0, y, W, y + 8], fill=(105, 88, 60))
        off = 0 if row % 2 == 0 else 270
        for x in range(-off, W, 540):
            d.rectangle([x, y, x + 8, y + bh], fill=(105, 88, 60))
            for k in range(2):
                cx = x + 135 + k * 270
                d.ellipse([cx - 14, y + bh // 2 - 14, cx + 14, y + bh // 2 + 14], fill=(55, 45, 32))
    shadow = Image.new("L", (W, 60)); sd = ImageDraw.Draw(shadow)
    for i in range(60): sd.line([(0, i), (W, i)], fill=int(140 * (1 - i / 60)))
    im.paste((30, 25, 18), (0, 0), shadow)
    return im

WALL = make_wall()

# ---------- big word with black outline ----------
_word_cache = {}
def word_img(text):
    if text in _word_cache: return _word_cache[text]
    size = 190
    while True:
        f = font(size)
        bb = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), text, font=f, stroke_width=16)
        if bb[2] - bb[0] <= 960 or size < 60: break
        size -= 6
    tw, th = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    im = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((30 - bb[0] + 10, 30 - bb[1] + 14), text, font=f, fill=(0, 0, 0, 150), stroke_width=16, stroke_fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    im.alpha_composite(sh)
    d.text((30 - bb[0], 30 - bb[1]), text, font=f, fill="white", stroke_width=16, stroke_fill=(15, 15, 15))
    _word_cache[text] = im
    return im

# ---------- scenes: each returns a function(t_local, dur) -> RGB scene image ----------
DAY = grad((108, 150, 205), (190, 215, 240))
SUNSET = grad((88, 48, 140), (255, 150, 110))
NIGHT = grad((24, 34, 70), (60, 80, 140))

def ground(d, y, col=(196, 200, 206)):
    d.rectangle([0, y, W, SCENE_H], fill=col)

def sc_preload(t, dur):
    im = NIGHT.copy(); d = ImageDraw.Draw(im)
    ground(d, 860, (70, 74, 96))
    # TV stand + TV
    box(d, 180, 780, 640, 90, 120, (110, 82, 60))
    d.rounded_rectangle([170, 300, 830, 700], 18, fill=(28, 28, 34))
    box(d, 180, 310, 640, 380, 40, (35, 35, 42))
    d.rectangle([205, 335, 795, 665], fill=(20, 60, 120))
    d.rectangle([470, 700, 530, 780], fill=(40, 40, 46))
    # download arrow bouncing
    by = 380 + math.sin(t * 7) * 18
    d.polygon([(470, by), (530, by), (530, by + 70), (575, by + 70), (500, by + 140), (425, by + 70), (470, by + 70)], fill=(255, 255, 255))
    # progress bar
    p = ease(t / (dur * 0.9))
    d.rounded_rectangle([250, 590, 750, 625], 17, fill=(10, 30, 60))
    d.rounded_rectangle([250, 590, 250 + max(34, 500 * p), 625], 17, fill=(80, 220, 120))
    d.text((500, 648), f"{int(p * 100)}%", font=font(40), fill="white", anchor="mm")
    # console
    box(d, 380, 720, 240, 60, 90, (235, 236, 240))
    d.rectangle([395, 742, 450, 750], fill=(60, 140, 255))
    # stars
    rnd = random.Random(1)
    for _ in range(40):
        x, y = rnd.randrange(W), rnd.randrange(260)
        a = 0.5 + 0.5 * math.sin(t * 4 + x)
        c = int(140 + 115 * a); d.ellipse([x, y, x + 5, y + 5], fill=(c, c, c))
    return im

def calendar(d, cx, cy, s, top, num, col=(220, 60, 60)):
    w, h = 420 * s, 460 * s
    x, y = cx - w / 2, cy - h / 2
    box(d, x, y, w, h, 50 * s, (248, 248, 248))
    d.rectangle([x, y, x + w, y + 120 * s], fill=col)
    for k in (0.28, 0.72):
        d.rounded_rectangle([x + w * k - 12 * s, y - 40 * s, x + w * k + 12 * s, y + 30 * s], 8, fill=(80, 80, 90))
    d.text((cx, y + 62 * s), top, font=font(int(58 * s)), fill="white", anchor="mm")
    d.text((cx, y + 290 * s), num, font=font(int(190 * s)), fill=(40, 40, 50), anchor="mm")

def sc_date(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im)
    cloud(d, 120 + t * 15, 180); cloud(d, 760 - t * 10, 260, 0.8)
    ground(d, 900)
    s = back(t / 0.5)
    if s > 0.02:
        calendar(d, 540, 620, 1.25 * s, "NOVEMBER", "19")
    rnd = random.Random(7)
    if t > 0.5:
        for i in range(60):
            x0 = rnd.randrange(W); sp = rnd.uniform(200, 450)
            yy = -40 + (t - 0.5) * sp + rnd.randrange(-300, 0)
            col = rnd.choice([(255, 90, 90), (90, 200, 255), (255, 210, 60), (120, 230, 140), (220, 120, 255)])
            a = (t * 5 + i)
            d.polygon([(x0 + 14 * math.cos(a), yy + 8 * math.sin(a)), (x0 - 14 * math.cos(a), yy - 8 * math.sin(a)),
                       (x0 - 14 * math.cos(a) + 6, yy + 12), (x0 + 6, yy + 14)], fill=col)
    return im

def xmark(d, cx, cy, r, prog):
    p1 = min(1, prog * 2); p2 = max(0, prog * 2 - 1)
    if p1 > 0: d.line([(cx - r, cy - r), (cx - r + 2 * r * p1, cy - r + 2 * r * p1)], fill=(230, 40, 40), width=30)
    if p2 > 0: d.line([(cx + r, cy - r), (cx + r - 2 * r * p2, cy - r + 2 * r * p2)], fill=(230, 40, 40), width=30)

def sc_delay(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im)
    ground(d, 980)
    items = [("HERBST", "2025", 0.0), ("MAI", "2026", 1.3), ("NOV", "2026", 2.6)]
    for i, (top, num, start) in enumerate(items):
        s = back((t - start) / 0.4)
        if s <= 0.02: continue
        cx = 200 + i * 340; cy = 640
        calendar(d, cx, cy, 0.62 * s, top, num, (220, 60, 60) if i < 2 else (40, 170, 90))
        if i < 2:
            xmark(d, cx, cy + 30, 110, ease((t - start - 0.6) / 0.4))
        elif t > start + 0.5:
            # green check
            p = ease((t - start - 0.5) / 0.4)
            pts = [(cx - 80, cy + 60), (cx - 20, cy + 120), (cx + 100, cy - 20)]
            if p > 0:
                d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * min(1, p * 2), pts[0][1] + (pts[1][1] - pts[0][1]) * min(1, p * 2))], fill=(40, 190, 90), width=28)
            if p > 0.5:
                q = (p - 0.5) * 2
                d.line([pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)], fill=(40, 190, 90), width=28)
    return im

def sc_city(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im)
    pan = -t * 40
    d.ellipse([380, 340, 700, 660], fill=(255, 210, 120))
    rnd = random.Random(4)
    x = -100 + pan
    while x < W + 100:
        bw = rnd.randrange(80, 150); bh = rnd.randrange(180, 460)
        col = rnd.choice([(120, 70, 150), (150, 80, 160), (100, 60, 130), (170, 100, 170)])
        box(d, x, 760 - bh, bw, bh, 40, col)
        for wy in range(int(760 - bh + 25), 740, 45):
            for wx in range(int(x + 15), int(x + bw - 20), 32):
                if rnd.random() < 0.55: d.rectangle([wx, wy, wx + 14, wy + 20], fill=(255, 220, 140))
        x += bw + rnd.randrange(10, 40)
    d.rectangle([0, 760, W, 900], fill=(60, 140, 190))
    for k in range(8):
        yy = 780 + k * 15
        off = (t * 60 + k * 47) % 200
        for xx in range(-200, W, 200):
            d.line([(xx + off, yy), (xx + off + 70, yy)], fill=(140, 200, 230), width=4)
    d.polygon([(0, 900), (W, 870), (W, SCENE_H), (0, SCENE_H)], fill=(238, 205, 150))
    sw = math.sin(t * 2.2)
    palm(d, 130 + pan * 0.5, 1110, 1.3, sw); palm(d, 900 + pan * 0.5, 1130, 1.15, -sw); palm(d, 1050 + pan * 0.5, 1010, 0.8, sw)
    return im

def sc_duo(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im)
    d.rectangle([0, 820, W, SCENE_H], fill=(170, 172, 180))
    d.polygon([(0, 950), (W, 900), (W, 930), (0, 985)], fill=(220, 220, 225))
    palm(d, 120, 870, 0.9, math.sin(t * 2)); palm(d, 980, 860, 0.95, -math.sin(t * 2))
    s1 = ease(t / 0.45); s2 = ease((t - 0.35) / 0.45)
    if s1 > 0: person(d, 360 - (1 - s1) * 500, 1110, (230, 120, 160), (40, 60, 120), (40, 28, 22), (205, 160, 125), True, math.sin(t * 6) * 4)
    if s2 > 0: person(d, 720 + (1 - s2) * 500, 1110, (60, 140, 90), (50, 80, 150), (70, 50, 30), (225, 188, 155), False, math.cos(t * 6) * 4)
    if t > 1.0:
        p = back((t - 1.0) / 0.4)
        r = 50 * p
        d.ellipse([540 - r, 450 - r, 540 + r, 450 + r], fill=(230, 60, 60))
        d.text((540, 452), "2", font=font(max(10, int(64 * p))), fill="white", anchor="mm")
    return im

def check(d, cx, cy, p, s=1.0):
    if p <= 0: return
    d.ellipse([cx - 60 * s, cy - 60 * s, cx + 60 * s, cy + 60 * s], fill=(40, 180, 90))
    pts = [(cx - 30 * s, cy), (cx - 8 * s, cy + 25 * s), (cx + 32 * s, cy - 22 * s)]
    d.line(pts, fill="white", width=int(16 * s), joint="curve")

def sc_platform(t, dur):
    im = DAY.copy(); d = ImageDraw.Draw(im)
    cloud(d, 80 + t * 12, 160, 0.8); cloud(d, 800 - t * 12, 230, 0.7)
    ground(d, 900)
    # left: two consoles
    s = back(t / 0.4)
    if s > 0.02:
        box(d, 110, 780 - 300 * s, 120 * s, 300 * s, 70, (240, 240, 244))
        d.rectangle([125, 800 - 300 * s, 200, 806 - 300 * s], fill=(60, 140, 255))
        box(d, 280, 780 - 260 * s, 150 * s, 260 * s, 80, (40, 44, 48))
        d.ellipse([320, 800 - 255 * s, 345, 825 - 255 * s], fill=(80, 200, 90))
    check(d, 290, 380, ease((t - 0.6) / 0.3), back((t - 0.6) / 0.3))
    # right: PC monitor
    s2 = back((t - 0.9) / 0.4)
    if s2 > 0.02:
        box(d, 610, 780, 120, 20, 40, (60, 60, 70))
        d.rectangle([660, 700, 690, 780], fill=(60, 60, 70))
        box(d, 560, 700 - 280 * s2, 330, 280 * s2, 30, (30, 30, 38))
        d.rectangle([578, 718 - 280 * s2, 872, 682], fill=(90, 110, 140))
        d.text((725, 700 - 140 * s2), "PC", font=font(max(10, int(90 * s2))), fill="white", anchor="mm")
    if t > 1.4:
        xmark(d, 725, 560, 120, ease((t - 1.4) / 0.4))
    return im

def car(d, x, y, col):
    d.polygon([(x, y), (x + 420, y), (x + 440, y - 60), (x + 330, y - 75), (x + 250, y - 140), (x + 110, y - 140), (x + 40, y - 75), (x - 10, y - 60)], fill=col)
    d.polygon([(x + 125, y - 125), (x + 240, y - 125), (x + 300, y - 78), (x + 80, y - 78)], fill=(150, 200, 235))
    d.line([(x + 190, y - 125), (x + 190, y - 78)], fill=col, width=8)
    d.rectangle([x + 420, y - 55, x + 442, y - 40], fill=(255, 240, 160))
    d.rectangle([x - 12, y - 55, x + 6, y - 40], fill=(230, 50, 50))
    for wx in (x + 90, x + 330):
        d.ellipse([wx - 48, y - 45, wx + 48, y + 51], fill=(25, 25, 28))
        d.ellipse([wx - 22, y - 19, wx + 22, y + 25], fill=(170, 170, 180))

def sc_outro(t, dur):
    im = SUNSET.copy(); d = ImageDraw.Draw(im)
    d.ellipse([600, 300, 860, 560], fill=(255, 210, 120))
    d.rectangle([0, 800, W, SCENE_H], fill=(70, 72, 80))
    d.rectangle([0, 800, W, 830], fill=(150, 150, 158))
    off = (t * 900) % 300
    for xx in range(-300, W + 300, 300):
        d.rectangle([xx - off, 985, xx - off + 150, 1000], fill=(240, 220, 120))
    for i, base in enumerate([0, 520]):
        px = ((base - t * 500) % (W + 400)) - 200
        palm(d, px, 805, 0.95, math.sin(t * 3 + i))
    cx = -460 + ease(t / 0.8) * 760
    bounce = math.sin(t * 25) * 3
    car(d, cx, 1080 + bounce, (225, 45, 85))
    for k in range(5):
        lx = cx - 60 - k * 70 - (t * 300 % 70)
        d.line([(lx, 1000 + k * 15), (lx - 80, 1000 + k * 15)], fill=(220, 220, 230), width=5)
    return im

SCENES = [
    # (duration, scene fn, big word, speaker line)
    (4.0, sc_preload, "PRELOAD", "Ab morgen könnt ihr GTA 6 schon vorab runterladen!"),
    (4.0, sc_date, "19. NOVEMBER", "Denn am 19. November erscheint das Spiel endlich."),
    (5.0, sc_delay, "VERSCHOBEN", "Eigentlich sollte es schon 2025 kommen, dann im Mai 2026 – jetzt ist es wirklich so weit."),
    (4.5, sc_city, "VICE CITY", "Gespielt wird in Vice City, im fiktiven Bundesstaat Leonida."),
    (4.0, sc_duo, "ZU ZWEIT", "Und zum ersten Mal mit einem Gangster-Duo: Lucia und Jason."),
    (4.5, sc_platform, "NUR KONSOLE", "Das Spiel kommt nur für PS5 und Xbox Series – eine PC-Version gibt es noch nicht."),
    (4.0, sc_outro, "FOLGT FÜR MEHR", "Holt ihr es euch zum Release? Folgt für mehr Gaming-News!"),
]

def render(idx):
    dur, fn, word, _ = SCENES[idx]
    n = int(round(dur * FPS))
    path = os.path.join(OUT, f"scene{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    wimg = word_img(word)
    for i in range(n):
        frame = render_frame(idx, i / FPS, dur, fn, wimg)
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(path, os.path.join(OUT, f"scene{idx}.mp4"))

def render_frame(idx, t, dur, fn, wimg):
    frame = Image.new("RGB", (W, H))
    sc = fn(t, dur)
    z = 1.0 + 0.05 * (t / dur)   # slow push-in
    if z > 1.001:
        zw, zh = int(W * z), int(SCENE_H * z)
        sc = sc.resize((zw, zh), Image.BILINEAR).crop(((zw - W) // 2, (zh - SCENE_H) // 2, (zw - W) // 2 + W, (zh - SCENE_H) // 2 + SCENE_H))
    frame.paste(sc, (0, 0))
    frame.paste(WALL, (0, SCENE_H))
    # word pop-in
    s = back(t / 0.22)
    if s > 0.02:
        ww, wh = int(wimg.width * s), int(wimg.height * s)
        wi = wimg.resize((max(1, ww), max(1, wh)), Image.BILINEAR)
        frame.paste(wi, ((W - ww) // 2, SCENE_H + 40 - wh // 2), wi)
    gt = sum(sc_[0] for sc_ in SCENES[:idx]) + t
    frame = mascot.overlay(frame, gt, t if idx == len(SCENES) - 1 else None)
    # white flash at cut
    if t < 0.08 and idx > 0:
        frame = Image.blend(frame, Image.new("RGB", (W, H), "white"), 0.6 * (1 - t / 0.08))
    return frame

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        for idx, (dur, fn, word, _) in enumerate(SCENES):
            render_frame(idx, dur * 0.75, dur, fn, word_img(word)).resize((360, 640)).save(os.path.join(OUT, f"prev{idx}.png"))
    else:
        render(int(sys.argv[1]))
