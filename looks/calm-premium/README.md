# Calm Premium

Restraint for a calm, premium speaker: one bold uppercase font, one deep brand colour, slow power-curve easing with real motion blur, clean captions with one boxed key word, and lower thirds and title cards that slide in and settle without a single bounce, glow or arrow.

## What you get

- Output: long-form talking-head video (YouTube), plus vertical cutdowns and a trailer.
- Aspect: 16:9 at the rush resolution (1920x1080 or 3840x2160). Graphics are built on a 1920x1080 overlay and sit at 200 % in a 4K sequence. All px values below are on that 1920x1080 overlay.
- Vertical cutdowns: 1080x1920 at 30.000 fps exactly; the footage sits in a rounded window 960x619 centred (about 60 px side margins, 33.9-66.1 % of the height) on a grey radial gradient, captions inside the window.
- Frame rate: follows the rushes (25 or 30). Frame counts below are at 30.
- Length: long-form of any length; trailer 30-60 s cut from the intro; 20 s end screen.
- Delivered: H.264 mp4 at the rush resolution, a frame-snapped gapless .srt, graphics as pre-rendered overlays with motion blur (alpha .mov) composited over the picture or relinked into the edit.

## The look in detail

### Type
One font only: Montserrat ExtraBold (800), UPPERCASE, antialiased, `text-rendering: geometricPrecision`. Measure every width with the real TTF and shrink to fit; never let the browser wrap.

| Element | px (1920x1080) |
|---|---|
| Caption | 100 (90-110; anything under 90 is a fail even if the builder allows 72) |
| Statement card | 88 (min 60; breaks to 2 lines past 1480 px) |
| Hero title | line 1 230, line 2 96 (line 2 fits 1420 px) |
| Chapter chip | 56 |
| List pill | 38-56 (largest size that keeps the stack within 650 px) |
| Icon disc | 200 px disc |
| Lower third | name 46, role 34 |
| Proof pop-up | 40 |
| CTA | head 40, big line 52, button 30 |
| Comment card | 96 |
| Full-screen insert | label 30, title 96, big number 210, sub 58 |
| End screen | kicker 28, head 76, slot label 34 |

Captions shrink 4 px at a time while a phrase is wider than 1700 px.

### Colour roles
| Role | Default | Use |
|---|---|---|
| text | `#FFFFFF` | all text |
| deep | `#1C2433` | key-word boxes, cards, lower thirds, chapter chips, panels, the hero dim |
| accent | `#CDB38B` | one key word or number on a card; never more than one accent element on screen |
| mistake | `#B3261E` | only to mark a mistake (box, strike, cross); never numbers, prices or charts |

Nothing else. No green, no yellow, no neon, no trading-style red and green numbers. Data visuals use white, deep and accent only (white 5 px axes, white bars with a 6 px top radius).

### Effects
- Caption shadow: `0 4px 10px rgba(0,0,0,.55), 0 1px 3px rgba(0,0,0,.35)` (black 50-60 %, small blur). No glow.
- Key-word box: deep fill, padding `.12em .3em .08em`, radius 0.14 em, shadow `0 6px 18px rgba(0,0,0,.28)`, white text with no shadow inside.
- Card shadows: statement `0 18px 50px rgba(0,0,0,.35)`; hero `0 30px 90px rgba(0,0,0,.45)`; chapter chip `0 12px 30px rgba(0,0,0,.3)`; pill `0 10px 28px rgba(0,0,0,.3)`; lower third `0 16px 44px rgba(0,0,0,.35)`; proof `0 16px 40px rgba(0,0,0,.35)`; CTA `0 20px 60px rgba(0,0,0,.35)`; comment `0 30px 80px rgba(0,0,0,.45)`.
- Radii: statement 22, hero 34, chapter chip 16, pill 16, lower third 22, proof 18, CTA 26, CTA button 14, comment 30, end slot 26.
- Hero dim: the deep colour at 55 % over the whole frame behind the hero card.
- Mistake strike: 10 px line in the mistake colour, struck text at 0.5 opacity, a mistake-colour cross badge per struck row that pops in as its row is struck.
- Glow: none, anywhere.
- White sets (white shirt, wall, sofa): the shadow is mandatory and a soft dark radial scrim may sit behind the caption. Everywhere else, no dark blob behind captions.
- Grade: natural and warm, true skin tones, no teal-orange. Starting chain (ffmpeg): `eq=contrast=1.07:saturation=0.96:gamma=0.97`, `curves=all='0/0 0.3/0.27 0.7/0.68 1/0.94'`, `colorbalance=rs=0.03:bs=-0.04:rm=0.045:gm=0.012:bm=-0.045:rh=0.03:bh=-0.05`, `vignette` angle 0.62. Warm the b-roll to sit with the talking head.
- Motion blur: adaptive 180-degree shutter, N = ceil(travel / 2.5 px) samples per frame, 1-32, premultiplied averaging. CSS blur is never motion blur.

