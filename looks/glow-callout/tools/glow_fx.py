# -*- coding: utf-8 -*-
"""Glow Callout renderer: the After Effects callout look rebuilt in Python (no AE needed).

Brand values come from a skin json (same keys as ../skin.example.json). Point the env var LOOK_SKIN at it before import:
    set LOOK_SKIN=path\to\skin.json
    python -c "import glow_fx as fx; ..."
Without a skin it falls back to neutral defaults and prints a warning.

Measured values (from the source After Effects comps and a finished frame):
- display font authored 48 px, sized by layer scale (237 % = 114 px etc.); Drop Shadow 80 % / 7 px / 20 (drop_shadow)
- Deep Glow 2: reverse-engineered from a real frame (tight bright halo + long faint tail, ADDITIVE: it lights the letters too,
  a #00DEFF text reads 31/254/248). Radius scales with the layer. Exposure 0.268 default; 0.10 for white two-line text, 0.12 logos.
- NWX pop: 14 % -> 100 % (+3 f) -> 116 % (+6 f) -> 100 % (+21 f) at 59.94
- lines of one callout staggered 0 / 0.05 / 0.10 s; every highlight fades out (0.25 s, the scrim with it)
- scrim (SCRIM_MAX 1.0): top black at y -0.11 -> clear at 0.503, bottom clear at 0.477 -> black at 1.086;
  'top_dense' (0.8 black, ends sooner) for text over a bright subject, 'left' for text on the left edge
- motion blur on the pop: 180-degree shutter, phase -90, 10 samples
- text_element prints 'WARN text shrunk to fit' when a card is too wide for its size: rewrite the text instead
"""
import json
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 60000 / 1001
WHITE = (255, 255, 255)
GLOW_RADIUS, GLOW_EXPOSURE = 416.0, 0.268
GLOW_GAIN = 0.7             # (old model, unused since the reverse-engineering; kept for calibration scripts)
GLOW_EASE = 2.0

_hx = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
_skin = {}
if os.environ.get("LOOK_SKIN"):
    try:
        _skin = json.load(open(os.environ["LOOK_SKIN"], encoding="utf-8"))
    except (OSError, ValueError) as _e:
        print("glow_fx: skin not loaded, using neutral defaults:", _e)
else:
    print("glow_fx: LOOK_SKIN not set, using neutral defaults")
FONT = _skin.get("font_display_file") or "arial.ttf"   # PIL finds arial.ttf on Windows; set a rounded sans in the skin
HIGHLIGHT_POSITIVE = _hx(_skin.get("highlight_positive", "#33CCFF"))
HIGHLIGHT_NEGATIVE = _hx(_skin.get("highlight_negative", "#FF3333"))
HIGHLIGHT_PRICE = _hx(_skin.get("highlight_price", "#33FF33"))
GLOW_EXPOSURE = float(_skin.get("glow_exposure", GLOW_EXPOSURE))
# Deep Glow, reverse-engineered 15 Oct 2026 from a real finished frame (dg_profile.py measures the profile below the letters,
# dg_fit2.py fits these weights): glow = sum_k w_k * gaussian(sigma_k * px / DG_PX_REF) of the text alpha (coloured), at exposure 0.268.
# Fit error under 3 % from 1 px to 160 px off the letter edge. Radius scales with the layer (px = 48 * layer scale).
DG_SIG = [1.2, 2.5, 5, 10, 20, 40, 80, 130]
DG_W = [0.3076, 0.1127, 0.0111, 0.4115, 0.0506, 0.5211, 0.3236, 0.0]
DG_PX_REF = 110.3
DG_COLOUR_LIFT = 0.4        # glow colour = text colour ** 0.4 (the real glow is a touch whiter than the text: G ~ B on cyan)
TRACK_HERO = 0.0            # em; typography.md TEST rule: -0.02 on hero words 150 px and up (A/B in ab_test.py)
SHUTTER_SAMPLES = 10


