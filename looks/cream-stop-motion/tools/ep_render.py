"""Stop-motion episode compositor: pose cut-outs on a flat set, lip flap from the voice track,
on-twos boil, captions, small marks, SFX, loudness-normalised mix.
python ep_render.py ep.json [skin.json]  ->  <out>.mp4 (1080x1920, 24 fps)
skin.json (optional) supplies the brand: set_bg, caption_ink, mark_tick, mark_heart, handle_ink (hex), font_caption (ttf),
handle_text. A key set in ep.json ("bg", "ink", "font", "handle") wins over the skin.
ep.json: {"poses": dir of pinned alpha PNGs, "ids": [pose ids in file order]   (one character; or "sets": ["epNN_poses_a.json",
          {"spec": "epNN_poses_b.json", "char_h": 600}, ...] for several characters, every frame id unique across them;
          {"dir", "ids"} also works), "sound": wav (a trend sound) OR a "take" on each spoken beat (a skit:
          the voice track is built from the takes), "sfx_dir": dir, "font": ttf, "bg": [r,g,b], "ink": [r,g,b],
          "handle": "@handle", "out": mp4,
          "beats": [{"t0": s, "t1": s (sound mode; skit mode times itself), "pose": "wave" (one character) or
                     "cast": [{"pose": "a_hope", "x": 0.3, "talks": true, "flip": false}, ...],
                     "take": mp3/wav, "hold": s before the take, "tail": s after it, "dur": s for a silent beat,
                     "caption": "...", "cap_y": px, "marks": "ticks"|"hearts"|null, "sfx": [[name, at, gain_db]], "talk_end": s}]}
A pose id P needs P_c (mouth closed) and P_o (mouth open) when it talks; a pose that never talks needs P_c only.
A painted set (trend remakes that copy the reference's composition): "bg_img": png replaces "bg"; a beat's
"bg_zoom": [zoom, fx, fy] frames a closer shot of it. A cast member can carry "y" (its bottom
edge, px; a medium or close-up set runs off the frame bottom), or "cy" + "rot" (top-down: a lying character placed and turned
by its own centre, with a soft drop shadow). A beat's "water": {"x": 0.5, "top": px, "to": px, "w": px} pours shower water.
On a painted set use a light "ink" with "cap_shadow": [r, g, b, alpha] (the brown ink vanished on tiles and wood).
"mouth": a vocal stem (Demucs) for a song: the mouth follows the singing, not the music ("mouth_thr": share of its
loud level that opens the mouth, default 0.25).
"""
import json, math, random, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

FFMPEG = shutil.which("ffmpeg") or sys.exit("ffmpeg not on PATH")
ep = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
skin = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else {}


def rgb(h):  # "#RRGGBB" -> [r, g, b]
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


for sk, ek, conv in (("set_bg", "bg", rgb), ("caption_ink", "ink", rgb), ("font_caption", "font", str), ("handle_text", "handle", str)):
    if sk in skin and ek not in ep:
        ep[ek] = conv(skin[sk])
missing = [k for k in ("bg", "ink", "font", "handle") if k not in ep]
assert not missing, f"set {missing} in ep.json or pass a skin.json"
TICK = tuple(rgb(skin.get("mark_tick", "#F6C440")))
HEART = tuple(rgb(skin.get("mark_heart", "#F4728A")))
HANDLE_INK = tuple(rgb(skin.get("handle_ink", "#282828")))
W, H, FPS, SR = 1080, 1920, 24, 48000
BG, INK = tuple(ep["bg"]), tuple(ep["ink"])
CHAR_H, FEET, CAP_Y = ep.get("char_h", 640), ep.get("feet", 1290), ep.get("cap_y", 600)
font = ImageFont.truetype(ep["font"], ep.get("cap_px", 46)); small = ImageFont.truetype(ep["font"], 30)