### Motion
Calm rules: power-curve outs, no overshoot, frame-1 travel at most ~150 px at 1080p, opacity as its own short tween, holds drift slightly, exits shorter than entrances.

| Element | In | Hold | Out |
|---|---|---|---|
| Caption from nothing (gap > 0.15 s) | opacity 0 -> 1 in 0.12 s (4 f) power2.out; scale 0.94 -> 1 and y 8 -> 0 in 0.32 s (10 f) power3.out | | opacity -> 0 in 0.1 s (3 f) power1.in, ending one frame before the out-point |
| Caption replacing a caption | clean cut + scale 0.97 -> 1 in 0.24 s (7 f) power3.out | | |
| Statement card | opacity 0.14 s; scale 0.93 -> 1, y 10 -> 0 in 0.45 s (13-14 f) power3.out | drift to 1.02, power1.inOut | 0.14 s |
| Hero title | dim in 0.35 s; card opacity 0.18 s, scale 0.92 -> 1 in 0.6 s (18 f) power3.out | drift to 1.03 | 0.18 s |
| Chapter chip | opacity + x -30 -> 0 in 0.5 s (15 f) power4.out | | |
| List pill (on its word) | opacity 0.16 s + x -60 -> 0 in 0.6 s (18 f) power4.out | | x -36 + fade, 0.26 s, stagger 0.035 s, power3.in |
| Strike | scaleX 0 -> 1 in 0.35 s power3.inOut | | |
| Icon disc | opacity 0.16 s + scale 0.7 -> 1 in 0.5 s power3.out | float y -8 px | scale 0.92 + fade, 0.2 s power2.in |
| Full-screen insert | settle scale 1.06 -> 1 in 0.8 s power3.out; text opacity + blur 6 -> 0 px in 0.3 s power2.out with y 26 -> 0 in 0.55 s power4.out | | |
| Lower third | bar scaleX 0 -> 1 from the left in 0.7 s (21 f) power4.out; avatar fade + scale 0.8 -> 1 in 0.5 s at +0.12 s; name, divider, role fade + x -24 -> 0 in 0.55 s, stagger 0.08 s, at +0.22 s | | text out 0.18 s at end -0.5 s; bar scaleX -> 0 in 0.4 s power3.in at end -0.42 s |
| Proof pop-up | opacity 0.16 s + scale 0.9 -> 1, y 12 -> 0 in 0.5 s power3.out | | 0.2 s |
| CTA card | opacity 0.2 s + y -40 -> 0 in 0.7 s power4.out | | y -30 + fade, 0.35 s power3.in |
| Comment card | opacity 0.18 s + scale 0.92 -> 1, y 14 -> 0 in 0.55 s power3.out | | |
| Split screen | speaker slides to x 0.75 of frame while the deep panel slides in from the left: 14 frames, ease in-out cubic, with motion blur | | |
| End screen | power3 / power4 outs | heading drifts 1 -> 1.025 over 17.5 s | |

