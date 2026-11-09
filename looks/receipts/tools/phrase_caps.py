"""Phrase captions: group spoken words into one-line captions by phrase, not by count.
  - max 3 words and 20 characters per line, one line;
  - never split a name or a fixed term: the generic UNITS below plus the skin's "caption_units" (product and place names);
  - a determiner / possessive / 'to' / 'of' stays with the word after it ("the paint", "to protect");
  - never end a line on a connector (and, but, with, by, as, that, which, ...);
  - lines like to start on a connector or a new clause ("to protect", "but to also");
  - a 'came in for' style phrasal verb stays together; force a break before a word with `brk`.
Hard breaks: sentence punctuation, commas, picture cuts, graphic start/end edges.
Example: this sedan | came in for | a full detail | to protect | the paint.
usage: spans(words, cuts, hide, n_frames, extra_units=(), brk=()) -> [(start_frame, end_frame, [(TEXT, f0, f1), ...]), ...]
`words` = [(TEXT upper, f0, f1)] with trailing punctuation kept.
CLI: python phrase_caps.py words.json [skin.json]   words.json = {"words": [[TEXT, f0, f1], ...], "cuts": [f, ...],
     "n_frames": N, "brk": [...]}  -> one caption per line: start end TEXT
     python phrase_caps.py --selftest"""
import re

UNITS = [  # generic fixed terms; product, model and place names come from the skin's "caption_units"
    "NUMBER ONE", "NUMBER 1", "5 STAR", "5-STAR", "FIVE STAR", "FIVE -STAR", "7 YEAR", "7 -YEAR", "10 YEAR", "10 -YEAR", "7 YEARS", "10 YEARS",
    "3 YEAR", "3 YEARS", "3 MONTH", "2 MONTHS", "10 MINUTES", "PEACE OF MIND", "LEARN MORE", "NEW CAR", "BRAND NEW", "ANNUAL CHECKUP",
    "FREE CHECKUP", "GOOGLE REVIEWS", "SINGLE RECALL", "ON THE SPOT", "ONE TO TWO WEEKS", "1 TO 2 WEEKS", "ANY SCRATCHES", "THE WHOLE CAR", "WHOLE CAR", "FULL OF",
]
GLUE_AFTER = {"THE", "A", "AN", "OUR", "HIS", "HER", "MY", "YOUR", "THIS", "THESE", "THOSE", "ITS", "THEIR", "EVERY", "ANY", "SOME", "NO", "TO", "OF", "THAT'S", "IT'S", "WE'RE", "YOU'RE",
              "BIG", "BUSY", "QUICK", "HEAVY", "MAJOR", "FRESH", "THIN", "HARD", "SUPER", "REALLY", "VERY", "ALSO"}
END_BAD = {"AND", "OR", "BUT", "WITH", "BY", "AS", "THAT", "WHICH", "IF", "SO", "BECAUSE", "WHILE", "WHEN", "FROM", "INTO", "WHO", "WHERE", "THE", "A", "AN", "OUR", "HIS", "HER", "MY", "YOUR", "TO", "OF", "THIS", "ITS", "THEIR", "WE", "I", "HE", "IT", "THEY", "YOU"}
STARTERS = {"TO", "AND", "BUT", "WHICH", "THAT", "WHEN", "WITH", "AS", "IF", "SO", "BECAUSE", "WHILE", "BY", "FROM", "WHERE", "WHO"}
PARTICLES = {"IN", "OUT", "UP", "BACK", "DOWN", "OFF"}


def norm(t):
    return re.sub(r"[^A-Z0-9']", "", t.upper())


