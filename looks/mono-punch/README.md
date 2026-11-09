# Mono Punch

Founder talking-head shorts where every spoken beat lands a big black-and-white graphic, with one optional accent colour, spring motion with real motion blur, and a picture that punches, shakes and drops to black and white on the hits.

## What you get

- Output: talking-head short, one speaker to camera.
- Aspect: 9:16, 1080x1920. A 16:9 long-form layout (1920x1080) exists on the same engine with the same type, motion and sound.
- Frame rate: follows the source. The approved finals ran at 59.94 (60000/1001); every frame count below is at 59.94.
- Length: 42-65 s. 27-39 graphic cues per short, 1-2 full-screen screens.
- Delivered: H.264 mp4 (libx264 slow, crf 16, yuv420p, bt709 tags written with setparams, AAC 320 kb/s with an 18 kHz cutoff, faststart) plus a phone review copy (720x1280, crf 24, AAC 160k through a limiter).

## The look in detail

### Type
- One family: Montserrat, weights 500-900, tracking -0.045 em on cards. Title Case on cards. Every text width is measured with the real TTF and shrunk to fit; the browser never wraps a line.
- Captions: Montserrat Bold 86 px, max width 960 px, centre y 1062 (slot top 1006, 112 px tall), tracking -0.02 em, white fill over a 9 px black text-stroke, shadow `0 4px 16px rgba(0,0,0,.55)`.
- Statement type: Montserrat ExtraBold 132 px, top y 1168, tracking -0.05 em, line-height 1.04. Captions hide while a statement is up.
- Phone UI inside lock screens and notifications: a system UI face (SF Pro Display or Inter) at about 1.5x iOS sizes so it reads on a phone.

### Colour roles
| Role | Default | Use |
|---|---|---|
| ink | `#000000` | title cards, dark chips, highlight-box text, logo pill |
| paper | `#FFFFFF` | all other type, database panels |
| accent | `#FFFFFF` (mono) | the ONE accent: highlight-box fill behind one keyword, chips, tabs, the strike, a few accent caption words, send-button flash, CTA arrow. Black type on every accent fill. |
| accent_soft | `#FFFFFF` (mono) | the lit column on kanban screens |
| glass | `#080808` at 0.90 | lower-band glass cards, 1 px border in the accent at 0.55 |
| bed | (computed) | under full-screen screens: the shot itself at 1/4 res, Gaussian blur sigma 7, 55 % colour + 45 % grey, brightness x0.46 |

With the mono default (accent = white) the send button turns black with a white arrow on send, because a white flash vanishes on the white comment box. Footage stays in colour; the black-and-white beats still go grey.

### Motion
- Closed-form springs (zeta, omega). Duration SD = 5 / (zeta x omega):

| Spring | zeta | omega | seconds | frames @59.94 |
|---|---|---|---|---|
| bouncy | 0.42 | 17 | 0.70 | 42 |
| snappy | 0.72 | 20 | 0.35 | 21 |
| soft | 0.62 | 16 | 0.50 | 30 |
| firm | 0.55 | 22 | 0.41 | 25 |
| land | 0.34 | 15 | 0.98 | 59 |

- Entrances (one tween per property, never stacked): chips and tabs from scale 0.35, y +24 on bouncy; cards from y +100, scale 0.9 on firm; list rows slide from x -90 on firm; the slam card from scale 1.22, y -34 on bouncy. A plain fade + 40 px slide or one scale-in is always safe. Two tweens on one property (a pop over a scale-in, a tilt plus a spring) read as a glitch.
- Kick on a key word: scale 1.07 (range 1.05-1.16) in 0.06 s (4 f) power2.out, then back on bouncy.
- Highlight box: accent box wipes in scaleX 0 -> 1, power3.out, 0.26 s (16 f), with the black copy of the word clipped in alongside. Words with descenders (g j p q y , ; ( )) get a box 0.11 em deeper; text wipes clip at `inset(-.4em ...)`, never `inset(0 ...)`.
- Word build on statements: each word pops on its spoken time from y +70, scale 0.7 on bouncy (generic word build: y +46, scale 0.86).
- Odometer numbers roll digit by digit to the value on the spoken word; a value stays hidden until its row lights.
- Fade out: every graphic fades over its last 0.2 s (12 f), power2.in. Only clips that end with the video or are shorter than 0.3 s skip it.
- Motion blur: adaptive 180-degree shutter (0.5 frame), N = ceil(travel / 2.5 px) samples per frame, clamped 1-32, premultiplied averaging.

