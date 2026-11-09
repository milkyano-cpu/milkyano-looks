# Cream Stop-Motion

Clay-style characters in real stop-motion on a flat cream set: a new drawn pose on every beat, the mouth flapping on the voice, the picture boiling on twos, a brown caption above, one joke in 6-20 seconds.

## What you get

- Output: a short character skit or a trend remake on an existing viral sound, one or two characters on stage.
- Aspect: 9:16, 1080x1920, 24 fps (the image updates on twos, so 12 drawings a second).
- Length: 6-22 s (most 6-20 s). 3-9 spoken lines (4-8 is the sweet spot), at most 260 voiced characters (60-200 typical).
- Delivered files: one H.264 mp4 (CRF 16, AAC 192k, -14 LUFS), the pose contact sheets (`alpha_sheet.jpg` per character), the episode json, and a one-line post caption.

## The look in detail

### Type

| Role | Font (default) | Size | Treatment |
|---|---|---|---|
| Caption | Inter Bold (original: Helvetica Neue Bold) | 46 px | `caption_ink`, no outline, no shadow on the cream set; centred x 540, line height 1.3x, block centred on y 590-600 |
| Punchline caption | same | 46 px | may move up to y 450 to sit above a bigger pose |
| Handle | same | 30 px | `handle_ink`, centred at y 1840 (80 px from the bottom) |
| Caption on a painted set | same | 46 px | light ink (white) over a soft drop shadow: blur 4, offset (2, 3), alpha 190/255 |

Captions are sentence case, punctuation allowed, at most 40 characters and 30 on a line, at most two lines (`\n` breaks). They carry the key words of the line and may shorten it ("Wait. That's MY pillow!"). A silent reaction beat often has the caption "...". CAPITALS on one word at most.

### Colour roles

| Role | Default | Use |
|---|---|---|
| `set_bg` | #FCF4DB (252, 244, 219) | flat cream set, full frame |
| `caption_ink` | #816B4C (129, 107, 76) | caption text |
| `handle_ink` | #282828 | handle at the bottom |
| `floor_shadow` | rgb(150, 120, 80) at alpha 50/255 | soft ellipse under each character's feet |
| `mark_tick` | #F6C440 | "!" surprise strokes beside the head |
| `mark_heart` | #F4728A | hearts on a soft moment |
| `pose_backdrop` | flat mid-grey | backdrop the pose generator draws on, cut out afterwards; flat pure white for a character dressed in grey; never white for a white character |

### Motion

All counts at 24 fps.

- **Stop-motion, never puppetry.** Every beat is a real drawn pose. A new feeling = a new pose; no change in feeling = the same pose again. Nothing is slid, scaled, bounced or swayed as a whole.
- **On twos.** The whole picture updates every 2 frames.
- **Boil.** Each character jitters on every 2-frame step by a seeded random offset: x +-3 px, y +-2 px, rotation +-0.8 deg.
- **Mouth flap.** Each pose that talks is a pair: `_c` mouth closed and `_o` mouth open. The frame shows `_o` when the voice RMS on that step is above the threshold and the step is not every third one (open, open, closed rhythm), so the mouth flaps rather than staying open. Speech threshold: `max(0.02, 0.6 x the 60th percentile RMS)`. Songs: drive the mouth from a vocal stem, threshold `max(0.01, 0.25 x the 95th percentile)`, so the mouth rests in vocal gaps. Only the character in "who" talks.
- **Squash-pop on a new pose.** When a character's pose changes from the previous beat, it scales `1 + 0.06 x e^(-14t)` for the first 0.25 s (6 f): width x s, height / sqrt(s). Tiny, quick.
- **Marks.** Ticks: three strokes 9 px wide at -50, -15 and 20 deg, from 34 px out to 62 px (68 px on alternate steps, so they wobble on twos), centred 0.42 x character height right of the speaker and 0.8 x character height above the feet. Hearts: one 36-size heart above the head bobbing 6 px on twos, four 22-size hearts floating up 120 px and shrinking 40 % at 0.6 cycles a second around the character.
- **"More crazy" variant.** A pose change on nearly every hit of the sound (every 0.15-0.25 s = 4-6 f), a big angle jump each time, 15 or more distinct poses.
- **One camera.** No camera moves, no zooms, no cuts to a closer framing that scales the set and the character differently. A reference's close-up beat becomes a full-body pose of that feeling.
- No motion blur (stop-motion holds).

