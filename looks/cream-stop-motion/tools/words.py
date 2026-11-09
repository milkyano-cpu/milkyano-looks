"""Word timings of a sound, to cut a trend remake into beats (laptop, GPU).
python words.py sound.wav  ->  one line per word: start end word (seconds)
"""
import os, sys
import torch
os.add_dll_directory(os.path.join(os.path.dirname(torch.__file__), "lib"))  # cuBLAS/cuDNN live in torch's lib folder
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")  # large-v3 times words better than turbo
segs, info = model.transcribe(sys.argv[1], word_timestamps=True)
print(f"# {info.language}, {info.duration:.2f} s")
for s in segs:
    for w in s.words:
        print(f"{w.start:6.2f} {w.end:6.2f} {w.word.strip()}")