poses = {}
for st in ep.get("sets") or [dict(dir=ep["poses"], ids=ep["ids"])]:
    st = dict(spec=st) if isinstance(st, str) else st
    if "spec" in st:  # a character's poses json: its cut-outs and its frame ids, in their order
        sp = json.loads(Path(st["spec"]).read_text(encoding="utf-8"))
        st = dict(st, dir=Path(sp["out"]) / "alpha", ids=[f["id"] for f in sp["frames"]])
    for i, pid in enumerate(st["ids"]):
        assert pid not in poses, f"pose id {pid} is used twice"
        im = Image.open(Path(st["dir"]) / f"{i:02d}.png").convert("RGBA")
        h = st.get("char_h", CHAR_H)
        poses[pid] = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def pcm(path):
    raw = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def trim(x, db=-40, pad=0.03):  # ElevenLabs takes carry silence at both ends (same rule as brainrot/prep.py)
    loud = np.flatnonzero(np.abs(x) > 10 ** (db / 20))
    return x if not len(loud) else x[max(loud[0] - int(pad * SR), 0):min(loud[-1] + int(pad * SR), len(x))]


if "sound" not in ep:  # a skit: one track from the takes, each beat timed by its own take
    parts, t = [], ep.get("lead", 0.3)
    for b in ep["beats"]:
        b["t0"] = t
        if b.get("take"):
            x = trim(pcm(b["take"]))
            parts.append((t + b.get("hold", 0.0), x))
            t += b.get("hold", 0.0) + len(x) / SR + b.get("tail", 0.15)
        else:
            t += b.get("dur", 1.0)
    ep["beats"][0]["t0"] = 0.0  # the lead-in silence belongs to the first beat
    for b, nxt in zip(ep["beats"], ep["beats"][1:] + [None]):
        b["t1"] = nxt["t0"] if nxt else 99
    track = np.zeros(int((t + ep.get("end", 0.6)) * SR) + 1, np.float32)
    for at, x in parts:
        track[int(at * SR):int(at * SR) + len(x)] += x
    ep["sound"] = str(Path(ep["out"]).with_suffix(".voice.wav"))
    subprocess.run([FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",  # both sides at full level, like
                    "-af", "pan=stereo|c0=c0|c1=c0", ep["sound"]],  # a mono clip in a stereo timeline (the default upmix is -3 dB)
                   input=np.clip(track, -1, 1).tobytes(), check=True)
for b in ep["beats"]:
    print(f"  {b['t0']:6.2f}-{min(b['t1'], 99):6.2f}  {b['caption'][:40]!r}", flush=True)

# voice envelope (RMS per frame) drives the mouth
a = pcm(ep["sound"])
dur = len(a) / SR; N = int(dur * FPS)
hop = SR // FPS
v = np.pad(pcm(ep["mouth"]), (0, N * hop)) if ep.get("mouth") else a  # a vocal stem: the mouth rests in the song's vocal gaps (27 Oct)
rms = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(N)])
thr = max(0.01, np.percentile(rms, 95) * ep.get("mouth_thr", 0.25)) if ep.get("mouth") else max(0.02, np.percentile(rms, 60) * 0.6)

prev = None  # a character pops (tiny squash) only when its pose changes from the beat before
for b in ep["beats"]:
    b["cast"] = b.get("cast") or [dict(pose=b["pose"], x=0.5, talks=True)]
    for k, c in enumerate(b["cast"]):
        c["_pop"] = not prev or k >= len(prev) or prev[k]["pose"] != c["pose"]
    prev = b["cast"]


