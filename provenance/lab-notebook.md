# Provenance: lab-notebook

Origin: **ours** (built in-house for one client, then stripped of the skin here).

## Source
- Skill: `C:\Users\adeki\.claude\skills\continue-motion\` (`SKILL.md`, `references\data-to-visual.md`, `references\episode-schema.md`, `references\series-plan.md`). Skill last edited 20 Oct 2026.
- Project and engine: `R:\Apps\Claude code\continue-longevity\` (`engine\build.py`, `engine\style.css`, `engine\helpers.js`, `engine\test_build.py`, `tools\mix.py`, `tools\render.py`, `brand\brand.json`, worked episodes `episodes\ep01-apa-itu-peptide\`, `episodes\ep03-retatrutide\`).
- Brain: `R:\BATMAN\brains\ContinueLongevity\rules.md` (CL-01 to CL-48, compiled 18 Oct 2026, rule loop additions 20 Oct), `style_dna\dna.json` (26 Oct 2026).
- Numbers taken from: `style.css` (type sizes, grid 54 px, layout), `helpers.js` and `build.py` (eases, durations, caption chunking 24 chars / 0.45 s, bloom 0.3), `mix.py` (loudness and SFX gains), `render.py` (120 fps, 2-sub-frame blend).

## Inspo
- Wellhaus-style peptide explainer reels (reference frames in `R:\Apps\Claude code\continue-longevity\refs\`). Layout bands (title ~25 %, visual ~48 %, caption ~69 %) were measured off them.

## Skins
- **Continue Longevity** (Jakarta, peptide education, Oct 2026). Values live in `R:\Apps\Claude code\continue-longevity\brand\brand.json` (from the client's brand book, Oct 2026): cream base, orange accent with light / deep / soft variants, Plus Jakarta Sans, lowercase wordmark files in `brand\`, research URL, empty disclaimer. Client rules (Indonesian VO with English terms, evidence labels, compliance wording, narrator voice id, music beds) are in the skill and `rules.md`.
- The look's defaults here use Inter and a blue accent so no client colour survives.

## Tools
- Copied: `tools\render.py` (unchanged; brand-free, takes the episode folder as an argument).
- Not copied, still at the source:
  - `engine\build.py`, `engine\style.css`, `engine\helpers.js`: the episode-to-HyperFrames compiler. Reads `brand\brand.json` from a fixed project-root path and the CSS carries hard-coded accent tints in the orb and bead gradients (`rgba(255,102,0,...)`, `#ffe0c8`, `#ffb47e`). It would need a skin-json argument and tint derivation to be brand-free.
  - `tools\mix.py`: brand-free code, but it reads SFX and beds from the engine's fixed `engine\assets\` folders. Its numbers are in the README.
  - `tools\scrape_research.py`: scrapes the client's research site.
  - `tools\transcribe.py`, `tools\fetch_elevenlabs.py`, `tools\scratch_vo.py`: tied to the project layout and the ElevenLabs flow.
- Media not copied: SFX kit (pop, whoosh, tick, chime, riser; ElevenLabs sound-effects v2), music beds `bed_a` / `bed_b` (ElevenLabs music, 108 BPM), illustrations, logos, fonts.

## Not carried over
- Client compliance and wording rules (health product).
- The episode JSON schema in full; the README keeps the data-to-visual mapping and layout, not every field.
- Orb gradient tints are described in words; the exact stops are orange-derived in the source CSS.