def spans(words, cuts, hide, n_frames, extra_units=(), brk=(), maxch=20, maxw=3, brk_at=()):
    n = len(words)
    nm = [norm(w[0]) for w in words]
    bp = sorted(set(cuts) | {e for r in hide for e in r})
    nobreak = [False] * max(n - 1, 0)                     # nobreak[i]: do not break between word i and i+1
    for u in list(UNITS) + list(extra_units):
        toks = [norm(x) for x in u.split() if norm(x)]
        L = len(toks)
        for i in range(n - L + 1):
            if nm[i:i + L] == toks:
                for k in range(i, i + L - 1): nobreak[k] = True
    for i in range(n - 1):
        if nm[i] in GLUE_AFTER: nobreak[i] = True
    brk_set = {norm(b) for b in brk}

    def forced(i):                                         # forced line end after word i
        if i == n - 1: return True
        if words[i][0][-1] in ".?!,": return True
        if any(words[i][1] < b <= words[i + 1][1] for b in bp): return True
        return nm[i + 1] in brk_set or words[i + 1][1] in brk_at

    def cost(i, j):                                        # words[i:j] as one line
        seg = words[i:j]; txt = " ".join(w[0].strip(",.?!") for w in seg)
        if len(seg) > maxw or len(txt) > maxch: return None
        c = 1.0
        if len(seg) == 1: c += 1.4
        last = nm[j - 1]
        if last in END_BAD and words[j - 1][0][-1] not in ".?!,": c += 4.0
        if nm[i] in STARTERS: c -= 0.6
        if nm[i] in PARTICLES and i > 0: c += 0.3
        if j < n and nobreak[j - 1]: c += 8.0                          # this line ends inside a unit / glue
        return c

    INF = 1e9; best = [INF] * (n + 1); back = [0] * (n + 1); best[0] = 0
    for j in range(1, n + 1):
        for k in range(1, maxw + 1):
            i = j - k
            if i < 0: break
            if any(forced(m) for m in range(i, j - 1)): break
            c = cost(i, j)
            if c is not None and best[i] + c < best[j]: best[j] = best[i] + c; back[j] = i
    lines, j = [], n
    while j > 0: lines.append(words[back[j]:j]); j = back[j]
    lines.reverse()
    out = []
    for i, ln in enumerate(lines):
        st = ln[0][1]; en = ln[-1][2] + 6
        if i + 1 < len(lines): en = min(en, lines[i + 1][0][1]) if lines[i + 1][0][1] >= ln[-1][2] else ln[-1][2]
        nb = next((b for b in bp if b > st), n_frames)
        out.append((st, min(max(en, ln[-1][2]), nb), [(w[0].strip(",.?!"), w[1], w[2]) for w in ln]))
    return out


def tail_hide(scene_a, scene_b, last_word_frame, word_starts):
    """caption hide window for a graphic scene: hidden while the headline carries the words, back for the tail the headline does not say.
    word_starts = sorted start frames of all spoken words."""
    nxt = next((s for s in word_starts if s > last_word_frame), scene_b)
    if scene_b - nxt >= 6: return (scene_a, nxt)
    return (scene_a, scene_b)


def units_from_skin(path):
    """the skin's fixed terms (product, model and place names) that must never be split"""
    import json
    return [u.upper() for u in json.load(open(path, encoding="utf-8")).get("caption_units", [])]


def _selftest():
    ws = [(w, i * 10, i * 10 + 8) for i, w in enumerate("THIS FAMILY SUV CAME IN FOR PAINT CORRECTION TO PROTECT THE PAINT.".split())]
    got = [" ".join(t for t, _, _ in ln) for _, _, ln in spans(ws, [], [], 200, extra_units=["FAMILY SUV", "PAINT CORRECTION"], brk=["CAME"])]
    assert got == ["THIS FAMILY SUV", "CAME IN FOR", "PAINT CORRECTION", "TO PROTECT", "THE PAINT"], got
    print("selftest ok")


if __name__ == "__main__":
    import json, sys
    if sys.argv[1:2] == ["--selftest"]:
        _selftest(); raise SystemExit
    job = json.load(open(sys.argv[1], encoding="utf-8"))
    extra = units_from_skin(sys.argv[2]) if len(sys.argv) > 2 else []
    words = [tuple(w) for w in job["words"]]
    n = job.get("n_frames", words[-1][2] + 30 if words else 0)
    for st, en, ln in spans(words, job.get("cuts", []), job.get("hide", []), n, extra_units=extra, brk=job.get("brk", ())):
        print(st, en, " ".join(t for t, _, _ in ln))
