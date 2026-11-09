# Tempo + energy map of a track (and its drum stem if present). python beat.py <track.mp3> [drums.mp3]
import sys, subprocess, numpy as np
SR = 22050
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
x = load(sys.argv[1]); dur = len(x) / SR
hop = 512; n = len(x) // hop
fr = np.lib.stride_tricks.sliding_window_view(x[:n * hop + 1024], 1024)[::hop][:n] * np.hanning(1024)
S = np.abs(np.fft.rfft(fr, axis=1)); S = np.log1p(S * 10)
flux = np.maximum(0, np.diff(S, axis=0)).sum(1); flux = (flux - flux.mean()) / (flux.std() + 1e-9)
fps = SR / hop
ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]
lags = np.arange(len(ac)) / fps; bpms = 60 / np.maximum(lags, 1e-9)
m = (bpms > 70) & (bpms < 180); bpm = bpms[m][np.argmax(ac[m])]
def win_rms(v, w, step):
    c = np.concatenate([[0], np.cumsum(v.astype(np.float64) ** 2)])
    idx = np.arange(0, len(v) - w, step)
    return np.sqrt((c[idx + w] - c[idx]) / w)
rms = win_rms(x, SR // 2, SR // 2)
db = 20 * np.log10(rms + 1e-6)
print(f"dur {dur:.1f}s  bpm ~{bpm:.1f}  beat {60/bpm:.3f}s  bar {240/bpm:.2f}s")
print("energy dB every 0.5s:")
for i in range(0, len(db), 16): print(f"{i*0.5:6.1f}s " + " ".join(f"{v:4.0f}" for v in db[i:i+16]))
if len(sys.argv) > 2:
    d = load(sys.argv[2]); dr = win_rms(d, SR // 2, SR // 2)
    ddb = 20 * np.log10(dr + 1e-6)
    print("drums dB every 0.5s:")
    for i in range(0, len(ddb), 16): print(f"{i*0.5:6.1f}s " + " ".join(f"{v:4.0f}" for v in ddb[i:i+16]))
