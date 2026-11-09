"""Check every look folder is complete and carries no client brand.

Run: python check_looks.py   (exit 1 on any problem)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent / "looks"
REQUIRED = ["README.md", "look.json", "skin.example.json"]
# Client names, people, characters and brand-only fonts. Provenance lives in provenance/, which is not scanned.
BANNED = [
    "mkp", "huggooling", "hug gooling", "gooling", "annababy", "anna", "loynx", "lonyx", "steroids",
    "sabri", "suby", "iilumo", "iilumolab", "meticulous", "daniel", "continue longevity", "continuelongevity",
    "abel", "arslan", "raihan", "james", "milkyano", "gcore", "neo refresh", "star car vault", "aspire",
    "mrsparkle", "kenny", "mochi", "bernie", "bruna", "polystories", "coolvetica", "bagel fat one",
    "batman", "_clients", "brains",
]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in BANNED) + r")\b", re.I)
TEXT = {".md", ".json", ".py", ".js", ".mjs", ".html", ".css", ".txt", ".jsx", ".ts"}


def check(look: Path) -> list[str]:
    errs = [f"missing {f}" for f in REQUIRED if not (look / f).exists()]
    if errs:
        return errs
    try:
        spec = json.loads((look / "look.json").read_text(encoding="utf-8"))
        skin = json.loads((look / "skin.example.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"bad json: {e}"]
    for k in ("name", "slug", "skin_slots"):
        if k not in spec:
            errs.append(f"look.json missing '{k}'")
    if spec.get("slug") != look.name:
        errs.append(f"slug '{spec.get('slug')}' != folder '{look.name}'")
    missing = set(spec.get("skin_slots", {})) - set(skin)
    if missing:
        errs.append(f"skin.example.json missing slots: {sorted(missing)}")
    for f in look.rglob("*"):
        if f.is_file() and f.suffix.lower() in TEXT:
            for n, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                m = BANNED_RE.search(line)
                if m:
                    errs.append(f"brand leak '{m.group(0)}' in {f.relative_to(look)}:{n}")
    return errs


if __name__ == "__main__":
    assert BANNED_RE.search("the MKP logo") and not BANNED_RE.search("annabelle panna")  # self-check
    bad = 0
    for look in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        errs = check(look)
        print(f"{'FAIL' if errs else 'ok  '} {look.name}")
        for e in errs[:15]:
            print(f"     - {e}")
        bad += bool(errs)
    sys.exit(1 if bad else 0)