General table (any new element): entrance slide `power4.out` 0.6-0.8 s; text/card focus entrance = opacity `power2.out` 0.12-0.2 s + position/scale `power3.out` 0.3-0.6 s; A-to-B reposition `power3.inOut` 0.8-0.9 s; calm pop `power3.out` from scale 0.7-0.92 in 0.45-0.6 s; exit `power3.in` / `power2.in` 0.2-0.45 s; hold drift `power1` scale +2-4 % or y 6-10 px; colour and opacity `power2.out` 0.2-0.35 s.

Measured eases you may use (frames at 30): softLand 12 f (text rises, panels, scale-ins; max move ~590 px in budget), glide 10 f (medium moves, ~915 px), softInOut 9 f (opacity, blur, colour), gentleIn 9 f and accelExit 13 f (exits). Not in this look: crashIn, popOver, bounceHard (overshoot), whip and snapSettle (too much travel on frame 1 for calm), cruise on any visible move.

Reference check: 332 graphic entrances measured on premium long-form channels had a median entry of 440 ms and an overshoot on 1.2 % of them.

Camera: no zoom punches and no zoom-settle on the talking head. Slow, near-linear push-ins of up to 10-15 % across a long shot, on about one long shot in three; the rest locked. No face tracking or per-clip reframing.

### Captions
- One line, 2-4 words per phrase (5-6 only when the speaker is too fast). Two lines only for a long name or number.
- At least 0.7 s on screen per phrase; a switch may lag the spoken word by up to 0.3 s to protect that.
- Break at punctuation; never end on a weak word (a, the, to, of, your); never split a key run. Drop a trailing full stop or comma; keep ? and !.
- Centred, text bottom 150 px above the frame bottom (~15 %), clear of the player bar. Word gap 0.26 em.
- At most one key run per phrase in the deep box (a number or a core concept); a mistake box only for a named mistake.
- Never on the face: shift the block, or stack it vertically and right-align it when it sits beside the speaker.
- Coverage can be full phrase-by-phrase or highlights only (about 23 % of runtime); pick one per job.
- No word-by-word blur, fade or rise cascades and no reverse blur-outs.
- .srt: every cue on a frame, each ending on the frame the next starts, no gaps, no doubled words, names spelled exactly.

### Graphics and elements (1920x1080)
- Lower third: first appearance only; left 90, top 790, height 124; avatar 104 px with a 4 px white ring; NAME | ROLE with a 4 x 54 px divider at 55 % white; white on deep.
- Chapter chip: top-left at 92, 78.
- Statement card: deep card, 140 px above the bottom; mistake-colour card for a named mistake.
- Hero title: centred card over the hero dim with a slow push of +3-4 % across the hold.
- Lists: split screen, speaker slid right, pills on a deep left-half panel; stack 150 px from the top, 92 px from the left, 16 px gap, pills max 880 px; number badges = white circle with a deep number; mistake lists get the strike and cross per row.
- Icons: white line icon (stroke 11) in a 200 px deep disc, 230 px from the top, 170 px from the left or right edge.
- Proof pop-up: 3-6 words, top right (right 110, top 170).
- CTA card: top right (right 90, top 80), at most 5 words, optional white button.
- Comment CTA: centred card at top 560, the keyword in the accent.
- Projections carry a one-line disclaimer.
- End screen: 20 s, subscribe animation on the subscribe line, two next-watch slots.
- Nothing covers the face: check every graphic on a real exported frame.

### Sound
- Dialogue first. Master -14 LUFS (highpass + compressor + loudnorm on the voice).
- Music: none, or soft and elegant well under the voice (about 26-29 dB under speech). End screen music fades in 1.5 s and out 3 s.
- SFX only to mark a key moment:

| Role | Sound | Gain | Placement |
|---|---|---|---|
| chapter | riser | -10.5 dB | ends on the card |
| list_pop | pop (rotate 3 variants) | -10.5 dB | one per item |
| list_check | check mark | -9.1 dB | check items |
| mistake_strike | pencil line | -9.1 dB | the strike |
| lower_third | slide | -6.9 dB | peak at in-point + 0.1 s |
| cta_popup | pop up | -9.1 dB (icons -10.5) | in-point + 0.05 s |
| cta_button | menu button | -12 dB | in-point + 1.2 s |
| comment_cta | pop / typing / click | -8 dB typing, -6.9 dB click | +0.02 s / +1.4 s / +2.4 s |

