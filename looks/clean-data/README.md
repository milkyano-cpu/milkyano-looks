# Clean Data

Short data beats for a reel: a line graph that draws itself while one big number counts up, a route across a white 3D city, or an exploded product with leader labels. Inter on black or white, one accent colour, no decoration.

## What you get

- Output: a stand-alone animated insert (stat beat, route beat, teardown beat) to cut into a short, or to post on its own.
- Aspect: 9:16, 1080x1920.
- Frame rate: 30 fps.
- Length: graph 4.0 s (120 f), route 4.0 s (120 f), exploded view 4.2 s (126 f), plus an optional `hold` on the last frame.
- Delivered files: `<name>.<kind>.mp4` and a contact sheet `<name>.<kind>.sheet.jpg` with the platform safe frame drawn on it.

## The look in detail

### Type

| Use | Font | px | Colour (light / dark) |
|---|---|---|---|
| graph label | Inter 500 | 34 | #8C8C8C / #8A8A8A |
| graph big number | Inter Tight 700, line-height 1, tracking -0.05 em, tabular figures | 180, shrinks so the final value fits 850 px | #000000 / #FFFFFF |
| graph axis labels | Inter 500 | 26 | #A3A3A3 / #707070 |
| route ETA title / sub | Inter 700 / 500 | 34 / 25 | #16181B / #6B6F75 |
| route destination name / detail | Inter 700 / 500 | 38 / 28 | #16181B / #6B6F75 |
| route street labels | Inter 600, tracking 0.01 em, white halo | 27 | #77797C |
| teardown header | JetBrains Mono 500, tracking 0.16 em, capitals | 26 | #7D828A, title part #E9E6E1 |
| teardown label number | JetBrains Mono 500, tracking 0.06 em | 24 | accent |
| teardown label name | Inter 600, line-height 1.05, tracking -0.01 em | 31 | #F3F1ED |
| teardown label note | JetBrains Mono 500 | 20 | #8B9098 |

All fonts are free (OFL): Inter, Inter Tight, JetBrains Mono.

### Colour roles

| Role | Default | Use |
|---|---|---|
| `background` | graph #FFFFFF (dark mode #000000); route #EEF0F1; teardown radial #2A2D33 -> #16181B -> #0A0B0D | the plate |
| `text` | #000000 on light, #FFFFFF on dark | big number, graph line, baseline |
| `muted` | #8C8C8C | labels |
| `grid` | #E6E6E6 light / #262626 dark | gridlines |
| `accent` | #2F7CF6 (route), #F08A5D (teardown) | route line, moving dot, ETA icon, label numbers, leader dots. One accent per video |
| `pin` | #F0483E | destination pin only |
| map palette | ground #F7F7F5, buildings #FFFFFF, plazas #E6E6E2, parks #D3E9C6, trees #8FCD78 / #7CBF68, river #9FCBF2 | fixed white city |

### Motion

Graph (frames at 30 fps):
- Baseline and two gridlines draw left to right in 14 f (0.45 s, power3.out), starting 0 / 2 / 4 f apart.
- Axis labels fade up 9 f each (power1.out) from f 3, 1 f apart.
- The tip dot fades in 5 f at f 9. The line draws itself from f 9 to f 90 (2.7 s, power1.inOut) as a Catmull-Rom curve through every point.
- The number counts with the tip: value under the tip x (final / last value), landing exactly on the final value at f 90.
- Landing: a ring grows r 13 -> 60 px and fades 0.18 -> 0 in 21 f (power2.out); a dotted line (3 / 9 px dash) drops to the baseline in 14 f (power2.inOut).

Route:
- Street labels fade in 0.15-0.5 s, only while inside x 140-940, y 400-1560.
- The route draws 0.25 -> 2.75 s (quad in-out) with a white edge ribbon; the moving dot pulses behind the head.
- Camera (30 deg FOV) rides behind the head: distance 62 -> 48 units in the first 1.0 s, polar angle 30 -> 38 deg, azimuth 28 -> 10 deg across the clip, then pulls back +30 units and tilts -10 deg from 2.45 s to the end.
- Pin drops at 2.62 s from height 9 in 0.28 s, one bounce to 1.1 by 0.5 s, 18% squash on landing, shadow fades in under it.
- ETA card counts down (`N min`, `x km to go`) and reads `Arrived` / `<distance> in <minutes> min` at the end.
- Destination card fades in and rises 16 px from 3.07 to 3.32 s above the pin.

