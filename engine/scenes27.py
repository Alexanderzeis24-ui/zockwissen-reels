"""Reel 42 – „Diese Orte gibt es wirklich“. Upgrades: Lippensynchron zur Stimme, eigener Synthwave-Beat + Bass-Hits,
Figur reagiert (Jubel-Pose, Schock-Symbole)."""
import sys, os, math, subprocess, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
ORIG_COMMENT = S13.comment13
import scenes25 as S25
import scenes21 as S21
import scenes19 as S19
import scenes7 as S7
import scenes2 as S2
import mascot
from scenes13 import (atext, gtext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from scenes14 import stamp
from reel2 import CH_X, CH_FEET
from PIL import Image, ImageDraw
import numpy as np

VID = "42_Echte_Orte"
S7.SCRIPTS7[VID] = [
    "Diese G T A sechs Orte gibt es wirklich, aber einer ist komplett unmöglich! Folg mir für mehr!",
    "Eins: Vice City ist Miami.",
    "Zwei: Die Leonida Keys sind die Florida Keys.",
    "Drei: Grassrivers sind die Everglades, mit echten Alligatoren.",
    "Vier: Ambrosia basiert auf Clewiston. Die Stadt nennt sich Amerikas süßeste Stadt, wegen Zucker.",
    "Fünf: Und Mount Kalaga? Solche Berge gibt es in Florida gar nicht. Der höchste Punkt dort ist nur hundertfünf Meter hoch.",
    "Welchen Ort willst du zuerst sehen? Schreib die Zahl! Und merk dir:",
]
S7.DISPLAY.update({"hundertfünf": "105"})
S7.COMMENT[VID] = ("WELCHER ORT?", "Vice City, sofort!")
S7.COVER[VID] = ("GTA 6", "ECHTE ORTE")
GRN = (90, 210, 120); GOLD = (255, 205, 70); BLUE = (60, 120, 255)
HEAD = [("DIESE ORTE", "GIBT ES WIRKLICH!"), ("VICE CITY", "= MIAMI"), ("LEONIDA KEYS", "= FLORIDA KEYS"), ("GRASSRIVERS", "= EVERGLADES"),
        ("AMBROSIA", "= CLEWISTON"), ("MOUNT KALAGA", "GIBT ES NICHT!"), ("WELCHEN ORT", "WILLST DU SEHEN?")]
SRC = [None, "LAUT KARTEN-VERGLEICHEN", "LAUT KARTEN-VERGLEICHEN", "LAUT KARTEN-VERGLEICHEN", "LAUT GTABOOM / CLEWISTON", "FLORIDAS HÖCHSTER PUNKT: 105 M", None]
ACC = [(CY, MAG), (MAG, ORG), (CY, BLUE), (GRN, LIME), (GOLD, ORG), (RD, VIO), (LIME, MAG)]
PAIRS = [None, ("VICE CITY", "MIAMI", 1), ("LEONIDA KEYS", "FLORIDA KEYS", 2), ("GRASSRIVERS", "EVERGLADES", 3), ("AMBROSIA", "CLEWISTON", 5), ("MOUNT KALAGA", "GIBT ES NICHT", 6)]

# ---------------- 1) Lippensynchron ----------------
_ENV = None
def _load_env():
    global _ENV
    v = os.environ.get("VOICE")
    if not v or not os.path.exists(v): return
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "12000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 400  # 30 Werte pro Sekunde
    n = len(a) // hop
    rms = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(1))
    rms = rms / (np.percentile(rms, 95) + 1e-6)
    _ENV = rms
_load_env()
_old_mouth = mascot.mouth_at
def mouth_at(gt):
    if _ENV is None: return _old_mouth(gt)
    i = int(gt * 30)
    if i < 0 or i >= len(_ENV): return 0
    v = _ENV[i] * 0.7 + (_ENV[i - 1] if i > 0 else 0) * 0.3
    return 0 if v < 0.12 else 1 if v < 0.35 else 2 if v < 0.65 else 3