def s2l(x):  # sRGB 0..1 -> linear
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


_S2L = None


def s2l_u8(u8):
    """s2l(u8 / 255) through a 256-entry table of s2l's own float32 results (same values, no per-pixel pow)"""
    global _S2L
    if _S2L is None:
        _S2L = s2l(np.arange(256, dtype=np.float32) / 255)
    return _S2L[u8]


def l2s(x):
    x = np.clip(x, 0, None)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(x, 1 / 2.4) - 0.055)


# ---------------------------------------------------------------- NWX pop
def _hermite(a, b, u, ease_in, ease_out):
    # cubic bezier-style ease: ease_out = fast start, ease_in = slow end
    if ease_in and ease_out:
        u = u * u * (3 - 2 * u)
    elif ease_out:
        u = 1 - (1 - u) ** 3
    elif ease_in:
        u = u ** 3
    return a + (b - a) * u


def nwx_scale(t):
    """layer scale factor t seconds after the layer in-point (0 before)."""
    if t < 0:
        return 0.0
    k = [(0.0, 0.14), (0.05, 1.0), (0.10, 1.16), (0.35, 1.0)]
    if t >= k[-1][0]:
        return 1.0
    for (t0, v0), (t1, v1), mode in zip(k, k[1:], ["out", "out", "both"]):
        if t <= t1:
            u = (t - t0) / (t1 - t0)
            return _hermite(v0, v1, u, mode in ("in", "both"), mode in ("out", "both"))
    return 1.0