def caption(text):
    lines = text.split("\n"); lh = round(font.size * 1.3)
    im = Image.new("RGBA", (W, lh * len(lines) + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, ln in enumerate(lines): d.text((W / 2, 10 + lh * k + lh / 2), ln, font=font, fill=INK, anchor="mm")
    sc = ep.get("cap_shadow")  # [r, g, b, a]: light ink over a soft drop shadow on a painted set (27 Oct: brown ink vanished on tiles)
    if sc:
        sh = Image.new("RGBA", im.size, tuple(sc[:3]) + (0,)); sh.putalpha(im.getchannel("A").filter(ImageFilter.GaussianBlur(4)).point(lambda v: v * sc[3] // 255))
        out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.alpha_composite(sh.crop((0, 0, W - 2, im.height - 3)), (2, 3)); out.alpha_composite(im)
        im = out
    return im


def heart(d, cx, cy, s, col=HEART):
    pts = [(cx + s * 0.06 * 16 * math.sin(t) ** 3, cy - s * 0.06 * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))) for t in np.linspace(0, 2 * math.pi, 48)]
    d.polygon(pts, fill=col)


def ticks(d, cx, cy, step):  # the little yellow "!" strokes beside the head, wobbling on twos
    for k, ang in enumerate((-50, -15, 20)):
        r0, r1 = 34, 62 + (step % 2) * 6
        a_ = math.radians(ang)
        d.line((cx + r0 * math.cos(a_), cy - r0 * math.sin(a_), cx + r1 * math.cos(a_), cy - r1 * math.sin(a_)), fill=TICK, width=9)


caps = {b["caption"]: caption(b["caption"]) for b in ep["beats"]}
BGI = Image.open(ep["bg_img"]).convert("RGBA").resize((W, H), Image.LANCZOS) if ep.get("bg_img") else None
bgs = {}


def set_bg(z):  # the painted set at [zoom, fx, fy]: a closer shot is a crop of the same set
    if z not in bgs:
        cw, ch = W / z[0], H / z[0]
        x0 = min(max(z[1] * W - cw / 2, 0), W - cw); y0 = min(max(z[2] * H - ch / 2, 0), H - ch)
        bgs[z] = BGI.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS)
    return bgs[z].copy()


def put(fr, p, x, y):  # alpha_composite clipped to the frame (close-ups run off its edges)
    box = (max(0, -x), max(0, -y), min(p.width, W - x), min(p.height, H - y))
    if box[0] < box[2] and box[1] < box[3]:
        fr.alpha_composite(p, (x + box[0], y + box[1]), box)


tmp = Path(tempfile.mkdtemp())
rng = random.Random(7)
for f in range(N):
    t = f / FPS; step = f // 2  # stop-motion: the image updates on twos
    b = next((x for x in ep["beats"] if x["t0"] <= t < x["t1"]), ep["beats"][-1])
    talking = rms[f - f % 2] > thr and t < b.get("talk_end", b["t1"])
    since = t - b["t0"]
    fr = set_bg(tuple(b.get("bg_zoom", (1, 0.5, 0.5)))) if BGI else Image.new("RGBA", (W, H), BG + (255,))
    focus = W / 2
    for k, c in enumerate(b["cast"]):
        cx = W * c.get("x", 0.5)
        im = poses[c["pose"] + ("_o" if talking and c.get("talks") and (step % 3) != 2 else "_c")]
        if "cy" in c:  # top-down: the body itself is the box it turns and sits by
            im = im.crop(im.getbbox())
        if c.get("flip"):
            im = ImageOps.mirror(im)
        r2 = random.Random(step if k == 0 else step * 31 + k); jx, jy, rot = r2.uniform(-3, 3), r2.uniform(-2, 2), r2.uniform(-0.8, 0.8)
        s = 1 + 0.06 * math.exp(-since * 14) * (1 if since < 0.25 and c["_pop"] else 0)  # tiny squash-pop on a new pose
        p = im.rotate(rot + c.get("rot", 0), resample=Image.BICUBIC, expand=True)
        p = p.resize((round(p.width * s), round(p.height / s ** 0.5)), Image.BILINEAR)
        x0 = round(cx - p.width / 2 + jx)
        y0 = round((c["cy"] - p.height / 2 if "cy" in c else c.get("y", FEET) - p.height + 10) + jy)
        if "cy" in c:  # lying on the set: a soft drop shadow, no floor ellipse; blurred inside a 30 px margin, or the box cut it straight (Ep06 V3)
            m = ImageOps.expand(p.getchannel("A"), 30)
            shd = Image.new("RGBA", m.size, (70, 50, 50, 0)); shd.putalpha(m.filter(ImageFilter.GaussianBlur(9)).point(lambda v: v * 0.4))
            put(fr, shd, x0 + 10 - 30, y0 + 14 - 30)
        elif "y" not in c:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - 170, FEET - 18, cx + 170, FEET + 18), fill=(150, 120, 80, 50))
            fr.alpha_composite(sh)
        put(fr, p, x0, y0)
        if c.get("talks") or len(b["cast"]) == 1:
            focus = cx
    wt = b.get("water")  # shower water: streaks from the head down, redrawn on twos like everything else
    if wt:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dv = ImageDraw.Draw(ov); r3 = random.Random(step * 7 + 3)
        for _ in range(wt.get("n", 70)):
            u = r3.random(); y = wt["top"] + u * (wt["to"] - wt["top"])
            x = W * wt["x"] + (r3.random() - 0.5) * wt["w"] * (0.35 + 0.65 * u)
            dv.line((x, y, x, y + r3.uniform(40, 110)), fill=(228, 244, 255, r3.randint(80, 160)), width=r3.choice((3, 4, 6)))
        fr.alpha_composite(ov)
    d = ImageDraw.Draw(fr)
    head_y = FEET - CHAR_H * 0.8
    if b.get("marks") == "ticks":
        ticks(d, focus + CHAR_H * 0.42, head_y, step)
    if b.get("marks") == "hearts":
        heart(d, focus, FEET - CHAR_H - 40 - 6 * (step % 2), 36)
        for k, (hx, hy) in enumerate(((-300, -330), (300, -300), (-260, -120), (280, -90))):
            u = ((t - b["t0"]) * 0.6 + k * 0.25) % 1
            heart(d, focus + hx + 10 * math.sin(6 * u + k), FEET + hy - 120 * u, 22 * (1 - 0.4 * u))
    c = caps[b["caption"]]; fr.alpha_composite(c, (0, round(b.get("cap_y", CAP_Y) - c.height / 2)))
    d.text((W / 2, H - 80), ep["handle"], font=small, fill=HANDLE_INK, anchor="mm")
    fr.convert("RGB").save(tmp / f"{f:04d}.png")
    if f % 48 == 0:
        print(f"  frame {f}/{N}", flush=True)

