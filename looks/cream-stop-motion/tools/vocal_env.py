"""Where does the vocal stem sing? One character per 1/12 s at a few thresholds (share of the loud level), to pick mouth_thr.
python vocal_env.py vocals.wav
"""
import subprocess, sys, shutil
import numpy as np

FF = shutil.which("ffmpeg") or sys.exit("ffmpeg not on PATH")
SR, FPS = 48000, 24
raw = subprocess.run([FF, "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
v = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
hop = SR // FPS
rms = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(len(v) // hop)])
p95 = np.percentile(rms, 95)
print(f"p95 {p95:.4f}  median {np.median(rms):.4f}  min {rms.min():.5f}")
for k in (0.12, 0.2, 0.3):
    on = rms[::2] > p95 * k  # the mouth updates on twos
    print(f"{k:4.2f} open {on.mean():4.0%} ", "".join("#" if x else "." for x in on))
print("     seconds  ", "".join(str(int(i / 12) % 10) if i % 12 == 0 else " " for i in range(len(rms[::2]))))
