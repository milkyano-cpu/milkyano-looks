# Lab Notebook

Faceless explainer reels drawn like a clean lab notebook: cream paper, a faint grid, ink line art drawing itself on, one accent colour, thin giant numbers, and a narrator who never shuts up without something new landing.

## What you get

- Output: faceless educational motion-graphic reel, narrated VO, no presenter, no footage.
- Aspect: 9:16, 1080x1920, 30 fps delivery (finals rendered at 120 fps and blended down for motion blur).
- Length: 60-110 s. An intro episode runs about 90 s; scenes are 5-13 s each.
- Delivered: `<episode>_final.mp4` (H.264 CRF 16, AAC 192k), plus the episode spec, the exact TTS script, the VO takes, `vo.mp3` and `mix.wav` kept with the delivery.

## The look in detail

### Type
- One sans family across everything. Default: Inter (variable, weights 200-800).
- Weights: 800 headlines, 700 titles and captions, 200 (ExtraLight) for big numbers.
- Title: 2 lines, 66 px, weight 800, line-height 1.12, letter-spacing -0.015em, centred, top of the title band at y 470. Line 2 is the accent colour, line 1 ink.
- Big stat number: 230 px, weight 200, letter-spacing -0.03em, accent colour, tabular figures, top at y 670. Its label 38 px / 700 at y 910.
- Caption: one line, 42 px / 700 in ink, highlighted words 800 in the accent. Never wraps: a caption wider than 900 px shrinks its font to fit.
- Pills and chips: 26-34 px / 700. List rows 42 px. Quote cards 34 px / 600 body, 24 px source tag.

### Colour roles
| role | default | used for |
|---|---|---|
| paper | `#F5F3EC` | the cream base |
| paper_glow | `#FFFFFF` | soft warm glow drifting behind the board (900 px radial at 68 %) |
| grid | `rgba(0,0,0,0.035)` | 1 px grid lines every 54 px, centred |
| ink | `#000000` | line art, titles, captions |
| text | `#3B3A35` | labels, secondary text |
| muted | `#8C8A80` | counts, axis text, neutral people dots, the neutral curve |
| line | `#DFDDD0` | bars, bonds, chip outlines, timeline track |
| accent | `#2563EB` | the one identity colour: title line 2, hot words, hero orb, result bar |
| accent_light | `#5B8DEF` | orb rims, dashed slots |
| accent_deep | `#1D4ED8` | gradient ends, pill text |
| accent_soft | `#DCE7FD` | pill and step backgrounds, chip halos |

Only the accent family carries colour. Everything else is neutral. Never put the accent on an accent background.

### Motion (30 fps; durations in frames)
- Default entrance: `power3.out`, 15-23 frames (0.5-0.75 s), from opacity 0 with a 10-30 px rise.
- Orbs: scale 0.55 to 1 with a 14 px blur clearing, 23 frames `power3.out`. Hero orb pulse ring: 48 frames `power2.out`, scale 1 to 1.55.
- Line art draws on with `stroke-dashoffset` 1 to 0: rings 33 frames `power3.out`, body/organ drawings 45 frames `power2.inOut` with 4-frame stagger, links 18 frames `power2.inOut`, curves 42 frames.
- Pop-ins (beads, slots, list numbers): `back.out(1.6-2)`, 13-14 frames.
- Count-ups: `power3.out`, tabular figures so width never jumps. A count tick is one 1.06x bump, 5 frames out and back.
- Sparks travel along links: 30 frames `power2.inOut`, 9-frame rest, repeated while the scene is up.
- Scene transitions: `fade` (default) 10 frames in `power2.out`, 9 frames out `power2.in`; `pan` sideways 0.55 of frame width, 28 frames `power3.inOut` (use when the idea continues); `cut` only for scene 1.
- Hold drift: the whole board pushes in 1.0 to 1.035 across each scene, `power1.inOut`, so no frame is dead still.
- Dead-air move: a soft accent bloom (680 px radial, peak opacity 0.3) behind the newest element, 14 frames in, 24 frames out.
- Caption: fade up 8 px over 4 frames `power2.out`, off on the next caption.
- Title: lines rise 26 px with an 8 px blur clearing, 18 frames `power3.out`, 4-frame stagger.
- Motion blur: final render at 120 fps, two sub-frames blended per output frame (180° shutter at 30 fps), every 4th frame kept.
- Only the new element moves on a beat. The board never scales or nudges as a whole.