### Picture moves (the punch)
Zoom per piece about the face: anchor x = face centre, anchor y = face top - 40 px. Piece modes:

| Mode | Zoom |
|---|---|
| W | 1.00 |
| M | 1.06 |
| T | 1.12 |
| P | push 1.00 -> 1.08 |
| S | 1.00 -> 1.05 (under screens) |
| K | hook keys: 1.16 on the cut, eased out to 1.00 over 0.62 s; kick 1.10 on the cut -> 1.06 over 0.42 s on the key word |
| BW | black and white |

- Ease modes in the picture pass: cut, out (1 - (1-u)^3), sine.
- Shake: default 10 px for 0.3 s; envelope amp x exp(-u / (0.4 d)) x (1 - u/d), x on a 13 Hz sine, y at 0.8 amp on an 11 Hz cosine, averaged over 3 sub-frame positions for blur. The overlay shakes with the picture.
- Flash beat: a white flash at 0.85 opacity fading to 0 in 0.08 s (5 f), with a hit SFX at -3 dB.
- Under a full-screen screen the bed is calm: one continuous run of the take (no jump cuts), one slow sine push 1.00 -> 1.04 about one anchor, cross-faded in 0.12 s and out 0.22 s (0.15 s cross-fade under full blur). Never per-cut zoom resets or pumping behind a screen.

### Captions
- 1-2 words per caption, 3 only for a keep-run ("seven out of 10"); max 20 characters; never across a cut; break after punctuation; never end on a weak word; merge flashes under 0.25 s.
- Timing from forced alignment of a hand-corrected script with spoken forms (money, %, k, decimals); starts pulled back to the audio onset.
- A few accent words per short in the accent colour (e.g. never, audit, leaking).
- Keep subtitles off the face.

### Graphics and elements
Layout on 1080x1920:
- Top zone (above the head): slam card top 250 with its tab at 194; title cards top 256, 90 px tall, max 800 px wide, ONE accent highlight-box word; tabs top 280 (92 px tall, 50 px type); chips top 284 (96 px, 50 px type); two dark chips at 256 (90 px, 46 px type) + one accent chip at 366.
- Headroom: a top graphic's bottom edge sits 44 px above the highest point of the hair while it is on screen, and never above the safe line y 238. If it cannot fit, shrink it.
- Chest: statement type, top 1168, centred, with a strike on a rejected word.
- Lower band: glass cards (card, checklist, meters, rows card) top 1176-1196, about 430 px tall.
- Full-screen screens over the blurred bed: heads at y 232 and 336; phone lock screen at 1.24 scale with notifications landing on their words and a rolling clock; white database panel; 2x2 KPI tiles with odometers.
- CTA: comment box top 1232 types the keyword, sends on the next word, arrow at 1404 bounces under it. Optional logo pill (skin). The CTA holds to the last frame; no separate outro.
- Limits: notification titles wrap past ~22 characters; two dark chips overflow past ~26 characters in total; a one-letter word right before a highlight box needs a 0.06 em margin.

### Sound
- Bed: a rap or trap instrumental arranged on its bar grid (regions redrop / continue; automation mute, duck, low-pass 800-900 Hz under screens, tape stop), 17 dB under the voice.
- SFX: real recordings, 2-4 variants per pool, rotated so no file plays twice in a row, +/-0.6 semitone jitter. Pools: hit_med + sub (slam), pop (chips, tabs, highlight), whoosh_small (cards in), whoosh_screen (screens in), swish (title cards, statements), tick (odometers, meters), click (checklist, rows), notif (phone notifications), typing + send (CTA), thud + paper (stamps), marker (strike), boom_big + sub (big shake).
- Levels: each SFX peak-normalised to -1 dBFS plus its pool gain, then a -3 dB trim under the voice. Dense beds add: whoosh_small +6, tick +4, notif +3, send +3, click +3, typing +2, pop +2, whoosh_screen +2. If the dialogue is 3+ dB off -20 LUFS, every pool moves by (dialogue + 20) dB. A cue is flagged buried under -8 dB or loud over +4 dB against voice + bed in its first 300 ms.
- Master: -14 LUFS integrated, true peak at or under -1 dBTP (finals measured -13.9 to -14.8 LUFS, -1.4 to -2.4 dBTP). Two-pass loudness, soft limit at -3 dBFS sample ceiling, transient limiter before any gain drop.

