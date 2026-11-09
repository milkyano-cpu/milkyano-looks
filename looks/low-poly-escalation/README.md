# Low-Poly Escalation

A "what if every X doubled" reel: a 3D subject on a golden-hour road whose stat doubles or triples every beat, a huge HUD number climbing with it, true motion blur, and a code-made sound mix that hits on every cut.

## What you get

- Output: code-rendered 3D escalation reel (three.js picture, 2D canvas HUD, seeked frame by frame by HyperFrames). No generation credits, no footage.
- Aspect: 9:16, 1080x1920, 30 fps.
- Length: 15-45 s. Five beats at 150 BPM make 15 s; twelve beats at 138 BPM make about 40 s.
- Delivered: `renders/final.mp4` (picture H.264 CRF 14 yuv420p + mastered mix), `renders/picture.mp4`, a contact sheet, the QC line and the sound report (LUFS, true peak, cue sync).

## The look in detail

### Type
- One bold sans for the whole HUD. Default: Inter Bold 700.
- Small line (the step, e.g. "gear 5"): 64 px, baseline y 372.
- Hero number: 206 px, unit 100 px, baseline y 586.
- Caption: 64 px, baseline y 668. All centred, max width 900 px (wider lines shrink, never shift).
- Hook: 1-3 lines at 96 / 150 / 96 px from y 300 with a 0.08 em gap; the big line in the accent.
- CTA: line 1 66 px at y 560, line 2 150 px accent at y 700, mark 330 px wide at y 800, line 3 48 px at y 1000 (y 830 with no mark).
- Text glow: 46 px and 16 px blurs, lighter blend. Drop shadow 80 % black, 20 px blur, 7 px down.
- Captions lowercase except proper nouns, no full stops, under ~35 characters, one coloured run.

### Colour roles
| role | default | used for |
|---|---|---|
| hud_text | `#FFFFFF` | small line, number, caption body |
| accent | `#00DEFF` | big hook line, CTA punch, default highlight run |
| alert | `#FF1A1A` | highlight run for danger beats (fire, heat) |
| go | `#3CFF00` | highlight run for wins |
| subject_primary | `#0D0F12` | main garment / body colour of the 3D subject |
| subject_accent | `#00DEFF` | trim and small props on the subject |

The world itself is not skinned: warm golden-hour light, peach fog, sea and sand. Sun at 16° elevation, 46° azimuth, warm key 6.5, hemisphere fill 0.6, image-based light 0.85, FogExp2 0.00028.

Grade: ACES, contrast 1.06, saturation 1.12, vignette 0.3, grain 0.02, chromatic aberration 0.0012 (0.002 on fire beats, 0.0024 on plasma). Bloom strength 0.28, radius 0.55, threshold 1.7. Ambient occlusion (GTAO) mix 0.55. Shadow lift 0.022 / 0.018 / 0.014 so the road never goes to mud at a low sun.

### Motion (30 fps)
- Every frame is a pure function of t. Seeded randomness, no clocks.
- Motion blur: 10-24 jittered sub-frames per frame (per shot), shutter 0.5 frame (180°), clamped so blur never crosses a cut. The HUD is accumulated per sub-frame while it animates, so the type blurs too.
- On-screen speed eases up over 0.32 s (about 10 frames) after each cut and drops instantly. Distance is integrated from it, so wheels, lane marks, lamps and cars agree.
- Hook: on screen from frame 0, settles with a spring, exits upward into beat 1.
- Every beat is a hard cut to a new camera plus a new number. A stomp on every cut.
- The crank (or stride) is phase-locked so the pose matches on every cut.
- Draft: 15 fps with 2 sub-frames.

### Captions
- HUD stack, top of frame: small line, hero number with unit, then one caption line. One claim per caption.
- Optional second caption swaps in mid-beat (default at half the beat).
- The highlighted run must match the caption text exactly. Highlight colours: accent, alert, go or white.
- Keep the subject out of y 250-760 in every shot (HUD block).

### Graphics and elements
- A detailed low-poly subject (V2: rider and road bike with IK legs and arms, a face with mouth, teeth, brows, cheek flap) on a coastal road: bike lane, two traffic lanes, promenade, sea wall, sand, beach huts, pines, lamps, a city skyline. Repeated parts are instanced chunks whose period divides 480 m.
- 14 camera shots: hook drone, side track, low front three-quarter, high chase, drivetrain close-up, wide from the sand, jet side, static roadside (boom), aerial chase, face-and-fire close, side plasma, lift-off chase, orbit pull-back, empty-lane CTA.
- 9 set pieces climbing the scale: dust, a jet alongside, sonic boom (vapour cone, flash and shock ring 0.3 s later, sand sheet, gulls scatter), a supersonic airliner overtaken, tyres on fire, plasma sheath, lift-off, orbit with Earth, scorch marks on the empty lane.
- Speed on screen is art direction: real up to ~200 m/s, about 150 m/s for a static boom camera, 700-1400 m/s for chase shots.
- Portrait cameras see only about ±12-13° sideways at fov 40-45: check the subject stays in frame.

### Legacy V1 variant (box rig)
- Low-poly box-character runner in a stadium: a hierarchy of flat-shaded boxes (hips, spine, head, arms, legs), about 2,700 instanced crowd people at 4 boxes each, ad boards, floodlights.
- HUD top-left: tracked uppercase label (Inter 600, 29 px, 0.15 em), number in a serif (500, 124 px) ticking through every in-between value one tick per 16th note with a small pop, turning pale yellow `#F7ECA6` on the last beats; comparison line in caps; step counter and a red rule pill (`#E0263C`, e.g. "x2 EVERY STEP"); mid-screen italic serif caption 64/70 px.
- Hook card 0-2.5 s: wide shot, the question centred in the top half in a large regular serif, no HUD.
- Look: flat shading, PCF soft shadows, GTAO, bloom, ACES.

