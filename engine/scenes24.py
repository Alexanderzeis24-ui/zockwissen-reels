"""Reel 39 – 3D-Look: kleine 3D-Engine (Meshes, Licht, Kamerafahrt, Bühnenspiegelung) + Figur auf der Bühne."""
import sys, os, math, random, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
import scenes7 as S7
import scenes2 as S2
import scenes12
from scenes13 import FX, FS, ease, back, W, H
from reel2 import draw_character
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

VID = "39_Verrueckte_Fakten_3D"
S7.SCRIPTS7[VID] = [
    "Diese fünf G T A sechs Fakten sind komplett verrückt! Folg mir, damit du nichts verpasst!",
    "Eins: Das Spiel ist seit über zehn Jahren in Entwicklung.",
    "Zwei: Es kostet laut Schätzungen über eine Milliarde Dollar. Mehr als jeder Film.",
    "Drei: Der erste Trailer baut echte virale Videos aus Florida nach.",
    "Vier: Der zweite Trailer hatte vierhundertfünfundsiebzig Millionen Aufrufe an einem Tag.",
    "Fünf: Schon G T A fünf hat sich über zweihundertfünfundzwanzig Millionen Mal verkauft.",
    "Welcher Fakt hat dich geschockt? Schreib die Zahl! Und merk dir:",
]
S7.DISPLAY.update({"zehn": "10", "vierhundertfünfundsiebzig": "475", "zweihundertfünfundzwanzig": "225"})
S7.COMMENT[VID] = ("WELCHER FAKT?", "Eine Milliarde?!")
S7.COVER[VID] = ("GTA 6", "VERRÜCKT")
LIME = (190, 255, 70); CY = (60, 220, 255); MAG = (255, 70, 190); GOLD = (255, 196, 50); RED = (255, 70, 90); VIO = (140, 100, 255); WH = (255, 255, 255); INK = (14, 16, 30)
HEAD = [("5 VERRÜCKTE", "GTA 6 FAKTEN"), ("ÜBER 10 JAHRE", "ENTWICKLUNG"), ("ÜBER 1 MRD $", "TEURER ALS FILME"), ("ECHTE VIRALE", "FLORIDA-VIDEOS"),
        ("475 MIO", "AN EINEM TAG"), ("GTA 5", "225 MIO VERKAUFT"), ("WELCHER FAKT", "SCHOCKT DICH?")]
ACC = [(MAG, VIO), (CY, VIO), (GOLD, (255, 140, 40)), (MAG, CY), (RED, MAG), (LIME, CY), (LIME, MAG)]
SRC = [None, "Laut Berichten (Bloomberg)", "Schätzung von Analysten", "Quelle: Trailer 1 / Medien", "Quelle: Rockstar Games", "Quelle: Take-Two", None]

# ---------------- 3D core ----------------
def rot(ax, ay, az=0.0):
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]); Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Ry @ Rx @ Rz

def box(sx, sy, sz):
    x, y, z = sx / 2, sy / 2, sz / 2
    V = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]], float)
    F = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [3, 7, 6, 2], [0, 4, 7, 3], [1, 2, 6, 5]]
    return V, F