### Captions
- One line, one short spoken chunk (24 characters max), centred at y 1330.
- A chunk breaks at punctuation, at 24 characters, or at a pause over 0.45 s. A chunk that would show under 0.45 s merges into the one before it; any caption under 0.4 s is a build error to fix.
- A caption stays up to 0.6 s past its last word or until the next one starts.
- Highlight: the keyword in the accent at 800 weight. Text has a paper-coloured halo (18/6/2 px) so it reads over the grid.
- Voice directions in the script are never captioned.

### Graphics and elements
Layout bands on 1080x1920: title band 470-620 (nothing drawn above ~640 besides the title), visual centre at (540, 930), source pill at y 1240-1260, caption at y 1330. Corner mark 40 px high at (64, 96).

The fixed data-to-visual mapping, one per kind of fact:

| the VO says | show |
|---|---|
| a thing, a compound, an actor | a pearl orb; the hero is the full-accent orb |
| X contains / works on N parts | a ring (radius ≤ 290 px) with the parts as orbs inside |
| X signals to Y | links between orbs, sparks travelling along them |
| a sequence or a length | beads in a row with a count label |
| long vs short | two bead chains, long neutral vs short accent |
| where in the body or system | line-art drawing plus an orb marker |
| a mechanism | receptor: the ligand flies in, docks, ripples, signal pills fan out |
| N people / participants | a 20x5 grid of tiny people (22x30 px) counting up to the real N |
| a duration | a filling timeline (14 px track) with ticks and a counter |
| a source | a source pill that stays up |
| a headline number | big ExtraLight count-up, then the bar |
| control vs treatment | a second bar landing on the word that names the control |
| a share of a group | that share of the people grid turns accent |
| a count of things | count-up, then the items break out as chips |
| how strong the evidence is | a staircase; the level discussed turns accent |
| a list | numbered rows, faint numbers waiting, each lighting on its word |
| a trend | a line chart drawing on, the key series in the accent |
| the hook question | hero orb with satellites, then focus dims the rest to 0.28 |

Orbs are pearl spheres: white highlight at 34 % / 28 %, tinting toward `accent_light` at the rim, soft accent shadow. Beads and people dots use flat fills and shadows, never gradients (more than ~40 gradient/filter/clip-path elements in a scene renders black).

### Sound
- VO normalised to -16 LUFS. Music bed -31 LUFS (15 dB under the voice), never ducked or compressed, 1 s fade in, 2.5 s fade out.
- SFX kit, each peak-normalised then set by kind: pop -21 dB on every landing (aligned on onset), whoosh -19 dB on every pan (aligned on its peak), tick -24 dB on count-ups, chime -18 dB when a stat lands, riser -15 dB into the hook (aligned on its peak).
- Master: -14 LUFS integrated, -1.2 dBTP, a gentle limiter (limit 0.86, attack 5 ms, release 80 ms) only catches stray peaks.
- Bed: one instrumental per episode, around 108 BPM.

### Pacing and cut rhythm
- Something new lands every 1-3 s. No stretch of VO over 1.6 s with nothing new landing (count-ups, colour changes and the end card are exempt).
- Every clause gets a visual, on the word that says it. Build the board up: setup pieces first, the result last and alone. Never show the result before the VO says it.
- Each scene's first visual lands at most 0.4 s after its first keyword. A scene never opens on an empty board while the line starts.
- Open on a question or a tension, never an introduction. End on one CTA line plus the end card, with a 1.6 s tail after the VO.

