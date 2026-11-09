# Glow Callout

Talking-head shorts where the key words pop on screen in a highlight colour with a soft additive bloom, over a dark scrim, with hard cuts and a light-line wipe between cut-out subjects.

## What you get

- Output: vertical talking-head short, ranked list ("top N"), product ride or shop tour, finished with captions, callouts, SFX, music bed and an end card.
- Aspect: 9:16, 1080x1920.
- Frame rate: follows the source. The measured look was built at 59.94 fps; some series ran at 30 fps. All frame counts below are at 59.94 unless marked.
- Length: 30 to 105 s (talking pieces and ranked lists). A hook-variant set is several videos with one identical body.
- Delivered files: H.264 mp4 (1080x1920, AAC 256 kb/s 48 kHz), Premiere XML with every graphic as its own ProRes 4444 alpha clip, SFX stem, music bed, the final SRT, a 720p phone preview.

## The look in detail

### Type

- One rounded display sans for every graphic and caption (`font_display`). One weight, never fake bold. Default: Nunito Black or any free rounded sans.
- Authored at 48 px, sized by scale. Tracking 0, leading 1.2.
- Type ladder on a 1080-wide frame (only these steps, max 3 levels per frame, at least 1.5x between levels):

| Level | px | Use |
|---|---|---|
| caption | 48 | running captions |
| support line 2 | 56-68 | the white tail of a two-line card (model, spec) |
| support line 1 | 104-114 | the coloured first line of a card |
| punch | 154 | one-word punch card |
| hero | 176-222 | price, the biggest word on a card |
| lockup exception | 330 / 200 | a hero number with a gradient word above it |

- Lines of one card stack tight: gap between the ink of one line and the next = 0.08 em of the lower line, not the font line height. Lead-in to hero ratio 1.6-2.2.
- A card's settled width stays at or under 80% of the frame (864 px), or the 116% overshoot runs off the edge.
- Social comment mock-ups only: Inter 39 px black on white, `Reply` Inter Medium 24 px #7D7D7D.

### Colour roles

| Role | Default | Meaning |
|---|---|---|
| `text_base` | #FFFFFF | every connector and generic word |
| `highlight_positive` | #4FD1FF | the named thing, the payoff, the winner. One hex family per video |
| `highlight_negative` | #FF3B3B | the problem, the loser, a negative verdict |
| `highlight_price` | #39E75F | prices only (and check icons) |
| `gradient_hero` | #6EE7FF -> #3B6CFF | two hero words of a punch phrase, 184 px |
| `gradient_4colour` | yellow TL #FFE600, green TR #2BFF6A, blue BR #2F7BFF, magenta BL #FF2BD6 | one gradient lockup word in a list hook |
| `gradient_metal` | #FFF4C8 0% / #FFDD6E 30% / #FFC03A 62% / #F28A1E 100% (vertical) | optional premium highlight word with a sheen |
| `saber_colour` | #FF1E1E | the light-line wipe |
| scrim | black only | never tinted |

Word rules: one highlight run per card, a whole word or a whole line, never part of a word. In two-line cards colour exactly one line and keep the same side all video. At most about one caption in three carries colour in pop-style captions; plain body captions stay white. A line with a winner and a loser colours both (positive and negative). A negative card is followed by its solution beat in the positive colour.

### Motion

The standard pop (every callout, hook line, price), frames at 59.94:

| frame from in-point | scale |
|---|---|
| 0 | 14% |
| 3 | 100% |
| 6 | 116% (overshoot) |
| 21 | 100% settled |

