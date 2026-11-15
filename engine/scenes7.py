"""v2 reels: hook-first, ~18-20 s, word captions, comment-CTA outro, custom covers."""
import sys, os, json, math, random, subprocess, functools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes6
import polish
scenes6.card = polish.card
from scenes6 import *
from PIL import Image, ImageDraw, ImageFilter
import scenes2 as S2

# ---------------- scripts ----------------
SCRIPTS7 = {
"21v2_GTA5_vs_GTA6": ["G T A sechs kostet zwanzig Dollar mehr als G T A fünf!", "Und nach dreizehn Jahren ändert sich fast alles.", "Statt drei Hauptfiguren gibt es nur noch ein Duo.", "Statt Los Santos geht es nach Vice City.", "Und es läuft nur noch auf PS fünf und Xbox Series.", "Welches ist besser? Schreib fünf oder sechs in die Kommentare!"],
"18v2_Bestseller": ["Nur ein einziges Spiel hat sich öfter verkauft als Minecraft!", "Platz fünf: Wii Sports, dreiundachtzig Millionen.", "Platz vier: Red Dead zwei, siebenundachtzig Millionen.", "Platz drei: G T A fünf, zweihundertdreißig Millionen.", "Platz zwei: Minecraft, vierhundertfünfundzwanzig Millionen.", "Und Platz eins: Tetris, mit über fünfhundert Millionen!", "Hättest du das gewusst? Schreib ja oder nein!"],
"19v2_Rockstar": ["Das allererste G T A ist älter als Rockstar selbst!", "G T A kam neunzehnhundertsiebenundneunzig, Rockstar erst ein Jahr später.", "Gegründet in New York, unter anderem von den Brüdern Sam und Dan Houser.", "Das Hauptstudio sitzt heute in Schottland.", "Insgesamt arbeiten rund viertausendsiebenhundert Leute für Rockstar.", "Wusstest du das? Schreib es in die Kommentare!"],
"20v2_GTA_Online": ["G T A Online hat angeblich über fünf Milliarden Dollar gemacht!", "Das zeigen geleakte Daten, bestätigt ist das aber nicht.", "Fast drei Viertel davon kamen durch Shark Cards.", "Dabei zahlen nur rund vier Prozent der Spieler überhaupt.", "Und an einem einzigen Weihnachtstag kamen über acht Millionen rein.", "Hast du schon mal Shark Cards gekauft? Kommentier!"],
}
# caption text: how words should be DISPLAYED (spoken spellings -> readable)
DISPLAY = {"G T A": "GTA", "sechs": "6", "fünf": "5", "drei": "3", "zwei": "2", "zwanzig": "20", "dreizehn": "13", "dreiundachtzig": "83", "siebenundachtzig": "87",
           "zweihundertdreißig": "230", "vierhundertfünfundzwanzig": "425", "fünfhundert": "500", "neunzehnhundertsiebenundneunzig": "1997",
           "viertausendsiebenhundert": "4.700", "acht": "8", "vier": "4"}
COMMENT = {"21v2_GTA5_vs_GTA6": ("5 ODER 6?", "6, ganz klar!"), "18v2_Bestseller": ("JA ODER NEIN?", "Nein, krass!"),
           "19v2_Rockstar": ("WUSSTEST DU'S?", "Wusste ich nicht!"), "20v2_GTA_Online": ("SCHON GEKAUFT?", "Noch nie, haha")}
COVER = {"21v2_GTA5_vs_GTA6": ("GTA 5 VS 6", "DAS ÄNDERT SICH"), "18v2_Bestseller": ("PLATZ 1?", "MEHR ALS MINECRAFT"),
         "19v2_Rockstar": ("GTA IST ÄLTER", "ALS ROCKSTAR?!"), "20v2_GTA_Online": ("5 MRD. $", "MIT GTA ONLINE?")}