### Sound
- Every SFX lands on a visible change; the mixer reads the same event times as the picture. Fix sync by moving the picture event, never the sound.
- On every cut: a whoosh, a number pop, a caption swipe and an escalating stomp or hit. A sub on the music drop and the big set pieces. Each set piece has its own sounds on its event frame (boom: riser, pass-by, blast, gull wings; plasma: riser and hit; lift-off; CTA pops).
- Risers hand over to their hit with an equal-power fade that ends on the hit frame. The pass-by ends 15 ms before the boom; the boom is the loudest thing in the video.
- Music (optional): measured first, drop placed on the hardest cut. Music pre-gain -12 dB, ducked -7 dB under the hits.
- Master: -15.5 LUFS integrated, -1.5 dBTP true peak, -1.9 dB sample ceiling (headroom for the AAC encode). Measure the encoded mp4, not the wav. V1 mastered to -14 LUFS / -1 dBTP.
- A bank-only mix without music leaves 1.4-1.7 s gaps: add a bed or wave and wind ambience before delivery.

### Pacing and cut rhythm
- Everything sits on the music grid. Segments are whole music beats: 6 by default (2.6 s at 138 BPM), boom and orbit at least 6. Hook about 6 beats, CTA about 8, then a 0.2-0.5 s dip to black.
- Skip steps to climb fast: steps 1, 3, 5, 7, 9 of a x3 ladder go from 25 to 164,025 in five beats.
- The escalation climbs scales the viewer knows (traffic, train, record, airliner, sound barrier, supersonic jet, fire, plasma, orbit, escape).

## Do / Don't

Do
- Assert every caption claim against a sourced constant before rendering ("twice as fast as a cheetah" gets `assert 1.9 < v / CHEETAH < 2.1`). Fix the caption, never loosen the assert.
- Stage each set piece in the shot built for it.
- Show stills and a contact sheet before the full render.
- Keep every sound on a picture event.

Don't
- Don't put a car between the lens and the subject; lane-side shots get no traffic.
- Don't let the subject sit behind the HUD block (y 250-760).
- Don't use random draws that change per frame (particles flicker) or state that leaks between frames.
- Don't encode with HyperFrames' own MP4 (8 px black stripe on the right edge); render PNGs and encode with ffmpeg.
- Don't overwrite a delivered mp4. New version, new file.

## How to make it

1. Copy the poly-animation engine template to a new project folder (see provenance for the path). Never work inside the skill folder.
2. Write the idea as an episode spec: the rule (x2 / x3 per step), the steps shown, hook lines, one caption per beat with its highlight, shot, set pieces, on-screen speed and pose per beat, the CTA lines. Write the PHYSICS block: `value(n)`, sourced constants, `physics(n, v)` (keep `mach` for speed ideas), one assert per caption claim.
3. Run the beat builder. It validates names, runs the asserts, lays the beats on the music grid, and warns on mismatched shot and set piece. Fix every warning.
4. Stills at one time per segment and at every event (boom, lift-off, caption swap). Check framing with the dev page `__ndc(t)` (|x| > 1 = out of frame, y 0.2-0.75 = behind the HUD).
5. Draft render (15 fps, 2 sub-frames) for timing and cut rhythm.
6. Full render: 4 workers, spike scan and re-render of near-black frames (up to 3 rounds), encode CRF 14, cut-side snapshots, QC. It must print `QC: PASS` (frame count, no duplicate frames outside the closing dip, every snapshot matches its own frame, PSNR ≥ 40 dB).
7. Sound: render the SFX bank with `earshot`, build the cue list from the resolved episode, mix and master to the numbers above, mux. Check with `earshot measure` and `earshot timeline --cues`.
8. Deliver the mp4 with the contact sheet; report frames and QC, render time, LUFS, true peak and cue sync.

Needs Node 18+ (`npx hyperframes@0.8.216`, pinned), Python 3.10+ with numpy and pillow, ffmpeg, earshot. On a laptop RTX 3050 the 15 s demo took 10.6 min end to end.

## Skin slots

| slot | controls |
|---|---|
| `font_family` | HUD font family |
| `font_file` | HUD font file (copied into the project's `fonts/`) |
| `font_weight` | HUD font weight |
| `hud_text` | number, small line and caption body colour |
| `accent` | hook big line, CTA punch, default highlight |
| `alert` | highlight for danger beats |
| `go` | highlight for win beats |
| `logo` | white mark on the CTA (file path or null) |
| `subject_logo` | whether the mark also appears on the subject's garment |
| `subject_primary` | subject's main garment colour |
| `subject_accent` | subject's trim colour |
| `subject_props` | prop colour (bottle, small parts) |
| `cta_lines` | the 3 CTA lines |
| `music` | optional music file with its BPM and drop time |
| `outro` | optional outro clip appended after the dip |

## Files in this folder

- `README.md`: this spec.
- `look.json`: defaults for HUD type, colour roles, motion, captions, sound, pacing, bans, skin slots.
- `skin.example.json`: a neutral demo skin, one key per slot, plus `engine_brand`: the same values in the engine's brand preset shape (`font`, `colors`, `logo`, `rider`), ready to save as `brands/<name>.json` in a project.
- No `tools/`: the engine needs vendored three.js and a bundled font to run, so it stays in its skill folder (see `provenance/low-poly-escalation.md`).
