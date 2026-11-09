# Provenance: calm-premium (Calm Premium)

Origin tag: ours. Built from one client's written editor SOP plus our own motion rules after the client asked whether the editor had changed.

## Inspo
- The client's SOP (calm, premium, never hype).
- Premium long-form channels measured in `abel-hq` (Iman Gadzhi, Ali Abdaal and others in `abel-hq\board\board.json`); used only for the entry-timing check (332 entries, median 440 ms, 1.2 % overshoot) computed from `abel-hq\motion\*.json`.

## Source skills and paths
- Skill `editor-grade-motion`: `C:\Users\adeki\.claude\skills\editor-grade-motion\` (SKILL.md; references motion.md, captions.md, motionmaxxing.md, pipeline.md; assets/caption_style_template.css; scripts). Origin: Abel's long-form, Sep 2026.
- motionmaxxing eases: `references/motionmaxxing.md`, taken 6 Nov 2026 from github.com/Tejashmakwana/motionmaxxing @8c8ec0f (Apache-2.0).
- `R:\BATMAN\brains\Abel\rules.md` (ABL-01..46, compiled 18 Oct 2026) and `R:\BATMAN\brains\Abel\dna.json` (sections fonts, type_ladder_px, colours, effects, motion, captions, graphics, placement, sfx_roles, audio, timing, do, dont).
- `R:\Apps\Claude code\abel-hq\SOP_CONFLICTS.md` (31 Oct 2026: SOP binding again; the SOP's own style video breaks its rules).
- Client SOP PDF: `R:\Whole R\Work\MILKYANO\Clients\Abel\YouTube_Editor_SOP_Abel_Raberin.pdf` (not opened; DNA and rules summarise it).
- Worked example build: `R:\Whole R\Work\MILKYANO\Clients\Abel\September\Abel - September 24th\Online\project_v2\` (gen_sop.py, gen_style_sop.css). Not opened.

## abel-high-quality skill
Searched `C:\Users\adeki\.claude` and `R:\Apps\Claude code`, `R:\BATMAN` for a SKILL.md named `abel-high-quality`: not found. Memory names it (project_abel_high_quality.md) and `abel-hq\` holds its working data (board, motion measurements, phase1/phase2 scripts), but no skill file exists on these paths.

## Dates
- 24 Sep 2026: first SOP-built long-form, approved.
- 1 Oct 2026: SOP received; split-screen lists, lower third.
- 2-5 Oct 2026: strike style, caption stacking, SRT rules.
- 31 Oct 2026: SOP binding again; references supply motion inside the SOP.
- 6 Nov 2026: motionmaxxing eases added to editor-grade-motion.

## Skins that exist today
One: Abel. Values live in `R:\BATMAN\brains\Abel\dna.json` and the SOP: Montserrat ExtraBold, white `#FFFFFF`, deep purple `#1A0A2E`, gold `#C9A24B`, red `#C62828`; lower third "ABEL RABÉRIN | FINANCE & BUSINESS MENTOR"; CTA "BOOK YOUR FREE CALL"; projection disclaimer; warm grade LUT `D:\MILKYANO\Abel Sep24 v2\grade\Abel_Sep24_warm_grade.cube`. The caption CSS template in editor-grade-motion is that skin. The look's neutral defaults (`#1C2433`, `#CDB38B`, `#B3261E`) are mine.

## Tools
None copied. editor-grade-motion scripts (mb_render.py, mbcap.js, caption_split.py, qa_sheet.py, qa_strip.py, motion_audit.py, gfx_audit_run.py, ref_pull.py, frame_strip.py, motionmaxxing lint.mjs and look.py) are general-purpose and referenced by skill name.

## Not carried over
- B-roll sourcing rules (stock library only, subject tagging by pronoun): client-specific.
- Delivery: naming, Frame.io, Notion, Slack.
- The client's push-in practice (user's own Transform ramps 100 -> 130 % over 8.9-18.4 s with linear keys) conflicts with the SOP's "10-15 % push"; the README follows the SOP.
- Conflict noted: editor-grade-motion says avoid dark blob scrims; the client rules require a scrim on white sets. README allows it on white sets only.
- Insert settle 1.06 -> 1 is kept for full-screen inserts; the "no zoom-settle" ban applies to the talking head.
- End-screen layout details, subscribe animation and data-chart specs beyond axes and bar radius.
