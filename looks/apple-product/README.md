# Apple Product

Short product ads in the style of an Apple keynote product film: clean sans type in two sentence-case lines, a product that lights up with a soft bloom, slow premium pushes, one before then one after, cut on the beat of the video's own song.

## What you get

- Output: paid product ad (also works for product heroes and UGC-hybrid ads).
- Aspect: 9:16, 1080x1920. Safe box x 55-1022, y 238-1636; below y 955 the right edge stays at x 910 or less, so centred text there is at most 740 px wide.
- Frame rate: 30 fps for the ad builds (frame counts below are at 30). Organic cuts follow the footage.
- Length: ad body 9.5-22.3 s plus a 3.5 s brand outro, 13.0-25.8 s total. Longer when the story needs it.
- Delivered: H.264 high mp4, yuv420p, bt709 tags, 30 fps, AAC 320 kb/s 48 kHz, faststart (libx264 slow crf 16).

## The look in detail

### Type
One SF-style grotesk throughout (SF Pro Display / Text, or Inter as the free default). Sentence case with full stops on headlines. Numbers as digits with a thousands separator, tabular figures on counters.

| Element | Weight | px | Tracking | Notes |
|---|---|---|---|---|
| Headline | Bold | 100 | -0.032 em, lh 1.05 | two lines at y 250 and 362; line 1 text white, line 2 grey on the black stage or soft white at 84 % on footage; any line over 980 px shrinks |
| Product name | Bold | 176 | -0.035 em, lh 1.0 | y 346 on the black stage |
| Product label | Semibold (Text) | 44 | +0.01 em | accent colour, category over the name, y 292 |
| Stat number | Bold | 236 | -0.045 em | count-up |
| Stat caption | Medium (Text) | 42 | | grey caption; lighter grey on footage |
| Talk caption | Semibold | 76 | -0.02 em, lh 1.1 | y 1330-1400 |
| Pill | Semibold (Text) | 32 | | 72 px tall, radius 36, 34 px side padding, 14 px colour dot |
| Spec value / caption | Semibold / Medium | 66 / 30 | -0.025 em | |
| Callout / sub | Semibold / Medium | 46 / 31 | -0.02 em | floating product callouts |
| Reviews number | Bold | 168 (compact card) / 236 (black stage) | -0.045 em | |
| Lineup name | Semibold | 64 (one item) / 44 (two or three) | -0.02 em | sub line 34 / 28 px grey |
| UGC caption | Semibold (Text) | 56 | -0.012 em, lh 1.16 | UGC variant: white on `#121214` at 84 %, padding 9/26/11 px, radius 15, y 330 |

### Colour roles
| Role | Default | Use |
|---|---|---|
| accent | `#3A8DFF` | product label, 1-3 accent caption words, our side's dot |
| text | `#F5F5F7` | all type |
| grey | `#86868B` | headline line 2 and spec captions on the black stage |
| grey_caption | `#A1A1A6` | small captions on black |
| caption_on_footage | `#D2D2D7` | small captions on footage |
| line2_on_footage | `#F2F2F7` at 0.84 | headline line 2 on bright plates |
| divider | `#3A3A3C` | 1.5 px spec dividers and rules |
| background | `#000000` | page, dips |
| stage | `#17171A` -> `#08080A` at 55 % -> `#000` | radial ellipse 70 % x 42 % at 50 % 55 % |
| stock_dot | `#9A9A9E` (warm option `#E0A060`) | "before" labels |
| dark_number | `#1D1D1F` | count-up on a white blast |
| pill_fill | `#161618` at 0.78, inset 1.5 px white at 14 % | pills |
| card_fill | `#18181A` at 0.60, inset 1.5 px white at 12 % | compact cards over blurred footage |
| glow_cool | `#EBF2FF` | white light bloom |
| glow_warm | `#FFAA28` (blink bloom `#FFA01E`, core `#FFD68C`) | amber light bloom |

### Effects
- Light ignite: the light snaps on, then breathes. Chip glow 0 -> 1 in 0.07 s (2 f) power1.out; halo (the glow mask blurred 22 px) in 0.22 s (7 f) power2.out; screen-blend bloom radius 520 px, peak 0.85, scale 0.6 -> 1 in 0.45 s (14 f) power2.out. One hot core per light source.
- Blink: on in 0.05 s, off in 0.14-0.16 s power2.in at half the period; outer bloom 560 px + core 190 px. A real LED switches in 1 frame; a filament fades over 7-12 frames.
- Whiteout: bloom grows to 5x and a white plate fades in over 0.30-0.32 s (9-10 f) power2.in, then cut to the next shot.
- Glow only: no thin streak line across the product, no mirrored reflection under it, no glow clipped into a square.
- Vignette on every footage scene: radial, clear to 55 %, black at 45 % on the edge.
- Gradients: top black 62 % -> 30 % at 26 % -> 0 at 44 % behind headlines on footage; bottom black 55 % -> 0 at 30 % under talk captions.
- Text shadow on footage: `0 2px 18-22px` black at 38-45 % plus a 2-3 px black edge at 25-35 %.
- Background blur behind cards: the same footage blurred 26-30 px at 40-50 % brightness.
- Motion blur: real sub-frame blur on every render, 180-degree shutter (0.5 frame), 3.5 px per sample, up to 12 samples at 30 fps.