### Pacing and cut rhythm
- A new graphic on every spoken beat; nothing holds longer than about 5 s without a change. A card enters on its first word; its highlight lands on the keyword.
- Hook: frame-0 slam card + tab with hit + sub + pop on frame 0, held to the end of the opening sentence; the hook zoom kicks on the stat word.
- The first frame is the first clean frame. A sentence's last word rings out 10-20 frames. Re-listen every join for doubled words.

## Do / Don't

Do:
- One accent at most; black type on every accent fill.
- Cards above the head, statements on the chest, nothing on the face.
- Read every numbered or ordered graphic as a sentence; it must match the speech.
- Hide a number until its row lights; a bar that does not move gets no sound.
- Snap a QA sheet of every beat on the picture pass before the full render.
- Check bt709 tags x3 and the right 8 px edge after every compose (compose in rgb24 / rgba).

Don't:
- Hard-cut a graphic away.
- Stack two tweens on one property.
- Zoom, punch or jump-cut the blurred bed under a full-screen screen.
- Let a highlight box cut a descender or let two highlights overlap.
- Use a second accent colour, glow, or a logo on the CTA unless the skin supplies one.
- Use template SFX packs that sound synthetic.

## How to make it

1. Cut: a clean talking-head rough cut, every join re-listened, doubles removed; or a finished clean vertical plate with a dialogue-only voice track. Stabilise with `broll-stabilize` where the camera moves. For a second angle, see `multicam-angle`.
2. Words and faces: forced word times on the corrected script, plus a face box per piece (for zoom anchors and headroom).
3. Design the beats on the words: one block per beat (slam, tab, chip, title card, statement, glass card, checklist, meters, money card, stamp, screen, phone lock, rows screen, tiles, panel, CTA), plus picture modes per piece, shakes and flash beats.
4. Write the overlay page (HTML + GSAP, HyperFrames-style) with the spring kit above. Apply the skin (see Skin slots).
5. Picture pass: zoom per piece about the face, shakes, black-and-white beats, calm blurred beds under screens.
6. QA sheet of every beat over the picture; run the headroom pass so top cards hug the head; fix, then render the overlay with adaptive motion blur (`editor-grade-motion` covers the shutter renderer and the QA strips).
7. Sound: arrange the bed on its bar grid, place the SFX pools on the cues, mix, check every cue against the buried/loud thresholds, master to -14 LUFS / -1 dBTP. Judge with `earshot`.
8. Compose with ffmpeg in rgb24 / rgba, write bt709 tags, export mp4 + phone copy, then watch the first and last second and every join.

## Skin slots

The engine is written in one base accent. A skin swaps that accent everywhere in the written page (hex and the `r,g,b` triplet used in rgba), swaps or strips the CTA logo, and then asserts no base accent survived. Black, white, Montserrat, layout, motion and sound never change: they are the look.

| Slot | Controls |
|---|---|
| accent | the one accent hex: highlight boxes, chips, tabs, strike, accent caption words, send flash, CTA arrow |
| accent_rgb | the same colour as `r,g,b` for rgba() uses (glass card border at 0.55, glows on chips) |
| accent_soft | tint of the lit column on kanban screens |
| send_button_on_send | colour the send button turns on send; black when the accent is white |
| logo_file | optional light lockup for the black CTA pill; null strips the pill |
| logo_width_px | width of that lockup on the pill (approved values 236-262) |
| cta_keyword | the word the comment box types (e.g. AUDIT) |

## Files in this folder

- `README.md`: this spec.
- `look.json`: the same numbers in machine-readable form.
- `skin.example.json`: a neutral demo skin filling every slot.