# audio: the sound (or the voice track) + SFX, -14 LUFS
inputs, filt = ["-i", ep["sound"]], []
k = 1
for b in ep["beats"]:
    for name, at, gain in b.get("sfx", []):
        inputs += ["-i", str(Path(ep["sfx_dir"]) / f"{name}.wav")]
        ms = round((b["t0"] + at) * 1000); filt.append(f"[{k + 1}:a]volume={gain}dB,adelay={ms}|{ms}[s{k}]"); k += 1  # input 0 is the frames, 1 the sound
mix = "".join(f"[s{i}]" for i in range(1, k))


ceil = 0.708  # -3 dBFS, not -1: AAC overshoots a dense song by 2-3 dB (Ep05, 27 Oct); lowered below if it still does


def chain(gain):  # the mix at a gain, a brickwall at the ceiling, always stereo
    return ";".join(filt + [f"[1:a]{mix}amix=inputs={k}:normalize=0:duration=first,volume={gain:.2f}dB,"
                            f"alimiter=limit={ceil:.3f}:attack=3:release=60:level=0:latency=1,aresample=48000,"
                            "aformat=channel_layouts=stereo[a]"])


def lufs(gain):  # ebur128 reads what earshot reads (loudnorm's own meter read 0.8 LU hot on Ep04)
    e = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", *inputs, "-filter_complex",
                        chain(gain) + ";[a]ebur128=framelog=quiet[m]", "-map", "[m]", "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1])


def mux(gain):
    subprocess.run([FFMPEG, "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%04d.png"), *inputs, "-filter_complex", chain(gain),
                    "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "-shortest", ep["out"]], check=True)


def true_peak(path):  # of the encoded file: AAC overshoots the limiter, 2-3 dB on a dense song (Ep05, 27 Oct)
    e = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace").stderr
    return float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])


gain, target = 0.0, ep.get("lufs", -14)
for _ in range(2):  # -14 LUFS (or "lufs"); the second look adds back what the limiter took from a big boost
    gain += target - lufs(gain)
mux(gain)
over = true_peak(ep["out"]) + 1.2
if over > 0:  # above -1 dBTP after AAC: a lower ceiling (a lower gain alone leaves the peaks on it), the gain found again
    print(f"  true peak {over - 1.2:+.1f} dBTP: ceiling {over:.1f} dB lower, encoded again", flush=True)
    ceil *= 10 ** (-over / 20)
    for _ in range(2):
        gain += target - lufs(gain)
    mux(gain)
shutil.rmtree(tmp, ignore_errors=True)  # the frames (~250 MB for 20 s) would fill the laptop's C: (27 Oct)
print("DONE", ep["out"], N, "frames")
