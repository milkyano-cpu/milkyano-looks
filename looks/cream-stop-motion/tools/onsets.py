"""Onset times of a sound (spectral flux peaks), to snap pose changes to the hits.
python onsets.py sound.wav [z]  ->  one line of times in seconds, the strongest marked with *
"""
import subprocess, sys, shutil
import numpy as np

FF = shutil.which("ffmpeg") or sys.exit("ffmpeg not on PATH")
SR, HOP, N = 22050, 220, 1024
raw = subprocess.run([FF, "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
fr = np.lib.stride_tricks.sliding_window_view(x, N)[::HOP] * np.hanning(N)
S = np.log1p(10 * np.abs(np.fft.rfft(fr, axis=1)))
flux = np.maximum(S[1:] - S[:-1], 0).sum(axis=1)
flux = (flux - flux.mean()) / (flux.std() + 1e-9)
t = (np.arange(len(flux)) + 1) * HOP / SR
z = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
peaks = [i for i in range(3, len(flux) - 3) if flux[i] > z and flux[i] == flux[i - 3:i + 4].max()]
assert peaks, "no onsets above z"
print(" ".join(f"{t[i]:.2f}{'*' if flux[i] > 2.5 else ''}" for i in peaks))
