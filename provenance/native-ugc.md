# Provenance: native-ugc

Origin: **cloned** (the method follows a paid ad course's "no editor" B-roll caption ad, Day 2 of the 100K Ad Challenge), with the client's brand rules layered on top.

## Source
- Skill `C:\Users\adeki\.claude\skills\huggooling-video-ads\SKILL.md` (last edited 3 Sep 2026): Mode 1 first batch, Mode 2 variations (incl. multi-clip and reference-style transplant), Mode 3 replicate a reference ad.
- Style DNA `R:\BATMAN\brains\HugGooling\style_dna\dna.json` (2026-10-26), `variants.video_ads_6s`: canvas 1080x1920 at 30 fps, 6.0 s, silent, 2-3 segment stitches (3 + 3 or 2 + 2 + 2 s), crf 16.
- First batch: `R:\Apps\Claude code\rheegan_batch\` (root, `v2\`, `v3\`; 23 ads built 3 Sep 2026, also archived in `R:\BATMAN\archive\HugGooling\rheegan_batch`). No build script was kept; the caption PNGs are 795x154 and 819x94.

## Inspo
- The course's single 6-second story block; Meta Ads Library sorted by impressions for references.
- TikTok/Instagram native caption boxes (black bold sans on white rounded boxes).

## Skins
- **HugGooling** (huggable pillows). Values today: the skill's brand-constraints section (banned words "body pillow", "bolster", "polyester"; product name never in a caption; no dashes; three locked lines; 8-angle bank with funnel stages; colourway list; Australian Gen Z audience) and `HugGooling_Content_Angles_Brief.pdf` (copy at `R:\Apps\Claude code\_RND\2026-10-20\huggooling\ws\handoff\`). Caption font in the shipped batch: Segoe UI Semibold 46 px (`C:\Windows\Fonts\seguisb.ttf`); the skill names Inter Bold.

## Tools
- None copied. No script exists for this look; the skill describes PIL box PNGs + ffmpeg overlay inline, and the README carries that procedure.

## Dates
- Skill written 3 Sep 2026. First batch 3 Sep 2026. Folded into this look 9 Nov 2026.

## Doubts and gaps
- The white-box caption in the skill was **rejected by the user on 3 Sep 2026** ("ini caption stylenya aneh, not IG style. remember the IG pills style?"), and an IG pill test too ("it looks IG but it's not IG. make sure the font is the same"). The root batch captions that passed ("okay those are great") were white text with a soft dark shadow and no box: Segoe UI Semibold 46 px, shadow blur 6, alpha 150/255, offset 2 px, wrap 34 characters, line gap 14, padding 24. That style is kept in look.json as `captions.alt_style_shadow`. No ad from the batch ever ran.
- Box numbers in this look (Inter Bold 50 px, radius 16, padding 24 x 14, gap 10, max width 900) are house defaults chosen to match the platform text tool. They were not measured from a client final. Measure a real TikTok/IG native caption frame before relying on them.
- The skill's own band rule (y 320-1600, middle two-thirds) and the DNA's `video_ads_6s` were kept. The later "UGC native" type for the same client (26 Oct 2026, `R:\BATMAN\brains\HugGooling\ugc_native\dna.json`: one white native-font line, 10-12 s, trending sound) is a different look and was not merged.
- The course mentions "about seven proven video formats" for Day 3 that were never reviewed; only the single-clip and multi-clip formats are covered.
- User notes on the cuts (show the product in use, "keep her hugging it", "cut it properly") are generalised to "show the product in use".
