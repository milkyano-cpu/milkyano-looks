# Provenance: low-poly-escalation

Origin: **adapted** (format taken from a public channel, engine written in-house).

## Source
- V2 skill: `C:\Users\adeki\.claude\skills\poly-animation\` (`SKILL.md`, `references\episode.md`, `references\engine.md`, `references\lessons.md`, `references\reference-build.md`, `template\`, `earshot\`). Skill dated 30 Oct 2026.
- V1 legacy skill: `C:\Users\adeki\.claude\skills\threejs-animation\` (`SKILL.md`, `references\`, `template\`). The 29 Oct 2026 "poly-x2" proof: box-rig runner in a stadium, 15 s, "What if every step you took was twice as fast?".
- Numbers taken from: `references\engine.md` (HUD layout, sun, grade, bloom), `references\episode.md` (fields, speeds, timing), `references\lessons.md` (render and sound rules, timings), `template\brands\default.json` (neutral colours), threejs-animation `SKILL.md` (V1 HUD).

## Inspo
- PolyStories-style "what if" escalation reels (public channel; 70-117 s, 20+ beats). Copy the format, not their characters or words.

## Skins
- **default** (neutral, ships with the engine): Inter Bold, cyan `#00DEFF`, no logo. Its values are the look's defaults here. Lives at `poly-animation\template\brands\default.json`.
- **MKP** (client brand preset, 30 Oct 2026 reference build "What if every pedal stroke doubled your speed?", 40.4 s, 1214 frames, approved): `poly-animation\template\brands\mkp.json` (Coolvetica, cyan, white MKP logo on the CTA and jersey). Client font and logo are not shipped; they come from the client's brand folder. The beat sheet and PHYSICS block are in `references\reference-build.md`; the episode is `template\examples\pedal-stroke-doubled.json`. The mix targets (-15.5 LUFS, -1.5 dBTP) came from that client's style DNA and are the engine default.
- The V2 world itself is a real road (Beach Road, Brighton, Melbourne) and the orbit shot shows Australia at sunset. Not skinned by the brand file; changing it means changing `world.js` / `space.js`.

## Tools
- Not copied. The template is in-house and brand-free once `brands\mkp.json` is dropped (only comments in `src\hud.js`, `src\world.js`, `src\traffic.js` name the client or place), but it cannot run from this folder without its vendored three.js r181 (`template\vendor\`) and bundled Inter font (`template\fonts\`), which this repo does not copy. Use it from the skill: copy `C:\Users\adeki\.claude\skills\poly-animation\template\` to a project folder.
- Template tools at the source: `tools\make_beats.py` (validate, PHYSICS asserts, music grid), `tools\render.py` (stills, draft, full render with spike loop and QC), `tools\finish.py`, `tools\qc.py`, `tools\scan_spikes.py`, `tools\rerender_range.py`, `tools\render_sfx.py` (earshot bank, 29 sounds in `audio\sfx_manifest.json`), `tools\mix.py`, `tools\devserver.py`; `earshot\es_remote.py` for a second render machine.
- V1 template at `threejs-animation\template\` (single `index.html`, ~640 lines; Inter + Lora fonts vendored).

## Not carried over
- Example episodes (they carry the client's captions and place names).
- Media: music, outro, library SFX wavs, client fonts and logos (none are shipped by the engine either).
- The V1 stadium build's beats and mix; only its HUD numbers are in the README.