def caption_words(line):
    s = line.replace("G T A", "GTA")
    out = []
    for w in s.split():
        core = w.strip("!?.,:")
        tail = w[len(w.rstrip("!?.,:")):] if w != w.rstrip("!?.,:") else ""
        key = core
        rep = DISPLAY.get(key, DISPLAY.get(key.lower(), key))
        if key == "GTA": rep = "GTA"
        out.append((rep + tail).upper())
    return out

# ---------------- comment outro ----------------
def comment_outro(d, fr, ot, vid):
    q, ans = COMMENT[vid]
    s = back(ot / 0.4)
    if s > 0.05:
        polish.card(d, (430, 940 - 10, 990, 1250), (255, 255, 255))
        d.ellipse([460, 975, 540, 1055], fill=(60, 160, 95), outline=INK, width=4)
        d.text((560, 990), "du", font=F(30), fill=(120, 120, 135))
        n = int(len(ans) * ease((ot - 0.5) / 1.0))
        txt = ans[:n] + ("|" if (int(ot * 3) % 2 == 0 and n < len(ans)) else "")
        d.text((560, 1040), txt, font=F(44), fill=INK)
        if ot > 1.6:
            hs = back((ot - 1.6) / 0.3)
            hx, hy = 930, 1180
            d.ellipse([hx - 26 * hs, hy - 22 * hs, hx, hy + 4 * hs], fill=RED); d.ellipse([hx - 4 * hs, hy - 22 * hs, hx + 22 * hs, hy + 4 * hs], fill=RED)
            d.polygon([(hx - 26 * hs, hy - 6 * hs), (hx + 22 * hs, hy - 6 * hs), (hx - 2 * hs, hy + 26 * hs)], fill=RED)
        pill(d, "+ FOLGEN", 710, 1300, 40, PINK, (255, 255, 255), back((ot - 0.2) / 0.35) * (1 + 0.05 * math.sin(ot * 9)))
    return (700, 1060)