- Text opacity 0 -> 100 over 6 f (0.10 s) during the pop.
- The bloom eases in after the text lands: 15 f (0.25 s), smoothstep. If it reads as a flash, use 27 f (0.45 s). Never a bloom that pops on at full strength.
- Lines of one card stagger 0 / 3 / 6 f. Rank and step cards pop all lines at once.
- Motion blur on the pop: 180-degree shutter, phase -90, 10 samples per frame.
- Out: every highlight card fades 15 f (0.25 s), the scrim with it; a single hero word may use 9 f (0.15 s). The fade finishes on a picture cut or at the end of the hold. Never a hard cut out.
- Glow (Deep Glow 2 settings): radius 416 in layer px (scales with the card), exposure 0.268, 8 iterations, radii easing 90. Lower exposure: 0.095-0.104 on all-white two-line text, 0.10 on a white line 2, 0.119 over bright footage, 0.12 on logos.
- Python glow (no AE): additive, eight gaussians, sigmas 1.2 / 2.5 / 5 / 10 / 20 / 40 / 80 / 130 px with weights 0.3076 / 0.1127 / 0.0111 / 0.4115 / 0.0506 / 0.5211 / 0.3236 / 0, scaled by card px / 110.3. Glow colour = text colour lifted (`c ** (1 - 0.6c)`), so bright channels whiten and red stays red. Measured falloff off the letter edge (linear light): 1 px 0.42, 3 px 0.29, 6 px 0.23, 12 px 0.16, 24 px 0.11, 36 px 0.077, 60 px 0.038, 100 px 0.0125, 160 px 0.0025, gone by 180 px.
- Drop shadow on any text over footage: 80% opacity, 7 px distance, softness 20. No strokes on callouts.
- Scrim: black gradient, multiply, on the same side as the text. Bottom: clear at y 0.477 -> black at 1.086 of frame height (about 85% black at the edge). Top: black at -0.11 -> clear at 0.503. Variants: `top_dense` (0.8 black, clear edge at 0.52, 0.32 soft ramp) for text over a bright subject; `mid` (clear edge at 0.30); `left` (x 0 -> 0.62, 0.85 black, window y 0.5 +- 0.16). Entrance 21 f (0.35 s): opacity up while the clear edge slides in from the frame edge, cubic ease-out.
- Zooms: scale only, eased fast-then-slow, never linear. Talking-head punch 100 -> 120% over 34-38 f, ending on the cut into a graphic. Comedy push 100 -> 115% about the face, quadratic ease-out. Whole-section push 100 -> 115% across a ranked run. Jump-cut steps 100 -> 112 -> 127% hard on cuts. B-roll drift 100 -> 110% linear. Keep punch-ins at or under 120%.
- Hook word fly-in (verdict hook): starts small and tilted, 2.4-2.7x at 0.25 s, 1.0x at 0.5 s, holds to 0.9 s, exits with a 0.125 s horizontal smear. 3D flip on key phrases: rotate X -32 -> 0 and Y 24 -> 0 in 8 f.
- Gradient lockup word: 73-86% of frame width for 0.4 s, then shrinks over 0.5-0.75 s to 44% width.
- Metal highlight pop (optional): scale 0.2 -> 1.12, y +90 -> 0, rotation -3 -> 0 deg in 0.24 s expo-out, then 1.12 -> 1 in 0.18 s; a white sheen (105 deg band, 42-58%) sweeps 120% -> -20% in 0.7 s at +0.2 s.

### Captions

- Display font 48 px, white, lowercase except `I`, names and brands. 1-4 words (mean 2.4-2.8, about 13.5 characters, 20 target, 25 max), one line, 0.5-0.9 s each (median 0.62-0.77 s).
- Centred x 540, baseline y 1300 (67.7%). If the speaker's own graphic sits in that band, move captions above it (e.g. y 1010).
- Entrance: rise 40 px over 10 f, cubic ease-out (`dy = 40 x (1 - u)^3`), opacity 0 -> 100 over 7 f. Never a scale-height squish.
- Thick soft shadow, two layers: black 59%, blur 9 px, offset 4/7 px; black 84%, blur 3.5 px, offset 3/4 px.
- Contiguous: close gaps under 0.45 s while speech continues. A caption never crosses a picture cut: split it there, the second piece arrives already risen.
- Punctuation: keep `?`, no full stops or commas, keep apostrophes. Spell what is said (`wanna`, `gonna`). Digits with units attached (`55mm`, `12-speed`), prices `$4,980`.
- Captions hide under cards in the caption band (y 1190-1402). A caption that repeats the card on screen is dropped: keep the card.
- A spoken opening question is a hook text stack, not a caption. Last caption fades 24 f (57 f when there is no end card).

### Graphics and elements

Positions on 1080x1920, x centred at 540:

