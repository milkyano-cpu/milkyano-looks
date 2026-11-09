# Receipts

A voiced service or product short that shows its proof: white phrase captions with the spoken word in mint, italic headline stacks, the review screenshot in a rounded card with a glowing ring, product cards that pop with a back-ease, a ding for every good thing and a buzzer for every bad one, and a fresh reaction meme on the funny beat.

## What you get

- Output: online edit of a voiced rough cut (a business owner or presenter explaining a job, a result, a service).
- Aspect: 9:16, 1080x1920, at the rough cut's rate (every job so far 30.000 fps). Frame counts below are at 30 fps.
- Length: about 39-70 s.
- Delivered files: one mp4 (H.264, AAC 256k 48 kHz stereo, -15 LUFS), a QA sheet of key frames, `captions.txt` (every caption line for review), and a hand-off note listing pop-ups, memes and any uncovered words.

## The look in detail

### Type

| Role | Font (default) | Size | Treatment |
|---|---|---|---|
| Caption | Montserrat ExtraBold | 68 px, shrinks 2 px at a time to fit 900 px | UPPERCASE, white, spoken word in `spoken_word`, hard shadow offset (5, 5), 90 %, blur 4 |
| Headline | Montserrat ExtraBold Italic | 54-170 px | colour by meaning, soft shadow blur 12, alpha 0.55, dy 8, plus a 2 px chromatic fringe at 0.45 (red #FF2828 shifted left, cyan #28E6FF right) |
| Slam (counter, #1, one-word slams) | Montserrat Black Italic | up to 170 px | same shadow; the #1 gets blur 30, alpha 0.6, fringe 3 px, glow blur 26 at 0.8 |
| Labels (icon row "YEAR 1", notification card) | Montserrat Bold | 26 px labels, 30-32 px card text | |
| Meme label | Montserrat SemiBold | 46 px | white, hard shadow (3, 3) at 85 % |
| CTA button | Montserrat ExtraBold | 58 px (card title 52 px) | `dark_text` on white |
| Accent script (rare, one word like "&") | Allura | 360 px | `spoken_word` colour |

### Colour roles

| Role | Default | Use |
|---|---|---|
| `spoken_word` | #7AFDF8 (mint) | the word being spoken in a caption, proof ring, product/benefit headline words, ripple, lit chip |
| `caption_fill` | #FFFFFF | captions, lead-in headline words, meme labels |
| `problem_red` | #FF1E2D | problem headline words (they get the buzzer), red lines |
| `stars` | #FFC531 | review stars |
| `icon_lit` | #2F8CFF | icons lighting up in a count-up row |
| `icon_unlit` | #3E4454 (labels #969CAC) | icons before they light |
| `x_badge` | #FF465A | X badge disc |
| `grid_bg` | #0B0B0D | explainer grid world background |
| `grid_line` | #96969B (mint-tinted #6E9696) | grid lines |
| `grid_red_wash` | #C81923 | red flood when a red line lands |
| `card_light` | #F6F6F8 | notification card (alpha 245) |
| `dark_text` | #0E1218 | button text and arrow |

Colour by meaning: `spoken_word` for the product or benefit, `problem_red` for the problem, white for lead-ins.

### Motion

Eases: `ease_out` cubic `1 - (1 - p)^3`; `ease_back` overshoot 1.7 by default, 2.0 on the product pop-up, 2.2 on an X badge, 2.4 on stars; `ease_io` smootherstep `6p^5 - 15p^4 + 10p^3`.

- Headline stack: each line pops on its own spoken word; the stack re-centres over 6 f (ease_out), drawn with 3 sub-frame samples (motion blur). A soft dark scrim (50 %, 520 px tall around the headline centre) fades in over 4 f when a headline sits over footage.
- Product pop-up: back-ease in over 8 f (overshoot 2.0), alpha ramps 1.4x faster. No exit animation: it stays until its scene's cut and is gone on the next scene's first frame.
- Proof card: rises 900 px over 8 f (review screen) or 760 px over 9 f (#1 screen) with 3-sample motion blur. Ring draws in over 11 f. Labels fade in over 4 f.
- Review counter: counts up over 18 f (ease_out), scale 1.25 -> 1.0 over 5 f, "+" appears once the count ends. Stars: 5, 4 f apart, back-ease 6 f.
- #1 slam: 1.7 -> 1.0 over 5 f, a 3-frame shake (-18, 12) (12, -8) (-5, 3), a 25 % white flash; a diagonal white shine (90 px band, 85 %) sweeps across it over 20 f, from +24 to +44 f. When the proof card arrives the #1 block shrinks to 45 % and rises 350 px over 10 f (ease_io). Behind it a 760 px ring of 36 accent arcs (6 deg each, 8 px, alpha 200) spins 1.2 deg a frame, and 12 rotating rays.
- Punch zoom: hard punch-in on a spoken word, scale 1.08-1.45 (a hook up to 1.6), centred, 3-frame shake (-16, 10) (11, -7) (-4, 3), a 20 % white flash, held to the next cut. No sound on a punch.
- Count-up icon row: icons appear 2 f apart (back-ease 6 f) and light up 3 f apart; each lit icon pulses +16 % over 8 f.
- Notification card: back-ease 9 f, scale 0.6 -> 1.0; its chip turns `spoken_word` on the second cue.
- Meme: pops up from the bottom over 5-6 f on a back-ease, 300 px travel.
- Grid world (explainer screens): perspective grid, 160 px spacing, 14 px wave, drifting 25 px/s, 60 dust specks, vignette 0.55, glow `max(grid x 0.75, blur 6 x 1.2)`. A red line smears in from both sides over 8 f (reach 150 px, ghost alpha 0.56); the grid floods red at 85 % and decays over about 14 f to 12 %.
- Transitions: a 2-frame soft white wipe (140 px edge) at grid-scene edges and at each closing screen. A push dissolve (zoom 1.22, blur up to 14, 16 f) is allowed between the two proof screens.
- CTA: question stack at cy 560; on "click" it drops 900 px in 4 f with motion blur; logo (0.6 -> 1) and button (0.5 -> 1) back-ease in over 8 f; on "more" the button dips to 94 % for 4 f and a `spoken_word` ripple ring grows over 14 f (max 900 px); a pointer glides in from (900, 1500) to the button.

### Captions

- Phrases, not word counts: one line, 1-3 words, at most 20 characters. Names and fixed terms never split. A determiner, possessive, "to" or "of" stays with the next word; short adjectives and adverbs stay with their noun or verb; a line never ends on and, but, with, by, as, that, which, if, so, when, from, the, a, to, of or a bare pronoun; phrasal verbs stay together. Example: `this family SUV | came in for | paint correction | to protect | the paint`. `tools/phrase_caps.py` does this.
- Centre (540, 1380), max width 900 px.
- Karaoke: only the word being spoken is `spoken_word`; earlier words return to white.
- Edges snap to the cut frame, never one frame off. A caption never crosses a cut. Each line holds 6 f past its last word unless the next starts sooner.
- Hidden only while a headline says the same words, and again under memes (whose label carries the words) and over the closing proof and CTA screens. Captions come back before a headline's first line and after its last line. No spoken content word may be lost: list "words with no caption and no headline" after each render; only tiny connectors at a cut may remain.

### Graphics and elements

- **Proof card.** The whole review or search-results screenshot, map or chrome cropped out, at native resolution, rounded corners 38-40 px, drop shadow blur 30, alpha 190/255. The client's row is marked with a ring only: `spoken_word`, 4 px stroke, glow 0.45 with blur 8, corner radius 26-28, kept outside the text, never a highlighter fill, never touching text. At least 60 f (2 s) on screen and never appearing in the last 0.5 s. When the voice is tight, pop the pieces 5 f apart (count, +5 stars, +11 label, +14 card, ring 10 f after the card) so the card lands early.
- **Review screen.** Counter at y 330 (set to the number the voice says, "over 180" -> "180+", even if the screenshot shows more), stars at y 500 stepped 128 px (radius 52, glow blur r x 0.35 laid twice), label at y 600, card centred at y 1120 in a 660 x 880 box. Background: grid x 0.9 plus a `spoken_word` radial glow at 0.22 centred (540, 760).
- **#1 screen.** Lead-in words at y 380 -> 270, locality line 520 -> 350, "#1" 870 -> 520, service lines at y 650 and 724, card centred y 1167 in a 566 x 755 box.
- **Product pop-up.** The product image as a rounded card (radius 44 px), 470-540 px wide, centred x 540 at y 1050-1210 (default 1100), clear of the headline and captions, drop shadow blur 30 alpha 190/255. On every spoken mention of the product or plan length (first mention and again when the product is named). Lives until its scene's cut. No fade out.
- **Count-up icon row** ("free check-ups for N years"): N icons in two rows of 5 at x 168, 354, 540, 726, 912 and y 1090, 1380, each 164 px wide, a label 74 px below ("YEAR 1"...), headline at cy 600.
- **Notification card.** 900 x 250 at cy 1180, radius 44, `card_light` at alpha 245, shadow blur 30 alpha 170/255.
- **X badge.** Disc radius 46 px in `x_badge`, 230 px above the headline centre; keep it inside the side margin.
- **CTA.** Question stack (max 780 px wide) carrying every service the voice names and one question mark on its last line; logo 420 px at cy 560; button 700 x 150 at cy 1040, radius 75, shadow blur 26 alpha 140/255; a help line at y 1290. The video ends on the CTA: no black frame.
- **Green-screen meme.** At least one per video on a beat that fits (a downside, a competitor's flaw, a punchline). Key `clip((G - max(R,B) - 25) / 40, 0, 1)`, despill G to max(R,B), crop to the alpha box (a fixed box when an arm moves). Bottom edge, centred, 700-1050 px wide (centre-frame figures about 860 px); a "win" card variant crops a wide meme, scales 1.15 and sits at y 330. Label 70 px above the figure. Never covers a headline line. One use per meme per batch.
- **Margins.** Nothing closer than 100 px to the side edges.

### Sound

No music bed. Every SFX lands on something visible, placed by the file's onset or peak (onset = first sample over 0.02), never by file start. At most two at once.

| Event | SFX type | Gain |
|---|---|---|
| Headline, first line | soft pop-up | -14 dB (-13 on a locality line, the CTA's second line, a chip) |
| Later headline lines | menu tick | -14 dB (-8 on the button press) |
| Stars 1, 3, 5 / count-up icon ticks | bubble pop | -12 dB / -17 dB |
| Proof ring lands | ding | -13 dB |
| Help line last word | ding | -12 dB |
| Product pop-up | soft pop-up | -11 dB on its in-point |
| Notification card | phone notification | -10 dB |
| Proof card slide / CTA click | quick swoosh | -10 / -9 dB |
| Scene transition (frame before a white wipe) | complex transition | -9 dB |
| Opening counter (once per video) | glass shimmer whoosh, trimmed to 1.3 s with 0.4 s fade | -14 dB |
| Win meme | positive UI kit | -10 dB |
| Joke only | vine boom | -9 to -6 dB |
| Positive word or result (free, forever, warranty, #1, a finished count) | rotating positive pool of 5 (ding, quick chime, ding 2, winning chimes, sparkle) | ding -8 on slams, -9 on the last icon, -10 on the #1 ring |
| Negative word, red line, X badge | rotating negative pool of 4 (wrong-answer buzzer 1.05 s with 80 ms fade, game-show buzz, fail low tone, buzzer 2) | about -9 dB |

- Rotate each pool in time order so the same file never plays twice in a row.
- Key-beat palette (each once per video, level with the voice or under it): a role-reveal sting on the hook, a confused-anime "what?" on a confused meme, a slam hit on a benefit, a slip squeak on a downside, a metal clang on protection words, an orchestral stab when a competitor enters, a glass smash when it fails, a cash register on the CTA.
- A buzzer never fires within 6 f of a transition sound; two buzzers within 20 f merge into one. No whip, no splash. No sound on a zoom punch. A long SFX never rings under the next scene.
- Meme audio: a crying-type meme keeps its own audio at -6 dB for 1.5 s, a shock meme at -12 dB, a confused meme gets a pop at -11 dB.
- Voice: loudnorm I -14.5, TP -1.5, LRA 11, 48 kHz stereo before SFX. Mix: VO + SFX bus, tanh soft clip x 0.98, limiter 0.89. Master -15 LUFS integrated (accept -15.2 to -14.3), peak under -1 dBFS. Stacked buzzers push a mix hot; trim the whole mix if it lands above -14.3.

### Pacing and cut rhythm

- The rough cut's picture cuts are kept; every caption and graphic edge snaps to them (snap window 6 f for scenes, 8 f for closing screens).
- Picture cuts land about every second; captions break on every cut.
- Closing script: review proof screen, #1 screen, CTA question, logo + button. Card read time: a help line needs 0.4 s + 0.25 s per word before the last frame or it is dropped.
- Memes: one to three per video; never on a price, a claim, a proof card or the CTA.

## Do / Don't

Do:
- Phrase captions with the spoken word lit; read `captions.txt` line by line before showing a render.
- Show proof whole: the full results list, the real screenshot, at least 2 s on screen.
- Ring the client's row with a thin glowing outline that never touches text.
- A different good sound each time and a different bad sound each time.
- Keep every headline and CTA a sentence that uses the spoken words ("YOUR BRAND NEW CAR?", not "BRAND NEW CAR?").
- End on the CTA.

Don't:
- One-word mid-frame captions or 3-word count chunks.
- A highlighter fill, or a ring on the text.
- A product pop-up that fades out, ends on a word inside its scene, or spills into the next scene.
- A buzzer near a transition, whip or splash SFX, a sound on a zoom punch, a meme SFX louder than the voice.
- The same meme twice in a batch, a meme over a headline.
- Music beds; a black last frame; anything inside the 100 px side margins.
- Off-message stock (other brands' shots).

## How to make it

1. Get the rough cut and its cut list (the user's XML when given; otherwise scene detection at threshold 0.30). Drop black frames from the tail.
2. Transcribe to word timings on the sequence frame grid.
3. Captions: run `tools/phrase_caps.py words.json skin.json` (units from the skin) and read every line; fix splits with more units or a `brk` word.
4. Spec the scenes: headlines (each line on its word, colour by meaning), product pop-ups (`at` = the spoken product word, `until` = the scene's end), punch zooms, grid explainers, red lines, count-up rows, notification card, memes, the closing proof screens and the CTA.
5. Proof screens: crop the screenshot, set the counter to the spoken number, time the pieces to the voice and enforce the 60 f hold.
6. Meme pass (skill `meme-pass`): pick by reaction, check the batch ledger, key and place.
7. SFX: positive and negative pools in time order, key-beat palette once each, transition spacing rules.
8. Render (PIL/numpy frame renderer or HyperFrames with real motion blur, `editor-grade-motion` for eases and QA). Segment long renders across workers and join with `-c copy`.
9. QA: `captions.txt`, the uncovered-words list, the proof-card hold, a QA sheet at every pop-up, proof landing, #1 screen, each meme and a tail caption; SFX list against the rules; loudness with `ffmpeg -af ebur128`; last frame is the CTA.
10. Deliver the mp4; keep earlier versions.

## Skin slots

| Slot | Controls |
|---|---|
| `font_caption` | caption font (default Montserrat ExtraBold) |
| `font_headline` | italic headline font |
| `font_slam` | black italic slam font |
| `font_label` | small label font |
| `spoken_word` | accent: spoken word, ring, benefit words, ripple |
| `problem_red` | problem colour |
| `stars` | star colour |
| `icon_lit` | lit icon colour in a count-up row |
| `proof_screenshot` | the review or search-results screenshot and its crop box |
| `proof_ring_box` | where the client's row sits on that screenshot (centre and size) |
| `review_count_spoken` | the number the voice says for the counter |
| `locality` | place name for the #1 screen |
| `services` | service names the CTA question must carry |
| `product_popups` | map of spoken trigger words to product card images |
| `count_icon` | icon used in the count-up row |
| `logo` | logo for the CTA screen |
| `cta_button_text` | button label |
| `caption_units` | product, model and place names never split across captions |
| `sfx_kit` | folder or lookup for the SFX roles and pools |
| `meme_pack` | green-screen meme source and the batch ledger path |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this description (Markdown) |
| `look.json` | machine-readable look spec (JSON) |
| `skin.example.json` | neutral demo skin filling every slot (JSON) |
| `tools/phrase_caps.py` | Python 3, no dependencies: phrase caption grouping (`spans`, `tail_hide`), CLI `python phrase_caps.py words.json [skin.json]` reading `caption_units` from the skin, `--selftest` |
