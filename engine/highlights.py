import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
from scenes13 import gtext, atext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK
from reel2 import draw_character
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(HERE, "ZOCKWISSEN_Highlights"); os.makedirs(OUT, exist_ok=True)
GOLD = (255, 205, 70)

def icon_mask(kind, S=600):
    m = Image.new("L", (S, S), 0); d = ImageDraw.Draw(m); c = S / 2
    if kind == "clock":
        d.ellipse([c - 230, c - 210, c + 230, c + 250], outline=255, width=44)
        d.rounded_rectangle([c - 60, c - 290, c + 60, c - 230], 20, fill=255)
        d.line([(c, c + 20), (c, c - 120)], fill=255, width=40); d.line([(c, c + 20), (c + 110, c + 90)], fill=255, width=40)
        d.ellipse([c - 34, c - 14, c + 34, c + 54], fill=255)
    elif kind == "bolt":
        d.polygon([(c + 60, c - 280), (c - 170, c + 40), (c - 10, c + 40), (c - 70, c + 280), (c + 170, c - 50), (c + 10, c - 50)], fill=255)
    elif kind == "pin":
        d.ellipse([c - 190, c - 280, c + 190, c + 100], fill=255)
        d.polygon([(c - 165, c - 0), (c + 165, c - 0), (c, c + 280)], fill=255)
        d.ellipse([c - 80, c - 170, c + 80, c - 10], fill=0)
    elif kind == "mega":
        d.polygon([(c - 200, c - 80), (c + 120, c - 240), (c + 120, c + 200), (c - 200, c + 60)], fill=255)
        d.rounded_rectangle([c - 260, c - 90, c - 160, c + 70], 20, fill=255)
        d.polygon([(c - 170, c + 50), (c - 90, c + 60), (c - 50, c + 230), (c - 130, c + 230)], fill=255)
        for r in (70, 150):
            d.arc([c + 120 - r, c - 20 - r, c + 120 + r, c - 20 + r], -40, 40, fill=255, width=34)
    elif kind == "pad":
        d.rounded_rectangle([c - 270, c - 130, c + 270, c + 110], 110, fill=255)
        d.ellipse([c - 270, c - 40, c - 90, c + 220], fill=255); d.ellipse([c + 90, c - 40, c + 270, c + 220], fill=255)
        d.rectangle([c - 190, c - 30, c - 90, c + 0], fill=0); d.rectangle([c - 155, c - 65, c - 125, c + 35], fill=0)
        for dx, dy in ((120, -45), (170, 0), (120, 45), (70, 0)): d.ellipse([c + dx - 22, c + dy - 37, c + dx + 22, c + dy + 7], fill=0)
    return m

def paste_icon(im, kind, cx, cy, size, c1, c2):
    m = icon_mask(kind).resize((size, size), Image.LANCZOS)
    x, y = int(cx - size / 2), int(cy - size / 2)
    g = m.filter(ImageFilter.GaussianBlur(size / 18)).point(lambda v: int(v * 0.8))
    im.paste(c1, (x, y), g)
    k = np.linspace(0, 1, size, dtype=np.float32)
    kk = ((k[None, :] + k[:, None]) / 2)[..., None]
    grad = (np.array(c1, np.float32) * (1 - kk) + np.array(c2, np.float32) * kk).astype(np.uint8)
    im.paste(Image.fromarray(grad), (x, y), m)

HL = [
    ("COUNTDOWN", "clock", RD, MAG, ("GTA 6", "COUNTDOWN"), ["Jeden Tag ein neuer Teil", "6 Fakten pro Video", "Bis zum Release am 19.11."], "FOLGEN = NICHTS VERPASSEN"),
    ("FAKTEN", "bolt", LIME, CY, ("DIE KRASSESTEN", "GTA 6 FAKTEN"), ["Polizei, Realismus, Story", "Immer mit Quelle", "Gerüchte klar markiert"], "WELCHEN KANNTEST DU?"),
    ("MAP", "pin", CY, VIO, ("LEONIDA", "& VICE CITY"), ["Map 2× so groß wie GTA 5", "Vice City = 2× Los Santos", "Hunderte Innenräume"], "ALLES ÜBER DIE MAP"),
    ("NEWS", "mega", ORG, RD, ("GTA 6", "NEWS"), ["Release, Preis, Trailer", "Kurz & klar erklärt", "Jeden Tag neu"], "IMMER UP TO DATE"),
    ("TIPPS", "pad", GOLD, ORG, ("TIPPS &", "GEHEIMNISSE"), ["Startet am 19.11.", "Geld-Tricks & Verstecke", "Easter Eggs & Secrets"], "BALD HIER"),
]

