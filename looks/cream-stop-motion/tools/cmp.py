"""Side-by-side QC for a trend remake: the reference reel on top, our render below, at the same times.
python cmp.py ref.mp4 ours.mp4 out.jpg t1 t2 ...
"""
import subprocess, sys, shutil
from PIL import Image

FF = shutil.which("ffmpeg") or sys.exit("ffmpeg not on PATH")
ref, ours, out, ts = sys.argv[1], sys.argv[2], sys.argv[3], [float(t) for t in sys.argv[4:]]
W, H = 240, 427


def grab(src, t):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return Image.frombytes("RGB", (W, H), raw)


sheet = Image.new("RGB", (W * len(ts), H * 2), "white")
for i, t in enumerate(ts):
    sheet.paste(grab(ref, t), (i * W, 0))
    sheet.paste(grab(ours, t), (i * W, H))
sheet.save(out, quality=88)
print("DONE", out)
