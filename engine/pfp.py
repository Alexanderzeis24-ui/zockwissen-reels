import math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 3840
F = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def font(n): return ImageFont.truetype(F, n)
def sh(c, f): return tuple(max(0, min(255, int(v * f))) for v in c)

im = Image.new("RGB", (S, S))
d = ImageDraw.Draw(im)
# background gradient
top, bot = (60, 30, 120), (255, 130, 90)
for y in range(S):
    t = y / S
    d.line([(0, y), (S, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
# light rays
cx, cy = S // 2, 1500
rays = Image.new("L", (S, S)); rd = ImageDraw.Draw(rays)
for i in range(16):
    a = i * math.pi / 8
    rd.polygon([(cx, cy), (cx + math.cos(a) * 4000, cy + math.sin(a) * 4000), (cx + math.cos(a + 0.18) * 4000, cy + math.sin(a + 0.18) * 4000)], fill=40)
im.paste((255, 255, 255), (0, 0), rays)
d = ImageDraw.Draw(im)
# sun
d.ellipse([cx - 1050, cy - 1050, cx + 1050, cy + 1050], fill=(255, 200, 110))
d.ellipse([cx - 900, cy - 900, cx + 900, cy + 900], fill=(255, 215, 130))
# skyline silhouette
rnd = random.Random(3); x = -50
while x < S:
    bw = rnd.randrange(220, 420); bh = rnd.randrange(500, 1200)
    d.rectangle([x, 2500 - bh, x + bw, 2600], fill=(110, 55, 130))
    for wy in range(2500 - bh + 60, 2450, 120):
        for wx in range(x + 40, x + bw - 50, 90):
            if rnd.random() < 0.5: d.rectangle([wx, wy, wx + 40, wy + 55], fill=(255, 215, 140))
    x += bw + rnd.randrange(20, 80)

def palm(x, y, s, flip=1):
    pts = [(x + flip * math.sin(i / 6 * 1.6) * 120 * s, y - i / 6 * 1500 * s) for i in range(7)]
    for i in range(6): d.line([pts[i], pts[i + 1]], fill=(70, 40, 70), width=int(90 * s))
    tx, ty = pts[-1]
    for ang in [-170, -130, -95, -60, -20, 200]:
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * 700 * s, ty + math.sin(a) * 260 * s + 260 * s
        mx, my = tx + math.cos(a) * 350 * s, ty + math.sin(a) * 260 * s - 110 * s
        d.polygon([(tx, ty), (mx, my - 80 * s), (ex, ey), (mx, my + 60 * s)], fill=(60, 35, 80))
palm(250, 2700, 1.2, 1); palm(3600, 2700, 1.1, -1)

# ---------- character (bust) ----------
skin = (232, 190, 152); shirt = (60, 160, 95); hair = (60, 40, 28)
# body / hoodie
d.rounded_rectangle([cx - 900, 2250, cx + 900, 3900], 420, fill=shirt)
d.polygon([(cx - 900, 2700), (cx - 600, 2350), (cx - 600, 3900), (cx - 900, 3900)], fill=sh(shirt, 0.85))
d.polygon([(cx + 900, 2700), (cx + 600, 2350), (cx + 600, 3900), (cx + 900, 3900)], fill=sh(shirt, 0.75))
d.chord([cx - 380, 2150, cx + 380, 2550], 0, 180, fill=sh(shirt, 0.7))   # hood collar
d.line([(cx - 120, 2500), (cx - 140, 2850)], fill=(240, 240, 240), width=30)
d.line([(cx + 120, 2500), (cx + 140, 2850)], fill=(240, 240, 240), width=30)
# neck
d.rectangle([cx - 160, 1950, cx + 160, 2300], fill=sh(skin, 0.88))
# head
d.ellipse([cx - 560, 900, cx + 560, 2140], fill=skin)
d.polygon([(cx + 100, 900), (cx + 560, 1300), (cx + 520, 1900), (cx + 200, 2140)], fill=sh(skin, 0.93))
# hair
d.chord([cx - 600, 820, cx + 600, 1700], 180, 360, fill=hair)
d.polygon([(cx - 600, 1260), (cx - 200, 1100), (cx + 300, 1180), (cx + 600, 1260), (cx + 560, 1060), (cx - 560, 1060)], fill=hair)
d.polygon([(cx - 300, 900), (cx - 100, 760), (cx + 50, 880)], fill=hair)
d.polygon([(cx - 50, 880), (cx + 150, 750), (cx + 280, 900)], fill=hair)
# eyes, brows, smile
for ex in (-230, 230):
    d.ellipse([cx + ex - 85, 1480, cx + ex + 85, 1650], fill="white")
    d.ellipse([cx + ex - 45, 1520, cx + ex + 45, 1630], fill=(40, 30, 30))
    d.ellipse([cx + ex - 10, 1530, cx + ex + 20, 1560], fill="white")
    d.line([(cx + ex - 100, 1420), (cx + ex + 90, 1400 + (ex > 0) * 0)], fill=hair, width=45)
d.arc([cx - 230, 1650, cx + 230, 1920], 15, 165, fill=(150, 70, 60), width=45)
d.ellipse([cx - 610, 1500, cx - 500, 1680], fill=sh(skin, 0.9)); d.ellipse([cx + 500, 1500, cx + 610, 1680], fill=sh(skin, 0.85))
# headset
d.arc([cx - 680, 780, cx + 680, 2100], 195, 345, fill=(35, 35, 45), width=110)
for sx in (-1, 1):
    x0 = cx + sx * 650
    d.rounded_rectangle([x0 - 130, 1400, x0 + 130, 1800], 90, fill=(35, 35, 45))
    d.rounded_rectangle([x0 - 80, 1450, x0 + 80, 1750], 60, fill=(230, 60, 90))
d.line([(cx - 650, 1750), (cx - 520, 1980), (cx - 250, 2010)], fill=(35, 35, 45), width=40, joint="curve")
d.ellipse([cx - 290, 1965, cx - 200, 2055], fill=(35, 35, 45))
# hands + controller
cw, ctop = 1300, 2620
d.rounded_rectangle([cx - cw / 2, ctop, cx + cw / 2, ctop + 420], 200, fill=(40, 40, 50))
d.ellipse([cx - cw / 2 - 60, ctop + 150, cx - cw / 2 + 380, ctop + 640], fill=(40, 40, 50))
d.ellipse([cx + cw / 2 - 380, ctop + 150, cx + cw / 2 + 60, ctop + 640], fill=(40, 40, 50))
# dpad
dx, dy = cx - 380, ctop + 220
d.rectangle([dx - 110, dy - 35, dx + 110, dy + 35], fill=(200, 200, 210)); d.rectangle([dx - 35, dy - 110, dx + 35, dy + 110], fill=(200, 200, 210))
# buttons
bx, by = cx + 380, ctop + 220
for (ox, oy), col in zip([(0, -100), (100, 0), (0, 100), (-100, 0)], [(80, 200, 120), (230, 70, 80), (80, 140, 240), (250, 200, 60)]):
    d.ellipse([bx + ox - 50, by + oy - 50, bx + ox + 50, by + oy + 50], fill=col)
d.ellipse([cx - 160, ctop + 260, cx - 40, ctop + 380], fill=(20, 20, 25)); d.ellipse([cx + 40, ctop + 260, cx + 160, ctop + 380], fill=(20, 20, 25))
for sx in (-1, 1):
    hx = cx + sx * 640
    d.ellipse([hx - 200, ctop + 260, hx + 200, ctop + 600], fill=skin)

# lightbulb badge (knowledge) top right
lx, ly = cx + 950, 820
d.ellipse([lx - 300, ly - 300, lx + 300, ly + 300], fill=(255, 255, 255))
d.ellipse([lx - 270, ly - 270, lx + 270, ly + 270], fill=(250, 200, 50))
d.ellipse([lx - 130, ly - 190, lx + 130, ly + 80], fill=(255, 245, 200))
d.rectangle([lx - 70, ly + 60, lx + 70, ly + 160], fill=(120, 120, 130))
d.line([(lx - 70, ly + 100), (lx + 70, ly + 100)], fill=(90, 90, 100), width=16)

# sparkles
rnd = random.Random(9)
for _ in range(18):
    x, y = rnd.randrange(400, 3440), rnd.randrange(250, 1300)
    if abs(x - cx) < 700: continue
    r = rnd.randrange(30, 80)
    d.polygon([(x, y - r), (x + r * .3, y - r * .3), (x + r, y), (x + r * .3, y + r * .3), (x, y + r), (x - r * .3, y + r * .3), (x - r, y), (x - r * .3, y - r * .3)], fill=(255, 245, 200))

# ---------- name banner ----------
NAME = "ZOCKWISSEN"
fs = 560
while True:
    f = font(fs); bb = d.textbbox((0, 0), NAME, font=f, stroke_width=36)
    if bb[2] - bb[0] <= 2900: break
    fs -= 10
ty = 3080
bw2 = (bb[2] - bb[0]) / 2 + 140
d.rounded_rectangle([cx - bw2, ty - 380, cx + bw2, ty + 330], 200, fill=(25, 20, 40))
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
sd.text((cx + 25, ty + 35), NAME, font=f, anchor="mm", fill=(0, 0, 0, 160), stroke_width=36, stroke_fill=(0, 0, 0, 160))
im = Image.alpha_composite(im.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(20))).convert("RGB")
d = ImageDraw.Draw(im)
d.text((cx, ty), NAME, font=f, anchor="mm", fill="white", stroke_width=36, stroke_fill=(15, 15, 15))
# small accent underline
d.rounded_rectangle([cx - 600, ty + 230, cx + 600, ty + 280], 25, fill=(255, 200, 60))

out = os.path.dirname(os.path.abspath(__file__)) + "/"
im.save(out + "Profilbild_ZOCKWISSEN_4K.png", optimize=True)
# circle preview like Instagram
pv = im.resize((480, 480)); m = Image.new("L", (480, 480)); ImageDraw.Draw(m).ellipse([0, 0, 480, 480], fill=255)
bg = Image.new("RGB", (480, 480), "black"); bg.paste(pv, (0, 0), m); bg.save(out + "pfp_preview.png")