mascot.mouth_at = mouth_at

# ---------------- 2) Musik + Bass-Hits ----------------
SR = 44100
def synthwave(total):
    n = int(SR * total); out = np.zeros(n, np.float32); bpm = 104; beat = 60 / bpm
    t = np.arange(n) / SR
    roots = [57, 53, 48, 55]  # A F C G
    for bar in range(int(total / (beat * 4)) + 1):
        r = roots[bar % 4]
        for step in range(8):
            t0 = bar * 4 * beat + step * beat / 2
            i0 = int(t0 * SR); L = int(beat / 2 * SR * 0.9)
            if i0 >= n: break
            seg = np.arange(min(L, n - i0)) / SR
            f = 440 * 2 ** ((r - 24 - 69) / 12)
            saw = 2 * ((seg * f) % 1) - 1
            out[i0:i0 + len(seg)] += 0.22 * saw * np.exp(-seg * 6)
        for k, iv in enumerate((0, 3 if bar % 4 == 0 else 4, 7)):
            i0 = int(bar * 4 * beat * SR); L = int(4 * beat * SR)
            seg = np.arange(min(L, max(0, n - i0))) / SR
            if len(seg) == 0: continue
            f = 440 * 2 ** ((r + iv - 69) / 12)
            pad = (np.sin(2 * np.pi * f * seg) + 0.5 * np.sin(2 * np.pi * f * 1.005 * seg)) * np.minimum(1, seg * 2) * np.minimum(1, (L / SR - seg) * 2)
            out[i0:i0 + len(seg)] += 0.05 * pad
    for b in range(int(total / beat) + 1):
        i0 = int(b * beat * SR)
        if i0 >= n: break
        seg = np.arange(min(int(0.25 * SR), n - i0)) / SR
        kick = np.sin(2 * np.pi * (50 + 90 * np.exp(-seg * 30)) * seg) * np.exp(-seg * 12)
        out[i0:i0 + len(seg)] += 0.55 * kick
        if b % 2 == 1:
            sn = np.random.default_rng(b).standard_normal(len(seg)) * np.exp(-seg * 22)
            out[i0:i0 + len(seg)] += 0.18 * sn
        for h in (0, 0.5):
            j0 = int((b + h) * beat * SR) + 1
            if j0 >= n: continue
            hs = np.random.default_rng(b * 7 + int(h * 2)).standard_normal(min(int(0.04 * SR), n - j0)) * np.exp(-np.arange(min(int(0.04 * SR), n - j0)) / SR * 90)
            out[j0:j0 + len(hs)] += 0.05 * np.diff(np.concatenate([[0], hs]))
    fade = np.minimum(1, t / 0.5) * np.minimum(1, (total - t) / 1.0).clip(0, 1)
    return out * fade

def boom(n_len):
    s = np.arange(n_len) / SR
    return np.sin(2 * np.pi * (40 + 60 * np.exp(-s * 8)) * s) * np.exp(-s * 3.5)

