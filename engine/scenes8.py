"""Reel 22: 6 side characters of GTA 6 (official Rockstar reveal), v2 format."""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes7 as S7
from scenes7 import *

VID = "22_Nebenfiguren"
S7.SCRIPTS7[VID] = [
    "Diese sechs verrückten Typen triffst du in G T A sechs!",
    "Käl: Jasons Kumpel, plant alles vom Sofa aus.",
    "Bubi Eik: vom Kleinkriminellen zum Immobilien-Boss.",
    "Dree-Kwan: Dealer mit eigenem Musiklabel.",
    "Riel Daims: zwei Rapperinnen wollen ihr Comeback.",
    "Raul: Bankräuber, immer auf der Jagd nach dem nächsten Coup.",
    "Brai-en: schmuggelt über seinen Bootshafen.",
    "Wer ist dein Favorit? Schreib's in die Kommentare!",
]
S7.DISPLAY.update({"Käl": "Cal", "Bubi": "Boobie", "Eik": "Ike", "Dree-Kwan": "Dre'Quan", "Riel": "Real", "Daims": "Dimez", "Brai-en": "Brian"})
S7.COMMENT[VID] = ("DEIN FAVORIT?", "Raul, safe!")
S7.COVER[VID] = ("6 NEUE TYPEN", "IN GTA 6 – KENNST DU SIE?")

NAMES = [("CAL", CYAN, False), ("BOOBIE IKE", YEL, False), ("DRE'QUAN", GRN, False), ("REAL DIMEZ", PINK, True), ("RAUL", RED, False), ("BRIAN", (90, 160, 220), False)]

def mini(d, i, cx, cy, s):
    n, col, lh = NAMES[i]
    if s <= 0.05: return
    card(d, (cx - 85 * s, cy - 115 * s, cx + 85 * s, cy + 115 * s), col, int(20 * s), int(8 * s))
    silhouette(d, cx, cy - 15 * s, 0.48 * s, lh, sh(col, 0.45))
    d.rectangle([cx - 80 * s, cy + 62 * s, cx + 80 * s, cy + 110 * s], fill=INK)
    label(d, n, cx, cy + 86 * s, max(8, (26 if len(n) < 8 else 20) * s), (255, 255, 255), 0)

def c_hook(im, d, t, dur):
    for i in range(6):
        cx = 530 + (i % 3) * 180; cy = 700 + (i // 3) * 270
        s = back((t - 0.08 * i) / 0.3) * 0.95
        mini(d, i, cx, cy + math.sin(t * 3 + i) * 5, s)
        if t > 0.6: V.qmark(d, cx + 60, cy - 100, 0.4 * back((t - 0.6 - 0.05 * i) / 0.3))
    return (710, 820)

def sofa(d, cx, cy, s):
    c = (150, 90, 140)
    d.rounded_rectangle([cx - 200 * s, cy - 120 * s, cx + 200 * s, cy], int(30 * s), fill=sh(c, 0.85), outline=INK, width=4)
    d.rounded_rectangle([cx - 230 * s, cy - 40 * s, cx + 230 * s, cy + 60 * s], int(30 * s), fill=c, outline=INK, width=4)
    for x in (-230, 170): d.rounded_rectangle([cx + x * s, cy - 90 * s, cx + (x + 60) * s, cy + 60 * s], int(24 * s), fill=sh(c, 0.9), outline=INK, width=4)
    for x in (-180, 160): d.rectangle([cx + x * s, cy + 60 * s, cx + (x + 20) * s, cy + 90 * s], fill=(80, 60, 50))

def can(d, cx, cy, s):
    d.rounded_rectangle([cx - 22 * s, cy - 45 * s, cx + 22 * s, cy + 45 * s], int(10 * s), fill=(200, 205, 215), outline=INK, width=3)
    d.rectangle([cx - 22 * s, cy - 15 * s, cx + 22 * s, cy + 15 * s], fill=YEL)

def c_cal(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (60, 70, 110))
    sofa(d, 710, 1080, back(t / 0.4) * 0.95)
    silhouette(d, 680, 960 + math.sin(t * 3) * 4, 0.7 * back((t - 0.2) / 0.4), False, (30, 40, 70))
    can(d, 830, 960, back((t - 0.6) / 0.3))
    # thought bubble plan
    s = back((t - 0.9) / 0.4)
    if s > 0.05:
        for k, (x, y, r) in enumerate([(760, 840, 12), (790, 800, 18)]): d.ellipse([x - r, y - r, x + r, y + r], fill="white", outline=INK, width=3)
        card(d, (760 - 150 * s, 640 - 80 * s, 760 + 150 * s, 640 + 80 * s), (255, 255, 255), 30, 6)
        d.line([(660, 660), (720, 610), (780, 650), (850, 600)], fill=RED, width=6)
        d.text((860, 600), "X", font=F(40 * s), fill=RED, anchor="mm")
    return (700, 960)

def c_boobie(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (120, 160, 210))
    rnd = random.Random(4)
    for i in range(5):
        h = (180 + rnd.randrange(0, 300)) * back((t - 0.12 * i) / 0.4)
        if h > 3:
            x = 450 + i * 105
            M.box(d, x, 1200 - h, 85, h, 34, [(90, 100, 140), (120, 110, 150), (100, 130, 160)][i % 3])
            for yy in range(int(1200 - h + 20), 1180, 40):
                for xx in range(x + 12, x + 75, 24): d.rectangle([xx, yy, xx + 12, yy + 20], fill=(255, 225, 150))
    s = back((t - 0.8) / 0.4)
    if s > 0.05:
        bx, by = 870, 700 + math.sin(t * 3) * 8
        d.ellipse([bx - 70 * s, by - 50 * s, bx + 70 * s, by + 80 * s], fill=(120, 170, 90), outline=INK, width=4)
        d.polygon([(bx - 30 * s, by - 50 * s), (bx + 30 * s, by - 50 * s), (bx, by - 85 * s)], fill=(120, 170, 90), outline=INK)
        label(d, "$", bx, by + 18 * s, 70 * s, (255, 255, 255), 5)
    pill(d, "IMMOBILIEN-BOSS", 640, 640, 32, YEL, INK, back((t - 0.4) / 0.4))
    return (870, 720)

def vinyl(d, cx, cy, r, t):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(25, 25, 30), outline=INK, width=4)
    for k in (0.85, 0.7, 0.55): d.ellipse([cx - r * k, cy - r * k, cx + r * k, cy + r * k], outline=(60, 60, 70), width=3)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3], fill=GRN, outline=INK, width=3)
    a = t * 6
    d.line([(cx + math.cos(a) * r * 0.35, cy + math.sin(a) * r * 0.35), (cx + math.cos(a) * r * 0.95, cy + math.sin(a) * r * 0.95)], fill=(120, 120, 135), width=5)

