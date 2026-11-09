# Sticker Pop

Loud, bubbly talking-head comedy: fat yellow outlined highlight words, an emoji sticker on almost every beat, meme punch-ins with a vine boom, and an Instagram "Replying to" question sticker as the hook.

## What you get

- Output: talking-head, vlog, skit or creator UGC short with speech.
- Aspect: 9:16, 1080x1920. Frame rate follows the source sequence (seen at 29.97, 30, 59.94 and 60); never resample.
- Length: main cut about 45 s; variations 30 s (hook re-arrange), 60 s, and a 15-20 s short cut. Skits and idea videos 15-21 s.
- Delivered files: main mp4 plus variation mp4s (V1 main, V2/V3 trials), an editable Premiere timeline (FCP7 XML) with one transparent clip per graphic event (ProRes 4444 or qtrle ARGB, named `cap_NNN_<text>`, `pop_NNN_<text>`, `ttl_NNN_<text>`), the cleaned dialogue WAV, and an SFX stem.

## The look in detail

All positions are on a 1080x1920 frame. Frame counts are at 30 fps; scale them for 60 fps sources.

### Type

| Role | Font (default) | Size | Treatment |
|---|---|---|---|
| Plain caption | Inter Bold (original: a Helvetica Neue Bold class grotesk) | 64 px (58 px in the lighter variant) | white, 10 px ink outline, soft shadow dy 5, blur 7, alpha 0.45 |
| Inline keyword inside a caption | display font | 1.12x the caption size (71 px) | highlight fill, 11 px ink outline, hard ink shadow 6 px |
| Highlight line (punchline, rating "100/10", "MY TURN") | display font | 100 px | highlight fill, 15 px ink outline, hard ink shadow 9 px straight down, rotation -4 deg settling to 0 |
| Hook title (2 lines, UPPERCASE) | display font | 122 px (a word-by-word "TOP 3" title used 150 / 84 / 132) | line 1 white, line 2 highlight fill, 17 px outline, hard shadow 10 px, line gap -14 px, rot -5 settling to -2 |
| Pill (URL, label) | display font | 70 px | ink text with no outline on a flat highlight pill, 7 px ink border, hard shadow 9 px, padding 40 x 16, radius = height / 2, rot 6 settling to 0 |
| Item pill (#1-#5) | display font | badge 92 px, item text 70 px | badge: highlight "#N" on an ink rounded rect (radius 30), 6 px highlight inner line 7 px in, 132 px tall; pill 104 px tall, 7 px ink border, hard shadow 10 px; whole sprite rotated -2.5 deg, at most 900 px wide |
| Info stamp (price, code, "60 NIGHTS FREE", "% OFF") | display font | 112-128 px | highlight or white fill, 16-17 px outline, hard shadow 10 px, tilt -4 deg at caption height |
| Price | display font | new price 150 px, old price 92 px | old: white, 14 px outline, red strike 11 px on a 20 px ink line; new: highlight fill, 18 px outline, hard shadow 11, 30 px right of the old one; rot -10 settling to -4 |
| Joke note ("*don't have a gf") | caption font | 46-52 px | white, 7-8 px outline, soft shadow dy 4 blur 6 alpha 0.45-0.5, rot -8 settling to -4, starts with `*`, max width 700-760 px |
| Script partner | free script (Great Vibes) | about the highlight size | white with a dark shadow; one or two per video at most ("she **lives** here now!") |
| Question sticker text | SF Pro class UI sans (fallback Segoe UI) | question 46 px, "Replying to" 37 px | question #121212, reply line #8E8E8E |

Draw order on every sprite: shadow first, then all outlines, then all fills on top. An outline drawn over the fill leaves dark seams inside letters like S and k.

Centre pill and stamp text on its ink bounds, not the font metrics; fat display fonts sit low.

### Colour roles

| Role | Default | Use |
|---|---|---|
| `highlight_fill` | #FFD43B | highlight words, title line 2, pills, stamps, karaoke word |
| `ink` | #111111 | every outline and hard shadow, pill borders, pill text |
| `caption_fill` | #FFFFFF | captions, title line 1, white stamps |
| `price_strike` | #E23B3B | strike line over an old price |
| `end_card_bg` | same as `highlight_fill` | full-frame end screen |
| `sticker_card` | #FFFFFF | IG question box, sticker white edge |
| `sticker_text` | #121212 | IG question text |
| `sticker_meta` | #8E8E8E | "Replying to" line |

Colour words in captions may take their own colour (a gold word in a gold display-font fill with ink outline; a black word in near-black with a white outline).

### Motion

Eases: `back-out` with overshoot s = 2.0 (peaks about 1.10), `expo-out`, `power3-out` (cubic `1 - (1 - u)^3`), `power2-in` for exits. Remotion equivalent of the steep ease-out: `Easing.bezier(0.16, 1, 0.3, 1)`.

- Pop-in (stickers, highlight lines, titles, pills, stamps, notes): length `min(0.42 s, max(0.22 s, half the event))` = 7-13 f. Scale 0.25 -> 1.0 on back-out (s 2.0), alpha in over 0.06 s (2 f), 26 px upward drift to rest, rotation from start angle to rest angle on expo-out. Then a slow 1.0 -> 1.04 grow on expo-out across the hold so nothing sits dead still.
- Exit: events longer than 0.6 s scale to 0 on power2-in with a fade over the last 0.18 s (5-6 f); a 0.10 s fade otherwise; hard cut out when the next item starts within 0.02 s.
- Caption in: fresh line 0.94 -> 1.0 over 0.30 s (9 f) power3-out, 10 px rise, 0.10 s (3 f) fade. Back-to-back line 0.965 -> 1.0 over 0.22 s (7 f), no fade. No bounce on plain captions.
- Zoom: scale only, 100 <-> 115 %, anchored on the frame centre vertically; at most a 70 px horizontal slide toward the speaker. Hard toggles 100/115 on jump cuts, plus slow push-ins or pull-outs across shots over 2.2 s on cubic ease-out. Hook shot pushes 1.00 -> 1.08 (or -> 1.15 across the shot). Punchlines punch to 1.15 on their first word. Compilation hooks 1.00 -> 1.06 per shot. Never above 1.15 in this look (house ceiling 1.20), never linear, never per-frame face following.
- Meme punch-in: on an awkward or deadpan beat, an eased push 100 -> 115-120 % over about 1.7 s (51 f), never a whip; or a hard punch to 115 on the joke word with the vine boom.
- Graphics lead the word by 0.10 s (3 f); word stamps by 0.08 s.
- Motion blur on every moving frame: true sub-frame accumulation, 180-degree shutter, 10 samples. Held frames are not blurred. First-frame travel at most 150 px.
- B-roll cuts in flat: no settle zoom on entry.

### Captions

- Source: the user's SRT, line for line. Never merge or regroup lines. One line only: shrink to fit, never wrap.
- 1-4 words, at most 20 characters, 0.25-1.0 s each, lines back to back (end = next start) except across a real pause over 0.6 s.
- Lowercase except I and names, no full stops or commas, keep `?`. Swear words starred in text (`sh*t`) and beeped in audio.
- Fixed position: centre (540, 1180), ink between y 1147 and 1196. Shrink to fit a 690 px lane. Centre on x 540 and shrink; never shift left; never move to dodge a face (other graphics dodge instead).
- Karaoke word (optional): the spoken word in `highlight_fill`. Inline keywords (numbers, $, %, "free", "never", "everyone", the product word) switch to the display font at 1.12x.
- Magnetic to cuts: a caption never crosses a cut; a shot's first line starts on the cut frame; inside a shot a line starts on the word onset, never late.
- A highlight line, info stamp, hook title or URL pill replaces the caption that says the same words. Never the same text twice on screen.
- Lighter variant (one-word captions): one word per clip, word pop scale 72 -> 82 -> 80 % over 0.2 s (6 f), pastel fill with 6 px black stroke at about 45 px, centred near (540, 1373).

### Graphics and elements

- **Emoji stickers on spoken words.** Real Apple-style colour emoji PNGs, 150-210 px (default 190), a white sticker edge (alpha dilated about 6 px, MaxFilter 13), soft shadow blur 7, alpha 0.45, dy 6. Start rotated +-10-14 deg, settle to +-6-8 deg tilted toward the frame centre. Lead 0.10 s; hold until the next cut or 0.5-1.4 s. Candidate spots: (250, 600), (830, 600), (250, 760), (830, 760), (540, 560), (200, 1000), (880, 1000), (540, 1460); on close-ups use the lower corners (850, 1420), (230, 1420) and up the sides. Never on a face.
- **Emoji per beat (dense variant).** One emoji on every spoken beat, chosen for the emotion of the words, not the literal words. Literal picks only for a named thing, a money line, or the comment CTA (a typing emoji on "comment below"). Fixed spot centred x 529, y 1225, same scale on every one (a 164 % scale on 128-512 px sources; drop to 78-104 % for large illustrations so they match optically), a drop shadow on every one. Cadence about one every 2 s, each 0.8-3.5 s (most 1.2-3.0 s), never under 0.8 s. Boundaries: every picture cut, plus chosen word edges; never mid-word, never across a cut. The layer runs with no gaps, also over b-roll. Prefer animated GIFs; fall back to stills as good GIFs get used. Loop a GIF by duplicating the clip back to back and trimming the last copy. Reuse a file only 6 s or more apart. Mix visual families (never three of one character family in a row). Openers are light, intensity stays mid; save the loudest reaction for a real shock. Leave section-header beats (a new item announced) empty of both emoji and caption when a big title will go there.
- **Repeated words** ("yeah yeah yeah"): one caption, plus one display-font sticker per repeat at scattered spots with slight rotation, each with a pop.
- **Joke note.** Small caption-font text starting with `*` above the speaker's head (clamped to y >= 278), or just above the caption (y 1060) when no face is in shot. Placed first; everything else routes around it. Lives on one shot, at least 1.2 s, 1.2-2.25 s.
- **Number pills.** One spot for the whole video, (540, 330) (fallback 350), top half only, always with context text ("#1 WORK FROM BED", never a bare "#1"). Each holds until the next number. Order matches the speech.
- **Hook title.** Centre (540, 470), fallback y 400, 560 or 1420; up to the first cut between 2.3 and 3.4 s, else 2.8 s.
- **IG "Replying to" question sticker (hook).** White box, 42 px corner radius, soft shadow 18 % alpha blurred 14 px and offset 6 px down, 80 px round avatar, padding 40 left / 44 right / 40 top and bottom, line height 62 px, text column max 620 px with balanced lines (no orphan word), real colour emoji 50 px inline. Centred horizontally, top edge at y 160 by default (move it off any face or burned-in label). Text is lowercase and casual like a real comment. Random, scrappy avatar (pet, food, blurry object, meme), never a real identifiable person; never the same username or avatar twice in a batch. On screen for the hook window.
- **Green-screen reaction meme.** Keyed per pixel `key = clip((G - max(R,B) - 25) / 40, 0, 1)`, alpha = 1 - key, despill `G = min(G, max(R,B))`, cropped to the alpha box (alpha > 40; fixed crop box when an arm moves). Anchored to the bottom edge centred on x 540 (figure may run off the bottom), 700-1050 px wide, pops up from the bottom over 5-6 f on back-ease with 300 px travel. Label in the caption font 46 px, white, hard shadow 3/3 at 85 %, 70 px above the figure; a meme that hides the captions carries the spoken words as its label. Card version: rounded card 43 % of frame width at y 48-67.5 %, 1.3-1.9 s. One shot only.
- **Camera flash + polaroid.** White over the whole frame peaking at 0.92, decaying over 0.45 s as `(1 - u)^2.2`; the frame freezes into a polaroid 330 px wide (card #FAFAF7, 16 px border, 64 px bottom with "click!" in the display font 34 px), shadow blur 12 alpha 0.5 offset (4, 10), rot -18 settling to -7, held 0.12-2.3 s, with a camera emoji 170 px beside it.
- **Non-consenting faces.** Cover with a tracked emoji sticker: face detect every frame at half res (score 0.55), tracks bridged over gaps up to 2 s, held 0.5 s past the ends, 9-frame moving average, sticker 2.1x face height with a white outline and soft shadow, centred slightly above the face. Never a mosaic.
- **End card (idea/UGC videos).** Full-frame `end_card_bg` with the logo popping (rot -4 to 0, ding), URL pill at (540, 1430), a CTA line.
- **Safe box.** Every graphic inside x 55-1022, y 238-1636, and x <= 910 below y 955. Sprites at most 800 px wide, pills 900, hook title 820. Nothing covers a face: check each graphic against the face box (face + 15 % each side, 35 % above, 8 % below) through the zoom every 0.1 s of its life.

### Sound

| Role | SFX type | Gain on the file's own level |
|---|---|---|
| Single pop-up (sticker, highlight) | bubble pop (2nd take) | -15 dB, cue +0 to -4 dB; pop at graphic start + 0.10 s |
| Titles, stamps, pills | bubble pop (1st take) | -15 dB |
| Pill | whip then pop | whip -6 dB at +0.02 s, pop -1 dB at +0.10 s |
| Transition / hook cut | whoosh | -12 dB (title in -3, hook cuts -8) |
| Joke / meme beat | vine boom | -18 dB (turn it down; it is loud) |
| Sudden zoom | awkward sting | by ear, under the voice |
| Sudden moment | bamboo bonk | -14 dB |
| Money / price stamp | cash register | -16 dB |
| Photo | camera shutter | -9 dB, always with a real white flash |
| Positive sticker (sparkle, thumbs) | positive UI chime | -6 dB (+2 on sparkle) |
| Sus / nonchalant | rizz sting | -16 dB, then 6-10 dB lower |
| Comedy | fart echo / taco bell bong | -16 dB |
| Silence / dead air | crickets | -18 dB |
| Logo card / payoff | ding | -10 to -14 dB |

- Every pop-up gets a sound, every sound lands on something that pops. The file's measured onset (YouTube rips carry 0.1-1 s of dead air) lands on the cue. 4 ms fade in, 30 ms fade out. Pops closer than 0.12 s apart are dropped. At most two SFX at once. A "very funny" version is denser SFX on reactions, not louder.
- Dialogue: vocal isolation (Demucs) -> high-pass 70 Hz -> loudnorm -16 LUFS, TP -1.5, LRA 11 -> DeepFilterNet3 -> exact source sample count. Normalise before adding SFX (raw phone dialogue sits at -34 to -42 LUFS). 8 ms ramps on every dialogue edge.
- Music: light comedy bed (Kevin MacLeod-style) at the dialogue minus 15-17 dB (-31 to -33 LUFS), fade in 0.25 s, fade out 1.2 s. Music untouched otherwise: no sidechain, no compressor.
- Censor: 1 kHz sine about 8 dB under speech RMS, voice muted under it, 12 ms ramps, edges from forced alignment.
- Master -14 LUFS integrated, true peak -1 dBTP, AAC 48 kHz 256k. Constant-power crossfade on every audio join; variations get 50 ms afades at joins with hard video cuts.
- Awkward beats keep their real silence; add crickets and a joke note instead of cutting the pause.

### Pacing and cut rhythm

- Way tighter than feels natural: jump-cut every phrase boundary (median 0.4-0.8 s removed, some only 0.10-0.15 s). Each beat keeps its single punchiest phrase. A finished cut is often 60-80 % of a first instinct cut.
- Handles: talking head in-point 0-140 ms before the word, tail 90-210 ms; skits cut on the word with 0 ms. Never a cut with no source gap.
- B-roll 30-55 % coverage, each insert at least 0.6 s, gaps under 0.35 s between inserts closed (no one-frame A-roll flash), last insert ends about 2.2 s before the end. B-roll proves the line literally.
- Graphic density: something pops roughly every 1-2 s. Emoji per beat about every 2 s in the dense variant.
- Variations open on visibly different beats (check the first 0.5 s of each pair). V2 = cold open on the payoff, V3 = short cut (60-70 % runtime) or the funny pass.

## Do / Don't

Do:
- Hard ink shadows and thick ink outlines on every display-font element.
- Captions locked at (540, 1180); everything else moves around faces and notes.
- One emoji per beat chosen by feeling; GIF first; mixed families.
- Every pop-up with a sound, on its onset.
- Read numbered graphics out loud: the order and wording must match the speech.

Don't:
- Glossy or gradient pills, white-outlined pill text, or soft shadows where the hard ink shadow belongs.
- Two-line captions, captions over 20 characters, or captions anywhere but the fixed spot.
- The same text twice (caption under a pill that says it).
- Graphics over a face; zooms aimed at the waist; zooms past 115 %; linear zooms; per-frame face following.
- An SFX with nothing popping on screen; a shutter with no flash.
- A one-frame A-roll flash between inserts; a settle zoom on b-roll.
- Mosaic blur on bystanders (use emoji faces).
- Ripped meme clips in paid ads without asking.

## How to make it

1. Intake: rough cut or raw, the SRT, how many variations and their hook idea, deadline. Make proxies if needed (DNxHR LB, half res, source fps).
2. Clean dialogue (Demucs + DeepFilterNet3, the chain above). Convert phone HLG footage to Rec709 (`iphone-hlg-grade`); stabilise b-roll (`broll-stabilize`).
3. Sync data first: captions from the SRT; refine each boundary on the audio (in-point on the first 10 ms frame where energy rises within +-150 ms, snap to the frame grid); read every V1 cut from the timeline and snap anything within 3 frames onto it; keep one `events.json` on the sequence time base (`srt-from-cut` if there is no SRT).
4. Plan per caption line: plain, karaoke, inline keyword, highlight line, stamp, or note. Mark punchlines, money lines, repeats, number items and section headers.
5. Emoji pass: one per beat by feeling (dense variant), or stickers on key spoken words. Check each placement against faces through the zoom.
6. Meme pass (skill `meme-pass`): two or three beats at most on deadpan, awkward, confused, fail or win moments. Never on a price, claim, CTA or outro. One use per meme per batch (keep a ledger).
7. Hook: build the IG question sticker with `tools/ig_sticker.py` (or a big hook title). Each variation gets a different username and avatar.
8. Zooms: scale-only 100/115 toggles on cuts, slow pushes on long shots, punch on punchlines.
9. Render one transparent clip per graphic event with real motion blur (`editor-grade-motion`, HyperFrames or Remotion, or a PIL renderer that draws shadow -> outlines -> fills).
10. SFX on onsets, music bed, censor beeps, master to -14 LUFS.
11. QA: frame strip of every graphic type, faces clear, safe box, captions never cross cuts, no repeated frames, loudness, SFX on visuals (`earshot` for timing).
12. Deliver the FCP7 XML (V1 footage, V2 b-roll, V3 zoom layer, V4+ one track per graphic type; A1 dialogue, A2-A3 SFX alternating, A4 music) and the mp4s.

## Skin slots

| Slot | Controls |
|---|---|
| `font_display` | fat rounded display font for highlights, titles, pills, stamps, price |
| `font_caption` | bold grotesk for captions and joke notes |
| `font_script` | script partner font (optional, one or two uses a video) |
| `font_sticker` | UI sans for the IG question sticker |
| `highlight_fill` | fill of highlight words, title line 2, pills, stamps, karaoke word |
| `ink` | outlines, hard shadows, pill borders |
| `caption_fill` | caption and title line 1 colour |
| `end_card_bg` | end screen background |
| `colour_words` | map of spoken colour words to fills (product colourways) |
| `keywords` | words that switch to the display font inside captions |
| `logo` | logo file for the end card |
| `url_text` | text of the URL pill |
| `cta_lines` | approved closing lines |
| `copy_bans` | words never used in copy we write |
| `emoji_library` | path to the emoji / GIF set |
| `avatar_dir` | folder of random avatar images for the question sticker |
| `emoji_cache_dir` | folder where downloaded emoji PNGs are cached |
| `music_bed` | music source or folder |
| `sfx_kit` | folder or lookup for the SFX roles above |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this description (Markdown) |
| `look.json` | machine-readable look spec (JSON) |
| `skin.example.json` | neutral demo skin filling every slot (JSON) |
| `tools/ig_sticker.py` | Python 3 + Pillow + ffmpeg: renders the IG "Replying to" question sticker as a 1080x1920 PNG or burns it onto a video; reads font, avatar folder and emoji cache from `--skin skin.json` |
