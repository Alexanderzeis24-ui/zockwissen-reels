"""python3 finalize11.py [voice.mp3]  -> with voice: exact sync + mix; without: 30 s preview."""
import sys, os, re, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import scenes14, scenes7 as S7
vid = sys.argv[1]; mp3 = sys.argv[2] if len(sys.argv) > 2 else None
lines = S7.SCRIPTS7[vid]; n = len(lines)
if mp3:
    L = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3]).decode())
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-35dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    lead = en[0] if st and st[0] < 0.05 else 0.0
    sil = [(s, e) for s, e in zip(st, en) if s > 0.4 and e < L - 0.15]
    tail = [s for s, e in zip(st, en) if e >= L - 0.15]
    speech_end = tail[0] if tail else L
    tot = sum(len(l) for l in lines); acc = 0; exp = []
    for l in lines[:-1]: acc += len(l); exp.append(lead + (speech_end - lead) * acc / tot)
    m = n - 1; K = len(sil); assert K >= m, f"nur {K} Pausen gefunden, brauche {m}"
    INF = 1e9
    cost = lambda i, j: abs((sil[j][0] + sil[j][1]) / 2 - exp[i]) - 1.5 * min(sil[j][1] - sil[j][0], 0.6)
    dp = [[INF] * K for _ in range(m)]; bk = [[-1] * K for _ in range(m)]
    for j in range(K): dp[0][j] = cost(0, j)
    for i in range(1, m):
        best = INF; bj = -1
        for j in range(K):
            if j > 0 and dp[i - 1][j - 1] < best: best = dp[i - 1][j - 1]; bj = j - 1
            if bj >= 0: dp[i][j] = best + cost(i, j); bk[i][j] = bj
    j = min(range(K), key=lambda q: dp[m - 1][q]); pick = []
    for i in range(m - 1, -1, -1): pick.append(j); j = bk[i][j]
    cuts = [sil[q] for q in reversed(pick)]
    if os.environ.get('CUTS'): cuts = [sil[int(q)] for q in os.environ['CUTS'].split(',')]
    segs = []; prev = lead + 0.02
    for (s, e) in cuts: segs.append((prev, s)); prev = e
    segs.append((prev, speech_end))
    total = round(L + 1.4, 2)
    bounds = [0.0] + [e - 0.06 for (s, e) in cuts] + [total]
    durs = [round(bounds[i + 1] - bounds[i], 3) for i in range(n)]
    T = S7.load_timing(); T[vid] = {"durs": durs, "segs": segs, "total": total}
    json.dump(T, open(S7.TF, "w"), indent=1)
    print("cuts", [round((s + e) / 2, 2) for s, e in cuts], "total", total)
else:
    T = S7.load_timing(); T[vid] = S7.est(vid); json.dump(T, open(S7.TF, 'w'), indent=1); total = round(T[vid]['total'], 2)
sd = os.path.join(HERE, "teil2", "_scenes", vid); os.makedirs(sd, exist_ok=True)
for f in os.listdir(sd):
    if f.endswith(".mp4"): os.remove(os.path.join(sd, f))
procs = []
for i in range(n):
    procs.append(subprocess.Popen([sys.executable, os.path.join(HERE, "scenes14.py"), "render", vid, str(i)]))
    if len(procs) == 2:
        for p in procs: p.wait()
        procs = []
for p in procs: p.wait()
missing = [i for i in range(n) if not os.path.exists(os.path.join(sd, f"s{i}.mp4"))]
assert not missing, f"Szenen fehlen: {missing}"
S7.setup(vid)
open(os.path.join(sd, "list.txt"), "w").write("".join(f"file 's{i}.mp4'\n" for i in range(n)))
wav = S7.S2.sfx(vid)
od = os.path.join(HERE, "ZOCKWISSEN_Reels_v2", vid); os.makedirs(od, exist_ok=True)
if mp3:
    out = os.path.join(od, f"{vid}_FERTIG_mit_Stimme.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(sd, "list.txt"), "-i", mp3, "-i", wav,
        "-filter_complex", f"[1:a]volume=1.0,apad[v];[2:a]volume=0.3,apad[s];[v][s]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total},alimiter=limit=0.95[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(total), "-movflags", "+faststart", out], check=True)
else:
    out = os.path.join(od, f"{vid}_VORSCHAU_ohne_Stimme.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(sd, "list.txt"), "-i", wav,
        "-filter_complex", "[1:a]volume=0.5,apad[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-t", str(total), "-movflags", "+faststart", out], check=True)
S7.make_cover(vid, os.path.join(od, f"{vid}_COVER.png"))
print("OK", out)
