"""python3 finalize7.py <vid> [voice.mp3]  -> with mp3: exact timing + mixed voice; without: preview with estimated timing."""
import sys, os, re, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes9, scenes7 as S7
vid = sys.argv[1]; mp3 = sys.argv[2] if len(sys.argv) > 2 else None
lines = S7.SCRIPTS7[vid]; n = len(lines)
T = S7.load_timing()
if mp3 and os.environ.get('MANUAL'):
    pass
elif mp3:
    L = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3]).decode())
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-35dB:d=0.15", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    sil = [(s, e) for s, e in zip(st, en) if s > 0.4 and e < L - 0.2]
    tot = sum(len(l) for l in lines); acc = 0; exp = []
    for l in lines[:-1]: acc += len(l); exp.append(L * acc / tot)
    cuts = []
    for e in exp:
        c = [(abs((s + en_) / 2 - e), (s, en_)) for (s, en_) in sil if not cuts or s > cuts[-1][1]]
        cuts.append(min(c)[1] if c else (e - 0.1, e + 0.1))
    speech_start = 0.05
    segs = []; prev = speech_start
    for (s, e) in cuts: segs.append((prev, s)); prev = e
    segs.append((prev, L))
    bounds = [0.0] + [(s + e) / 2 for (s, e) in cuts]
    total = round(L + 1.6, 2)
    bounds.append(total)
    durs = [round(bounds[i + 1] - bounds[i], 3) for i in range(n)]
    T[vid] = {"durs": durs, "segs": segs, "total": total}
else:
    T[vid] = S7.est(vid)
json.dump(T, open(S7.TF, "w"), indent=1)
total = T[vid]["total"] if "total" in T[vid] else sum(T[vid]["durs"])
sd = os.path.join(HERE, "teil2", "_scenes", vid); os.makedirs(sd, exist_ok=True)
for f in os.listdir(sd):
    if f.endswith(".mp4"): os.remove(os.path.join(sd, f))
ns = len(S7.defs(vid, T[vid]["durs"]))
procs = []
for i in range(ns):
    procs.append(subprocess.Popen([sys.executable, os.path.join(HERE, "scenes9.py"), "render", str(i)]))
    if len(procs) == 2:
        for p in procs: p.wait()
        procs = []
for p in procs: p.wait()
S7.setup(vid)
missing = [i for i in range(ns) if not os.path.exists(os.path.join(sd, f"s{i}.mp4"))]
assert not missing, f"Szenen fehlen: {missing}"
open(os.path.join(sd, "list.txt"), "w").write("".join(f"file 's{i}.mp4'\n" for i in range(ns)))
wav = S7.S2.sfx(vid)
od = os.path.join(HERE, "ZOCKWISSEN_Reels_v2", vid); os.makedirs(od, exist_ok=True)
if mp3:
    out = os.path.join(od, f"{vid}_FERTIG.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(sd, "list.txt"), "-i", mp3, "-i", wav,
        "-filter_complex", f"[1:a]volume=1.0,apad[v];[2:a]volume=0.3[s];[v][s]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total},alimiter=limit=0.95[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-movflags", "+faststart", out], check=True)
else:
    out = os.path.join(od, f"{vid}_VORSCHAU_ohne_Stimme.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(sd, "list.txt"), "-i", wav,
        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", "-movflags", "+faststart", out], check=True)
S7.make_cover(vid, os.path.join(od, f"{vid}_COVER.png"))
open(os.path.join(od, "TTS_Text.txt"), "w").write("\n\n".join(lines) + "\n")
print("OK", out, total)