## Do / Don't

Do
- Keep one accent family. Neutral everything else.
- Draw line art on; let numbers count up in ExtraLight.
- Mark the beat on the real spoken word, never inside a number.
- Read the script aloud before building: spoken order must match visual order.

Don't
- Don't let two elements overlap, cover the caption, or run text out of its box.
- Don't scale the whole board on a beat. Only the new element moves.
- Don't use a second identity colour, photos, faces, or before/after imagery.
- Don't tween to CSS variable colours; tween to hex.
- Don't leave VO talking over a still board.

## How to make it

1. Pick the topic and gather the facts from one source set. Every number on screen must come from it.
2. Storyboard clause by clause with the mapping table above. Write a scene list: per scene the VO line, the 2-line title, the primitive or layered board, and a beat marker on each word where the next item lands.
3. Write the spoken script short and hook-first. Generate the VO in two takes (ElevenLabs or another narrator voice; set in the skin). Pick the take on pace and clean words.
4. Transcribe the take with word timings (Whisper / WhisperX) and align the beats to the words.
5. Build the HyperFrames composition from the scene list (`hyperframes` skills). Fix every dead-air warning by adding a beat and a layer; beat changes never need a new VO.
6. Mix VO, bed and SFX to the numbers in Sound (ffmpeg loudnorm + a limiter). Check with `earshot measure`.
7. `npx hyperframes lint` with 0 errors. Take snapshots at the late moment of every beat that matters and check the title band, the pill and the caption for collisions.
8. Render: `python tools/render.py <episode dir> --final` (120 fps ProRes, ffmpeg blend down to 30 fps, mux `mix.wav`). Launch it detached; a 90 s final takes about 40 min. Draft: no `--final`, 30 fps.
9. QC: duration, columns 1072-1079 are paper colour (HyperFrames' own MP4 encode can leave an 8 px black stripe, which is why `render.py` encodes with ffmpeg), a frame strip of a pan, audio length.
10. Deliver with `editor-grade-motion` QA rules.

## Skin slots

| slot | controls |
|---|---|
| `font_family` | the one font family (needs weights 200, 700, 800) |
| `font_file` | the variable font file used by the composition |
| `paper` | base background |
| `paper_glow` | the drifting glow colour |
| `grid` | grid line colour (keep alpha near 0.035) |
| `ink` | line art, titles, captions |
| `text` | secondary text |
| `muted` | counts, axes, neutral dots |
| `line` | bars, bonds, outlines |
| `accent` | the identity colour |
| `accent_light` | orb rims, dashed slots |
| `accent_deep` | gradient ends, pill text |
| `accent_soft` | pill and step fills |
| `corner_mark` | small mark top-left (file path or null) |
| `end_mark` | mark on the end card (file path or wordmark text) |
| `end_url` | URL pill on the end card |
| `end_note` | small line under the URL (empty to hide) |
| `cta_line` | the one spoken CTA line |
| `vo_voice` | narrator voice name or id |
| `vo_language` | VO and caption language, and which terms stay in English |
| `music_bed` | the instrumental bed file |

## Files in this folder

- `README.md`: this spec.
- `look.json`: the machine-readable defaults (type, colour roles, motion, captions, sound, pacing, bans, skin slots).
- `skin.example.json`: a neutral demo skin filling every slot.
- `tools/render.py`: Python 3. Renders a HyperFrames episode folder: draft at 30 fps, or `--final` at 120 fps with a 2-sub-frame blend to 30 fps, encodes H.264 with ffmpeg and muxes `mix.wav` (or `vo.mp3`). Needs Node (`npx hyperframes@0.8.141`) and ffmpeg. Usage: `python tools/render.py <episode dir> [--final] [--workers 1]`.
