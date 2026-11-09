# Looks

Brand-free visual styles for short-form video and motion. Each folder in `looks/` is one look: what it looks like, the numbers behind it, and how to make it. A brand is applied on top as a skin (fonts, colours, logo), so any client can get any look.

| Look | Folder | What you see | Output |
|---|---|---|---|
| Glow Callout | `looks/glow-callout` | Rounded sans, keywords flash in highlight colours with a deep glow, gradient scrims, multi-colour hero words, saber light wipes | 9:16 talking-head short |
| Sticker Pop | `looks/sticker-pop` | Fat bubbly font with thick outline and hard shadow, emoji on spoken words, meme punch-ins, reply-sticker hooks | 9:16 talking / vlog / skit |
| Mono Punch | `looks/mono-punch` | Black and white, spring motion with real blur, shake on hits, flips to mono on beats | 9:16 founder short |
| Apple Product | `looks/apple-product` | Clean product hero shots, soft glow, slow premium moves, minimal type | Product ad |
| Receipts | `looks/receipts` | White captions with the spoken word in mint, proof screenshots in glowing cards, ding/buzzer on proof | 9:16 VO edit |
| Lab Notebook | `looks/lab-notebook` | Cream paper with a faint grid, one accent colour, line art drawing on, thin giant numbers | Faceless explainer reel |
| Calm Premium | `looks/calm-premium` | No glow, no neon, no bounce, one deep colour, slow calm easing | Talking-head / brand edit |
| Native UGC | `looks/native-ugc` | Black bold sans on white rounded boxes, 6-second cuts | 6 s B-roll caption ad |
| Cream Stop-Motion | `looks/cream-stop-motion` | Stop-motion characters on a cream set, soft shadows, brown bold captions | Character episode |
| Low-Poly Escalation | `looks/low-poly-escalation` | 3D low-poly world, huge HUD number climbing every beat | 3D "what if" reel |
| Clean Data | `looks/clean-data` | Inter on black or white, one accent, line graphs, 3D route maps, exploded views | Stat / map / teardown beat |
| Cinematic Captions | `looks/cinematic-captions` | Captions composited behind the subject, rail by default, embedded hero words at the peak | Captioned talking head |

## Layout

- `looks/<slug>/README.md`: the look in detail and how to make it.
- `looks/<slug>/look.json`: the tokens (type, colour roles, motion, captions, sound, pacing, bans, skin slots).
- `looks/<slug>/skin.example.json`: a neutral demo skin filling every slot.
- `looks/<slug>/references/`, `tools/`: optional recipes and brand-free scripts.
- `provenance/<slug>.md`: where each look came from and which skins exist. Not brand-free on purpose.
- `CONTRACT.md`: the rules every look folder follows.

## Check

```bash
python check_looks.py
```

Fails on a missing file, bad JSON, a skin missing a slot, or any client name, person, character or client-only font inside `looks/`.
