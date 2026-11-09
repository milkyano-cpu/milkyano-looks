# Provenance: cream-stop-motion (Cream Stop-Motion)

Origin tag: adapted. Our own stop-motion pipeline, approved on HugGooling brain-rot Ep04 "U So Beautiful" (24 Oct 2026: "it's so good, dia stop motion"). Episode structure adapted from the DiEM Archive skit format (two characters, one joke, setup in the first two seconds, small caption, handle at the bottom).

## Inspo
- DiEM Archive (Instagram, @diemarchive): structure only.
- pocketduckk (Instagram): the source of Ep04's trend sound; research account for trend remakes.

## Source skills and paths
- `C:\Users\adeki\.claude\skills\huggooling-brainrot\SKILL.md`: the look, rules, trend/skit/painted-set/lip-sync/"more crazy" variants, make steps.
- `R:\BATMAN\brains\HugGooling\brainrot\show.json`: cast (voices, FLUX anchors, backdrops, widths), formats (reveal, chant, literal, hotline, wishes, expert), banned words, pun rule, limits (lines 3-9, 260 voiced chars, caption 40 / 30 per line, 6-22 s, 2 on stage, 24 frames).
- `R:\BATMAN\brains\HugGooling\brainrot\writer.md`: the daily script brief (beat schema, hold/tail, marks, SFX levels, post caption style, Ep03 example).
- Tools: `R:\Apps\Claude code\_CLIENTS\HugGooling\brainrot-account\stopmo\` (`ep_render.py`, `stopmo.py`, `alpha.py`, `words.py`, `onsets.py`, `vocal_env.py`, `cmp.py`, `bear_vo.py`, `make_ep.ps1`, `post_daily.py`, templates, `ep04.json`). The real numbers (24 fps, twos, boil, squash, caption 46 px at y 590-600, feet 1290, char 640, colours, -14 LUFS, ceiling 0.708) come from `ep_render.py` and `ep04.json`.
- `R:\Apps\Claude code\brainrot\` (`render.py`, `prep.py`, `poses\`): the retired Ep01-02 puppet renderer and the ComfyUI pose setup. Read for history only; the puppet look is banned in this look.
- Memory `feedback_stopmotion_not_sliding.md` (24 Oct 2026).

## Dates
- 20 Oct 2026: brief for the brain-rot account.
- Ep01-02: puppet look (Ep02 posted), retired.
- 24 Oct 2026: Ep04 stop-motion approved.
- 27 Oct 2026: painted-set trend remakes (Ep05 Shower Singer, Ep06 Bed Hog), one-shot rule, lip sync on a vocal stem, "more crazy" variant.
- 29 Oct 2026: cut-outs moved from rembg to BiRefNet-HR.

## Skins that exist today
One: the HugGooling brain-rot account. Values live in `R:\BATMAN\brains\HugGooling\brainrot\show.json` (five characters with ElevenLabs voice ids and FLUX anchors, the pillow prop, banned words, pun rule) and in each episode json (`bg` [252,244,219], `ink` [129,107,76], `handle` "@hug.gooling", Helvetica Neue Bold at `C:\Claude code\brainrot\fonts\` on the laptop). Character reference PNGs: `C:\Claude code\brainrot\src\<Name>.png` on the laptop.

## Tools
- Copied:
  - `tools/ep_render.py`: changes are a hard-coded ffmpeg path replaced by `shutil.which("ffmpeg")`, an optional second argument `skin.json` (set_bg, caption_ink, font_caption, handle_text fill the ep keys when the ep does not set them; mark_tick, mark_heart, handle_ink replace hard-coded colours), a clear assert when bg/ink/font/handle are missing, and character names removed from the docstring. Render logic unchanged. Smoke-tested on a dummy one-pose episode with the demo skin (28 frames, correct cream set, caption, ticks, handle).
  - `tools/words.py` unchanged; `tools/onsets.py`, `tools/vocal_env.py`, `tools/cmp.py` with the ffmpeg path replaced by `shutil.which`. No brand values in any of them.
- Left in place:
  - `stopmo.py` (ComfyUI at `C:\AI\ComfyUI_windows_portable`, model file names, laptop paths).
  - `alpha.py` (calls the BiRefNet venv at `C:\ClaudeWork\bike_cutout` on the laptop).
  - `make_ep.ps1`, `launch*.ps1`, `run_*.bat` (laptop orchestration).
  - `bear_vo.py` (fallback voices tied to the cast), `post_daily.py` (posts to the agency Slack thread).
  - `R:\Apps\Claude code\brainrot\render.py` / `prep.py` (retired puppet look).

## Not carried over
- Character reference images, voice ids, FLUX anchors, the pillow prop, the episode list and the pun rule (all skin).
- The fonts, SFX pack (Formatngedit pack plus OpenGameArt pops), and the BATMAN daily scheduler (`server\brainrot.py`).
- The ComfyUI graph and the BiRefNet cut-out as runnable tools (described in the README as steps with their settings).