### Captions

- One caption per beat, every beat has one, above the characters at y 590-600 (bottom of the head room), two lines at most.
- Timed to the beat: on screen from the beat's start to the next beat's start.
- Written in the line's words, cut to the key words; the punchline caption lands with the punchline beat.

### Graphics and elements

- **Set.** Full-frame `set_bg`, nothing else on it. No props, emoji, labels, photos or flying elements. A place or a time ("3 a.m.", "the office") goes in a line or the caption's first line ("6:00 AM\nFive more minutes...").
- **Characters.** Cut-outs (alpha) with the feet pinned to one point across all poses. Height 640 px alone, about 600 px for two on stage. Feet line y 1290. One character at x 0.5; two at x 0.29 and 0.71 (at least 0.4 apart), the right one usually mirrored to face the left. At most two on stage. Floor shadow: ellipse 340 x 36 px centred on the feet line.
- **Hero prop (optional).** One object only, and it exists only inside a pose's words ("hugging a long soft pillow as tall as his body with both arms"), drawn by the pose generator from a second reference image.
- **Painted-set variant (trend remake that copies the reference's composition).** A background drawn from words alone at 720x1280 replaces the cream. One camera for the whole episode. Lying characters seen from above are placed by their centre and turned, with a soft drop shadow (blur 9, alpha 0.4, offset 10, 14). Shower water is drawn as 70 streaks redrawn on twos. Mix pose sets only at matched heights (measure the alpha boxes).
- **Handle.** Small, bottom centre, every frame.

### Sound

- Voice: one take per line from a TTS voice per character (one voice per character slot), at most one audio tag per line ([sighs], [gasps], [yawns]), "..." for a pause. Takes are trimmed at -40 dBFS with 30 ms padding. Lead-in 0.3 s before the first line; 0.6 s after the last.
- Beat timing in a skit: `hold` before the take (0.3-0.5 s for a deadpan answer), the take, then `tail` (default 0.15 s; 0.8-1.0 s after the punchline so it breathes). Silent beats last 0.4-3 s (default 1 s).
- Trend remake: the original sound is the track; beats are cut on its word timings and snapped to its onsets.
- SFX: a few that land on something, not one every beat. Pop at -14 dB when a character snaps into a new pose on a beat that matters; boing at -8 dB or a whoosh for a surprise; sparkle at -10 dB, 0.05 s in, on a soft moment; a record scratch at -3 dB on a "caught you". At most two at once.
- Mix: voice track (mono, panned to both sides at full level) + SFX, gain found in two passes to -14 LUFS integrated, brickwall limiter at -3 dBFS (0.708) because AAC overshoots, true peak at most -1 dBTP on the encoded file (re-encoded with a lower ceiling if not), AAC 192k 48 kHz stereo. No music bed in skits.

### Pacing and cut rhythm

- Setup line spoken inside the first 1-2 s (first word within the first second). No intro.
- One joke, building to one punchline, the last line lands it.
- Short lines that sound said: a 30-character line takes about 2.5 s.
- Pose changes only on feeling changes (or on every hit in the "more crazy" variant). 10-18 drawn frames is a normal episode, 24 at most.
- No cuts: one continuous camera.

## Do / Don't

Do:
- A real drawn pose per beat, a closed/open mouth pair for every pose that talks.
- Boil on twos, flap on the voice, a small squash on a new pose.
- One set, one camera, one joke, two characters at most.
- Captions in brown ink above the characters, sentence case.
- Keep it PG and swear-free; a post caption in lowercase that makes people tag a friend, no hashtags.
- Check every pose sheet before trusting a render (wrong colour, extra paws, drifted prop: redraw that frame).

Don't:
- Slide, scale, bounce or sway one still image around (the retired puppet look).
- Camera moves, zooms that scale the set and character differently, emoji, labels, flying props, outlined captions, pills.
- Lying, sitting or jumping poses on the cream set (the generator draws standing figures; a nap is eyes closed while standing).
- Pose words that ask for a leg straight up or a bicycle (the generator draws a pillar, or wheels).
- Copying another account's characters, lines or drawings: borrow structure only.
- Swearing, even mild; jokes about death, war, guns, drugs, alcohol, vaping or sex.

## How to make it

1. Write the episode: kind (skit format or trend remake), 4-8 beats, each with who, text, caption, cast (pose name, x, talks, flip), hold/tail or dur, marks and sfx. Show the script before spending on voice or drawings.
2. Trend remake: download the reference (`instagram-download`), extract the sound (`ffmpeg -i ref.mp4 -vn -ac 2 -ar 48000 sound.wav`), get word timings with `tools/words.py` and hits with `tools/onsets.py`, cut beats on them. For a song, split vocals with Demucs (`--two-stems vocals`) and check gaps with `tools/vocal_env.py` before setting `mouth_thr`.
3. Skit: voice each line once with the character's TTS voice (one take), save each as a file per beat.
4. Draw poses: one poses file per character (reference image, look anchor, a fixed seed, `chain: false`, size 768x1024, a suffix asking for front view, full body centred, standing, the backdrop colour, soft even studio light, clay 3D render, exactly two arms and two paws). Image-edit model (FLUX.2 klein class, 4 steps) per frame from the clean reference.
5. Cut out every frame (BiRefNet-HR class matting), drop specks under 2 % of the body, pin the feet to one bottom-centre point with a 20 px margin, export PNGs and an `alpha_sheet.jpg`. Look at the sheet; redraw bad frames.
6. Composite with `tools/ep_render.py ep.json skin.json`.
7. QC: a 6-frame contact sheet, loudness with `earshot` measure (-14 LUFS, true peak at most -1 dBTP), the right mouth moving on each line, captions on the right beats, characters the same size. Trend remakes: `tools/cmp.py ref.mp4 ours.mp4 sheet.jpg t1 t2 ...` (reference on top) and look for anything a real camera could not film.
8. Deliver the mp4 with the post caption. Revisions are `R1`, `R2`; another take or hook is a variation `V2`.

## Skin slots

| Slot | Controls |
|---|---|
| `characters` | list of character slots: name, reference image, look anchor words, voice id, personality, speaking style, backdrop colour, pose-id prefix |
| `hero_prop` | the one allowed object: its pose words and reference image (optional) |
| `set_bg` | cream set colour |
| `caption_ink` | caption text colour |
| `handle_ink` | handle text colour |
| `mark_tick` | colour of the "!" ticks |
| `mark_heart` | colour of the hearts |
| `font_caption` | caption and handle font file |
| `handle_text` | the account handle printed at the bottom |
| `tts_model` | voice model used for every line |
| `sfx_kit` | folder holding the named SFX wavs (pop, boing, whoosh, sparkle, scratch) |
| `banned_words` | words the script and poses must never use |
| `post_caption_style` | example post captions for the account |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this description (Markdown) |
| `look.json` | machine-readable look spec (JSON) |
| `skin.example.json` | neutral demo skin filling every slot (JSON) |
| `tools/ep_render.py` | Python 3 (numpy, Pillow, ffmpeg on PATH): the episode compositor; `python ep_render.py ep.json [skin.json]`; brand colours, font and handle come from the skin |
| `tools/words.py` | Python 3 (faster-whisper large-v3, CUDA): word timings of a trend sound |
| `tools/onsets.py` | Python 3 (numpy, ffmpeg): onset times of a sound, strongest marked `*`, to snap pose changes to hits |
| `tools/vocal_env.py` | Python 3 (numpy, ffmpeg): where a vocal stem sings at a few thresholds, to pick `mouth_thr` |
| `tools/cmp.py` | Python 3 (Pillow, ffmpeg): side-by-side QC sheet, reference on top, our render below |