def bg(c1, c2, w, h, gt=3.0):
    a = S13.aurora(gt, c1, c2)
    if (w, h) != a.size:
        a = a.resize((w, int(w * a.height / a.width)), Image.BICUBIC)
        top = (a.height - h) // 2; a = a.crop((0, top, w, top + h))
    return a

def cover(name, kind, c1, c2):
    im = bg(c1, c2, 1080, 1080)
    d = ImageDraw.Draw(im, "RGBA")
    for k in range(6):
        r = 420 - k * 6
        d.ellipse([540 - r, 540 - r, 540 + r, 540 + r], outline=c1 + (40 + k * 25,), width=3)
    d.ellipse([150, 150, 930, 930], fill=(8, 9, 20, 150))
    paste_icon(im, kind, 540, 540, 470, c1, c2)
    im.save(os.path.join(OUT, f"Cover_{name}.png"))
    return im

def story(name, kind, c1, c2, head, bullets, cta):
    W_, H_ = 1080, 1920
    im = S13.aurora(4.0, c1, c2); im.paste(S13.OVER, (0, 0), S13.OVER)
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([64, 163, 84, 183], fill=LIME + (255,)); d.text((96, 173), "ZOCKWISSEN", font=FS(30), fill=(255, 255, 255, 230), anchor="lm")
    d.text((1016, 173), "HIGHLIGHT", font=FS(30), fill=(255, 255, 255, 230), anchor="rm")
    atext(im, 64, 300, head[0], S13.fit(FX, head[0], 76, 950), WH, 1, "lm")
    gtext(im, head[1], 0, 412, S13.fit(FX, head[1], 112, 950), c1, c2, left=64)
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = 430, 560, 1010, 1240
    im.paste(c1, (x0 - 120, y0 - 120), S13._glow(x1 - x0, y1 - y0).point(lambda v: int(v * 0.3)))
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle([x0, y0, x1, y1], 48, fill=(10, 12, 28, 215), outline=(255, 255, 255, 70), width=3)
    d.line([(x0 + 60, y0 + 2), (x1 - 60, y0 + 2)], fill=c1 + (220,), width=4)
    paste_icon(im, kind, 720, 790, 330, c1, c2)
    d = ImageDraw.Draw(im, "RGBA")
    for i, b in enumerate(bullets):
        y = 1010 + i * 70
        d.ellipse([470, y - 12, 494, y + 12], fill=c1 + (255,))
        f = S13.fit(FS, b, 34, 470)
        d.text((512, y), b, font=f, fill=(255, 255, 255, 240), anchor="lm")
    chip(im, cta, 690, 1400, 36, c1, INK if sum(c1) > 450 else WH)
    draw_character(im, 1.6, 1.6, "point", (520, 900))
    im.save(os.path.join(OUT, f"Story_{name}.png"))
    return im

covers, stories = [], []
for name, kind, c1, c2, head, bullets, cta in HL:
    covers.append(cover(name, kind, c1, c2)); stories.append(story(name, kind, c1, c2, head, bullets, cta))
sheet = Image.new("RGB", (5 * 300, 300 + 534), (20, 20, 30))
for i, (c, s) in enumerate(zip(covers, stories)):
    cc = c.resize((300, 300)); m = Image.new("L", (300, 300), 0); ImageDraw.Draw(m).ellipse([20, 20, 280, 280], fill=255)
    sheet.paste(cc, (i * 300, 0), m); sheet.paste(s.resize((300, 534)), (i * 300, 300))
sheet.save(os.path.join(HERE, "hl_sheet.png"))
print("ok")
