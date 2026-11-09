# Provenance: sticker-pop (Sticker Pop)

Origin tag: ours. Built from our own HugGooling talking-head comedy edits (24 Sep, 29 Sep, 2 Oct 2026 house look) and the annababy emoji / one-word-caption system, plus the house meme pass and the IG question sticker. The "Replying to" sticker copies the public Instagram reply-sticker UI.

## Inspo
- Instagram comment-reply sticker (measured off a real one, scaled to 1080 wide).
- Creator TikTok/Reels energy: reaction emoji on every beat (annababy's own approved cut was the ground truth).

## Source skills and paths
- `C:\Users\adeki\.claude\skills\huggooling-editing\SKILL.md`: sync-first workflow, rough-cut tightness numbers (3b), SRT style (3c), review rounds 3e/3g, zooms, pops, SFX palette, Premiere delivery.
- `C:\Users\adeki\.claude\skills\milkyano-video-editing\SKILL.md`: house rules this extends (SRT final, 20 chars, safe box, pop animation, zoom rules, music untouched, repeated-word stickers).
- `C:\Users\adeki\.claude\skills\annababy-editing\SKILL.md`: one-word subtitle variant (pop 72 > 82 > 80 over 0.2 s, Tahoma Bold 45 px pink #F8A4DA, stroke 6), awkward-silence rule, crossfades, loudness.
- `C:\Users\adeki\.claude\skills\annababy-emoji\SKILL.md`: emoji-per-beat rules measured on the approved 40.6 s cut (position 0.4898/0.6380, scale 164, cadence, GIF-first, loop by duplication, family mixing, section-header blanks).
- `C:\Users\adeki\.claude\skills\meme-pass\SKILL.md`: meme placement, key formula, ledger, vine boom rules.
- `C:\Users\adeki\.claude\skills\ig-question-sticker\` (SKILL.md, `ig_sticker.py`).
- Style DNA `R:\BATMAN\brains\HugGooling\style_dna\dna.json` (version 2026-10-26): canvas, fonts, colours, effects, motion, timing, captions, placement, sfx_roles, audio, do, dont. The main source of the numbers.
- `R:\BATMAN\brains\annababy\hub\CONTEXT.md` (no style_dna folder there; the hub points to `R:\Apps\Claude code\_STYLE_DNA\annababy\dna.json`, not read).

## Dates
- Highlight font approved 28 Sep 2026; huggooling-editing built 1 Oct; zoom rule (scale only 100/115, centred) 3 Oct; review round 3 Oct; HugGooling DNA versions 20 Oct and 26 Oct.
- annababy emoji system measured mid Oct 2026; annababy inactive since 16 Oct 2026.
- IG question sticker skill: Oct/Nov 2026 (date not in the file).

## Skins that exist today
- HugGooling (talking-head comedy look): yellow #FCD127, ink #111111, highlight font Bagel Fat One, captions Helvetica Neue Bold, script Great Vibes, gold #E8B455 / black #1C1C1C colour words, red strike #E23B3B, URL pill text, locked CTA lines, copy bans ("body pillow", "bolster", "polyester", medical promises), Kevin MacLeod beds. Values live in `R:\BATMAN\brains\HugGooling\style_dna\dna.json` and `R:\Apps\Claude code\_CLIENTS\HugGooling\CONTEXT.md`. Fonts in `R:\BATMAN\archive\HugGooling\huggooling_29sep\fonts\`.
- annababy (emoji-per-beat + one-word captions): pink #F8A4DA Tahoma Bold captions, emoji library `D:\annababy\assets\EMOJI` (750 files with emotion catalogues), Premiere drop-shadow preset "annababy facecam shadow". Client inactive.
- The look.json defaults (Lilita One, Inter, #FFD43B) are neutral stand-ins, not a skin.

## Tools
- Copied: `tools/ig_sticker.py` from `skills\ig-question-sticker\ig_sticker.py`. Changes: `--skin` reads `font_sticker`, `avatar_dir`, `emoji_cache_dir`; font lookup no longer crashes when SF Pro is missing (clear exit instead); empty avatar folder gives a clear exit; self-test makes its own avatar and uses a neutral question. Measurements, wrapping, emoji regex and ffmpeg burn are unchanged. `--selftest` passes with and without the demo skin.
- Left in place (client-tied or machine paths):
  - `R:\BATMAN\archive\HugGooling\huggooling_29sep\gfx29.py`, `render29.py`, `plan29.py`, `cute_faces.py`, `censor29.py`, `clean_dialogue.py` (PIL sprite engine, face censor, beep, dialogue clean; all read HugGooling paths and constants).
  - `R:\BATMAN\archive\HugGooling\huggooling_2oct\render4.py` + `sfx_onsets.json` (engine with safe-border abort and measured SFX onsets).
  - `R:\BATMAN\engines\HugGooling\` (engine.json, render.py, pipeline.py, job templates).
  - `R:\Apps\Claude code\huggooling_24sep\` (`make_srt.py`, `retime.py`, `align.py`, `online\` scripts) and `R:\Apps\remotion\src\couchtalk\` (Remotion components).
  - annababy stream-highlight scripts (`render_v2.py`, `v2_edl.py`, `mms_align.py`) in her Drive project folder.
  - meme keying code in `R:\Apps\Claude code\_CLIENTS\Meticulous\refs\sfx_pool_proposal\render_job.py` (`load_meme`, `crop_alpha`, `meme`).

## Not carried over
- Fonts (Bagel Fat One, Helvetica Neue Bold, SF Pro, Tahoma), the emoji/GIF library, avatars, the iOS emoji cache, meme pack, SFX and music files. Named as asset types in the skin slots.
- annababy's Premiere drop-shadow preset values (it is a saved preset; numbers were not recorded).
- The 6 s B-roll ad, static ad, personal-brand and brain-rot variants in the HugGooling DNA (other looks).
- Client copy rules beyond the generic `copy_bans` slot.
