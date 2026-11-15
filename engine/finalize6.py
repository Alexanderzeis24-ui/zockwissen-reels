"""Usage: python3 finalize6.py <vid> <voice.mp3>
Detects sentence pauses in the voice, retimes the 7 scenes, re-renders and mixes voice + sfx."""
import sys, os, re, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
vid, mp3 = sys.argv[1], sys.argv[2]
sys.path.insert(0, HERE)
from scenes6 import SCRIPTS

def probe_len(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

L = probe_len(mp3)
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-35dB:d=0.15", "-f", "null", "-"], capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
sil = [((s + e) / 2, s, e) for s, e in zip(starts, ends) if s > 0.5 and e < L - 0.3]
lines = SCRIPTS[vid]
tot = sum(len(l) for l in lines); acc = 0; expect = []
for l in lines[:-1]:
    acc += len(l); expect.append(L * acc / tot)
cuts = []; used = set()
for e in expect:
    cands = [(abs(m - e), i) for i, (m, s, en) in enumerate(sil) if i not in used and (not cuts or m > cuts[-1])]
    if cands:
        _, i = min(cands); used.add(i); cuts.append(sil[i][0])
    else:
        cuts.append(e)
total = round(L + 1.6, 2)
bounds = [0.0] + cuts + [total]
durs = [round(bounds[i + 1] - bounds[i], 3) for i in range(7)]
last_start = bounds[6]
tail = [m for (m, s, e) in sil if m > last_start + 0.8]
follow = (tail[-1] - last_start) if tail else max(1.2, durs[6] - 2.0)
tf = os.path.join(HERE, "timing6.json")
T = json.load(open(tf)) if os.path.exists(tf) else {}
T[vid] = {"durs": durs, "follow": round(follow, 3), "voice_len": L}
json.dump(T, open(tf, "w"), indent=1)
print("durs", durs, "follow", follow, "len", L)

sd = os.path.join(HERE, "teil2", "_scenes", vid)
for f in os.listdir(sd):
    if f.startswith("s") and f.endswith(".mp4"): os.remove(os.path.join(sd, f))
procs = []
for i in range(7):
    procs.append(subprocess.Popen([sys.executable, os.path.join(HERE, "run6.py"), "render", vid, str(i)]))
    if len(procs) == 2:
        for p in procs: p.wait()
        procs = []
for p in procs: p.wait()
import run6, scenes2 as S
open(os.path.join(sd, "list.txt"), "w").write("".join(f"file 's{i}.mp4'\n" for i in range(7)))
wav = S.sfx(vid)
od = os.path.join(HERE, "ZOCKWISSEN_Reels_Teil5", vid); os.makedirs(od, exist_ok=True)
outp = os.path.join(od, f"{vid}_FERTIG_mit_Stimme.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(sd, "list.txt"), "-i", mp3, "-i", wav,
                "-filter_complex", f"[1:a]volume=1.0,apad[v];[2:a]volume=0.35[s];[v][s]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total},alimiter=limit=0.95[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-movflags", "+faststart", outp], check=True)
t0 = 0; tl = []
for (d, _, _, words, _), l in zip(S.R[vid], lines):
    tl.append(f"{t0:5.2f}–{t0 + d:5.2f} s  [{' / '.join(w[1] for w in words)}]  {l}"); t0 += d
open(os.path.join(od, "Timing.txt"), "w").write("\n".join(tl) + "\n")
print("OK", outp)
