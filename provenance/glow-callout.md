# Provenance: glow-callout

Origin: **adapted** (the callout look was rebuilt in Python from a client editor's After Effects comps and finished videos; the saber wipe rebuilds a Video Copilot Saber rig; the metal highlight comes from a second client's HyperFrames builds).

## Source
- Skill `C:\Users\adeki\.claude\skills\mkp-sop\` (SKILL.md edited 28 Oct 2026): `references\style-tokens.md`, `graphics-recipes.md`, `automation.md`, `highlight-rules.md`, `subtitles.md`, `premiere-edit.md` (pace table, zooms, crossfades). Measured from 7 AE masters, 7 Premiere projects and about 48 finished MKP videos (13 Aug to 29 Sep 2026) plus the user's corrections of 10, 15 and 16 Oct 2026.
- Python Deep Glow: fitted 15 Oct 2026 on a frame of the 29 Sep 2026 MKP final (`tools\cal_ref.png`, cyan word at 110 px) with `tools\dg_profile.py` and `tools\dg_fit2.py`.
- Skill `C:\Users\adeki\.claude\skills\mkp-top5-saber\` (16 Oct 2026): `saber_outline.py`, rebuilt from the 24 Sep 2026 "Best bikes" .aep (Comp 27 and "Saber Wipe 1-3"), verified against the 24 Sep triathlon final at 12.45-12.85 s.
- Skill `C:\Users\adeki\.claude\skills\loynx-editing\SKILL.md` (26 Oct 2026): gold gradient + glow + sheen highlight word, sweep/blur reveals, no RGB-split glitch.
- Style DNA `R:\BATMAN\brains\MKP\style_dna\dna.json` and `R:\BATMAN\brains\LoynX\style_dna\dna.json` (both version 2026-10-26): type ladder, stack gap 0.08 em, scrim variants, SFX roles and gains, audio chain, holds, metal pop and sheen numbers.

## Inspo
- The client editor's (Raihan) AE callout system: Animation Composer `NWX` pop, Deep Glow 2 radius 416 / exposure 0.268, Gradient Ramp multiply scrims.
- Video Copilot Saber (Preset 3) wipes in the 24 Sep 2026 ranked-bike video.

## Skins
- **MKP** (bike shop, Melbourne). Values today: `R:\BATMAN\brains\MKP\style_dna\dna.json` and `mkp-sop\references\style-tokens.md`. Font Coolvetica Regular (`_CLIENTS\MKP\asset-cache\fonts\coolvetica rg.ttf`), cyan #00DEFF (range #00C0FF-#00FFD8), red #FF0000 / hook #FF1A1A, green #3CFF00 (range #00FF18-#3CFF00), hero gradient #00C6FF -> #0072FF, 4-colour THIS lockup, saber blue #31A0F2 (Sep) or red #FF1E1E (Oct top 5), outro file 317 f, brand logos in `_CLIENTS\MKP\asset-cache\brand-logos`, music choices per job in the DNA.
- **LoynX** (supercar rideshare). Values today: `R:\BATMAN\brains\LoynX\style_dna\dna.json` and the loynx-editing skill. Coolvetica Hv Comp heroes, Helvetica Now Display ExtraBold 68 px captions, yellow #FFD447, cyan #3FE3EE, ink #07080A, gold gradient `#FFF7C2 / #FFE066 / #FFC233 / #FF8A1A`, logo layers in `loynx-editing\assets\logo\`. LoynX runs at 30 fps with a different caption system (word rise in 0.38 s power4.out); only its gold highlight and sheen fed this look.

## Tools
- Copied and made brand-free:
  - `tools\glow_fx.py` from `mkp-sop\tools\mkp_fx.py` (16 Oct 2026). Edits: header docstring rewritten; font, three highlight colours, glow exposure and safe box read from a skin json named by env `LOOK_SKIN` (was a hard-coded font path and a client DNA path); colour constants renamed to roles (`HIGHLIGHT_POSITIVE`, `HIGHLIGHT_NEGATIVE`, `HIGHLIGHT_PRICE`); `COOL` renamed `FONT`; second DNA block (sizes, fades, gap) replaced by its own built-in values; YuNet model path from skin `face_model` or env `YUNET_ONNX`; name mentions in comments removed. Glow model, pop, scrim, stack, speed code and error handling unchanged.
  - `tools\saber_wipe.py` from `mkp-top5-saber\saber_outline.py`. Edits: docstring; `--skin` argument reads `saber_colour` (`--color` still overrides, default FF1E1E, bad skin file falls back with a message). `--selftest` passes.
- Not copied (left at the source):
  - `mkp-sop\tools\online.py` (57 KB, the full online engine): job-file driven, client outro, logos, music paths and DNA paths throughout.
  - `run_parallel.py`, `online_xml.py`: drive `online.py`.
  - `dg_profile.py`, `dg_fit2.py`, `cal_ref.png`, `dg_profile.json`, `dg_weights.json`: the glow fit needs a client frame as the reference. The fitted weights are in `glow_fx.py` and look.json.
  - `ab_test.py`, `qc_review.py`, `contrast_check.py`: import a job's `build.py`.
  - `stab2.py`, `jitter_subj.py`: retired; use skill `broll-stabilize`.
  - `mkp-top5-saber\saber.py` (plain vertical line) and `fire.py`: the user rejected both ("100% wrong", "too big").
  - BiRefNet cut-out scripts (`R:\Apps\Claude code\mkp-top5\cutouts\biref.py`, `finish.py`): tied to the PC venv and hand fixes per bike.
- Media not copied: fonts, logos, outro clip, SFX (Pop Bubbles 2, cash register, Swoosh 04, Camera Shutter.mp4), music, emoji PNGs, bike cut-outs.

## Dates
- Callout look measured Aug-Sep 2026; Python renderer 10 Oct 2026; glow refit 15 Oct 2026; one engine 16 Oct 2026; saber outline 16 Oct 2026; DNA 26 Oct 2026. Folded into this look 9 Nov 2026.

## Not carried over
- AE-only steps (duplicate the previous comp, Dynamic Link naming, Animation Composer markers) beyond their numbers.
- Client copy rules (brand spelling table, shipped-typo list, problem/solution card order with client examples, logos for named brands).
- Video-type templates (brand verdict, archetype series, bike-fit consult, shop tour) and their per-type hook recipes; only the general hook fly-in, lockup and staircase numbers survived.
- Money-rain, name tag, rider roto glow and tracked callouts (one-off client effects).
- LoynX logo draw-on, 3D collage, grain and plate-blur rules.
- The default display font is a free rounded sans (Nunito Black); the measured look used a client font, so line widths and the 0.08 em gap may need a retune on the new face.
