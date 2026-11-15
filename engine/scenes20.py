"""Extra-Reel 34b – Zu realistisch? Genial oder nervig. Diskussions-Reel, v3-Stil."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes13 as S13
ORIG_COMMENT = S13.comment13
import scenes18, scenes16, scenes15, scenes14
import scenes7 as S7
import scenes2 as S2
from scenes13 import (atext, gtext, chip, FX, FS, LIME, VIO, CY, MAG, ORG, RD, WH, INK, ease, back, W, H)
from PIL import Image, ImageDraw

VID = "34_Zu_realistisch"
S7.SCRIPTS7[VID] = [
    "Ist G T A sechs zu realistisch? Du entscheidest: genial oder nervig!",
    "Eins: Stirbst du, ist dein Bargeld weg.",
    "Zwei: Jedes Auto hat eine Tankanzeige.",
    "Drei: Die Polizei merkt sich dein Outfit.",
    "Vier: Beute musst du erst beim Hehler verkaufen.",
    "Fünf: Sprengst du den Tresor, ist ein Teil der Beute kaputt.",
    "Sechs: Passanten reagieren sogar auf schlechten Geruch.",
    "Also: genial oder nervig? Schreib ein Wort in die Kommentare! Und folg mir für Teil drei vom Countdown!",
]
S7.COMMENT[VID] = ("GENIAL ODER NERVIG?", "Genial, endlich echt!")
S7.COVER[VID] = ("GTA 6", "ZU REALISTISCH?")
HEAD = [("ZU REALISTISCH?", "GENIAL ODER NERVIG"), ("TOT?", "BARGELD WEG"), ("JEDES AUTO", "HAT EINE TANKANZEIGE"), ("DIE POLIZEI", "MERKT SICH DEIN OUTFIT"),
        ("BEUTE?", "ERST ZUM HEHLER"), ("TRESOR GESPRENGT", "= BEUTE KAPUTT"), ("PASSANTEN", "RIECHEN DICH"), ("GENIAL", "ODER NERVIG?")]
SRC = [None, "LAUT MEHREREN VORSCHAUEN", "QUELLE: EDGE-MAGAZIN, VORSCHAU", "QUELLE: EDGE-MAGAZIN, VORSCHAU", "LAUT MEHREREN VORSCHAUEN",
       "LAUT VORSCHAU (IGN)", "QUELLE: EDGE-MAGAZIN, VORSCHAU", None]
ACC = [(LIME, RD), ((90, 210, 120), LIME), (RD, ORG), (CY, VIO), ((255, 205, 70), ORG), (ORG, RD), ((120, 220, 90), LIME), (LIME, RD)]

def g_hook(im, d, t, dur):
    D = ImageDraw.Draw(im, "RGBA"); cx, cy = 720, 760
    a = 0.25 * math.sin(t * 2.2) * ease(t / 0.5)
    D.polygon([(cx - 40, 1060), (cx + 40, 1060), (cx, cy + 10)], fill=(200, 204, 222, 255))
    D.rounded_rectangle([cx - 120, 1060, cx + 120, 1085], 12, fill=(200, 204, 222, 255))
    L = 190; lx, ly = cx - L * math.cos(a), cy - L * math.sin(a); rx, ry = cx + L * math.cos(a), cy + L * math.sin(a)
    D.line([(lx, ly), (rx, ry)], fill=(230, 232, 245, 255), width=12)
    D.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(230, 232, 245, 255))
    for (x, y, col, lab, fg) in ((lx, ly, LIME, "GENIAL", INK), (rx, ry, RD, "NERVIG", WH)):
        D.line([(x, y), (x - 70, y + 120)], fill=(200, 204, 222, 255), width=4); D.line([(x, y), (x + 70, y + 120)], fill=(200, 204, 222, 255), width=4)
        D.chord([x - 100, y + 60, x + 100, y + 180], 0, 180, fill=col + (255,))
        chip(im, lab, x, y + 200, 30, col, fg, back((t - 0.4) / 0.4))
        D = ImageDraw.Draw(im, "RGBA")
    return (cx, cy)

def g_end(im, d, t, dur):
    act = int(t * 2) % 2
    for i, (lab, col, fg) in enumerate((("GENIAL", LIME, INK), ("NERVIG", RD, WH))):
        s = back((t - i * 0.1) / 0.35) * (1.12 if act == i else 1.0)
        chip(im, lab, 580 + i * 280, 720, 44, col, fg, s)
    atext(im, 720, 820, "SCHREIB EIN WORT", FS(30), WH, ease((t - 0.4) / 0.3))
    return (720, 720)

def vote(fr, idx, t, dur):
    if not 1 <= idx <= 6: return
    a = ease(t / 0.3)
    k = int((t + idx) * 2) % 2
    chip(fr, "GENIAL", 560, 1505, 26 * (1.1 if k == 0 else 1), LIME, INK, a)
    chip(fr, "NERVIG", 820, 1505, 26 * (1.1 if k == 1 else 1), RD, WH, a)

SC = [g_hook, scenes16.v_cash, scenes15.r_fuel, scenes14.p_heat, scenes16.v_fence, scenes18.r_boom, scenes15.r_smell, g_end]
S13.VID, S13.HEAD, S13.SRC, S13.ACC, S13.SC = VID, HEAD, SRC, ACC, SC
S13.RUMOR = None; S13.COVER_CHIP = "GENIAL ODER NERVIG?"
S13.TOP0 = "DEINE MEINUNG"; S13.TOPLAST = "DEINE MEINUNG"; S13.EXTRA = vote
S13.comment13 = ORIG_COMMENT

if __name__ == "__main__":
    cmd, vid = sys.argv[1], sys.argv[2]
    if cmd == "preview":
        T = S7.setup(vid); words = S7.word_times(vid, T); R = S2.R[vid]; n = len(R)
        fr_ = [0.75, 0.85, 0.85, 0.85, 0.85, 0.7, 0.85, 0.9]
        ims = [S7.frame(vid, i, R[i][0] * fr_[i], T, words).resize((360, 640)) for i in range(n)]
        ims.append(S7.frame(vid, 0, 0.0, T, words).resize((360, 640)))
        S7.make_cover(vid, os.path.join(HERE, f"cov_{vid}.png")); ims.append(Image.open(os.path.join(HERE, f"cov_{vid}.png")).resize((360, 640)))
        for part in range(2):
            shp = Image.new("RGB", (360 * 5, 640))
            for i, im in enumerate(ims[part * 5:part * 5 + 5]): shp.paste(im, (i * 360, 0))
            shp.save(os.path.join(HERE, f"p20_{part}.png"))
    elif cmd == "render":
        S7.render(vid, int(sys.argv[3]))
