# Provenance: apple-product (Apple Product)

Origin tag: adapted. Apple keynote / product-film style, built and approved on one client's paid-ad batch.

## Inspo
Apple product films and keynote product reveals (public style reference).

## Source skills and paths
- Skill `iilumo-editing`: `C:\Users\adeki\.claude\skills\iilumo-editing\SKILL.md` ("V2 iilumo" style, the Apple-clean look).
- DNA: `R:\BATMAN\brains\iilumo\dna.json` (= `style_dna\dna.json`, version after 2026-11-04). Sections used: canvas, fonts, colours, effects, motion, timing, captions, layout, sfx_roles, audio, outro, do, dont, measured.
- Rules: `R:\BATMAN\brains\iilumo\rules.md` (ILU-01..37, revision audit ILU-41..56). Skimmed by heading; the checklist in the skill summarises ILU-41..56.
- Evidence: `R:\BATMAN\brains\iilumo\style_dna\evidence_2026-10-26.md` (not read in full).
- Renderer: `R:\Apps\Claude code\iilumo-variation-kit\` (make.py -> prep.py -> render.py with mbcap2.js -> mix.py -> qa2.py).
- iilumolab style json: not referenced by the skill for this look (it covers the workshop account's own finals). Not used.

## Dates
- 10th October 2026 shoot; paid-ad batch jobs 01-10 delivered 22-24 Oct 2026. "We really like the iilumo edit on the recent ones, like the ads" (user, 26 Oct).
- 4 Nov 2026: named "V2 iilumo" among three styles.
- 5 Nov 2026: revision audit (113 notes) folded into rules ILU-41..56.

## Skins that exist today
One: iilumo (product account). Values live in the DNA: brand yellow `#FCB515` (accent), logo yellow `#FFBC00`, cube shade `#C48C00`, brand dark `#231F20`; fonts SF Pro Display / Text; CTA outro files per fps in `R:\Apps\Claude code\_CLIENTS\iilumo\asset-cache\CTA outro\`; product names, spec lines and approved headlines in DNA `copy`. The workshop account (gradient cube) and the collab account have no Apple-style outro.

## Tools
- Copied: `tools/beat.py` from `iilumo-variation-kit\beat.py`, unchanged. It holds no brand values.
- Left in place: `blink.py` (hard-coded raw footage paths), `make.py`, `prep.py`, `render.py`, `mbcap2.js`, `mix.py`, `qa2.py`, `stab4.py`, `subjstab.py`, `shake2.py` (kit-wide, tied to `slots.json`, the kit's media folder and laptop paths), and the outro script `iilumo_cta.py`.

## Not carried over
- SF Pro font files (Apple licence) and the client's URL font; the README defaults to Inter.
- The CTA outro animation (brand cube fly-in) and its SFX; replaced by the `outro_files` slot.
- The SFX wav files from the kit's media folder; the README gives query words and gains.
- Organic-reel, hype-edit and website-hero variants from DNA `variants` (separate looks).
- Music licensing question (commercial tracks on paid ads) is unresolved in the source.
- Accent default `#3A8DFF` is a placeholder of mine, not from the source.