# ---------------------------------------------------------------- elements
class Element:
    """one AE layer on a full-frame canvas: text (or PNG) and its bloom kept apart so the bloom can ease in.
    text, glow: premultiplied linear float32 HxWx4. anchor: the scale centre (x, y)."""
    TEXT_FADE = 0.10   # text opacity 0 -> 100 during the pop
    GLOW_FADE = 0.25   # bloom eases in right behind the pop (user 2026-10-10: no flash; 2026-10-15: 'needs to look like Deep Glow')

    def __init__(self, text, glow, anchor, t_in, t_out, fade_out=0.0):
        self.text, self.glow, self.anchor, self.t_in, self.t_out, self.fade_out = text, glow, anchor, t_in, t_out, fade_out

    def _look(self, lt):
        a = min(1.0, max(0.0, lt / self.TEXT_FADE))
        u = min(1.0, max(0.0, lt / self.GLOW_FADE))
        g = u * u * (3 - 2 * u)
        img = self.text * a
        if self.glow is not None and g > 0:
            # Deep Glow is additive: it lights the letters too (real letters measure 31/254/248 on a #00DEFF text),
            # so the bloom is added over the text, then clamped to the alpha the overlay carries.
            ta = img[..., 3:4]
            gc, ga = self.glow[..., :3] * g, self.glow[..., 3:4] * g
            alpha = ta + ga * (1 - ta)
            rgb = np.minimum(img[..., :3] + gc, alpha)
            img = np.concatenate([rgb, alpha], -1)
        return img

    def frame(self, t):
        """premult linear RGBA at time t with NWX pop + motion blur, or None."""
        if t < self.t_in - 0.5 / FPS or t >= self.t_out:
            return None
        lt = t - self.t_in
        op = 1.0
        if self.fade_out and t > self.t_out - self.fade_out:
            op = max(0.0, (self.t_out - t) / self.fade_out)
        if lt > 0.40:  # scale settled; only the bloom may still be easing
            return self._look(lt) * op
        acc, ns = None, 0
        for i in range(SHUTTER_SAMPLES):  # 180 deg shutter, phase -90
            ts = lt + (-0.25 + 0.5 * (i + 0.5) / SHUTTER_SAMPLES) / FPS
            s = nwx_scale(ts)
            if s <= 0:
                continue
            ax, ay = self.anchor
            M = np.float32([[s, 0, ax * (1 - s)], [0, s, ay * (1 - s)]])
            img = cv2.warpAffine(self._look(max(ts, 0)), M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
            acc = img if acc is None else acc + img
        if acc is None:
            return None
        return acc / SHUTTER_SAMPLES * op


def _blur(img, s):
    f = max(1, int(s / 6))
    if f == 1:
        return cv2.GaussianBlur(img, (0, 0), max(0.5, s))
    small = cv2.resize(img, (W // f, H // f), interpolation=cv2.INTER_AREA)
    b = cv2.GaussianBlur(small, (0, 0), max(0.6, s / f))
    return cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR)


def _glow(prem, px, exposure):
    """Deep Glow as measured on a real finished frame (see DG_*): tight bright halo + long faint tail, coloured like the text."""
    a = prem[..., 3:4]
    col = np.where(a > 1e-4, prem[..., :3] / np.maximum(a, 1e-4), 0)
    c = np.clip(col, 0, 1)
    src = (np.power(c, 1 - (1 - DG_COLOUR_LIFT) * c) * a).astype(np.float32)   # bright channels lift (G ~ B on cyan), dark channels stay dark (red stays red)
    k = px / DG_PX_REF
    out = np.zeros_like(src)
    for s_, w_ in zip(DG_SIG, DG_W):
        if w_ > 0:
            out += w_ * _blur(src, s_ * k)
    return out * (exposure / GLOW_EXPOSURE)


def _split_glow(rgba_srgb_u8, layer_scale, exposure=GLOW_EXPOSURE):
    """-> (text premult linear, bloom premult linear)"""
    a = rgba_srgb_u8[..., 3:4].astype(np.float32) / 255
    lin = s2l_u8(rgba_srgb_u8[..., :3]) * a
    text = np.concatenate([lin, a], -1).astype(np.float32)
    g = _glow(text, layer_scale * 48.0, exposure)
    ga = np.clip(np.max(g, -1, keepdims=True), 0, 1)
    glow = np.concatenate([np.minimum(g, ga), ga], -1).astype(np.float32)
    return text, glow


def text_width(t, px, track=None):
    """on-screen width of one run (same tracking rule as text_element)"""
    if track is None:
        track = TRACK_HERO if px >= 150 else 0.0
    font = ImageFont.truetype(FONT, int(round(px)))
    if not track:
        return font.getlength(t)
    return sum(font.getlength(ch) + track * px for ch in t) - track * px


def drop_shadow(text_prem, dist=7, soft=20, opacity=0.8):
    """AE Drop Shadow 80 % / 7 px / 20 (SOP non-negotiable 3): black, down-right, gaussian softness/2. Alpha only (rgb stays the text's)."""
    a = text_prem[..., 3]
    d = dist / 1.4142
    sh = cv2.warpAffine(a, np.float32([[1, 0, d], [0, 1, d]]), (W, H))
    sh = cv2.GaussianBlur(sh, (0, 0), soft / 2.0) * opacity
    out = text_prem.copy()
    out[..., 3] = a + sh * (1 - a)
    return out


def text_element(runs, px, cx, baseline, t_in, t_out, max_w=0.9 * W, fade_out=0.0, caps=False, lead=None, double=False,
                 track=None, align="center", exposure=GLOW_EXPOSURE, shadow=True):
    """runs: [(text, colour)] on one line, or a list of such lists for several lines (lead = line pitch px).
    px = on-screen font size (48 * layer scale). Anchor = centre of the text block. align='left': cx is the left edge.
    track = tracking in em (default: TRACK_HERO for px >= 150, else 0)."""
    lines = runs if isinstance(runs[0], list) else [runs]
    if caps:
        lines = [[(t.upper(), c) for t, c in ln] for ln in lines]
    if track is None:
        track = TRACK_HERO if px >= 150 else 0.0
    font = ImageFont.truetype(FONT, int(round(px)))

    def adv(t):          # width of a run, with tracking (per-character advance only when tracking is on)
        if not track:
            return font.getlength(t)
        return sum(font.getlength(ch) + track * px for ch in t)

    widths = [sum(adv(t) for t, _ in ln) - (track * px if track else 0) for ln in lines]
    if max(widths) > max_w:  # shrink to fit, never wrap (every hit is scale drift: typography.md section 1, fix the text instead)
        print("WARN text shrunk to fit:", [t for t, _ in lines[0]], round(px), "->", round(px * max_w / max(widths)))
        px *= max_w / max(widths)
        font = ImageFont.truetype(FONT, int(round(px)))
        widths = [sum(adv(t) for t, _ in ln) - (track * px if track else 0) for ln in lines]
    lead = lead or px * 1.2
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, (ln, w) in enumerate(zip(lines, widths)):
        x = cx if align == "left" else cx - w / 2
        y = baseline + i * lead
        for t, c in ln:
            if track:
                for ch in t:
                    d.text((x, y), ch, font=font, fill=tuple(c) + (255,), anchor="ls")
                    x += font.getlength(ch) + track * px
            else:
                d.text((x, y), t, font=font, fill=tuple(c) + (255,), anchor="ls")
                x += font.getlength(t)
    bb = im.getbbox()
    anchor = ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)
    text, glow = _split_glow(np.array(im), px / 48.0, exposure)
    if shadow:   # shadow=False gives the pure glyph alpha (dg_fit2.py needs it to fit the glow)
        text = drop_shadow(text)
    if double:  # the editor's duplicate payoff layer; off by default since the user found the bloom too strong
        glow = glow * 1.6
    return Element(text, glow, anchor, t_in, t_out, fade_out)


def image_element(path, width_px, cx, cy, t_in, t_out, glow_exposure=None, fade_out=0.0, fade_bottom=0.0):
    """fade_bottom: fraction of the icon height that dissolves to transparent at the bottom (USER 15 Oct: check/cross sit
    BEHIND the claim text, overlapping it, with the bottom of the icon masked to a soft dissolve)."""
    src = Image.open(path).convert("RGBA")
    h = int(round(src.height * width_px / src.width))
    src = src.resize((int(width_px), h), Image.LANCZOS)
    if fade_bottom:
        a = np.array(src).astype(np.float32)
        yy = (np.arange(h, dtype=np.float32) + 0.5) / h
        m = np.clip((1.0 - yy) / fade_bottom, 0, 1)
        m = m * m * (3 - 2 * m)
        a[..., 3] *= m[:, None]
        src = Image.fromarray(a.astype(np.uint8))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    im.alpha_composite(src, (int(cx - width_px / 2), int(cy - h / 2)))
    arr = np.array(im)
    if glow_exposure:
        text, glow = _split_glow(arr, width_px / 300.0, glow_exposure)
    else:
        a = arr[..., 3:4].astype(np.float32) / 255
        text, glow = np.concatenate([s2l_u8(arr[..., :3]) * a, a], -1).astype(np.float32), None
    return Element(text, glow, (cx, cy), t_in, t_out, fade_out)


# ---------------------------------------------------------------- scrim
# The ramp separates text from footage, so it sits on the text's side (user rule 2026-10-10).
# The measured ramps: top black at y -0.11 -> clear at 0.503; bottom clear at 0.477 -> black at 1.086.
# Entrance: opacity 0 -> 100 and the clear edge extends from the frame edge to its final y (ease-out).
_y = (np.arange(H, dtype=np.float32) + 0.5) / H
SCRIM_IN, SCRIM_MAX = 0.35, 1.0   # 1.0 = the measured ramp (factor 0.18 at the top edge); 0.85 was too weak for cyan over a white wall


def _ease_out(u):
    u = min(1.0, max(0.0, u))
    return 1 - (1 - u) ** 3


def scrim_alpha(t, t_in, t_out, band="low", fade_out=0.0):
    """the scrim's alpha only: None, a (H,) float32 column (one value per row: top/top_dense/low/mid) or a (H, W) array ('left').
    Same float32 ops as the full frame scrim() builds from it (16 Oct speed pass: the engine composites rows, not a full frame)."""
    if band is None or t < t_in - 0.5 / FPS or t >= t_out:
        return None
    u = _ease_out((t - t_in + 1 / FPS) / SCRIM_IN)
    if band == "left":  # text on the left edge, mid height: dark ramp from the left edge, soft vertical window
        x = (np.arange(W, dtype=np.float32) + 0.5) / W
        ramp = np.clip((0.62 - x) / 0.62, 0, 1)[None, :]
        vwin = np.clip(1 - (np.abs(_y - 0.5) - 0.07) / 0.09, 0, 1)[:, None]
        op = min(1.0, (t_out - t) / fade_out) if fade_out else 1.0
        return (ramp * vwin * 0.85 * u * op).astype(np.float32)
    if band == "top_dense":  # text over a bright subject (white shirt): the dark zone reaches 0.8 black and ends sooner
        edge = 0.52 * u
        d = np.clip((edge - _y) / 0.32, 0, 1)
        d = d * d * (3 - 2 * d)
        op = min(1.0, (t_out - t) / fade_out) if fade_out else 1.0
        return (d * 0.8 * u * op).astype(np.float32)
    if band == "top":
        edge = 0.503 * u
        d = np.clip((edge - _y) / (edge + 0.11), 0, 1) if edge > 0 else np.zeros_like(_y)
    else:  # 'low' (lower third) or 'mid' (text in the middle: the clear edge goes higher)
        final = 0.477 if band == "low" else 0.30
        edge = 1.0 - (1.0 - final) * u
        d = np.clip((_y - edge) / (1.086 - edge), 0, 1)
    op = min(1.0, (t_out - t) / fade_out) if fade_out else 1.0
    return (d * SCRIM_MAX * u * op).astype(np.float32)


def scrim(t, t_in, t_out, band="low", fade_out=0.0):
    a = scrim_alpha(t, t_in, t_out, band, fade_out)
    if a is None:
        return None
    out = np.zeros((H, W, 4), np.float32)
    out[..., 3] = a if a.ndim == 2 else a[:, None]
    return out


# ---------------------------------------------------------------- compositing
def over(dst, src):
    """premult linear 'over'."""
    if src is None:
        return dst
    return src + dst * (1 - src[..., 3:4])


def to_srgb_rgba(prem):
    """premult linear -> straight sRGB RGBA uint8 (what Premiere composites)."""
    a = prem[..., 3:4]
    rgb = np.where(a > 1e-6, prem[..., :3] / np.maximum(a, 1e-6), 0)
    rgb = l2s(np.clip(rgb, 0, 1))
    return (np.concatenate([rgb, a], -1) * 255 + 0.5).clip(0, 255).astype(np.uint8)


def comp_on(bg_srgb_u8, prem):
    """composite an overlay onto an sRGB frame the way Premiere does (normal blend, sRGB)."""
    o = to_srgb_rgba(prem).astype(np.float32) / 255
    bg = bg_srgb_u8.astype(np.float32) / 255
    out = o[..., :3] * o[..., 3:4] + bg * (1 - o[..., 3:4])
    return (out * 255 + 0.5).astype(np.uint8)


# ---------------------------------------------------------------- stacks and face-aware placement (USER 15 Oct 2026)
# User-calibrated IG/TikTok safe box on 1080x1920 (memory feedback_caption_length_safe_zone): x 55-1022, y 238-1636,
# and below y 955 nothing right of x 910 (like/comment column). Override with skin key safe_box.
SAFE, SAFE_LOW_Y, SAFE_RIGHT_LOW = (55, 238, 1022, 1636), 955, 910
SAFE = tuple(_skin.get("safe_box", SAFE))
STACK_GAP_EM = 0.08   # gap between the ink of one line and the ink of the next, in em of the lower line ("spacing a lot closer")


def stack(lines, cx, top, t_in, t_out, gap_em=None, build=True):
    """lines: [(runs, px, opts)] top to bottom. Each line's ink starts gap_em*px below the ink of the line above, so the
    block stays tight whatever the descenders are. top = y of the first line's ink top. Returns (elements, ink_bottom_y).
    build=False: layout only (elements are None, same ink_bottom_y), for measuring a block before placing it."""
    gap_em = STACK_GAP_EM if gap_em is None else gap_em
    if top < SAFE[1]:  # IG/TikTok UI covers the top: push down, never let it sit higher
        print(f"SAFE: stack top {top:.0f} above y {SAFE[1]}, moved down")
        top = SAFE[1]
    els, bottom = [], None
    for runs, px, opts in lines:
        font = ImageFont.truetype(FONT, int(round(px)))
        txt = "".join(s for s, _ in runs)
        l, tp, r, b = font.getbbox(txt.upper() if opts.get("caps") else txt, anchor="ls")
        base = (top if bottom is None else bottom + gap_em * px) - tp
        opts = dict(opts)
        # centred on x 540 always; the safe box only limits WIDTH (USER: never shift left, shrink or shorten instead)
        right = SAFE_RIGHT_LOW if base + b > SAFE_LOW_Y else SAFE[2]
        opts.setdefault("max_w", 2 * min(cx - SAFE[0], right - cx))
        els.append(text_element(runs, px, cx, base, t_in, t_out, **opts) if build else None)
        bottom = base + b
    if bottom > SAFE[3]:
        print(f"SAFE: stack bottom {bottom:.0f} below y {SAFE[3]} (platform UI)")
    return els, bottom


_YUNET = _skin.get("face_model") or os.environ.get("YUNET_ONNX", "face_detection_yunet_2023mar.onnx")   # OpenCV Zoo YuNet


def face_box(frame_rgb):
    """largest face as (x0, y0, x1, y1) in frame px, or None. YuNet, same model the face-censor tools use."""
    h, w = frame_rgb.shape[:2]
    det = cv2.FaceDetectorYN.create(_YUNET, "", (w, h), 0.6)
    _, faces = det.detect(cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
    if faces is None or not len(faces):
        return None
    x, y, fw, fh = max(faces, key=lambda f: f[2] * f[3])[:4]
    return (x, y, x + fw, y + fh)


def hits_face(face, y0, y1, margin=0.06):
    """True when a text block spanning y0..y1 (plus its bloom) would reach the face."""
    return face is not None and y1 + margin * H > face[1] and y0 - margin * H < face[3]


def stack_above_head(lines, frame_rgb, cx, t_in, t_out, gap_frac=0.025):
    """USER 15 Oct: top-band hooks sit just above the speaker's head, not up at the top of the safe box.
    Bottom of the block = top of the hair (face box top minus 45% of the face height) minus a small gap; never above y 238."""
    els, b = stack(lines, cx, SAFE[1], t_in, t_out)
    face = face_box(frame_rgb)
    if face is None:
        return els, b
    head_top = face[1] - 0.45 * (face[3] - face[1])
    top = max(SAFE[1], head_top - gap_frac * H - (b - SAFE[1]))
    return stack(lines, cx, top, t_in, t_out)


# ---------------------------------------------------------------- the rest of the Style DNA (16 Oct): sizes, timing, spacing
# Builds ask for a level instead of a number: fx.SIZE["hero"] etc. Top of each type-ladder range.
SIZE = {"caption": 48, "support2": 68, "support1": 114, "punch": 154, "hero": 222}


# ---------------------------------------------------------------- speed (16 Oct 2026, user: 'render lama bet')
# The pop + motion blur runs on the element's own box (ink + glow, grown 18 % for the 116 % overshoot) and the look is
# built once per frame, not per shutter sample: 12x faster, max difference 1 % on the first pop frame only.
def _prep(self):
    a = self.text[..., 3] + (self.glow[..., 3] if self.glow is not None else 0)
    ys, xs = np.nonzero(a > 1e-4)
    ax, ay = self.anchor
    g = 1.18
    y0 = int(max(0, np.floor(ay - (ay - ys.min()) * g) - 4)); y1 = int(min(H, np.ceil(ay + (ys.max() + 1 - ay) * g) + 4))
    x0 = int(max(0, np.floor(ax - (ax - xs.min()) * g) - 4)); x1 = int(min(W, np.ceil(ax + (xs.max() + 1 - ax) * g) + 4))
    self._box = (y0, y1, x0, x1)
    self._t = self.text[y0:y1, x0:x1].copy()
    self._g = self.glow[y0:y1, x0:x1].copy() if self.glow is not None else None
    self._a = (ax - x0, ay - y0)


def _look_c(self, lt):
    a = min(1.0, max(0.0, lt / self.TEXT_FADE))
    u = min(1.0, max(0.0, lt / self.GLOW_FADE))
    g = u * u * (3 - 2 * u)
    if a >= 1.0 and g >= 1.0:          # text and bloom fully in: the look no longer changes, build it once (16 Oct speed pass)
        L = getattr(self, "_settled", None)
        if L is None:
            L = self._settled = _look_raw(self, a, g)
            L.flags.writeable = False
        return L
    return _look_raw(self, a, g)


# numba twin of _look_raw: same float32 ops in the same order on every core (16 Oct speed pass); numpy when numba is missing
try:
    from numba import njit as _njit, prange as _prange
except ImportError:
    _njit = None
_LOOK_NB = []


def _look_kernel():
    if not _LOOK_NB and _njit is not None:
        f32 = np.float32

        @_njit(parallel=True, cache=True)
        def k(t, gl, a, g, out):
            one = f32(1.0)
            for y in _prange(t.shape[0]):
                for x in range(t.shape[1]):
                    ta = t[y, x, 3] * a
                    al = ta + gl[y, x, 3] * g * (one - ta)
                    for c in range(3):
                        out[y, x, c] = min(t[y, x, c] * a + gl[y, x, c] * g, al)
                    out[y, x, 3] = al

        @_njit(parallel=True, cache=True)
        def add(acc, b):                       # acc += b
            for y in _prange(acc.shape[0]):
                for x in range(acc.shape[1]):
                    for c in range(4):
                        acc[y, x, c] = acc[y, x, c] + b[y, x, c]

        @_njit(parallel=True, cache=True)
        def div_mul(acc, d, m, use_m):         # acc = acc / d (* m)
            for y in _prange(acc.shape[0]):
                for x in range(acc.shape[1]):
                    for c in range(4):
                        v = acc[y, x, c] / d
                        acc[y, x, c] = v * m if use_m else v

        @_njit(parallel=True, cache=True)
        def mul(src, m, out):                  # out = src * m
            for y in _prange(src.shape[0]):
                for x in range(src.shape[1]):
                    for c in range(4):
                        out[y, x, c] = src[y, x, c] * m
        _LOOK_NB.extend([k, {"add": add, "div_mul": div_mul, "mul": mul}])
    return _LOOK_NB[0] if _LOOK_NB else None


def _ops():
    """float32 add / divide-multiply / multiply kernels (same IEEE ops as numpy's in-place ones), or None without numba"""
    return _LOOK_NB[1] if _look_kernel() is not None else None


def _look_raw(self, a, g):
    # Python floats only: an np.float64 time makes numpy promote the look to float64, and that caller keeps the numpy path
    if self._g is not None and g > 0 and type(a) is float and type(g) is float and _look_kernel() is not None:
        out = np.empty_like(self._t)
        _look_kernel()(self._t, self._g, np.float32(a), np.float32(g), out)
        return out
    img = self._t * a
    if self._g is not None and g > 0:
        ta = img[..., 3:4]
        gc, ga = self._g[..., :3] * g, self._g[..., 3:4] * g
        alpha = ta + ga * (1 - ta)
        rgb = np.minimum(img[..., :3] + gc, alpha)
        img = np.concatenate([rgb, alpha], -1)
    return img


def frame_box(self, t):
    """-> (crop premult linear float32, (y0, y1, x0, x1)) or None. The crop is read-only when the card is settled (shared cache)."""
    if t < self.t_in - 0.5 / FPS or t >= self.t_out:
        return None
    if not hasattr(self, "_box"):
        _prep(self)
    y0, y1, x0, x1 = self._box
    lt = t - self.t_in
    op = 1.0
    if self.fade_out and t > self.t_out - self.fade_out:
        op = max(0.0, (self.t_out - t) / self.fade_out)
    if lt > 0.40:
        L = _look_c(self, lt)
        K = _ops() if L.dtype == np.float32 and type(op) is float else None
        if op == 1.0:
            crop = L                           # x * 1.0 is x: the settled crop is reused as is
        elif K is not None:
            crop = np.empty_like(L); K["mul"](L, np.float32(op), crop)
        else:
            crop = L * op
    else:
        acc, tmp, hw = None, None, (x1 - x0, y1 - y0)
        L = _look_c(self, max(lt, 0))          # look once per frame (fade/bloom move < 1/120 s inside the shutter)
        for i in range(SHUTTER_SAMPLES):
            ts = lt + (-0.25 + 0.5 * (i + 0.5) / SHUTTER_SAMPLES) / FPS
            s = nwx_scale(ts)
            if s <= 0:
                continue
            ax, ay = self._a
            M = np.float32([[s, 0, ax * (1 - s)], [0, s, ay * (1 - s)]])
            if acc is None:
                acc = cv2.warpAffine(L, M, hw, flags=cv2.INTER_LINEAR, borderValue=0)
            else:                              # in place: same sums, no new 16 MB array per sample
                tmp = cv2.warpAffine(L, M, hw, dst=tmp, flags=cv2.INTER_LINEAR, borderValue=0)
                K = _ops() if acc.dtype == np.float32 else None
                if K is not None:
                    K["add"](acc, tmp)
                else:
                    acc += tmp
        if acc is None:
            return None
        K = _ops() if acc.dtype == np.float32 and type(op) is float else None
        if K is not None:
            K["div_mul"](acc, np.float32(SHUTTER_SAMPLES), np.float32(op), op != 1.0)
        else:
            acc /= SHUTTER_SAMPLES
            if op != 1.0:
                acc *= op
        crop = acc
    return crop, self._box


def is_static(self, t):
    """True when frame_box(t) is the settled crop untouched (scale settled, look settled, no fade-out yet)."""
    lt = t - self.t_in
    return (self.t_in - 0.5 / FPS <= t < self.t_out and lt > 0.40 and lt >= self.TEXT_FADE and lt >= self.GLOW_FADE
            and not (self.fade_out and t > self.t_out - self.fade_out))


def frame(self, t):
    r = frame_box(self, t)
    if r is None:
        return None
    crop, (y0, y1, x0, x1) = r
    out = np.zeros((H, W, 4), np.float32)
    out[y0:y1, x0:x1] = crop
    return out


Element.frame_box = frame_box
Element.is_static = is_static
Element.frame = frame


# Memory (16 Oct 2026): 8 render workers ran out of RAM holding every element as two full-frame float32 arrays (66 MB each).
# CROP_ON_INIT = True keeps only the element's own box from creation (about 5x less). Off by default: dg_fit2.py reads e.text.
CROP_ON_INIT = False
_init_full = Element.__init__


def _init_crop(self, text, glow, anchor, t_in, t_out, fade_out=0.0):
    _init_full(self, text, glow, anchor, t_in, t_out, fade_out)
    if CROP_ON_INIT:
        _prep(self)
        self.text = self.glow = None


Element.__init__ = _init_crop
