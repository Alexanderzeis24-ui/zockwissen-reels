"""Visual upgrade layer: soft shadows, glossy cards, cinematic backgrounds, camera moves, sticker shine, grain."""
import functools, random, math, os, sys, subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import reel2, scenes2, scenes3, scenes4, scenes5
import scenes2 as S2
from reel2 import W, H, FPS, ease, back, sh, lerp, THEMES, INK, YEL, PINK, sticker, draw_character, outro, particles as _p

MODS = [reel2, scenes2, scenes3, scenes4, scenes5]

# ---------- soft shadow sprites ----------
@functools.lru_cache(maxsize=256)
def shadow_sprite(w, h, r, blur=22):
    pad = blur * 3
    m = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(m).rounded_rectangle([pad, pad, pad + w, pad + h], r, fill=150)
    return m.filter(ImageFilter.GaussianBlur(blur)), pad

_CUR = {"im": None}

def card(d, b, fill=(255, 255, 255), r=40, sh_off=14):
    x0, y0, x1, y1 = [int(v) for v in b]
    w, h = max(2, x1 - x0), max(2, y1 - y0)
    im = _CUR["im"]
    if im is not None and w > 20 and h > 20:
        q = 8
        m, pad = shadow_sprite((w // q) * q + q, (h // q) * q + q, int(r))
        im.paste((10, 6, 24), (x0 - pad + 6, y0 - pad + 22), m)
    d.rounded_rectangle([x0, y0, x1, y1], int(r), fill=fill, outline=sh(fill, 0.55), width=4)
    # gloss: lighter top band + inner highlight
    gh = int(h * 0.42)
    if gh > 12:
        d.rounded_rectangle([x0 + 6, y0 + 6, x1 - 6, y0 + gh], max(4, int(r) - 6), fill=sh(fill, 1.08))
        d.rectangle([x0 + 6, y0 + gh - 12, x1 - 6, y0 + gh], fill=sh(fill, 1.08))
        d.rounded_rectangle([x0 + 6, y0 + gh, x1 - 6, y1 - 6], max(4, int(r) - 6), fill=fill)
    d.line([(x0 + r * 0.8, y0 + 7), (x1 - r * 0.8, y0 + 7)], fill=sh(fill, 1.25), width=3)

for m in MODS: m.card = card

# ---------- cinematic backgrounds ----------
_bg = {}
def bg(theme):
    if theme in _bg: return _bg[theme]
    a, b, floor = THEMES[theme]
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(x + (z - x) * t) for x, z in zip(a, b)))
    # light source glow
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
    gd.ellipse([520, -300, 1400, 700], fill=150)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    im.paste(sh(b, 1.45), (0, 0), glow)
    # bokeh
    bk = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(bk)
    rnd = random.Random(hash(theme) % 1000)
    for _ in range(14):
        x, y, r = rnd.randrange(W), rnd.randrange(1400), rnd.randrange(30, 110)
        bd.ellipse([x - r, y - r, x + r, y + r], fill=rnd.randrange(25, 60))
    bk = bk.filter(ImageFilter.GaussianBlur(10))
    im.paste((255, 255, 255), (0, 0), bk)
    # floor with gradient and horizon glow
    fd = ImageDraw.Draw(im)
    for y in range(1490, H):
        t = (y - 1490) / (H - 1490)
        fd.line([(0, y), (W, y)], fill=sh(floor, 1.1 - 0.45 * t))
    hz = Image.new("L", (W, 120), 0); ImageDraw.Draw(hz).rectangle([0, 50, W, 70], fill=200)
    hz = hz.filter(ImageFilter.GaussianBlur(14))
    im.paste(sh(b, 1.5), (0, 1440), hz)
    for x in range(-400, W + 400, 140):
        fd.line([(540 + (x - 540) * 0.35, 1500), (x, H)], fill=sh(floor, 0.85), width=2)
    # vignette
    vg = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vg)
    vd.rectangle([0, 0, W, H], fill=140); vd.ellipse([-260, -120, W + 260, H + 160], fill=0)
    vg = vg.filter(ImageFilter.GaussianBlur(140))
    im.paste((0, 0, 0), (0, 0), vg)
    _bg[theme] = im
    return im

@functools.lru_cache(maxsize=8)
def glow_dot(r):
    m = Image.new("L", (r * 6, r * 6), 0)
    ImageDraw.Draw(m).ellipse([r * 2, r * 2, r * 4, r * 4], fill=255)
    return m.filter(ImageFilter.GaussianBlur(r * 0.9))

def particles(fr, gt, theme):
    rnd = random.Random(42)
    for i in range(18):
        x = (rnd.randrange(W) + math.sin(gt * 0.6 + i) * 30) % W
        y = (rnd.randrange(1500) - gt * rnd.uniform(20, 50)) % 1480
        r = rnd.choice([6, 8, 10])
        m = glow_dot(r)
        tw = 0.55 + 0.45 * math.sin(gt * 3 + i)
        fr.paste((255, 250, 230), (int(x - r * 3), int(y - r * 3)), m.point(lambda v, k=tw: int(v * k)))

