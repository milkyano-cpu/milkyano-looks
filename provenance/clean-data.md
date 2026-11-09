# Provenance: clean-data

Origin: **cloned** (MIT templates from `github.com/artemnovitckii/claude-animation-skills`, commit 5dbea55, 1 Nov 2026), ported to Windows and a laptop render on 6 Nov 2026.

## Source
- Skills `C:\Users\adeki\.claude\skills\graph\SKILL.md`, `...\map-route\SKILL.md`, `...\breakdown\SKILL.md` (all 6 Nov 2026).
- Templates and kit: `R:\Apps\Claude code\anim-skills\`
  - `skills\graph\template.html` + `build.py` (layout, Inter sizes, GSAP timeline, Catmull-Rom line, count logic)
  - `skills\map-route\template.html` + `build.py` (three.js city palette, camera path, pin bounce, ETA and destination cards)
  - `skills\breakdown\template.html` + `build.py` (phone geometry, explode timing, leader lines, label column)
  - `kit\anim.py` (spec loading, HyperFrames 0.8.216 render, safe frame 220 / 1500 / 100 px, contact sheet), `kit\lap_build.sh` (laptop sync and render)
  - `NOTICE.txt`, `LICENSE` (MIT); vendored GSAP 3.12.5 (GreenSock Standard "No Charge" licence, not open source), three.js 0.181.2 (MIT), Inter / Inter Tight / JetBrains Mono / Poppins (OFL).

## Inspo
- The upstream repo's stat, route and teardown reels.

## Skins
- None built yet. The skills name intended uses: Steroids / Milkyano stat beats (graph), LoynX rides, MKP ride routes and Star Car Vault locations (map-route), iilumo bulb teardown (breakdown, needs new lathe geometry). Client fonts and accents would come from each `R:\Apps\Claude code\_CLIENTS\<Client>\CONTEXT.md` into a template copy.

## Tools
- None copied into the look. The templates are brand-free already, but they only run with the shared kit (anim.py, vendored GSAP and three.js, fonts) and the laptop build script, which syncs to `C:\ClaudeWork\anim-skills`. Copying them would split the kit. Use them in place from `R:\Apps\Claude code\anim-skills\`.

## Dates
- Upstream commit 1 Nov 2026; port 6 Nov 2026; render times measured on the laptop 6 Nov 2026 (graph about 40 s, map-route 1m23s, breakdown 1m22s). Folded into this look 9 Nov 2026.

## Not carried over / gaps
- Motion blur (`mb_render.py` from `editor-grade-motion`) has not been tried on these templates.
- The route is fixed (up, right, up, right); custom routes need edits to `WP`, the pull-back target and `LBL` in a template copy.
- The exploded view only models a phone; other objects need new geometry.
- Sound is not part of the templates; the README's SFX guidance is a house suggestion, not measured.
- The default teardown spec puts the 06 note against the bottom of the safe frame and the assembled phone crosses the left edge at 0 s (noted in the skill).