### Motion
| Move | From | Duration | Ease |
|---|---|---|---|
| Headline word reveal | opacity 0, y +34, blur 12 px | 0.7 s (21 f), stagger 0.06 s (2 f) | power3.out |
| Headline line 2 | same | starts 0.17-0.42 s after line 1 (default 0.42) or on a later beat | power3.out |
| Fade-up (labels) | opacity 0, y +26, blur 8 px | 0.6 s (18 f) | power3.out |
| Pills / specs / small captions | rise 14 / 22 (stagger 0.09 s) / 12-16 | 0.45 / 0.6 / 0.5 s | power3.out |
| Fade out | | 0.3 s (9 f) | power2.in |
| Count-up | 0 | 1.0-1.2 s (30-36 f); a rating 0.0 -> 4.8 in 0.9 s | power3.out |
| Footage push | scale 1.00 -> 1.04-1.08 (wides 1.02 -> 1.09; punch-ins 1.12-1.20 inside one take) | the whole shot | power1.out, origin on the subject, which ends centred |
| Product entrance | opacity 0, y +90, scale 0.92 | 0.95 s (28-29 f) | power3.out, then hold 1 -> 1.035 power1.inOut |
| Lineup entrance | opacity 0, y +70, scale 0.94 | 0.85 s, stagger 0.1 s, lights stagger 0.12 s | power3.out |
| Slider | line to x 540 over 0.12-0.42 of the scene, then x 1080 over 0.64-0.94 | scene length | power3.inOut; 4 px white line with a 24 px glow, 92 px knob at y 1240; rig pushes 1.00 -> 1.05 |
| Stars | scale 0.4 | 0.45 s, stagger 0.07 s | back.out(2), the only overshoot allowed |
| Talk caption | opacity 0, y +18, scale 0.96 | 0.22 s (7 f) | power3.out; hard cut at the next phrase |
| UGC caption | opacity 0, scale 0.94 | 0.26 s in, 0.12 s out | power3.out / power1.in |
| Floating product | y +150, -5 deg | spring damping 0.7, omega 10, over 1.15 s | then bob 10 px, period 1.43 s, sine.inOut, tilt +/-0.7 deg; shadow = its own silhouette, black, blur 24 px, 36-50 % |
| Callout | dot 16 px from scale 0.4 | dot 0.3 s; 2 px line at 88 % draws 0.45 s; label 0.5 s rise 14 | power3.out / power3.inOut |
| Card settle | scale 1.035 -> 1 | 0.55 s on the cut | power3.out |
| Dip to black (into outro) | | 0.36-0.45 s (11-14 f) | power1.in |

Never: linear or default eases, typewriter text, bounce on text. Zoom inside each panel of a comparison, never the whole composition.

### Captions
- Talk scenes only. 1-5 words, max 22 characters; break after punctuation or 3 words; follow the speaker's phrasing.
- Sentence case as spoken, punctuation kept, numbers as digits. One to three key words in the accent.
- Never across a cut; at most 740 px wide below y 955.
- Headlines are not captions: two-line sentence-case statements at y 250 / 362, one idea per section.

### Graphics and elements
- Black product stage: label y 292, name y 346, the product centred on x 540, y 1060-1120, 840 px wide (or 820 px tall).
- Spec grid: 2 columns x 370 px (x 170-910) at y 1330, 140 px rows. Never below y 1636 or right of x 910 below y 955.
- Count-up: number at y 250, caption 250 px below.
- Pills: 72 px tall, centred, y 1430-1500; slider pills at x 270 (ours, left) and 810 (before, right).
- Split vertical: two halves 958 px tall (0-958 ours, 962-1920 before), each pill 110 px above its half's bottom.
- Side-by-side: two cards 506 x 1040 px at y 540, 26 px side margin, 16 px gap, radius 30, ours left.
- Reviews: compact card 600 x 470, radius 44, at y 760 over the shot blurred 26 px; brand mark straddling the top edge; 168 px number at y+92; stars y+288, 70 px apart. Black-stage version: number 236 px at y 740, five 58 px stars at y 980 (76 px apart), 420 x 1.5 px rule at y 1136.
- Lineup: one item at x 540 (cy 1040, name cy+470); two at x 320 / 760; three at 230 / 560 / 880 (cy 960, names cy+330); headline y 330, sub y 442.
- Comparison order: ours / after on top or left, before on bottom or right, in every split, slider, side-by-side and toggle. Label the before side from its first frame; label ours when it lights and hold it to the end of the scene.
- Close: dip to black into the brand's own outro at the sequence fps; pure black in and out, no flash.

