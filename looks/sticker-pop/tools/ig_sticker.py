"""Instagram "Replying to <user>" question sticker, burned onto a vertical video (or saved as a PNG overlay).

python ig_sticker.py --video in.mp4 --out out.mp4 --q "bf won't stay home, help 😭" [--user name] [--avatar file]
                     [--start 0] [--end 6.9] [--top 160] [--skin skin.json]
python ig_sticker.py --png sticker.png --q "..."        # transparent 1080x1920 overlay only
python ig_sticker.py --selftest
--skin reads font_sticker, avatar_dir and emoji_cache_dir; without it: the first installed UI sans, ./avatars, ./emoji_cache.
"""
import argparse, glob, json, os, random, re, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.expandvars(r"%LOCALAPPDATA%/Microsoft/Windows/Fonts/")
FONT = next((p for p in (FD + "SF-Pro-Text-Regular.otf", "C:/Windows/Fonts/SF-Pro-Text-Regular.otf",
                         "C:/Windows/Fonts/segoeui.ttf") if os.path.exists(p)), None)
AVATARS, EMOJI_CACHE = os.path.join(HERE, "avatars"), os.path.join(HERE, "emoji_cache")


def load_skin(path):
    global FONT, AVATARS, EMOJI_CACHE
    s = json.load(open(path, encoding="utf-8"))
    FONT = s.get("font_sticker", FONT)
    AVATARS = s.get("avatar_dir", AVATARS)
    EMOJI_CACHE = s.get("emoji_cache_dir", EMOJI_CACHE)
    if not FONT or not os.path.exists(FONT):
        raise SystemExit(f"sticker font not found: {FONT}")
W, H, SS = 1080, 1920, 2
# measured off a real IG reply sticker, scaled to 1080 wide
PAD_L, AV, AV_GAP, PAD_R, PAD_T, PAD_B, LINE, RAD = 40, 80, 32, 44, 40, 40, 62, 42
QPX, RPX, EMO, MAXTXT = 46, 37, 50, 620

E1 = "[🀀-🫿☀-➿]️?[🏻-🏿]?"
EMOJI_RE = re.compile(f"({E1}(?:‍{E1})*)")  # one emoji, incl. skin tone + ZWJ sequences

def emoji_png(e):
    code = "-".join(f"{ord(c):x}" for c in e if c != "\ufe0f")
    p = os.path.join(EMOJI_CACHE, code + ".png")
    if not os.path.exists(p):
        os.makedirs(EMOJI_CACHE, exist_ok=True)
        url = f"https://cdn.jsdelivr.net/npm/emoji-datasource-apple@15.0.1/img/apple/64/{code}.png"
        urllib.request.urlretrieve(url, p)
    return Image.open(p).convert("RGBA")

def parts(s):
    return [x for x in EMOJI_RE.split(s) if x]

def tlen(f, s, emo):
    return sum(emo + 6 if EMOJI_RE.fullmatch(x) else f.getlength(x) for x in parts(s))

def wrap(f, text, emo):
    def greedy(maxw):
        out, cur = [], ""
        for w in text.split():
            t = (cur + " " + w).strip()
            if tlen(f, t, emo) > maxw and cur:
                out.append(cur); cur = w
            else:
                cur = t
        return out + [cur]
    n, w = len(greedy(MAXTXT)), MAXTXT
    while w > 200 and len(greedy(w - 10)) == n:      # balance lines, no orphan word
        w -= 10
    return greedy(w)

FIRST = ["bec", "jess", "maddie", "danny", "milo", "tash", "kev", "lulu", "remy", "soph", "ziggy", "bri", "noah", "kiki", "tom"]
LAST = [".harlow_", "_tanaka", ".oconnell", "reyes88", "_the_lab_dad", "pugsandpasta", ".xo", "_ffs", ".cooks", "_waffle",
        "lol", ".mp4", "_irl", "2003", ".jpeg", "_n0t_a_bot"]

def random_user():
    return random.choice(FIRST) + random.choice(LAST)

def random_avatar():
    pool = glob.glob(os.path.join(AVATARS, "*.*"))
    if not pool:
        raise SystemExit(f"no avatar images in {AVATARS}: add some or pass --avatar")
    return random.choice(pool)