_old_sfx = S2.sfx
def sfx(vid):
    path = _old_sfx(vid)
    if vid != VID: return path
    with wave.open(path, "rb") as w:
        ch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        a = np.frombuffer(w.readframes(nf), np.int16).astype(np.float32).reshape(-1, ch) / 32768
    total = nf / sr
    mus = synthwave(total)
    R = S2.R[vid]; t0 = 0
    for i, s in enumerate(R):
        if i > 0:
            i0 = int(t0 * SR); bm = boom(int(0.9 * SR))
            j = min(len(mus), i0 + len(bm)); mus[i0:j] += 1.1 * bm[: j - i0]
        t0 += s[0]
    mix = a + mus[:len(a), None] * 0.9
    mix = np.clip(mix, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    return path
S2.sfx = sfx

# ---------------- 3) Figur reagiert ----------------
REACT = {1: 0.9, 2: 0.9, 3: 1.0, 4: 1.2, 5: 1.4}
def posefn(idx, t, pose):
    if idx in REACT and REACT[idx] < t < REACT[idx] + 0.9: return "cheer"
    return pose

def react_fx(fr, idx, t, dur):
    if idx not in REACT: return
    rt = t - REACT[idx]
    if not 0 < rt < 1.2: return
    D = ImageDraw.Draw(fr, "RGBA")
    hx, hy = CH_X, CH_FEET - 560
    s = back(rt / 0.25) * (1 - ease((rt - 0.9) / 0.3))
    if s < 0.05: return
    for k in range(5):
        a = math.radians(-150 + k * 30)
        r0, r1 = 150 * s, 200 * s
        D.line([(hx + r0 * math.cos(a), hy + r0 * math.sin(a)), (hx + r1 * math.cos(a), hy + r1 * math.sin(a))], fill=(255, 230, 60, 255), width=8)
    txt = "WOW!" if idx != 5 else "WAS?!"
    f = FX(int(52 * s)); w = D.textlength(txt, font=f)
    bx, by = hx + 120, hy - 190
    D.rounded_rectangle([bx - w / 2 - 22, by - 40 * s, bx + w / 2 + 22, by + 40 * s], int(30 * s), fill=(255, 255, 255, 245))
    D.polygon([(bx - 30, by + 36 * s), (bx - 60, by + 80 * s), (bx - 4, by + 38 * s)], fill=(255, 255, 255, 245))
    D.text((bx, by), txt, font=f, fill=INK, anchor="mm")

# ---------------- scenes ----------------
def o_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA")
    x0, y0, w, h = 520, 640, 420, 450
    D.polygon([(x0 + px * w, y0 + py * h) for px, py in S19.MAP], fill=(70, 90, 120, 255), outline=(255, 255, 255, 140))
    for i, k in enumerate((1, 2, 3, 5, 6)):
        px, py = S19.PINS[k]; cx, cy = x0 + px * w, y0 + py * h
        s = back((t - 0.2 - i * 0.15) / 0.3)
        if s < 0.1: continue
        col = RD if k == 6 else LIME
        D.ellipse([cx - 22 * s, cy - 22 * s, cx + 22 * s, cy + 22 * s], fill=col + (255,), outline=(255, 255, 255, 255), width=4)
        if k == 6 and t > 1.2:
            atext(im, cx, cy, "?", FX(30), WH)
            chip(im, "UNMÖGLICH?", cx + 20, cy - 60, 24, RD, WH, back((t - 1.2) / 0.3))
            D = ImageDraw.Draw(im, "RGBA")
    q = dur * 0.5
    if t > q:
        S25._follow(im, t - q, 730, 1170); return (730, 1170)
    return (730, 860)

def icon(D, im, idx, t):
    cx, cy = 840, 680
    if idx == 1:
        for k in range(4):
            h = 60 + (k * 37) % 70
            D.rectangle([cx - 90 + k * 40, cy + 50 - h, cx - 60 + k * 40, cy + 50], fill=(MAG if k % 2 else CY) + (255,))
        S19.palm(D, cx + 90, cy + 60, 0.6, t)
    elif idx == 2:
        D.ellipse([cx - 110, cy + 20, cx + 110, cy + 60], fill=(60, 170, 220, 255))
        D.ellipse([cx - 50, cy + 10, cx + 50, cy + 40], fill=(245, 220, 160, 255)); S19.palm(D, cx, cy + 25, 0.5, t, (40, 120, 60))
    elif idx == 3:
        D.rectangle([cx - 110, cy + 20, cx + 110, cy + 60], fill=(40, 80, 60, 255)); S19.gator(D, cx - 20 + 10 * math.sin(t * 2), cy + 34, 0.6)
    elif idx == 4:
        for r in range(3):
            for c in range(3 - r):
                x = cx - 60 + c * 42 + r * 21; y = cy + 30 - r * 40
                D.rounded_rectangle([x, y, x + 38, y + 38], 6, fill=(250, 250, 255, 255), outline=(200, 200, 220, 255), width=2)
    elif idx == 5:
        D.polygon([(cx - 110, cy + 60), (cx - 20, cy - 70), (cx + 70, cy + 60)], fill=(70, 120, 90, 255))
        D.polygon([(cx - 40, cy - 40), (cx - 20, cy - 70), (cx, cy - 40)], fill=(220, 230, 225, 255))
        D.line([(cx + 100, cy + 60), (cx + 100, cy + 30)], fill=(255, 255, 255, 255), width=4)
        atext(im, cx + 100, cy + 14, "105 m", FX(22), GOLD)

def o_fact(idx):
    game, real, pin = PAIRS[idx]
    def f(im, d, t, dur):
        D = ImageDraw.Draw(im, "RGBA")
        S19.minimap(im, pin, t)
        D = ImageDraw.Draw(im, "RGBA"); icon(D, im, idx, t)
        s1 = back((t - 0.1) / 0.35)
        if s1 > 0.1:
            D = ImageDraw.Draw(im, "RGBA")
            D.rounded_rectangle([470, 800, 970, 920], 26, fill=(255, 255, 255, 22), outline=(255, 255, 255, 120), width=3)
            atext(im, 500, 828, "IM SPIEL", FS(22), (190, 196, 220), min(1, s1), "lm")
            atext(im, 500, 878, game, S13.fit(FX, game, 44, 440), WH, min(1, s1), "lm")
        if t > 0.55:
            atext(im, 720, 960, "=" if idx != 5 else "≠", FX(64), LIME if idx != 5 else RD, ease((t - 0.55) / 0.2))
        s2 = back((t - 0.8) / 0.35)
        if s2 > 0.1:
            col = GRN if idx != 5 else RD
            D = ImageDraw.Draw(im, "RGBA"); off = (1 - min(1, s2)) * 80
            D.rounded_rectangle([470, 1000 + off, 970, 1130 + off], 26, fill=col + (60,), outline=col + (255,), width=4)
            atext(im, 500, 1030 + off, "IN ECHT", FS(22), (220, 240, 225), min(1, s2), "lm")
            atext(im, 500, 1082 + off, real, S13.fit(FX, real, 48, 440), WH, min(1, s2), "lm")
        if idx == 5: stamp(im, "UNMÖGLICH", 720, 1185, t - 1.6, RD, -7, 46)
        return (720, 1060) if t > 0.8 else (720, 860)
    return f

SC = [o_hook] + [o_fact(i) for i in range(1, 6)] + [S21.f_end]

def fx(fr, idx, t, dur):
    S25.fx.__wrapped__(fr, idx, t, dur) if hasattr(S25.fx, "__wrapped__") else None
    n = len(SC)
    if idx == 0 and t < 0.25: fr.paste(CY, (0, 0), Image.new("L", (W, H), int(140 * (1 - t / 0.25))))
    if idx == n - 1 and t > dur - 0.3: fr.paste(CY, (0, 0), Image.new("L", (W, H), int(140 * (t - (dur - 0.3)) / 0.3)))
    react_fx(fr, idx, t, dur)

S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "ECHTE ORTE!"; S13.FACTLBL = "ORT"
S13.TOP0 = "GTA 6 VS. REALITÄT"; S13.TOPLAST = "DEINE MEINUNG"; S13.EXTRA = fx
S13.POSEFN = posefn
S13.comment13 = ORIG_COMMENT

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.3, 0.8, 0.8, 0.8, 0.8, 0.85, 0.8]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, R[0][0] * 0.8, T, words).resize((360, 640)))
        ims.append(S7.frame(vid, 1, REACT[1] + 0.35, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p27_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
