import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
from scenes13 import gtext, atext, chip, FX, FS, LIME, RD, WH, INK, ORG, CY
from scenes14 import stamp
from reel2 import draw_character
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
a = np.array(S13.aurora(2.0, LIME, (20, 120, 60)), np.float32)
b = np.array(S13.aurora(5.0, RD, (140, 20, 40)), np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
m = np.clip(((xx - W / 2) + (yy - H / 2) * 0.35) / 60 + 0.5, 0, 1)[..., None]
im = Image.fromarray((a * (1 - m) + b * m).astype(np.uint8))
im.paste(S13.OVER, (0, 0), S13.OVER)
d = ImageDraw.Draw(im, "RGBA")
# glowing split line
p0 = (W / 2 + (H / 2) * 0.35, 0); p1 = (W / 2 - (H / 2) * 0.35, H)
gl = Image.new("L", (W, H), 0); ImageDraw.Draw(gl).line([p0, p1], fill=255, width=26)
im.paste((255, 255, 255), (0, 0), gl.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7)))
d = ImageDraw.Draw(im, "RGBA"); d.line([p0, p1], fill=(255, 255, 255, 255), width=6)
# top text
chip(im, "GTA 6", 540, 330, 50, WH, INK)
gtext(im, "ZU REAL?", 540, 520, S13.fit(FX, "ZU REAL?", 250, 960), (255, 255, 255), (255, 230, 120))
# vs pills
def pill(txt, cx, cy, col, fg, rot, mark):
    f = FX(92); w = int(f.getlength(txt)) + 200; h = 170
    L = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.rounded_rectangle([20, 20, w + 20, h + 20], 85, fill=col + (255,), outline=(255, 255, 255, 255), width=8)
    dl.text((w / 2 + 20 - 40, h / 2 + 20), txt, font=f, fill=fg, anchor="mm")
    mx = w - 45
    if mark == "ok": dl.line([(mx - 30, h / 2 + 20), (mx - 8, h / 2 + 46), (mx + 32, h / 2 - 8)], fill=fg, width=16)
    else:
        dl.line([(mx - 26, h / 2 - 6), (mx + 26, h / 2 + 46)], fill=fg, width=16); dl.line([(mx + 26, h / 2 - 6), (mx - 26, h / 2 + 46)], fill=fg, width=16)
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", L.size, (0, 0, 0, 0)); sh.putalpha(L.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.6)))
    im.paste(sh, (int(cx - L.width / 2 + 10), int(cy - L.height / 2 + 18)), sh)
    im.paste(L, (int(cx - L.width / 2), int(cy - L.height / 2)), L)
pill("GENIAL", 430, 740, LIME, INK, 6, "ok")
pill("NERVIG", 740, 1060, RD, WH, -6, "x")
# VS burst
d = ImageDraw.Draw(im, "RGBA"); cx, cy = 620, 905; pts = []
for k in range(24):
    ang = k * math.pi / 12; r = 120 if k % 2 == 0 else 78
    pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
d.polygon(pts, fill=(255, 215, 60, 255), outline=(20, 20, 30, 255), width=6)
d.text((cx, cy), "VS", font=FX(80), fill=INK, anchor="mm")
# fact chips
for txt, x, y, col, rot in (("$0 BEIM TOD", 860, 1300, (20, 20, 30), -5), ("TANK LEER", 820, 1420, (20, 20, 30), 4), ("POLIZEI MERKT SICH ALLES", 760, 1540, (20, 20, 30), -3)):
    f = FX(40); w = int(f.getlength(txt)) + 60
    L = Image.new("RGBA", (w, 80), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.rounded_rectangle([0, 0, w - 1, 79], 40, fill=col + (235,), outline=(255, 255, 255, 200), width=4)
    dl.text((w / 2, 40), txt, font=f, fill=WH, anchor="mm")
    L = L.rotate(rot, expand=True, resample=Image.BICUBIC)
    im.paste(L, (int(x - L.width / 2), int(y - L.height / 2)), L)
draw_character(im, 1.3, 1.3, "point", (600, 905))
out = os.path.join(HERE, "ZOCKWISSEN_Reels_v2/34_Zu_realistisch/34_Zu_realistisch_THUMBNAIL.png")
im.save(out)
# check sheet: full + 3:4 grid crop
chk = Image.new("RGB", (540 + 540, 960), (30, 30, 30))
chk.paste(im.resize((540, 960)), (0, 0)); chk.paste(im.crop((0, 240, 1080, 1680)).resize((540, 720)), (540, 120))
chk.save(os.path.join(HERE, "thumb_chk.png")); print(out)