# ---------------- captions ----------------
def draw_caption(fr, words, gt):
    """words: list of (start, end, text) global times."""
    cur = None
    for i, (a, b, w) in enumerate(words):
        if a <= gt < b + 0.05: cur = i
    if cur is None:
        prev = [i for i, (a, b, w) in enumerate(words) if b <= gt]
        if not prev or gt - words[prev[-1]][1] > 0.35: return
        cur = prev[-1]
    g0 = (cur // 3) * 3; chunk = words[g0:g0 + 3]
    d = ImageDraw.Draw(fr)
    f = F(62)
    texts = [w for (_, _, w) in chunk]
    widths = [d.textlength(t, font=f) for t in texts]
    total = sum(widths) + 22 * (len(texts) - 1)
    x = 690 - total / 2; y = 1395
    if total > 600:
        f = F(int(62 * 600 / total)); widths = [d.textlength(t, font=f) for t in texts]; total = sum(widths) + 22 * (len(texts) - 1); x = 690 - total / 2
    for k, (t, w) in enumerate(zip(texts, widths)):
        active = (g0 + k) == cur
        a, b, _ = chunk[k]
        pop = 1 + 0.12 * (1 - ease((gt - a) / 0.15)) if active else 1
        if active:
            d.rounded_rectangle([x - 10, y - 44 * pop, x + w + 10, y + 44 * pop], 16, fill=YEL)
        ff = f if pop == 1 else F(int(f.size * pop))
        d.text((x + w / 2, y), t, font=ff, fill=INK if active else (255, 255, 255), anchor="mm", stroke_width=0 if active else 8, stroke_fill=INK)
        x += w + 22

# ---------------- timing ----------------
TF = os.path.join(HERE, "timing7.json")
def load_timing():
    return json.load(open(TF)) if os.path.exists(TF) else {}

def est(vid):
    lines = SCRIPTS7[vid]
    raw = [len(l) / 15.5 + 0.35 for l in lines]
    bounds = [0]; segs = []
    for r in raw:
        segs.append((bounds[-1] + 0.05, bounds[-1] + r - 0.3)); bounds.append(bounds[-1] + r)
    total = bounds[-1] + 1.5
    durs = [bounds[i + 1] - bounds[i] for i in range(len(lines))]
    durs[-1] += 1.5
    return {"durs": durs, "segs": segs, "total": total}

def word_times(vid, T):
    out = []
    for line, (a, b) in zip(SCRIPTS7[vid], T["segs"]):
        ws = caption_words(line)
        spoken = line.replace("G T A", "GTA").split()
        lens = [max(2, len(w)) for w in spoken]
        tot = sum(lens); t = a
        for w, l in zip(ws, lens):
            dt = (b - a) * l / tot
            out.append((t, t + dt, w)); t += dt
    return out

# ---------------- reel definitions ----------------
def defs(vid, durs):
    if vid == "21v2_GTA5_vs_GTA6":
        sc = [vs_price, vs_years, vs_heroes, vs_map, vs_console, vs_outro]
        w = [("+20 $", PINK), ("13 JAHRE", CYAN), ("DUO STATT TRIO", PINK), ("NEUE MAP", GRN), ("NUR NEXT-GEN", CYAN), ("5 ODER 6?", PINK)]
        th = ["gold", "sky", "sunset", "ocean", "night", "purple"]
    elif vid == "18v2_Bestseller":
        sc = [rk_intro, rank_scene(5), rank_scene(4), rank_scene(3), rank_scene(2), rank_scene(1), rk_outro]
        w = [("MEHR ALS MINECRAFT?", PINK), ("PLATZ 5", CYAN), ("PLATZ 4", PINK), ("PLATZ 3", GRN), ("PLATZ 2", CYAN), ("PLATZ 1", PINK), ("JA ODER NEIN?", GRN)]
        th = ["gold", "sky", "sunset", "mint", "ocean", "purple", "night"]
    elif vid == "19v2_Rockstar":
        sc = [rs_older, rs_ny, rs_brothers, rs_scotland, rs_people, rs_outro]
        w = [("ÄLTER ALS ROCKSTAR?!", PINK), ("1997 VS 1998", CYAN), ("DIE GRÜNDER", PINK), ("SCHOTTLAND", GRN), ("4.700 LEUTE", CYAN), ("WUSSTEST DU'S?", PINK)]
        th = ["mint", "sky", "sunset", "ocean", "gold", "purple"]
    else:
        sc = [go_5bn, go_outro_leak, go_shark, go_4pct, go_xmas, go_intro]
        w = [("5 MILLIARDEN $?!", PINK), ("NUR EIN LEAK", CYAN), ("SHARK CARDS", CYAN), ("NUR 4 %", PINK), ("8,5 MIO. AN 1 TAG", GRN), ("SCHON GEKAUFT?", PINK)]
        th = ["gold", "night", "ocean", "purple", "night", "mint"]
    poses = ["wave"] + ["point"] * (len(sc) - 2) + ["point"]
    return [(durs[i], th[i], sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(len(sc))]

def go_outro_leak(im, d, t, dur):
    card(d, (420, 560, 1000, 1150), (40, 30, 80))
    stamp(im, "LEAK", 710, 760, t, 0.15, -10, 1.3, YEL)
    stamp(im, "NICHT BESTÄTIGT", 710, 960, t, 0.7, 6, 0.75)
    return (710, 860)

def setup(vid):
    T = load_timing().get(vid) or est(vid)
    S2.R[vid] = defs(vid, T["durs"])
    return T

# ---------------- frame ----------------
def frame(vid, idx, t, T, words, cover=False, no_sticker=False):
    dur, theme, fn, wds, pose0 = S2.R[vid][idx]
    gt = sum(s[0] for s in S2.R[vid][:idx]) + t
    fr = polish.bg(theme).copy(); polish._CUR["im"] = fr
    polish.particles(fr, gt, theme)
    d = ImageDraw.Draw(fr)
    tt = t + (0.45 if idx == 0 else 0)          # hook: scene 0 already in motion on frame 1
    target = fn(fr, d, tt, dur)
    last = idx == len(S2.R[vid]) - 1
    ot = None
    if last and not cover:
        ot = t - 0.15
        if ot > 0: target = comment_outro(d, fr, ot, vid)
    pose = pose0
    if pose0 == "wave" and t > 1.2: pose = "point"
    draw_character(fr, t, gt, pose, target)
    st = polish.sticker(wds[0][1], wds[0][2])
    lt = t if idx else t + 0.6
    s = back(lt / 0.22)
    if s > 0.03 and not no_sticker:
        st2 = polish.shine(st, (lt - 0.25) / 0.45)
        ang = -3 + 4 * (1 - ease(lt / 0.3)) + math.sin(gt * 2) * 1.2
        r = st2.resize((max(1, int(st2.width * s)), max(1, int(st2.height * s))), Image.BILINEAR).rotate(ang, expand=True, resample=Image.BICUBIC)
        m = r.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.5))
        fr.paste((0, 0, 0), (int(W / 2 - r.width / 2) + 8, int(380 - r.height / 2) + 18), m)
        fr.paste(r, (int(W / 2 - r.width / 2), int(380 - r.height / 2)), r)
    polish._CUR["im"] = None
    if not cover: draw_caption(fr, words, gt)
    # camera
    z = 1.0 + 0.04 * ease(t / dur)
    sx = math.sin(t * 60) * 12 * max(0, 1 - t / 0.2) if idx > 0 else 0
    zw, zh = int(W * z), int(H * z)
    big = fr.resize((zw, zh), Image.BILINEAR)
    ox = (zw - W) // 2 + int(sx); oy = (zh - H) // 2 + int(sx * 0.5)
    fr = big.crop((ox, oy, ox + W, oy + H))
    if idx > 0 and t < 0.22 and not cover:
        dd = ImageDraw.Draw(fr); p = ease(t / 0.22); x = -300 + p * (W + 700)
        for k, (off, col) in enumerate([(0, YEL), (-130, PINK), (-200, (255, 255, 255))]):
            dd.polygon([(x - 260 + off, 0), (x + 120 + off - k * 40, 0), (x - 120 + off - k * 40, H), (x - 500 + off, H)], fill=col)
    fr = Image.blend(fr, Image.merge("RGB", [polish.grain(int(gt * 30))] * 3), 0.05)
    return fr

