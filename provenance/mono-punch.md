# Provenance: mono-punch (Mono Punch)

Origin tag: adapted. A public founder-shorts style, rebuilt as our own engine and approved by the agency.

## Inspo
Sabri Suby founder shorts (public). Name kept here only.

## Source skills and paths
- Skill `steroids-shorts`: `C:\Users\adeki\.claude\skills\steroids-shorts\SKILL.md`.
- Style DNA: `R:\BATMAN\brains\Steroids\style_dna\dna.json` (version 2026-11-04). Most numbers in the README come from here.
- Engine (shortkit): `R:\Apps\Claude code\steroids-style\style\`. Read for this look: `theme.py` (skin swap), `picture.py` (zoom modes, bed blur, BED_PUSH 1.04, BED_IN/OUT 0.12/0.22, ease modes), `sui.py` (springs SP/SD, `sin`, `kick`, `wb`, `shake_xy`, AUTO_OUT), `shortkit.py` (`shake` default 10 px 0.3 s, `flash_bw`), `mbcap.js` (SHUTTER 0.5, PX_PER_SAMPLE 2.5, MAX_SAMPLES 32).
- Frozen approved engine: `R:\Apps\Claude code\steroids-style\DNA\engine_2026-11-03\`.
- Reference sheets: `R:\Apps\Claude code\steroids-style\DNA\refs\`.
- Handover with the latest lessons: `R:\Apps\Claude code\reports\Steroids Style - Handover.md` (items 9-10). Not re-read for this pass.

## Dates
- 2 Nov 2026: Short 10 R2 approved by Raihan; Shorts 9 and 2 R1 delivered.
- 3 Nov 2026: logo removed from the CTA; James Lie's shorts go black and white only (theme `mono`); iilumo adopts the look as a theme.
- 4-5 Nov 2026: calm bed under screens, revision audit (33 notes), headroom rule, highlight-box descender fix.
- 6 Nov 2026: 16:9 long-form layout (`longkit.py`).

## Skins that exist today (the theme mechanism)
`theme.py` `THEMES` dict. The engine writes pages in the base yellow; `apply()` swaps `#FFF000` and `255,240,0` for the theme's colour, swaps or strips the CTA logo pill, and asserts no base yellow survives.
- `steroids`: accent `#FFF000`, no logo (Harley's shorts).
- `mono`: accent `#FFFFFF`, lit kanban column `#fff7a8` -> `#ffffff`, send button black with a white arrow, no logo (James Lie's shorts). This is the look's default skin.
- `iilumo`: accent `#FCB515`, logo `themes\iilumo\logo.png` at 236 px on the pill.
- Brand colours also recorded in the DNA `styles` and `themes` blocks.

## Tools
None copied.
- The engine (shortkit, sgfx, sui, picture, render, mbcap, mix2, finish_short, headroom) is large, hard-wired to machine paths (`R:\`, `C:\ClaudeWork`), the soundlib library and the PC/laptop venvs. Listed here instead.
- `theme.py` could be made skin-driven, but it only works on pages the engine writes, so it stays with the engine.

## Not carried over
- Client fonts and logos, the soundlib SFX pools and beds (the README names pool roles only).
- The exact per-pool base gains (live in `sound_plan.py` / `tune_pools.py`; not read).
- Rough-cut tools (`steroids-style\cut\`), `plate_prep.py`, `words_faces.py`, BiSeNet headroom model.
- Client delivery rules (Drive tree, naming, BATMAN registration) and music licensing classes.
- Kanban, money card, stamp and meters blocks are named but not specified to the pixel; their sizes live in `sui.py` / `shortkit.css`.
