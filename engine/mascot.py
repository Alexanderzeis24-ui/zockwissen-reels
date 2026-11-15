import math
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def sh(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

R = 1000  # draw radius
def draw_badge(mouth=0, blink=False, size=600):
    D = 2 * R
    im = Image.new("RGB", (D, D)); d = ImageDraw.Draw(im)
    top, bot = (60, 30, 120), (255, 130, 90)
    for y in range(D):
        t = y / D
        d.line([(0, y), (D, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    cx, oy = R, -500  # coordinates match profile picture with head ~1500 -> 1000
    Y = lambda y: y + oy
    d.ellipse([cx - 900, Y(1500) - 900, cx + 900, Y(1500) + 900], fill=(255, 210, 125))
    skin, shirt, hair = (232, 190, 152), (60, 160, 95), (60, 40, 28)
    d.rounded_rectangle([cx - 900, Y(2250), cx + 900, Y(3900)], 420, fill=shirt)
    d.chord([cx - 380, Y(2150), cx + 380, Y(2550)], 0, 180, fill=sh(shirt, 0.7))
    d.rectangle([cx - 160, Y(1950), cx + 160, Y(2300)], fill=sh(skin, 0.88))
    d.ellipse([cx - 560, Y(900), cx + 560, Y(2140)], fill=skin)
    d.chord([cx - 600, Y(820), cx + 600, Y(1700)], 180, 360, fill=hair)
    d.polygon([(cx - 600, Y(1260)), (cx - 200, Y(1100)), (cx + 300, Y(1180)), (cx + 600, Y(1260)), (cx + 560, Y(1060)), (cx - 560, Y(1060))], fill=hair)
    d.polygon([(cx - 300, Y(900)), (cx - 100, Y(760)), (cx + 50, Y(880))], fill=hair)
    d.polygon([(cx - 50, Y(880)), (cx + 150, Y(750)), (cx + 280, Y(900))], fill=hair)
    for ex in (-230, 230):
        if blink:
            d.line([(cx + ex - 85, Y(1570)), (cx + ex + 85, Y(1570))], fill=(40, 30, 30), width=34)
        else:
            d.ellipse([cx + ex - 85, Y(1480), cx + ex + 85, Y(1650)], fill="white")
            d.ellipse([cx + ex - 45, Y(1520), cx + ex + 45, Y(1630)], fill=(40, 30, 30))
            d.ellipse([cx + ex - 10, Y(1530), cx + ex + 20, Y(1560)], fill="white")
        d.line([(cx + ex - 100, Y(1420 - mouth * 15)), (cx + ex + 90, Y(1400 - mouth * 15))], fill=hair, width=45)
    if mouth == 0:
        d.arc([cx - 230, Y(1650), cx + 230, Y(1920)], 15, 165, fill=(150, 70, 60), width=45)
    else:
        h = [0, 90, 170, 240][mouth]
        d.chord([cx - 210, Y(1760) - h * 0.2, cx + 210, Y(1760) + h], 0, 180, fill=(110, 40, 45))
        d.rectangle([cx - 150, Y(1760) - h * 0.2 + 2, cx + 150, Y(1760) + 25], fill=(250, 250, 250))
        d.ellipse([cx - 90, Y(1760) + h * 0.55, cx + 90, Y(1760) + h * 0.95], fill=(220, 100, 110))
    d.arc([cx - 680, Y(780), cx + 680, Y(2100)], 195, 345, fill=(35, 35, 45), width=110)
    for sx in (-1, 1):
        x0 = cx + sx * 650
        d.rounded_rectangle([x0 - 130, Y(1400), x0 + 130, Y(1800)], 90, fill=(35, 35, 45))
        d.rounded_rectangle([x0 - 80, Y(1450), x0 + 80, Y(1750)], 60, fill=(230, 60, 90))
    d.line([(cx - 650, Y(1750)), (cx - 520, Y(1980)), (cx - 250, Y(2010))], fill=(35, 35, 45), width=40, joint="curve")
    d.ellipse([cx - 290, Y(1965), cx - 200, Y(2055)], fill=(35, 35, 45))
    out = Image.new("RGBA", (D + 120, D + 120), (0, 0, 0, 0)); od = ImageDraw.Draw(out)
    od.ellipse([0, 0, D + 120, D + 120], fill=(255, 255, 255, 255))
    m = Image.new("L", (D, D)); ImageDraw.Draw(m).ellipse([0, 0, D, D], fill=255)
    out.paste(im, (60, 60), m)
    return out.resize((size, size), Image.LANCZOS)

_cache = {}
def badge(mouth, blink):
    k = (mouth, blink)
    if k not in _cache: _cache[k] = draw_badge(mouth, blink)
    return _cache[k]

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def back(t):
    t = max(0, min(1, t)); c = 1.7
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

def mouth_at(gt):
    v = abs(math.sin(gt * 10.5) * math.sin(gt * 3.3 + 1))
    return 0 if v < 0.15 else 1 if v < 0.45 else 2 if v < 0.75 else 3

def overlay(frame, gt, outro_t=None):
    """frame: RGB 1080x1920. gt: global time. outro_t: seconds into outro (None if not outro)."""
    blink = (gt % 3.2) < 0.12
    b = badge(mouth_at(gt), blink)
    bob = math.sin(gt * 3) * 6
    tilt = math.sin(gt * 1.7) * 4
    if outro_t is None:
        intro = back(gt / 0.5)
        cx, cy, r = 185, 960 + bob, 145 * intro
    else:
        p = ease(outro_t / 0.6)
        cx = 185 + (540 - 185) * p; cy = 960 + (520 - 960) * p + bob; r = 145 + (270 - 145) * p
    if r < 3: return frame
    sz = int(2 * r)
    img = b.resize((sz, sz), Image.BILINEAR).rotate(tilt, resample=Image.BICUBIC)
    # soft shadow
    shd = Image.new("RGBA", (sz, sz), (0, 0, 0, 0)); ImageDraw.Draw(shd).ellipse([0, 0, sz, sz], fill=(0, 0, 0, 90))
    frame.paste(shd, (int(cx - r + 10), int(cy - r + 16)), shd)
    frame.paste(img, (int(cx - r), int(cy - r)), img)
    if outro_t is not None and outro_t > 0.5:
        s = back((outro_t - 0.5) / 0.35) * (1 + 0.06 * math.sin(outro_t * 8))
        if s > 0.05:
            d = ImageDraw.Draw(frame)
            w, h = 420 * s, 110 * s; y0 = cy + r + 40
            d.rounded_rectangle([540 - w / 2, y0, 540 + w / 2, y0 + h], int(55 * s), fill=(235, 50, 80), outline="white", width=max(1, int(8 * s)))
            d.text((540, y0 + h / 2), "+ FOLGEN", font=ImageFont.truetype(FONT, max(8, int(64 * s))), fill="white", anchor="mm")
    return frame