def note(d, x, y, s, col):
    d.ellipse([x - 18 * s, y - 12 * s, x + 18 * s, y + 12 * s], fill=col, outline=INK, width=2)
    d.line([(x + 16 * s, y), (x + 16 * s, y - 70 * s)], fill=INK, width=max(2, int(6 * s)))
    d.polygon([(x + 16 * s, y - 70 * s), (x + 46 * s, y - 55 * s), (x + 16 * s, y - 45 * s)], fill=INK)

def c_drequan(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (30, 25, 50))
    vinyl(d, 710, 900, 230 * back(t / 0.45), t)
    for i in range(5):
        p = ((t * 0.6 + i * 0.2) % 1)
        note(d, 500 + i * 110, 1180 - p * 560, 0.9, [PINK, CYAN, YEL, GRN, (180, 120, 255)][i])
    pill(d, "EIGENES LABEL", 710, 1190, 36, GRN, (255, 255, 255), back((t - 0.6) / 0.4))
    return (710, 900)

def mic(d, cx, cy, s, col):
    d.rounded_rectangle([cx - 38 * s, cy - 110 * s, cx + 38 * s, cy], int(36 * s), fill=(190, 195, 210), outline=INK, width=4)
    for k in range(4): d.line([(cx - 30 * s, cy - 95 * s + k * 22 * s), (cx + 30 * s, cy - 95 * s + k * 22 * s)], fill=(140, 145, 160), width=2)
    d.rectangle([cx - 14 * s, cy, cx + 14 * s, cy + 120 * s], fill=col, outline=INK, width=3)

def c_dimez(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (90, 40, 110))
    mic(d, 590, 900 + math.sin(t * 6) * 6, back(t / 0.4) * 1.3, PINK)
    mic(d, 830, 900 + math.cos(t * 6) * 6, back((t - 0.2) / 0.4) * 1.3, CYAN)
    for k in range(18):
        h = 20 + abs(math.sin(t * 9 + k * 0.7)) * 90
        x = 450 + k * 30
        d.rounded_rectangle([x, 1150 - h, x + 18, 1150], 8, fill=YEL)
    pill(d, "COMEBACK", 710, 640, 40, PINK, (255, 255, 255), back((t - 0.4) / 0.4))
    return (710, 880)