| Element | y px (fraction) |
|---|---|
| safe box for every overlay | x 55-1022, y 238-1636; below y 955 stay left of x 910 |
| hook text | 269-672 (0.14-0.35), sitting just above the speaker's head (bottom of block = hair top minus 0.025 H) |
| rank header `#N` + name | 403-499 (0.21-0.26), top scrim |
| price card (top) | label 384-499, price 461-557 |
| spec card line 1 / line 2 | 1267-1325 / 1363-1402 (bottom scrim) |
| callout band | 1190-1402 (0.62-0.73) |
| logo intro | 192-576, 40-69% of width |
| check icon / cross icon | 1171-1344, 14-18.5% width / 1114-1190, 18-20% width |
| quote / payoff card | 1286-1402, 80% wide |
| comment mock-up | 1037, 54% wide |

- Spec card: line 1 the named component in `highlight_positive` (104-130 px), line 2 the rest in white at 0.4-0.6x (56-68 px, glow 0.10). 2 lines max.
- Rank header: `#N` white small (64 px) over the name in `highlight_positive` (176 px); the name is its own beat, specs follow on the next beat. Rank cards hold 3-4.5 s to a later cut.
- Price hero: `highlight_price`, the biggest element on its card (176-222 px), lands 0.06 s after the spoken price; size label white above it, 0.13-0.28 s later.
- Check: rounded square in `highlight_price` with a white lowercase claim under it. Cross: `highlight_negative` with the claim in ALL CAPS.
- Emoji over a highlighted word: 13% of width, 94 px above the caption line, same pop, drop shadow 80/7/20.
- Quote-card emoji: 20% of width, centred on the quote, its centre on the text cap line so the lower half sits behind the text.
- Saber wipe between cut-out subjects (ranked lists): the incoming subject's outline burns as an electric line inside a band moving left to right; the subject appears behind it and the outgoing one vanishes behind the same edge. 42 f (0.7 s), core start x -0.1W -> 1.1W, reveal edge 230 px behind the leading edge, feathers 30 / 160 / 25 px, band = subject box + 120 px. Saber settings: intensity 45, spread 0.18, bias 0.26, core size 1.6. One wipe on every subject cut, none after the last one. A soft shadow PNG under all cut-outs fades 29 -> 100% over 41 f.
- Other transitions: footage to footage is a hard cut. 1-3 f white flash between chapters. Camera-shutter flash 8 f from 4 f before the cut. Dissolves only on graphics (20-31 f).
- End card: 30 f dip to black on the picture, dialogue fades, music rises under the end card (`outro_file`).

### Sound

- SFX on every graphic in-point, nothing pops silent and no SFX without a pop. Pop at -14 dB. Max 2 SFX at once.
- Price: cash register within 8 f of the price in-point (-14 dB). Negative price or option: error tone (-14 dB).
- `next` transition: whoosh at -20 dB, 0.234 s before the cut. Saber wipe: saber whoosh on the wipe in-point.
- Music bed under the whole video from frame 0 (0.2 s fade in), -20 to -25 dB, steady, no ducking, no pumping. Music out under a gag (0.06-0.12 s fades), back on the next cut. Rises to -9 dB from 15 f before the end cut to 0.3 s after, holds under the end card, fades over the last 1.4 s.
- Voice chain: high-pass 85 Hz, denoise, -1.5 dB at 220 Hz, +2.5 dB at 3.2 kHz, +1 dB shelf at 9 kHz, compressor 3.2:1, loudnorm -15.5 LUFS (TP -1.5, LRA 6), limiter.
- Equal-power crossfade on every dialogue join: 6 f on fast edits, 8-16 f on slower ones.
- Master -15.5 LUFS +- 1 LU, peaks under 0 dBFS.

### Pacing and cut rhythm

- Open on the claim or the pain point at frame 0. No introductions. Hook window 0-3.4 s, no lower captions under the hook.
- Talking pieces: 13-26 cuts per minute, mean shot 2.1-2.2 s, median 1.7-1.9 s, never a mean above 3.1 s. Jump cuts inside takes every 0.7-5.6 s.
- Voice-over montage: 42-47 cuts per minute, median shot 1.05-1.25 s.
- Put every cut, caption edge and card edge on the same frame. Graphics start 0.0-0.3 s after the word they name and end on a picture cut.
- Holds: callout 1.4-2.3 s, spec line 0.9-3.0 s, ranked header 2.4-5.0 s, minimum read 0.4 s + 0.25 s per word (hero 0.8 s).

