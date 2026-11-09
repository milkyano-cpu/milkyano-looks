# Provenance: cinematic-captions

Origin: **cloned** (third-party skill, used as installed).

## Source
- Skill: `C:\Users\adeki\.claude\skills\embedded-captions\` (`SKILL.md`, `CATALOG.md`, `themes\README.md` + 25 theme JSONs, `dna\README.md` + 10 DNA JSONs, `references\` incl. `rail.md`, `composition-craft.md`, `motion-vocabulary.md`, `scripts\`, `assets\`). Files dated 6 Oct 2026.
- Upstream: HeyGen HyperFrames, repo `heygen-com/hyperframes` (the skill updates itself with `npx hyperframes skills update embedded-captions`).
- Numbers taken from: `themes\anchor.json` (palette, Sora, rail 46 px / bottom 96 px, hero 150 px, yield, plate), `dna\cream.json` (motion presets, hero three-act), `references\rail.md` (rail size 0.045h, 9:16 position, timing), `references\composition-craft.md` (hero 0.16-0.22h, tiers), `references\motion-vocabulary.md`, `SKILL.md` non-negotiables, `CATALOG.md` shortlisting heuristics.

## License
- The local skill folder has no LICENSE file.
- The `hyperframes` npm package (in the npx cache, `node_modules\hyperframes\package.json`) declares `Apache-2.0`. The skill ships inside that project, so Apache-2.0 is assumed; confirm on the upstream repo before redistributing anything from it.
- The matting model it downloads (u2net_human_seg) is Apache-2.0 per the skill. A PP-MattingV2 ONNX is referenced in its `.gitignore` as shipped with the skill.
- The 35 identities use free fonts (Inter, Sora, Bodoni Moda, Anton, Press Start 2P and others) plus Hershey stroke fonts in `assets\strokefonts\`.

## Inspo
- The skill's own reference bar and example renders (`references\reference-bar.md`, `references\example-renders\`).

## Skins
- None. No client skin exists for this look yet. Identity choice plus palette and font are the skin.

## Tools
- Nothing copied, by rule (third-party). All scripts stay in the skill: `scripts\prepare.sh`, `matte.cjs`, `transcribe.cjs`, `audio-envelope.cjs`, `safe-zones.cjs`, `make-cinematic.cjs`, `make-theme.cjs`, `make-composition.cjs`, `fill-timings.cjs`, `fit-fonts.cjs`, `preview-frames.cjs`, `render-and-composite.sh`, `render-theme.sh`, the `check-*.cjs` gates.
- `CATALOG.md` and the theme and DNA registries are not copied wholesale; the README summarises the 35 identities and how to pick.

## Not carried over
- Per-identity setpiece details (25 themed setpieces with their own timings).
- The rail position for 9:16 is a range from `rail.md` (600-700 px from bottom); `anchor.json` ships `bottomPx` 96 and the skill does not say which orientation that was tuned for.
