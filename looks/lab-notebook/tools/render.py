# Render an episode. HyperFrames renders a ProRes MOV intermediate (its own MP4 encode adds an 8 px black stripe on the
# right edge on this PC, checked 2026-10-12 on hyperframes 0.8.141; MOV/WebM are clean, a PNG sequence at 120 fps would
# need ~106 GB), then ffmpeg encodes the MP4 and muxes vo.mp3. ~14 GB temp for a 107 s final.
# Draft = 30 fps. Final = motion blur: 120 fps, 2 subframes blended per output frame (180-degree shutter at 30 fps),
# every 4th kept. Temp frames go to the system temp drive (C:), not the project drive.
# usage: python tools/render.py episodes/<ep> [--final] [--workers 1]
import pathlib, subprocess, sys, tempfile, shutil

ep = pathlib.Path(sys.argv[1]).resolve()
final = "--final" in sys.argv
workers = sys.argv[sys.argv.index("--workers") + 1] if "--workers" in sys.argv else "1"   # 1 when Premiere/AE are open
out = ep / "renders" / (ep.name + ("_final.mp4" if final else "_draft.mp4"))
out.parent.mkdir(exist_ok=True)
if out.exists():   # keep the last final: a small late fix is then a re-render of one scene + an ffmpeg stitch, not 30 min
    out.replace(out.with_name(out.stem + "_prev.mp4"))
fps = 120 if final else 30
tmp = pathlib.Path(tempfile.mkdtemp(prefix="cl_render_"))
try:
    subprocess.run([shutil.which("npx") or "npx", "--yes", "hyperframes@0.8.141", "render", str(ep), "-w", workers,
                    "--fps", str(fps), "--format", "mov", "-o", str(tmp / "hi.mov")], check=True)
    vf = "tmix=frames=2:weights='1 1',select='eq(mod(n\\,4)\\,0)',setpts=N/30/TB," if final else ""
    audio = ep / "mix.wav" if (ep / "mix.wav").exists() else ep / "vo.mp3"     # tools/mix.py soundtrack when present
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "hi.mov"), "-i", str(audio),
                    "-vf", vf + "format=yuv420p", "-r", "30", "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                    "-map", "0:v", "-map", "1:a", "-af", "apad", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print("->", out)