## Do / Don't

Do:
- Colour carries meaning: positive = named thing, negative = problem, price colour = price only.
- Ease the bloom in after the text lands.
- Put the scrim on the text's side and fade it with the card.
- Read every numbered card as a sentence before export (#5 first, #1 last).
- Keep the card text in the speaker's words.
- Stabilise every handheld b-roll shot.

Don't:
- A bloom that flashes on at full strength, or doubled glow layers.
- Sizes outside the ladder, two heroes on one frame, more than 3 type levels.
- A tinted scrim, strokes on callouts, RGB-split glitch.
- A caption and a card saying the same words at once.
- A card over the speaker's face.
- Scale-height squish on captions.
- Footage-to-footage dissolves.
- Squished footage: crop or cover only.

## How to make it

1. Get the rough cut (XML or mp4) and its final SRT. The SRT is the graphics script: each entry is a caption or the text of a card.
2. Transcribe on GPU with word timestamps if there is no SRT (skill `srt-from-cut`). Check the first word of every cut.
3. Detect picture cuts (ffmpeg `scdet`). Every card ends on one.
4. Stabilise b-roll (skill `broll-stabilize`).
5. Mark the words: brands, models, numbers, verdict phrases -> positive; problems and losers -> negative; prices -> price colour. One run per card.
6. Write the card list (text, colour runs, ladder level, band, in/out, SFX). Render one settled still per card over the real frame first and check layout, safe box and faces.
7. Render the cards with `tools/glow_fx.py` (`LOOK_SKIN=skin.json`): `text_element`, `stack`, `stack_above_head`, `scrim`, `image_element`. Write each card as ProRes 4444 alpha.
8. Ranked lists: cut each subject out to a full-frame 1080x1920 RGBA PNG (BiRefNet or SAM 2, skill `person-matte-sam` for people), then `python tools/saber_wipe.py --png next.png --prev current.png --mode in --skin skin.json --out a_to_b.mov` on every subject cut. Check one still first with `--still 0.5 --bg plate.png`.
9. Sound: SFX per the table, music bed, voice chain, crossfades. Check loudness with ffmpeg `ebur128`.
10. QA: frames at every pop (+0.02 / +0.05 / +0.10 s), repeated-frame scan, proof every word against the voice track. Follow `editor-grade-motion` for the frame checks.
11. Export the mp4 and the XML (cards on V5+, captions, SFX A3/4, music A5/6, voice A7/8).

## Skin slots

| Slot | Controls |
|---|---|
| `font_display` | name of the display font for every card and caption |
| `font_display_file` | path to that font file (read by `glow_fx.py`) |
| `highlight_positive` | named thing / payoff colour |
| `highlight_negative` | problem / loser colour |
| `highlight_price` | price and check-icon colour |
| `gradient_hero` | two-stop gradient for punch-phrase hero words |
| `gradient_4colour` | four corner colours for the list-hook lockup word |
| `gradient_metal` | optional metal gradient stops for a premium highlight word |
| `saber_colour` | the light-line wipe colour |
| `glow_exposure` | default bloom exposure (0.268) |
| `safe_box` | platform safe box [x0, y0, x1, y1] |
| `face_model` | path to a YuNet face model for head-aware hook placement |
| `outro_file` | the end card clip and its length |
| `logo_files` | logo PNGs shown white with glow on a spoken brand name |
| `music_bed` | default track and gain under speech |
| `sfx_files` | pop, cash register, error, whoosh, saber whoosh, shutter |
| `spelling` | brand and product spellings to enforce in captions |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this guide |
| `look.json` | the look as data |
| `skin.example.json` | a neutral demo skin filling every slot |
| `tools/glow_fx.py` | Python module: card renderer with the measured pop, additive glow, drop shadow, scrim, tight stacks, safe box and face-aware placement. Reads the skin from env `LOOK_SKIN` |
| `tools/saber_wipe.py` | CLI: saber outline wipe between two 1080x1920 RGBA cut-outs, ProRes 4444 alpha out, `--selftest` built in. Reads `saber_colour` from `--skin` |