def vault(d, cx, cy, r, t, open_p):
    d.rounded_rectangle([cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30], 30, fill=(110, 115, 130), outline=INK, width=5)
    if open_p > 0:
        d.rectangle([cx - r, cy - r, cx + r, cy + r], fill=(30, 30, 40))
        for i in range(3): V.bill_stack(d, cx - r + 20 + i * 70, cy + r - 10, 55, 60 + i * 25)
    ww = r * 2 * (1 - 0.85 * open_p)
    d.ellipse([cx - r, cy - r, cx - r + ww, cy + r], fill=(170, 175, 190), outline=INK, width=5)
    a = t * 2 * (1 - open_p)
    hx = cx - r + ww / 2
    for k in range(3):
        aa = a + k * 2 * math.pi / 3
        d.line([(hx, cy), (hx + math.cos(aa) * ww * 0.35, cy + math.sin(aa) * r * 0.7)], fill=INK, width=12)
    d.ellipse([hx - 20, cy - 20, hx + 20, cy + 20], fill=YEL, outline=INK, width=3)

def c_raul(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (40, 40, 55))
    vault(d, 710, 880, 200, t, ease((t - 1.2) / 0.6))
    on = int(t * 6) % 2
    d.ellipse([460, 600, 500, 640], fill=RED if on else (90, 30, 30)); d.ellipse([920, 600, 960, 640], fill=(60, 120, 255) if not on else (30, 40, 90))
    pill(d, "BANKRÄUBER", 710, 1180, 40, RED, (255, 255, 255), back((t - 0.4) / 0.4))
    return (710, 880)

def c_brian(im, d, t, dur):
    card(d, (420, 560, 1000, 1240), (70, 160, 210))
    d.rectangle([426, 566, 994, 760], fill=(255, 190, 140))
    d.rectangle([426, 1040, 994, 1234], fill=(130, 90, 60))
    for x in range(440, 990, 60): d.line([(x, 1040), (x, 1234)], fill=(100, 70, 45), width=4)
    bob = math.sin(t * 3) * 6
    bx = 990 - ease(t / 1.4) * 420
    d.polygon([(bx, 960 + bob), (bx + 260, 960 + bob), (bx + 300, 910 + bob), (bx - 20, 910 + bob)], fill=(250, 250, 250), outline=INK)
    d.rectangle([bx + 60, 860 + bob, bx + 170, 910 + bob], fill=(230, 230, 235), outline=INK)
    for i in range(3): M.box(d, bx + 190 + i * 32, 880 + bob, 28, 28, 14, (190, 140, 90))
    for k in range(5):
        y = 990 + k * 12; off = (t * 80 + k * 40) % 160
        for x in range(380, 1000, 160):
            if 430 < x + off < 930: d.line([(x + off, y), (x + off + 50, y)], fill=(170, 220, 245), width=4)
    pill(d, "SCHMUGGEL", 710, 640, 40, YEL, INK, back((t - 0.5) / 0.4))
    return (bx + 130, 900)

def c_cta(im, d, t, dur):
    for i in range(6):
        cx = 530 + (i % 3) * 180; cy = 700 + (i // 3) * 270
        mini(d, i, cx, cy, 0.8 * (1 + 0.05 * math.sin(t * 6 + i)))
    return (710, 820)

_old_defs = S7.defs
def defs(vid, durs):
    if vid != VID: return _old_defs(vid, durs)
    sc = [c_hook, c_cal, c_boobie, c_drequan, c_dimez, c_raul, c_brian, c_cta]
    w = [("6 NEUE TYPEN", PINK), ("CAL", CYAN), ("BOOBIE IKE", YEL), ("DRE'QUAN", GRN), ("REAL DIMEZ", PINK), ("RAUL", RED), ("BRIAN", CYAN), ("DEIN FAVORIT?", PINK)]
    th = ["purple", "night", "sky", "night", "sunset", "night", "ocean", "purple"]
    poses = ["wave"] + ["point"] * 7
    return [(durs[i], th[i], sc[i], [(0, w[i][0], w[i][1])], poses[i]) for i in range(8)]
S7.defs = defs

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        T = S7.setup(VID); words = S7.word_times(VID, T); R = S2.R[VID]
        ims = [S7.frame(VID, 0, 0.0, T, words).resize((270, 480))] + [S7.frame(VID, i, R[i][0] * (0.9 if i == 7 else 0.6), T, words).resize((270, 480)) for i in range(8)]
        shp = Image.new("RGB", (270 * 5, 480 * 2))
        for i, im in enumerate(ims[:10]): shp.paste(im, ((i % 5) * 270, (i // 5) * 480))
        S7.make_cover(VID, os.path.join(HERE, "cov22.png"))
        shp.paste(Image.open(os.path.join(HERE, "cov22.png")).resize((270, 480)), (4 * 270, 480))
        shp.save(os.path.join(HERE, "p8.png"))
    elif cmd == "render":
        S7.render(VID, int(sys.argv[2]))