Exploded view:
- The phone turns from -33 to -23 deg yaw over 4.2 s with a 2 deg sway (sin 1.3 t).
- Layers lift apart from 0.45 s, 1.25 s each, cubic in-out, 0.07 s stagger, top layer first.
- Leader lines (2 px, #C9CCD1) draw dot -> elbow -> label from 1.05 s, 0.13 s apart, 0.3 s each.
- Renderer: ACES filmic tone mapping, exposure 1.05; key light 2.2, warm rim 1.2, hemisphere 0.45; camera FOV 26 deg.

Motion blur: not applied yet on these templates. If you add it, follow `editor-grade-motion`.

### Captions

None inside the beat. The label is a plain noun ("Followers", "Monthly revenue"). If the beat sits in a captioned short, the short's captions continue over it, inside the safe frame.

### Graphics and elements

Positions on 1080x1920:

| Element | Position |
|---|---|
| platform safe frame | top 220 px, bottom 420 px (y 1500), sides 100 px are covered |
| graph label | x 120, y 330 |
| graph number | x 114, y 382 |
| chart box | x 120-940; zero at y 1330, highest value at y 770; gridlines y 770 / 1050 / 1330, 2 px |
| graph line / tip | 6 px round-capped stroke; tip r 13 px with a 5 px background-colour ring |
| axis labels | y 1388, centred under each point; more than 12 points shows every other one |
| route ETA card | x 110, y 250; white, radius 28, padding 20 x 28, 58 px accent icon tile (radius 18); shadow 0 10 30 rgba(30,40,60,.14) |
| route destination card | above the pin, clamped to x 100-980; white, radius 26, padding 22 / 30 / 24; shadow 0 14 40 rgba(30,40,60,.18) |
| teardown header | x 110, y 250 |
| teardown labels | column at x 690, 250 px wide, rows from y 470 every 170 px (pushed up if the last passes y 1440, never above y 400) |

- Graph: one number, one line, real data only. No callouts, no "83x" chips, no marketing words.
- Route: one route, one red pin, five small grey place labels. The city is decoration, not real geography. Destination name up to about 26 characters.
- Exploded view: exactly six layers, names about 16 characters, notes about 22. Facts or one dry joke.

### Sound

The templates are silent. In an edit: one soft tick or whoosh on the line start, a light thud on the pin landing or the last label, at least 12 dB under the voice. Every SFX lands on a visible change.

### Pacing and cut rhythm

- One beat per idea, 4-4.2 s, cut in hard. Hold the final frame (`hold`) when the next shot needs a beat; never end on a frame that is still moving.
- The final value, the arrived ETA and all six labels must be readable for at least 0.8 s before the cut.

## Do / Don't

Do:
- Use the real numbers, oldest first. If you only have start and end, say the curve is illustrative.
- Show the real shape of the data even when it is not a hockey stick.
- Keep one accent colour.
- Check the contact sheet: number on one line, last frame shows the final value, everything inside the safe frame.

Don't:
- Invent data points.
- Add arrows, badges, extra callouts or slogans.
- Use more than one accent, or a gradient.
- Put a street label on the ETA card, or a teardown label over the object.
- Place text in the top 220 px or below y 1500.

## How to make it

The templates are a Windows port of the MIT project `artemnovitckii/claude-animation-skills` (commit 5dbea55): HyperFrames 0.8.216, GSAP, three.js 0.181.2, all vendored. Skills `graph`, `map-route`, `breakdown` drive them.

1. Get the inputs: values and labels (graph); destination, minutes and distance (route; estimate the missing one at 12 min/km walking, 4 cycling, 2 driving in town and say so); six layer names and notes (teardown).
2. Write a spec next to the job: `<name>.graph.json`, `<name>.map.json` or `<name>.breakdown.json` (fields in `look.json` under `specs`).
3. Skin it: copy the skill's `template.html` next to the spec, swap fonts and colours from the skin, add `"template": "template.html"` to the spec.
4. Build on a render machine with `kit/lap_build.sh <kind> <spec>` (graph about 40 s, the 3D ones about 1.5 min). Use `--snap 3.5` (or `--snap 1.0,3.8`) to check stills before the full render.
5. Check the sheet, then drop the mp4 on the timeline.

## Skin slots

| Slot | Controls |
|---|---|
| `font_ui` | label and card font (default Inter) |
| `font_number` | big number font (default Inter Tight 700) |
| `font_mono` | teardown header and notes (default JetBrains Mono) |
| `mode` | `light` or `dark` plate for the graph |
| `accent` | the one accent colour |
| `pin` | destination pin colour |
| `place_names` | five place labels that fit the city of the brand |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this guide |
| `look.json` | the look as data, including the three spec formats |
| `skin.example.json` | a neutral demo skin filling every slot |

No scripts are copied: the templates need the shared kit (renderer, vendored GSAP, three.js and fonts), which stays in its own repo. See the provenance file.