- Banned: whooshes, swooshes and swishes on cuts into or out of b-roll and inserts, camera shutters, flash SFX. Constant-power crossfades on every audio join.

### Pacing and cut rhythm
- Hook within 3-5 s; no flashy intro.
- Cut every pause, breath, hesitation and crutch word but keep a calm rhythm; pauses over 0.35 s are rare. Jump cuts between a front medium and a three-quarter side angle.
- Inserts 2.4-6.4 s, two in the first 20 s, then one every 30-90 s, none in the last ~100 s. Plain hard cuts into and out of every insert, no flash transition.
- Graphics land within about 3 frames of the spoken noun; the lower third leads the name (slide starts ~0.34 s before the name, lands ~0.38 s after).
- Read every numbered card aloud as a sentence; "first" is #1.

## Do / Don't

Do:
- Follow the brand's written rules over any older reference look.
- One font, one deep colour, at most one accent element per screen.
- Real motion blur on every move; power-curve eases; opacity tweened separately.
- Check every graphic on the real frame for face collisions.
- Export the .srt with the video.

Don't:
- Glow, neon, arrows, light leaks, money rain, emoji, hashtags, handles.
- Bounce or overshoot on anything; zoom punches; zoom-settle on the talking head.
- Linear or default eases; `expo.out` on long slides; `expo.inOut` on repositions; stitched overshoot tweens.
- Whooshes on cuts; flash transitions.
- The mistake colour on numbers, prices or charts.
- Dark blob scrims behind captions (white sets excepted).
- Template SaaS-style cards.

## How to make it

1. Load the brand's rules (font, colour roles, caption rules, bans) into a one-page spec; where none exist, write one from the brand's own past videos and get it confirmed.
2. Lock the tight talking-head cut, re-listen every join, mark inserts on concrete nouns.
3. Grade warm and natural; stabilise any handheld b-roll with `broll-stabilize`.
4. Split captions with `editor-grade-motion` (`caption_split.py`) and read every break.
5. Build captions, cards, lower thirds and title cards as HTML + GSAP compositions (HyperFrames-style) on the 1920x1080 overlay with the motion table above.
6. Render with adaptive motion blur (`editor-grade-motion`: `mb_render.py` + `mbcap.js`).
7. QA with `editor-grade-motion`: `qa_sheet.py` over a clean plate, `motion_audit.py` for frame-1 jumps over 100 px, `gfx_audit_run.py` for overflow and collisions, the motionmaxxing `lint.mjs` (no page chrome) and `look.py --hold-warn 2.0` gates, and a framing check on frames exported from the live sequence.
8. Mix dialogue to -14 LUFS with sparse key-moment SFX; check with `earshot`.
9. Relink the overlays into the edit, export mp4 + .srt, cut the trailer from the intro.

## Skin slots

| Slot | Controls |
|---|---|
| font_display | the one font (bold sans, uppercase) |
| text | text colour |
| deep | the deep brand colour: boxes, cards, lower thirds, panels, hero dim |
| accent | one key word or number per screen |
| mistake | mistake box, strike and cross only |
| lower_third_name | name on the first-appearance lower third |
| lower_third_role | role after the divider |
| avatar_image | round avatar in the lower third |
| cta_text | CTA card line, 5 words max |
| comment_keyword | the word in the comment CTA |
| disclaimer_line | line under any projection or claim |
| grade_lut | optional .cube for the warm natural grade |

## Files in this folder

- `README.md`: this spec.
- `look.json`: the same numbers in machine-readable form.
- `skin.example.json`: a neutral demo skin filling every slot.
- No tools copied: the renderer, caption splitter and QA scripts are general-purpose and live in the `editor-grade-motion` skill.