def sticker(q, user, avatar):
    f, fr = ImageFont.truetype(FONT, QPX), ImageFont.truetype(FONT, RPX)
    lines = wrap(f, q, EMO)
    reply = f"Replying to {user}"
    tw = max([tlen(f, l, EMO) for l in lines] + [fr.getlength(reply)])
    bw = int(PAD_L + AV + AV_GAP + tw + PAD_R)
    bh = int(PAD_T + LINE * len(lines) + 8 + 50 + PAD_B - 14)
    s = SS
    img = Image.new("RGBA", (bw * s, bh * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, bw * s - 1, bh * s - 1), RAD * s, fill=(255, 255, 255, 255))
    av = Image.open(avatar).convert("RGB")
    m = min(av.size)
    av = av.crop(((av.width - m) // 2, (av.height - m) // 2, (av.width + m) // 2, (av.height + m) // 2)).resize((AV * s, AV * s), Image.LANCZOS)
    mask = Image.new("L", av.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, AV * s - 1, AV * s - 1), fill=255)
    img.paste(av, (PAD_L * s, (PAD_T + 4) * s), mask)
    fq, frs = ImageFont.truetype(FONT, QPX * s), ImageFont.truetype(FONT, RPX * s)
    x0, y = (PAD_L + AV + AV_GAP) * s, PAD_T * s
    for l in lines:
        x = x0
        for p in parts(l):
            if EMOJI_RE.fullmatch(p):
                img.alpha_composite(emoji_png(p).resize((EMO * s, EMO * s), Image.LANCZOS), (int(x + 6 * s), int(y + 4 * s)))
                x += (EMO + 6) * s
            else:
                d.text((x, y), p, font=fq, fill=(18, 18, 18, 255)); x += fq.getlength(p)
        y += LINE * s
    d.text((x0, y + 8 * s), reply, font=frs, fill=(142, 142, 142, 255))
    return img.resize((bw, bh), Image.LANCZOS)

def overlay(q, user, avatar, top):
    st = sticker(q, user, avatar)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = (W - st.width) // 2                           # always centred horizontally
    a = Image.new("L", (W, H), 0); a.paste(st.split()[3].point(lambda v: v * 0.18), (x, top + 6))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.filter(ImageFilter.GaussianBlur(14)))
    canvas.alpha_composite(sh); canvas.alpha_composite(st, (x, top))
    return canvas

def burn(video, out, png, start, end):
    en = f"between(t,{start},{end})" if end else f"gte(t,{start})"
    # cover-scale to 1080x1920 (never squish), then overlay
    vf = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1[b];"
          f"[b][1:v]overlay=0:0:enable='{en}'[v]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", png, "-filter_complex", vf, "-map", "[v]", "-map", "0:a?",
                    "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy",
                    "-movflags", "+faststart", out], check=True)

def selftest():
    assert EMOJI_RE.fullmatch("😭") and not EMOJI_RE.fullmatch("help")
    assert parts("help 😭") == ["help ", "😭"] and parts("💀🙏") == ["💀", "🙏"]
    av = os.path.join(os.environ.get("TEMP", "/tmp"), "ig_selftest_avatar.png")
    Image.new("RGB", (64, 64), (200, 120, 90)).save(av)  # no avatar pool needed for the self-test
    img = overlay("what should i cook tonight?", "test_user", av, 160)
    assert img.size == (W, H) and img.getbbox()[1] >= 120  # shadow blur bleeds ~30px above
    print("selftest ok")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--q"); ap.add_argument("--user"); ap.add_argument("--avatar")
    ap.add_argument("--video"); ap.add_argument("--out"); ap.add_argument("--png")
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float)
    ap.add_argument("--top", type=int, default=160); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--skin")
    a = ap.parse_args()
    if a.skin:
        load_skin(a.skin)
    if not FONT:
        raise SystemExit("no sticker font found: pass --skin with font_sticker")
    if a.selftest:
        selftest(); raise SystemExit
    user, avatar = a.user or random_user(), a.avatar or random_avatar()
    img = overlay(a.q, user, avatar, a.top)
    png = a.png or os.path.splitext(a.out)[0] + "_sticker.png"
    img.save(png)
    if a.video:
        burn(a.video, a.out, png, a.start, a.end)
    print(json.dumps({"user": user, "avatar": os.path.basename(avatar), "png": png, "out": a.out}))
