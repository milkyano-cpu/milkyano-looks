# Provenance: receipts (Receipts)

Origin tag: adapted. Our online-edit look for Meticulous Detailing (Daniel's voiced rough cuts), matched to the client's main reference (Daniel's Tesla video) and the approved board of 16 Oct 2026, then revised through many client notes. The rotating SFX idea is adapted from an Instagram reel Daniel sent.

## Inspo
- Daniel's Tesla video (main reference) and two newer reels for graphics ideas (MET-01).
- @hygienehubau reel DZMu1WixB5o (sent 19 Oct 2026): "a different sound each time instead of ding". Analysis in `R:\BATMAN\brains\Meticulous\hub\refs\sfx_reference_DZMu1WixB5o.md`.

## Source skills and paths
- `C:\Users\adeki\.claude\skills\meticulous-online-edit\SKILL.md`: caption phrasing, tail-hide, proof-card hold, product pop-ups, SFX pools and the reel palette, memes and ledger, checklist.
- `R:\BATMAN\brains\Meticulous\rules.md` (MET-01..22).
- `R:\BATMAN\brains\Meticulous\style_dna\dna.json` (same as `dna.json` in the brain root): canvas, fonts, colours, effects, motion, timing, captions, layout, green_screen, sfx_roles, audio, do, dont. Main source of the numbers.
- `R:\BATMAN\brains\Meticulous\hub\refs\` (`sfx_reference_DZMu1WixB5o.md`, `sfx_pool_proposal\render_job.py` + diff).
- Renderer: `R:\Whole R\Work\MILKYANO\Clients\Meticulous\_tools\` (`render_job.py`, `specs.py`, `meticulous_caps.py`, `meticulous_fx.py`, `prep_job.py`, `cutcheck.py`, `render_mg_v2.py`).
- `C:\Users\adeki\.claude\skills\meme-pass\SKILL.md` and `skills\milkyano-video-editing\references\meticulous-sfx-greenscreen-audit.md` (not read in full).

## Dates
- 7th October 2026 batch (RAV4, Santa Fe, MG IM6, BYD Sealion 7, BMW M2 CS); board approved 16 Oct; caption phrasing rule 16 Oct; proof-card layout fix 17 Oct; product pop-up "until the scene ends" 20 Oct (Zeekr 7X); SFX pools 29 Oct; reel SFX palette 30 Oct (Zeekr X R12); black-tail trim 4 Nov.

## Skins that exist today
One: Meticulous Detailing. Values live in `R:\BATMAN\brains\Meticulous\style_dna\dna.json`, `rules.md`, and `R:\Apps\Claude code\_CLIENTS\Meticulous\CONTEXT.md`: mint #7AFDF8, warning red #FF1E2D, intended caption font ZY Starry (not installed; Montserrat ExtraBold stand-in), the Google proof screenshot `ASSETS\Google businesses Springvale Elite paid Meticulous organic 193.png` (Elite as the paid ad, Meticulous ringed below), locality "SPRINGVALE'S", product images `ASSETS\7 year.png` and `ASSETS\10 year.png`, the reel SFX in `ASSETS\meme_sfx\`, the logo and LEARN MORE CTA, caption units (car models, coating names). ASSETS sit under `R:\Whole R\Work\MILKYANO\Clients\Meticulous\`.

The look's default `spoken_word` stays mint (#7AFDF8) because mint is what the look is named for; a skin can change it.

## Tools
- Copied: `tools/phrase_caps.py` from `_tools\meticulous_caps.py`. Changes: car-model, product and client-only terms moved out of `UNITS` into the skin key `caption_units` (`units_from_skin()`), docstring example made neutral, a CLI (`words.json [skin.json]`) and a `--selftest` added. `spans()` and `tail_hide()` unchanged. Self-test passes.
- Left in place:
  - `render_job.py`, `render_job_single.py`, `specs.py` (per-video specs with client words and asset paths), `render_mg_v2.py`, `render_mg.py` (fixed frame numbers for one video).
  - `meticulous_fx.py` (grid world, stars, rings, wipes: reads client constants; a candidate for a later brand-free port).
  - `prep_job.py`, `cutcheck.py` (job-folder layout and XML cut reading tied to the client folders).
  - BATMAN's `metjob` engine.

## Not carried over
- Screenshots, product images, logo, the meme pack and keyed memes, the SFX files and pools (licences listed in the SFX reference md), and ZY Starry.
- The proof-card layout rule naming a competitor as the paid ad (client-specific, MET-18).
- The unconfirmed Mini Cooper S V2 ring (10 px + 1.04 push-in, possibly a BATMAN test): left out on purpose.
- Delivery steps (Drive folder, Slack thread).
