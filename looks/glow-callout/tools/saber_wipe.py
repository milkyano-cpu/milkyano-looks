"""Saber outline wipe between cut-out subjects, rebuilt from an After Effects rig (VC Saber, Core Type = layer masks
auto-traced from the incoming cut-out). The subject's OUTLINE burns as an electric saber inside a moving band; the subject
appears behind it. Variable names say 'bike' because the rig was built for product cut-outs; any RGBA cut-out works.

Rig in the .aep (per wipe solid): Saber Preset 3, intensity 45, spread 0.18, bias 0.26, core size 1.6; Core Start x
-0.1W -> 1.1W in 0.7 s (linear). Linear Wipe A (angle 270, feather 30) completion = (x - 230) / W; Linear Wipe B
(feather 160) trails it. Bike PNG: Linear Wipe (angle 270, feather 25) driven by the same x.
So: leading edge L = x, reveal edge R = x - 230. Glow lives between R (fading over 160 px behind it) and L.

  python saber_wipe.py --png b.png --prev a.png --mode in --skin skin.json --out a_to_b.mov   # subject to subject
  python saber_wipe.py --png bike.png --mode in  --frames 42 --out in.mov
  python saber_wipe.py --png bike.png --mode out --frames 30 --hold 104 --out out.mov
  python saber_wipe.py --png bike.png --mode in --frames 42 --still 0.5 --bg plate.png --out check.png
  python saber_wipe.py --selftest
"""
import argparse, subprocess, sys
import numpy as np, cv2
from PIL import Image

W, H = 1080, 1920
RATE = '60000/1001'
OFFSET, FEATHER_LEAD, FEATHER_TRAIL, FEATHER_BIKE = 230.0, 30.0, 160.0, 25.0
X0, X1 = -0.1 * W, 1.1 * W + OFFSET          # keep going until the reveal edge has cleared the frame
SUB = 2

def hexcol(h): return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255

def outline(alpha):
    """Auto-trace like AE: every contour of the bike alpha (outer + holes: wheels, spokes, frame triangles)."""
    m = (alpha > 0.5).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cs = [c for c in cs if cv2.arcLength(c, True) > 40]
    return cs