### Sound
- Music: each video its own song, cut on its own grid. The drop lands on the before -> after moment. Music is only trimmed, faded and ducked: 80 ms fade-in (songs start mid-phrase); fade from 0.35 s before the hero ends to 1.6 s after (curve ^1.6) under the outro's own sound.
- Voice (talk scenes): the speaker's own take, mono, 20 ms edge fades; music ducks 19 dB (0.15 s in, 0.25 s out). Heavier speakers: duck 14 dB with a high-pass + 4:1 voice chain.
- B-roll and third-party clips are muted: music only.
- SFX are sparse, one per visible event. Each render normalised to -20 LUFS-M max, then the role gain:

| Role | Sound | Gain | When |
|---|---|---|---|
| product_in | soft velvet swipe | -16 dB | 0.05-0.1 s after a product, card or split enters |
| light_on | glass shimmer | -10 (later cuts -11 to -13) | the frame the light ignites, with light_thud |
| light_thud | short soft impact | -16 (-12 on a real bang) | with light_on |
| whiteout | big whoosh swell | -12 | 0.05 s before a whiteout cut |
| blink_on | glass hover tick | -12 (-14 on value pops) | each blink-on |
| blink_off | soft hover tick | -15 | each blink-off |
| slide | glide swipe | -14 | start of each slider, split or whip |
| stars | pop tink | -19 | five, 0.06-0.07 s apart |
| lineup_light | airy pop-in | -14 (-15 to -17 on soft card entries) | one per item lighting, 0.12 s apart |
| install_click | latch toggle click | -10 to -18 | the frame the part seats |

- Master: -11 LUFS integrated, two-pass loudnorm I=-11, TP=-2.0, LRA=9, linear (TP -2.0 so AAC lands under -1 dBTP). Constant-power crossfade on every join.

### Pacing and cut rhythm
- Scene lengths are counted in units of the song (beat, eighth or 16th) so every cut lands on the grid.
- Frame 0 already shows the product or the problem; headline line 1 starts at 0.05 s.
- One before shot held until the drop; after the drop every cut is a new shot. Never ping-pong between before and after, never chop one shot into several cuts, never repeat a background shot.
- Shots 1.1-2.5 s; product stage scenes 2-4 s; talk scenes 4-6 s; proof cards hold 2.3-3.1 s.

## Do / Don't

Do:
- One idea, one song and one set of footage per video; never copy a structure across a batch.
- One clear before, then the after, once, plus one concrete value point taken from the brand's own spec page.
- Show the install or the moment of action in motion, not already done.
- Push in slowly on every static shot and end with the subject centred.
- Stabilise every b-roll shot (shake rms under 0.15).
- Read every card in order as a sentence.

Don't:
- Reflections under the product, streak lines across a light, glow clipped square.
- Bounce on text, typewriter text, linear eases.
- Timers or clock text that is not real; invented numbers; hype words.
- Sound from b-roll; crew voices; stray ticks on the hook.
- A flash into or out of the outro.
- Scaling a whole comparison layout.

## How to make it

1. Pick the song and map its grid: `python tools/beat.py <song> [drums_stem]` prints bpm, beat and bar length and an energy map every 0.5 s. Place the drop on the before -> after scene boundary.
2. Pick footage per slot: product alone, the before, the install, the after. Stabilise with `broll-stabilize`; iPhone HLG clips through `iphone-hlg-grade` first. Make glow masks for the lit parts.
3. Write the spec in song units: scenes, headlines, labels, counters, comparison devices.
4. Build the graphics as HTML + GSAP (HyperFrames-style) with the motion table above; use `editor-grade-motion` for easing checks and its adaptive motion-blur renderer.
5. Render at 30 fps with motion blur, then QA a frame sheet: safe box, comparison order, no reflection, every card read as a sentence.
6. Mix: song trimmed and faded, sparse SFX on visible events, voice ducking on talk scenes, constant-power joins, -11 LUFS / TP under -1 dBTP. Check with `earshot`.
7. Dip to black into the brand outro and export with ffmpeg (bt709 tags, faststart).

## Skin slots

| Slot | Controls |
|---|---|
| font_display | headline, product name, stat number (SF-style grotesk) |
| font_text | labels, pills, captions (text cut of the same family) |
| accent | product label, accent caption words, our side's dot |
| brand_mark | small mark on the compact reviews card |
| outro_files | brand outro clip per fps (24 / 30 / 59.94), about 3.5 s, black in and out |
| product_names | product names as printed, with their case |
| spec_source | where value points come from (the brand's spec pages) |
| shared_lines | approved short lines (warranty, shipping, rating) |
| comparison_labels | text for the before and after labels |
| glow_colour | bloom colour for the product's light (cool or warm) |

## Files in this folder

- `README.md`: this spec.
- `look.json`: the same numbers in machine-readable form.
- `skin.example.json`: a neutral demo skin filling every slot.
- `tools/beat.py`: tempo and energy map of a song (and optional drum stem) for cutting on the grid. Python 3, numpy, ffmpeg on PATH. No brand values.