def render(vid, idx):
    T = setup(vid); words = word_times(vid, T)
    dur = S2.R[vid][idx][0]; n = int(round(dur * FPS))
    od = os.path.join(HERE, "teil2", "_scenes", vid); os.makedirs(od, exist_ok=True)
    tmp = os.path.join(od, f"s{idx}.tmp.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(vid, idx, i / FPS, T, words).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(od, f"s{idx}.mp4"))

def make_cover(vid, path):
    T = setup(vid)
    fr = frame(vid, 0, 1.2, T, [], cover=True, no_sticker=True)
    sh_ = Image.new("L", (W, H), 0); ImageDraw.Draw(sh_).rectangle([0, 0, W, 560], fill=170)
    fr.paste((10, 6, 24), (0, 0), sh_.filter(ImageFilter.GaussianBlur(60)))
    d = ImageDraw.Draw(fr)
    a, b = COVER[vid]
    st = polish.sticker(a, PINK); st = st.resize((int(st.width * 1.15), int(st.height * 1.15)))
    fr.paste(st, (int(W / 2 - st.width / 2), 100), st)
    label(d, b, W / 2, 100 + st.height + 60, 64, YEL, 10)
    fr.save(path)

if __name__ == "__main__":
    cmd = sys.argv[1]; vid = sys.argv[2]
    if cmd == "preview":
        T = setup(vid); words = word_times(vid, T); R = S2.R[vid]
        ims = [frame(vid, i, R[i][0] * (0.9 if i == len(R) - 1 else 0.55), T, words).resize((270, 480)) for i in range(len(R))]
        ims.insert(0, frame(vid, 0, 0.0, T, words).resize((270, 480)))
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims[:8]): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(HERE, f"p7_{vid}.png"))
    elif cmd == "render":
        render(vid, int(sys.argv[3]))
    elif cmd == "cover":
        make_cover(vid, sys.argv[3])
    elif cmd == "n":
        setup(vid); print(len(S2.R[vid]))