# ---------- grain ----------
_grain = []
def grain(i):
    if not _grain:
        rnd = random.Random(5)
        for k in range(4):
            g = Image.effect_noise((W // 2, H // 2), 40).resize((W, H))
            _grain.append(g.point(lambda v: max(0, min(255, int((v - 128) * 0.35 + 128)))))
    return _grain[i % 4]

# ---------- sticker shine ----------
def shine(st, p):
    if p <= 0 or p >= 1: return st
    w, h = st.size
    band = Image.new("L", (w, h), 0); bd = ImageDraw.Draw(band)
    x = -h + (w + 2 * h) * p
    bd.polygon([(x, 0), (x + 70, 0), (x + 70 - h, h), (x - h, h)], fill=170)
    band = ImageChops.multiply(band, st.split()[3])
    out = st.copy(); out.paste((255, 255, 255), (0, 0), band)
    return out

# ---------- frame ----------
def frame(vid, idx, t):
    dur, theme, fn, words, pose0 = S2.R[vid][idx]
    gt = sum(s[0] for s in S2.R[vid][:idx]) + t
    fr = bg(theme).copy(); _CUR["im"] = fr
    particles(fr, gt, theme)
    d = ImageDraw.Draw(fr)
    target = fn(fr, d, t, dur)
    last = idx == len(S2.R[vid]) - 1
    cur = [w for w in words if w[0] <= t][-1]
    ot = (t - cur[0]) if (last and cur[1] == "FOLGT FÜR MEHR") else None
    if ot is not None: target = outro(d, fr, ot)
    pose = pose0
    if pose0 == "wave" and t > 1.6: pose = "point"
    if pose0 == "cheer" and ot is not None: pose = "point"
    draw_character(fr, t, gt, pose, target)
    st = sticker(cur[1], cur[2]); lt = t - cur[0]
    s = back(lt / 0.25)
    if s > 0.03:
        st2 = shine(st, (lt - 0.3) / 0.5)
        ang = -3 + 4 * (1 - ease(lt / 0.35)) + math.sin(gt * 2) * 1.2
        r = st2.resize((max(1, int(st2.width * s)), max(1, int(st2.height * s))), Image.BILINEAR).rotate(ang, expand=True, resample=Image.BICUBIC)
        # soft shadow under sticker
        m = r.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.5))
        fr.paste((0, 0, 0), (int(W / 2 - r.width / 2) + 8, int(380 - r.height / 2) + 18), m)
        fr.paste(r, (int(W / 2 - r.width / 2), int(380 - r.height / 2)), r)
    _CUR["im"] = None
    # camera: slow push-in + impact shake at scene start
    z = 1.0 + 0.035 * ease(t / dur)
    sx = math.sin(t * 60) * 10 * max(0, 1 - t / 0.25) if idx > 0 else 0
    if z > 1.001 or sx:
        zw, zh = int(W * z), int(H * z)
        big = fr.resize((zw, zh), Image.BILINEAR)
        ox = (zw - W) // 2 + int(sx); oy = (zh - H) // 2 + int(sx * 0.5)
        fr = big.crop((ox, oy, ox + W, oy + H))
    # wipe transition with motion blur feel
    if idx > 0 and t < 0.3:
        dd = ImageDraw.Draw(fr); p = ease(t / 0.3); x = -300 + p * (W + 700)
        for k, (off, col) in enumerate([(0, YEL), (-130, PINK), (-200, (255, 255, 255))]):
            dd.polygon([(x - 260 + off, 0), (x + 120 + off - k * 40, 0), (x - 120 + off - k * 40, H), (x - 500 + off, H)], fill=col)
    # grain
    fr = Image.blend(fr, Image.merge("RGB", [grain(int(gt * 30))] * 3), 0.06)
    return fr

def render(vid, idx):
    dur = S2.R[vid][idx][0]; n = int(round(dur * FPS))
    od = os.path.join(reel2.OUT, "_scenes", vid); os.makedirs(od, exist_ok=True)
    tmp = os.path.join(od, f"s{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(vid, idx, i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(od, f"s{idx}.mp4"))

if __name__ == "__main__":
    cmd = sys.argv[1]; vid = sys.argv[2]
    if cmd == "preview":
        R = S2.R[vid]
        ims = [frame(vid, i, R[i][0] * (0.95 if i == len(R) - 1 else 0.7)).resize((270, 480)) for i in range(len(R))]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(reel2.HERE, f"pp_{vid}.png"))
        frame(vid, 2, 2.0).save(os.path.join(reel2.HERE, f"pp_full_{vid}.png"))
    elif cmd == "render":
        render(vid, int(sys.argv[3]))
