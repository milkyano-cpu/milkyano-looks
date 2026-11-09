# Look folder contract

Every folder in `looks/<slug>/` is one brand-free visual style. A brand (a "skin") is applied on top through a skin file. Nothing in a look folder may name a client, a person, a client character, a client logo, a client URL or a client-only font. `check_looks.py` enforces that.

## Required files

### README.md
Sections, in this order:
1. `# <Look name>` and a one-line pitch.
2. **What you get**: output type, aspect ratio, typical length, delivered files.
3. **The look in detail**: Type, Colour roles, Motion (eases, durations in frames at the stated fps, motion blur), Captions, Graphics and elements, Sound, Pacing and cut rhythm. Use real numbers from the source skills.
4. **Do / Don't**: what makes it this look, and what breaks it.
5. **How to make it**: the brand-free procedure, step by step, naming the general skills and tools it needs (e.g. `editor-grade-motion`, `broll-stabilize`, HyperFrames, ffmpeg).
6. **Skin slots**: every value a brand supplies, with what it controls.
7. **Files in this folder**: each file and its format.

### look.json
```json
{
  "name": "Glow Callout",
  "slug": "glow-callout",
  "output": {"type": "talking-head short", "aspect": "9:16", "fps": "follow source", "length_s": [30, 90], "deliver": ["mp4", "premiere xml"]},
  "type": {},
  "colour_roles": {},
  "motion": {},
  "captions": {},
  "sound": {},
  "pacing": {},
  "bans": [],
  "skin_slots": {"font_display": "headline / hero word font", "accent_1": "..."}
}
```
Default values in `type` and `colour_roles` are neutral (free fonts such as Inter or Montserrat, plain hex). Brand values go in `skin_slots` only as descriptions.

### skin.example.json
A neutral demo skin that fills every key in `skin_slots`. No real brand.

## Optional
- `references/*.md`: longer brand-free recipes.
- `tools/`: scripts made brand-free (brand values read from a skin json passed as an argument). Copy a script only when it can be made brand-free; otherwise list it in `provenance/<slug>.md`.
- `stills/`: example frames (added later, brand-free or blurred).

## Provenance
`provenance/<slug>.md` (outside `looks/`, not brand-checked) records where the look came from: source skills, client finals, inspo, dates, and which skins exist. Origin tag: ours / cloned / adapted.
