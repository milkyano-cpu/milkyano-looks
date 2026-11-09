# Native UGC

Six-second vertical B-roll ads that look posted from a phone: one real clip, three short first-person lines in black bold sans on white rounded boxes, made in batches.

## What you get

- Output: caption-led B-roll video ad, no on-camera talent needed, no voiceover.
- Aspect: 9:16, 1080x1920.
- Frame rate: 30 fps (180 frames per ad).
- Length: exactly 6.0 s.
- Delivered files: H.264 mp4 per ad (crf 16, yuv420p), named `<angle> - <one-line concept>.mp4`. A batch is 4 to 10 ads.

## The look in detail

### Type

- One bold sans (`font_caption`), default Inter Bold. Closest bold sans if missing.
- 50 px on a 1080-wide frame (cap height about 36 px). Black text.
- Sentence case as a person would type it, `POV` in capitals. No dashes anywhere in the copy. `?` and `!` allowed, no full stop at the end of a line.
- Each line short enough to read at a glance: about 20-34 characters, one line per box.

### Colour roles

| Role | Default | Use |
|---|---|---|
| `caption_text` | #000000 | caption text |
| `caption_box` | #FFFFFF | rounded box behind each line, 100% opaque |
| footage | natural phone colour | no grade look, no LUT, no vignette |

### Motion

- None. All three caption boxes are on screen from frame 0 to frame 179. No staggered reveal, no pop, no zoom, no speed ramp.
- The footage carries the movement: one continuous handheld or static phone shot.

### Captions

- Three lines, each on its own white rounded rectangle sized to that line (never one block behind all three).
- Box: radius 16 px, padding 24 px left and right, 14 px top and bottom, 10 px gap between boxes.
- Boxes centred on x 540, each line centred in its box. Widest box at most 900 px.
- The block sits inside the middle two-thirds of the frame: y 320 to 1600. Nothing in the top or bottom sixth, so a 4:5 feed crop never cuts it. Also stay inside the platform safe box x 55-1022, y 238-1636, and left of x 910 below y 955.
- Never over the product. Pick the upper or lower part of the band, whichever is clear for all 6 s.
- Copy voice: the buyer talking casually, first person, a little unpolished. "I used to / now I" when it fits. "I" statements about what happened are fine; promises about what it will do for the viewer are not.

### Graphics and elements

- No logo, no end card, no CTA graphic, no emoji, no stickers. The three lines are the only graphic.
- Product name never written in a caption: refer to it as "this", "it" or the skin's plain noun.

### Sound

- Silent by default. Music is added in the platform at upload (licensed there).
- If the ad must carry sound, use a track you hold rights to at -14 LUFS, no SFX, no voiceover.

### Pacing and cut rhythm

- Single-clip ad: one clip, the best 6 continuous seconds, no cuts.
- Multi-clip variant (only after single-clip ads are working): 2 or 3 segments, 3 + 3 s or 2 + 2 + 2 s, hard cuts, same three captions held throughout.
- The bar is six usable seconds, not a usable clip. A messy 15 s clip with one clean 6 s window is enough.
- Show the product in use (hugged, worn, held, used), not tossed or just lying there.

## Do / Don't

Do:
- One box per line, black on white, all three visible the whole 6 s.
- Hands-and-product footage, window light, vertical.
- Name exports by angle and concept so winners can be traced in the ad manager.
- Change angle, copy and clip together for every variation.
- Flag any health or medical wording with `[MEDICAL CLAIM]` for human review.

Don't:
- One big box behind all three lines.
- Captions over the product, or in the top or bottom sixth.
- Animated text, outlines, stroked text, brand-colour boxes.
- Dashes, invented stats, research, experts, or "fixes / treats / cures" promises.
- The product name inside a caption.
- Reskinning the same ad with new text and calling it a variation.

## How to make it

1. Research who buys: current product details, price and reviews from the brand's site, plus competitor positioning. Note the words buyers actually use.
2. Read every clip in the folder. Note what each shows (close-up, hands, lifestyle, unboxing, wide). Descriptive file names help.
3. Pick an angle from the skin's angle bank that the strongest clip can carry.
4. Write 3 caption lines in the buyer's voice. Apply the skin's copy rules and banned words. End with the angle's locked line when the angle has one.
5. `ffprobe` the clip (duration, size, rotation). Trim the best 6 s: `ffmpeg -ss <start> -t 6`.
6. Scale to cover 1080x1920 (crop, never squish), 30 fps.
7. Draw each line as a PNG with PIL: rounded rectangle sized to the text bounds plus padding, black text. Composite with ffmpeg `overlay` at the chosen y. For a plain box, ffmpeg `drawtext` with `box=1:boxcolor=white@1:boxborderw=24` per line works, but it has square corners.
8. Export H.264 crf 16, 1080x1920, exactly 180 frames. Name it `<angle> - <concept>.mp4`.
9. Variations: next unused angle, new copy, new clip. Same specs.
10. Replicating a reference ad: download it (skill `instagram-download` or `yt-dlp`), pull a frame at each cut, read the on-screen text, then rebuild the same shot rhythm, caption length and box style with the skin's own footage and copy.

General skills: `ffmpeg`, `instagram-download`, `iphone-hlg-grade` for iPhone HDR clips, `broll-stabilize` if a clip is shaky.

## Skin slots

| Slot | Controls |
|---|---|
| `font_caption` | caption font name or file |
| `caption_text` | caption text colour |
| `caption_box` | caption box colour |
| `product_noun` | how captions refer to the product ("this", "a hug", "the bag") |
| `banned_words` | words never used in copy |
| `locked_lines` | fixed lines and where each one is allowed |
| `angle_bank` | angles with funnel stage and closing line |
| `audience` | who buys, in one sentence |
| `claims_policy` | what counts as a claim and how to flag it |

## Files in this folder

| File | Format |
|---|---|
| `README.md` | this guide |
| `look.json` | the look as data |
| `skin.example.json` | a neutral demo skin filling every slot |
