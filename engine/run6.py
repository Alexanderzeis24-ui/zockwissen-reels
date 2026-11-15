import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes6
import polish
scenes6.card = polish.card
from PIL import Image
import scenes2 as S2

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview":
        vid = sys.argv[2]; R = S2.R[vid]
        ims = [polish.frame(vid, i, R[i][0] * (0.95 if i == 6 else 0.75)).resize((270, 480)) for i in range(7)]
        shp = Image.new("RGB", (270 * 4, 480 * 2))
        for i, im in enumerate(ims): shp.paste(im, ((i % 4) * 270, (i // 4) * 480))
        shp.save(os.path.join(polish.reel2.HERE, f"p6_{vid}.png"))
    elif cmd == "render":
        polish.render(sys.argv[2], int(sys.argv[3]))
    elif cmd == "jobs":
        for v in scenes6.R6:
            for i in range(7): print(v, i)