def noise(seed, h, w, s):
    rng = np.random.default_rng(seed)
    g = rng.standard_normal((h // s + 3, w // s + 3)).astype(np.float32)
    return cv2.resize(g, ((w // s + 3) * s, (h // s + 3) * s), interpolation=cv2.INTER_CUBIC)[:h, :w]

class Rig:
    def __init__(self, bike, col, prev=None):
        self.bike = bike; self.col = col; self.prev = prev
        self.cs = outline(bike[..., 3])
        ys, xs = np.nonzero(bike[..., 3] > 0.5)
        self.box = (max(0, ys.min() - 120), min(H, ys.max() + 120))   # band height = bike + margin

    def core(self, f):
        """Electric core: contours re-drawn with a flickering wiggle (Saber 'energy' preset look)."""
        img = np.zeros((H, W), np.float32)
        rng = np.random.default_rng(1000 + f)
        dx = noise(2 * f + 1, H // 4, W // 4, 6); dy = noise(2 * f + 2, H // 4, W // 4, 6)
        for c in self.cs:
            p = c[:, 0, :].astype(np.float32)
            qi = np.clip((p / 4).astype(int), 0, [W // 4 - 1, H // 4 - 1])
            p[:, 0] += dx[qi[:, 1], qi[:, 0]] * 3.2; p[:, 1] += dy[qi[:, 1], qi[:, 0]] * 3.2
            cv2.polylines(img, [p.astype(np.int32).reshape(-1, 1, 2)], True, 1.0, 2, cv2.LINE_AA)
        # sparse arcs: random short bolts off the outline
        pts = np.concatenate([c[:, 0, :] for c in self.cs]) if self.cs else np.zeros((0, 2), int)
        for _ in range(28):
            if not len(pts): break
            a = pts[rng.integers(len(pts))].astype(np.float32); seg = [a]
            ang = rng.random() * 6.283
            for _ in range(5):
                ang += rng.normal(0, 0.8); a = a + np.array([np.cos(ang), np.sin(ang)]) * rng.uniform(5, 14); seg.append(a)
            cv2.polylines(img, [np.array(seg, np.int32).reshape(-1, 1, 2)], False, 0.8, 1, cv2.LINE_AA)
        return img * rng.uniform(0.85, 1.15)

    def frame(self, t, f, mode):
        x = X0 + (X1 - X0) * t
        L, R = x, x - OFFSET
        xs = np.arange(W, dtype=np.float32)[None, :]
        lead = np.clip((L - xs) / FEATHER_LEAD + 0.5, 0, 1)                 # 1 left of the leading edge
        trail = np.clip((xs - (R - FEATHER_TRAIL)) / FEATHER_TRAIL, 0, 1)    # fades out behind the reveal edge
        band = np.repeat(lead * trail, H, 0)
        y0, y1 = self.box; band[:y0] = 0; band[y1:] = 0
        shown = np.clip((R - xs) / FEATHER_BIKE + 0.5, 0, 1)                 # bike visible left of R
        m = shown if mode == 'in' else 1 - shown
        a_b = self.bike[..., 3] * np.repeat(m, H, 0)
        rgb = self.bike[..., :3] * a_b[..., None]
        if self.prev is not None and mode == 'in':                          # outgoing bike disappears behind the same edge
            a_p = self.prev[..., 3] * np.repeat(1 - shown, H, 0) * (1 - a_b)
            rgb = rgb + self.prev[..., :3] * a_p[..., None]; a_b = a_b + a_p
        c = self.core(f) * band
        # glow: white-hot core + three coloured falloffs (intensity 45 / spread 0.18 / bias 0.26 by eye)
        g1 = cv2.GaussianBlur(c, (0, 0), 3); g2 = cv2.GaussianBlur(c, (0, 0), 9); g3 = cv2.GaussianBlur(c, (0, 0), 26)
        haze = cv2.GaussianBlur(band * (self.bike[..., 3] > 0.5), (0, 0), 40) * 0.18     # soft energy haze in the band
        glow = (g1 * 2.2 + g2 * 2.6 + g3 * 2.4 + haze)[..., None] * self.col
        hot = np.clip(c * 1.4 + g1 * 0.6, 0, 1)[..., None] * (0.55 + 0.45 * self.col)  # core desaturates to white
        add = glow + hot
        rgb = rgb + add
        a = np.clip(a_b + np.clip(add.max(-1), 0, 1) * (1 - a_b), 0, 1)
        return np.clip(rgb, 0, None), a

def frames(rig, mode, n, hold):
    if mode == 'out':
        plain = (rig.bike[..., :3] * rig.bike[..., 3:4], rig.bike[..., 3].copy())
        for _ in range(hold): yield plain
    for i in range(n):
        acc_r = 0; acc_a = 0
        for s in range(SUB):
            t = min(1.0, (i + (s + 0.5) / SUB) / n)
            r, a = rig.frame(t, i, mode); acc_r = acc_r + r / SUB; acc_a = acc_a + a / SUB
        yield acc_r, acc_a

def write_mov(out, gen):
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-s', f'{W}x{H}', '-r', RATE,
                          '-i', '-', '-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', out],
                         stdin=subprocess.PIPE)
    n = 0
    for rgb, a in gen:
        st = np.clip(rgb / np.maximum(a[..., None], 1e-4), 0, 1)
        p.stdin.write((np.dstack([st, a]) * 65535).astype('<u2').tobytes()); n += 1
    p.stdin.close(); p.wait(); assert p.returncode == 0
    return n

def load(p):
    im = Image.open(p).convert('RGBA')
    assert im.size == (W, H), f'{p} is {im.size}, need {W}x{H}'
    return np.asarray(im, np.float32) / 255

def selftest():
    b = np.zeros((H, W, 4), np.float32); cv2.circle(b, (540, 1300), 200, (0.2, 0.2, 0.2, 1), 30)
    rig = Rig(b, hexcol('FF1E1E'))
    assert len(rig.cs) >= 2, 'outer + inner contour'
    _, a = rig.frame(0.0, 0, 'in'); assert a[1300, 350] < 0.05
    _, a = rig.frame(1.0, 0, 'in'); assert a[1300, 350] > 0.95
    _, a = rig.frame(1.0, 0, 'out'); assert a[1300, 350] < 0.05
    r, a = rig.frame(0.5, 0, 'in'); assert r[..., 0].max() > 0.5, 'glow present mid-wipe'
    p = np.zeros((H, W, 4), np.float32); p[100:200, 100:900] = 1
    rig2 = Rig(b, hexcol('FF1E1E'), p)
    _, a = rig2.frame(0.0, 0, 'in'); assert a[150, 500] > 0.95, 'outgoing bike shown before the edge'
    _, a = rig2.frame(1.0, 0, 'in'); assert a[150, 500] < 0.05, 'outgoing bike gone after the edge'
    print('selftest ok')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--png'); ap.add_argument('--mode', choices=['in', 'out']); ap.add_argument('--frames', type=int, default=42)
    ap.add_argument('--hold', type=int, default=0); ap.add_argument('--out'); ap.add_argument('--color', help='hex, overrides the skin'); ap.add_argument('--skin', help='skin json: saber_colour')
    ap.add_argument('--still', type=float); ap.add_argument('--bg'); ap.add_argument('--prev', help='outgoing bike PNG (bike-to-bike wipe)'); ap.add_argument('--selftest', action='store_true')
    r = ap.parse_args()
    if r.selftest: selftest(); sys.exit()
    if not r.color:
        r.color = 'FF1E1E'
        if r.skin:
            import json
            try:
                r.color = json.load(open(r.skin, encoding='utf-8')).get('saber_colour', '#FF1E1E')
            except (OSError, ValueError) as e:
                print('skin not loaded, using FF1E1E:', e)
    r.color = r.color.lstrip('#')
    rig = Rig(load(r.png), hexcol(r.color), load(r.prev) if r.prev else None)
    if r.still is not None:
        rgb, a = rig.frame(r.still, int(r.still * r.frames), r.mode)
        bg = np.asarray(Image.open(r.bg).convert('RGB').resize((W, H)), np.float32) / 255 if r.bg else np.full((H, W, 3), .1, np.float32)
        Image.fromarray((np.clip(rgb + bg * (1 - a[..., None]), 0, 1) * 255).astype(np.uint8)).save(r.out); sys.exit()
    print(write_mov(r.out, frames(rig, r.mode, r.frames, r.hold)), 'frames ->', r.out)