def cyl(r, h, n=28, r2=None):
    r2 = r if r2 is None else r2
    V = [[r * math.cos(2 * math.pi * k / n), -h / 2, r * math.sin(2 * math.pi * k / n)] for k in range(n)] + [[r2 * math.cos(2 * math.pi * k / n), h / 2, r2 * math.sin(2 * math.pi * k / n)] for k in range(n)]
    F = [[k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
    F.append(list(range(n))[::-1]); F.append([n + k for k in range(n)])
    return np.array(V, float), F

def prism(poly, d):
    n = len(poly)
    V = [[x, y, -d / 2] for x, y in poly] + [[x, y, d / 2] for x, y in poly]
    F = [list(range(n)), [n + k for k in range(n)][::-1]] + [[k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
    return np.array(V, float), F

class Cam:
    def __init__(self, pos, look, f=1500):
        self.p = np.array(pos, float); fwd = np.array(look, float) - self.p; fwd /= np.linalg.norm(fwd)
        right = np.cross([0, 1, 0], fwd); right /= np.linalg.norm(right); up = np.cross(fwd, right)
        self.R = np.stack([right, up, fwd]); self.f = f
    def view(self, P): return (np.asarray(P) - self.p) @ self.R.T
    def proj(self, Pc): return np.stack([540 + self.f * Pc[..., 0] / Pc[..., 2], 960 - self.f * Pc[..., 1] / Pc[..., 2]], -1)

LIGHT = np.array([-0.5, 0.8, -0.6]); LIGHT /= np.linalg.norm(LIGHT)

def add_mesh(faces_out, cam, V, F, col, R=None, T=(0, 0, 0), mirror=False, emissive=0.0):
    Vw = V @ (R.T if R is not None else np.eye(3)) + np.array(T, float)
    if mirror: Vw = Vw * np.array([1, -1, 1])
    Vc = cam.view(Vw)
    for face in F:
        P = Vw[face]; Pc = Vc[face]
        if np.any(Pc[:, 2] < 0.2): continue
        n = np.cross(P[1] - P[0], P[2] - P[0]); nn = np.linalg.norm(n)
        if nn < 1e-9: continue
        n = n / nn
        if mirror: n = -n
        c = P.mean(0)
        if np.dot(n, cam.p - c) <= 0: continue
        dif = max(0.0, float(np.dot(n, LIGHT)))
        vdir = (cam.p - c); vdir /= np.linalg.norm(vdir); hvec = LIGHT + vdir; hvec /= np.linalg.norm(hvec)
        spec = max(0.0, float(np.dot(n, hvec))) ** 24
        k = 0.32 + 0.75 * dif + emissive
        rgb = tuple(int(min(255, col[i] * k + 255 * spec * 0.55)) for i in range(3))
        faces_out.append((float(Pc[:, 2].mean()), [tuple(p) for p in cam.proj(Pc)], rgb))

def draw_faces(im, faces, alpha=255):
    d = ImageDraw.Draw(im, "RGBA")
    for z, pts, rgb in sorted(faces, key=lambda f: -f[0]):
        d.polygon(pts, fill=rgb + (alpha,))
        d.line(pts + [pts[0]], fill=tuple(min(255, int(c * 1.15)) for c in rgb) + (int(alpha * 0.35),), width=1)

# ---------------- environment ----------------
def _sky():
    y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    a = np.array([8, 6, 26], np.float32); b = np.array([40, 16, 70], np.float32); c = np.array([10, 8, 22], np.float32)
    col = np.where(y < 0.55, a * (1 - y / 0.55) + b * (y / 0.55), b * (1 - (y - 0.55) / 0.45) + c * ((y - 0.55) / 0.45))
    return Image.fromarray(np.repeat(col, W, 1).astype(np.uint8))
SKY = _sky()

def environment(cam, gt, acc):
    im = SKY.copy(); d = ImageDraw.Draw(im, "RGBA")
    # floor plane
    corners = np.array([[-30, 0, -6], [30, 0, -6], [30, 0, 40], [-30, 0, 40]], float)
    Pc = cam.view(corners)
    if np.all(Pc[:, 2] > 0.1): d.polygon([tuple(p) for p in cam.proj(Pc)], fill=(12, 10, 28, 255))
    # grid
    for x in range(-14, 15):
        A = cam.view(np.array([[x, 0, -3], [x, 0, 30]], float))
        if A[0, 2] > 0.3:
            pp = cam.proj(A); d.line([tuple(pp[0]), tuple(pp[1])], fill=acc[1] + (50,), width=2)
    off = (gt * 1.5) % 1
    for zz in range(-3, 30):
        z = zz + off
        A = cam.view(np.array([[-14, 0, z], [14, 0, z]], float))
        if A[0, 2] > 0.3 and A[1, 2] > 0.3:
            pp = cam.proj(A); d.line([tuple(pp[0]), tuple(pp[1])], fill=acc[1] + (int(70 * max(0.15, 1 - z / 30)),), width=2)
    # stage ring
    for r, a_ in ((2.3, 200), (2.6, 90)):
        pts = cam.view(np.array([[r * math.cos(k / 48 * 2 * math.pi) + 0.9, 0.01, r * math.sin(k / 48 * 2 * math.pi)] for k in range(49)]))
        if np.all(pts[:, 2] > 0.2): d.line([tuple(p) for p in cam.proj(pts)], fill=acc[0] + (a_,), width=4)
    # back light beams
    for k in range(3):
        bx = 540 + (k - 1) * 360 + 60 * math.sin(gt * 0.6 + k)
        poly = [(bx - 30, 0), (bx + 30, 0), (bx + 260, 1300), (bx - 260, 1300)]
        m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=26)
        im.paste(acc[0], (0, 0), m.filter(ImageFilter.GaussianBlur(30)))
    return im

# ---------------- objects per scene ----------------
def pedestal(faces, cam, acc, mirror=False):
    V, F = cyl(1.1, 0.5, 36); add_mesh(faces, cam, V, F, (40, 44, 70), T=(0.9, 0.25, 0), mirror=mirror)
    V, F = cyl(1.12, 0.06, 36); add_mesh(faces, cam, V, F, acc[0], T=(0.9, 0.52, 0), mirror=mirror, emissive=0.6)

def obj_hook(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    R = rot(0.25, t * 1.6); h = back(t / 0.5)
    if h < 0.05: return
    V, F = box(0.5, 1.6, 0.5); add_mesh(faces, cam, V * h, F, RED, R, (0.9, 0.55 + 1.5 * h, 0), mirror)
    V, F = box(0.5, 0.5, 0.5); add_mesh(faces, cam, V * h, F, RED, R, (0.9, 0.55 + 0.35 * h, 0), mirror)

def obj_hourglass(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    R = rot(0.15 * math.sin(t), t * 1.2 + math.pi * ease((t % 2.2 - 1.6) / 0.5)); s = back(t / 0.5)
    if s < 0.05: return
    for y, (rb, rt) in ((0.55, (0.75, 0.1)), (1.35, (0.1, 0.75))):
        V, F = cyl(rb, 0.8, 24, rt); add_mesh(faces, cam, V * s, F, CY, R, (0.9, 0.55 + y * s + 0.4 * s, 0), mirror)
    for y in (0.55, 2.15):
        V, F = cyl(0.85, 0.12, 24); add_mesh(faces, cam, V * s, F, GOLD, R, (0.9, 0.55 + y * s, 0), mirror)

def obj_money(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    n = min(9, int(t * 6) + 1)
    for i in range(n):
        lay, k = divmod(i, 3); s = back((t - i * 0.12) / 0.3)
        if s < 0.05: continue
        V, F = box(0.62, 0.26, 0.32); R = rot(0, 0.3 + (lay % 2) * 0.2)
        add_mesh(faces, cam, V * s, F, GOLD, R, (0.25 + k * 0.66, 0.68 + lay * 0.27, 0), mirror)
    for j in range(3):
        a = t * 1.5 + j * 2.1; V, F = cyl(0.32, 0.07, 24)
        add_mesh(faces, cam, V, F, (255, 210, 80), rot(math.pi / 2, a * 2), (0.9 + 1.5 * math.cos(a), 2.3 + 0.25 * math.sin(a * 2), 1.5 * math.sin(a)), mirror)

def obj_phone(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    s = back(t / 0.5)
    if s < 0.05: return
    R = rot(-0.1, -0.5 + 0.5 * math.sin(t * 1.3))
    V, F = box(1.2, 2.2, 0.14); add_mesh(faces, cam, V * s, F, (30, 32, 46), R, (0.9, 0.6 + 1.15 * s, 0), mirror)
    V, F = box(1.04, 1.95, 0.02); add_mesh(faces, cam, V * s, F, MAG, R, (0.9, 0.6 + 1.15 * s, 0) + R @ np.array([0, 0, -0.08]) * s, mirror, emissive=0.5)
    tri = [(-0.22, -0.28), (0.3, 0.0), (-0.22, 0.28)]
    V, F = prism(tri, 0.12); add_mesh(faces, cam, V * s, F, WH, R, (0.9, 0.6 + 1.15 * s, 0) + R @ np.array([0, 0, -0.16]) * s, mirror, emissive=0.4)

def obj_views(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    hts = [0.4, 0.6, 0.9, 1.3, 2.4]
    for i, h in enumerate(hts):
        p = ease((t - 0.1 - i * 0.12) / 0.5); hh = max(0.02, h * p)
        V, F = box(0.32, hh, 0.32)
        add_mesh(faces, cam, V, F, RED if i == 4 else MAG, rot(0, 0.4), (0.25 + i * 0.33, 0.55 + hh / 2, 0.1), mirror, emissive=0.15 if i == 4 else 0)

def obj_stack(faces, cam, t, acc, mirror):
    pedestal(faces, cam, acc, mirror)
    for i in range(7):
        s = back((t - i * 0.1) / 0.3)
        if s < 0.05: continue
        V, F = box(1.0, 0.18, 1.35); a = 0.3 * math.sin(i * 1.7) + t * 0.3
        drop = (1 - ease((t - i * 0.1) / 0.3)) * 2
        add_mesh(faces, cam, V * s, F, LIME if i % 2 else (90, 200, 120), rot(0, a), (0.9, 0.64 + i * 0.19 + drop, 0), mirror)

def obj_end(faces, cam, t, acc, mirror):
    act = int(t * 2.4) % 5
    for i in range(5):
        s = back((t - i * 0.08) / 0.3)
        if s < 0.05: continue
        V, F = box(0.62, 0.62, 0.62); up = 0.35 if i == act else 0
        add_mesh(faces, cam, V * s, F, LIME if i == act else (70, 76, 120), rot(0.2, 0.5 + t * 0.6 + i), (-1.0 + i * 0.95, 0.4 + up, 0), mirror)

OBJ = [obj_hook, obj_hourglass, obj_money, obj_phone, obj_views, obj_stack, obj_end]
FOCUS = (0.9, 1.6, 0)

# ---------------- 2D overlay helpers ----------------
@functools.lru_cache(maxsize=64)
def text3d(txt, size, c1, c2, depth=14):
    f = FX(size); l, t_, r, b = f.getbbox(txt); w, h = r - l, b - t_
    P = 20 + depth
    m = Image.new("L", (w + 2 * P, h + 2 * P), 0); ImageDraw.Draw(m).text((P - l, P - t_), txt, font=f, fill=255)
    out = Image.new("RGBA", m.size, (0, 0, 0, 0))
    for k in range(depth, 0, -1):
        sh = tuple(int(c * (0.18 + 0.25 * (1 - k / depth))) for c in c2)
        out.paste(sh + (255,), (k, k), m)
    kk = np.linspace(0, 1, m.height, dtype=np.float32)[:, None, None]
    g = (np.array(WH, np.float32) * (1 - kk) * 0.35 + np.array(c1, np.float32) * (0.65 + 0.35 * kk)).clip(0, 255).astype(np.uint8)
    front = Image.fromarray(np.repeat(g, m.width, 1))
    out.paste(front, (0, 0), m)
    hl = m.filter(ImageFilter.FIND_EDGES).point(lambda v: int(v * 0.6))
    out.paste((255, 255, 255, 255), (0, 0), hl)
    return out

def put(im, img, cx, cy, s=1.0, left=None):
    if s < 0.05: return
    if s != 1.0: img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.BILINEAR)
    x = int(left - 20) if left is not None else int(cx - img.width / 2)
    im.paste(img, (x, int(cy - img.height / 2)), img)

def follow3d(im, ot):
    done = ot > 1.9
    b = back(ot / 0.3) * (1 + (0.05 * math.sin(ot * 10) if not done else 0))
    if b < 0.12: return
    btn = text3d("+ FOLGEN" if not done else "✓ GEFOLGT", 62, LIME if not done else (150, 160, 190), (40, 120, 40) if not done else (60, 60, 90), 10)
    pad = Image.new("RGBA", (btn.width + 80, btn.height + 30), (0, 0, 0, 0)); dp = ImageDraw.Draw(pad)
    for k in range(10, 0, -1): dp.rounded_rectangle([k, k + 6, pad.width - 12 + k, pad.height - 6 + k], 40, fill=(10, 30, 14, 255))
    dp.rounded_rectangle([0, 6, pad.width - 12, pad.height - 6], 40, fill=(20, 24, 40, 255), outline=(LIME if not done else (120, 130, 160)) + (255,), width=5)
    pad.paste(btn, (30, 8), btn)
    put(im, pad, 540, 1150, b)
    p = ease((ot - 0.7) / 0.6)
    if p > 0:
        d = ImageDraw.Draw(im, "RGBA"); fx, fy = 860 - 150 * p, 1330 - 160 * p
        d.ellipse([fx - 28, fy - 28, fx + 28, fy + 28], fill=(236, 190, 150, 255), outline=(255, 255, 255, 255), width=4)
        if 1.6 < ot < 1.9: d.ellipse([fx - 52, fy - 52, fx + 52, fy + 52], outline=(255, 255, 255, 170), width=4)

def mascot3d(im, cam, t, gt, target):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_character(layer, t, gt, "point", target)
    bb = layer.getbbox()
    if not bb: return
    spr = layer.crop(bb)
    foot = cam.proj(cam.view(np.array([[-0.95, 0, -0.5]])))[0]
    headp = cam.proj(cam.view(np.array([[-0.95, 2.7, -0.5]])))[0]
    hpx = foot[1] - headp[1]; s = hpx / spr.height
    spr = spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.LANCZOS)
    # shadow + reflection
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([foot[0] - spr.width * 0.35, foot[1] - 18, foot[0] + spr.width * 0.35, foot[1] + 18], fill=(0, 0, 0, 120))
    refl = spr.transpose(Image.FLIP_TOP_BOTTOM); gr = Image.linear_gradient('L').resize(refl.size).point(lambda v: int((255 - v) * 0.22)); a = ImageChops.multiply(refl.split()[3], gr.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_TOP_BOTTOM)); refl.putalpha(a)
    im.paste(refl, (int(foot[0] - spr.width / 2), int(foot[1])), refl)
    # rim light
    rim = Image.new("RGBA", spr.size, (0, 0, 0, 0)); al = spr.split()[3]
    edge = ImageChops.subtract(al, al.filter(ImageFilter.MinFilter(5)).transform(al.size, Image.AFFINE, (1, 0, -4, 0, 1, 0)))
    rim.paste((120, 220, 255, 255), (0, 0), edge.point(lambda v: int(v * 0.8)))
    im.paste(spr, (int(foot[0] - spr.width / 2), int(foot[1] - spr.height)), spr)
    im.paste(rim, (int(foot[0] - spr.width / 2), int(foot[1] - spr.height)), rim)

def captions(im, words, gt):
    groups = []; cur = []
    for i, (a, b, w) in enumerate(words):
        cur.append(i)
        if len(cur) == 2 or w[-1] in ".!?:": groups.append(cur); cur = []
    if cur: groups.append(cur)
    act = None
    for i, (a, b, w) in enumerate(words):
        if a <= gt < b + 0.05: act = i
    if act is None:
        prev = [i for i, (a, b, w) in enumerate(words) if b <= gt]
        if not prev or gt - words[prev[-1]][1] > 0.35: return
        act = prev[-1]
    g = next(g for g in groups if act in g)
    d = ImageDraw.Draw(im); f = FX(84)
    txts = [words[i][2] for i in g]; ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 28 * (len(ws) - 1)
    if tot > 960: f = FX(int(84 * 960 / tot)); ws = [d.textlength(x, font=f) for x in txts]; tot = sum(ws) + 28 * (len(ws) - 1)
    x = 540 - tot / 2
    for i, tx, w in zip(g, txts, ws):
        on = i == act
        d.text((x + w / 2 + 6, 1462 + 6), tx, font=f, fill=(0, 0, 0), anchor="mm")
        d.text((x + w / 2, 1462), tx, font=f, fill=LIME if on else WH, anchor="mm", stroke_width=6, stroke_fill=(10, 10, 20))
        x += w + 28

def bloom(im):
    sm = im.resize((W // 4, H // 4), Image.BILINEAR).point(lambda v: max(0, v - 150) * 2).filter(ImageFilter.GaussianBlur(8)).resize((W, H), Image.BILINEAR)
    return ImageChops.screen(im, sm)

def frame24(vid, idx, t, T, words, cover=False, no_sticker=False):
    R = S2.R[vid]; dur = R[idx][0]; n = len(R)
    gt = sum(s[0] for s in R[:idx]) + t
    acc = ACC[idx]
    yaw = 0.22 * math.sin(gt * 0.25) + 0.2
    cpos = (0.2 + 7.4 * math.sin(yaw), 2.6 + 0.3 * math.sin(gt * 0.4), -7.4 * math.cos(yaw))
    dolly = 1 - 0.12 * ease(t / dur) + (0.25 * (1 - ease(t / 0.45)) if idx > 0 and not cover else 0)
    cpos = (cpos[0] * dolly, cpos[1], cpos[2] * dolly)
    cam = Cam(cpos, (0.1, 1.7, 0), 1500)
    im = environment(cam, gt, acc)
    tt = t + (0.5 if idx == 0 else 0) + (2.0 if cover else 0)
    refl = []; OBJ[idx](refl, cam, tt, acc, True)
    if refl:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); draw_faces(lay, refl)
        a = lay.split()[3].point(lambda v: int(v * 0.25)); lay.putalpha(a); im.paste(lay, (0, 0), lay)
    faces = []; OBJ[idx](faces, cam, tt, acc, False); draw_faces(im, faces)
    fp = cam.proj(cam.view(np.array([FOCUS])))[0]
    target = (float(fp[0]), float(fp[1]))
    if idx == 0 and not cover and t > dur * 0.5: target = (540, 1150)
    mascot3d(im, cam, t if not cover else 2.0, gt, target)
    im = bloom(im)
    # headline 3D
    l1, l2 = HEAD[idx]
    a1 = ease(tt / 0.3); a2 = back((tt - 0.15) / 0.4)
    put(im, text3d(l1, S13.fit(FX, l1, 70, 900).size, WH, acc[1], 8), 0, 300 + (1 - a1) * 40, 1.0 if a1 > 0.05 else 0, left=64)
    if a2 > 0.05: put(im, text3d(l2, S13.fit(FX, l2, 116, 920).size, acc[0], acc[1], 16), 0, 420, min(1.0, a2), left=64)
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse([64, 163, 84, 183], fill=LIME + (255,)); d.text((96, 173), "ZOCKWISSEN", font=FS(30), fill=(255, 255, 255, 230), anchor="lm")
    d.text((1016, 173), "3D FAKTEN" if idx == 0 else (f"FAKT {idx}/5" if idx < n - 1 else "DEINE MEINUNG"), font=FS(30), fill=(255, 255, 255, 230), anchor="rm")
    if idx == n - 1 and t > 0.8 and not cover:
        ot = t - 0.8; s = ease(ot / 0.3); off = (1 - back(ot / 0.4)) * 80
        d.rounded_rectangle([250, 560 + off, 830, 740 + off], 36, fill=(14, 16, 28, int(230 * s)), outline=(255, 255, 255, int(90 * s)), width=3)
        d.ellipse([280, 590 + off, 344, 654 + off], fill=(60, 160, 95, int(255 * s)))
        ans = S7.COMMENT[VID][1]; nn = int(len(ans) * ease((ot - 0.4) / 1.0))
        d.text((364, 604 + off), "du", font=FS(28), fill=(170, 174, 200, int(255 * s)), anchor="lm")
        d.text((364, 660 + off), ans[:nn], font=FX(40), fill=(255, 255, 255, int(255 * s)), anchor="lm")
        if ot > 1.6: scenes12.heart(ImageDraw.Draw(im), 790, 715 + off, back((ot - 1.6) / 0.3), RED)
    if not cover:
        if idx == 0 and t > dur * 0.5: follow3d(im, t - dur * 0.5)
        if SRC[idx]:
            sa = ease((t - 0.5) / 0.3)
            if sa > 0.02:
                d = ImageDraw.Draw(im, "RGBA"); fs = FS(26); w_ = d.textlength(SRC[idx], font=fs)
                d.rounded_rectangle([700 - w_ / 2 - 24, 1290, 700 + w_ / 2 + 24, 1336], 23, fill=(0, 0, 0, int(160 * sa)), outline=(255, 255, 255, int(70 * sa)), width=2)
                d.text((700, 1313), SRC[idx], font=fs, fill=(255, 255, 255, int(225 * sa)), anchor="mm")
        captions(im, words, gt)
        d = ImageDraw.Draw(im, "RGBA"); sw = (W - 120 - (n - 1) * 10) / n
        for i in range(n):
            x0 = 60 + i * (sw + 10); d.rounded_rectangle([x0, 118, x0 + sw, 128], 5, fill=(255, 255, 255, 60))
            f_ = 1 if i < idx else (t / dur if i == idx else 0)
            if f_ > 0.03: d.rounded_rectangle([x0, 118, x0 + sw * f_, 128], 5, fill=(255, 255, 255, 240))
        if idx == 0 and t < 0.2: im = Image.blend(im, Image.new("RGB", (W, H), acc[0]), 0.5 * (1 - t / 0.2))
        if idx == n - 1 and t > dur - 0.2: im = Image.blend(im, Image.new("RGB", (W, H), ACC[0][0]), 0.5 * (t - (dur - 0.2)) / 0.2)
    else:
        put(im, text3d("VERRÜCKT!", 120, LIME, (40, 120, 40), 16), 540, 1400, 1)
    return im

_oldf, _oldd, _oldc = S7.frame, S7.defs, S7.make_cover
def _frame(vid, *a, **k): return frame24(vid, *a, **k) if vid == VID else _oldf(vid, *a, **k)
def _defs(vid, durs):
    if vid != VID: return _oldd(vid, durs)
    return [(durs[i], "night", None, [(0, "", None)], "point") for i in range(len(S7.SCRIPTS7[VID]))]
def _cover(vid, path):
    if vid != VID: return _oldc(vid, path)
    T = S7.setup(vid); frame24(vid, 0, 1.0, T, [], cover=True).save(path)
S7.frame, S7.defs, S7.make_cover = _frame, _defs, _cover

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.75, 0.8, 0.7, 0.8, 0.85, 0.85]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.8, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 2, 0.4, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p24_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
