# Anime Fanart Imagegen

Portable Codex skill for generating anime fan posters, scenes, and character renders for known anime, game, and visual-novel characters while preserving recognizable identity.

This repo is designed to be copied into other repositories or installed directly as a Codex skill. The workflow is optimized for the common case where the user knows the character and the vibe, but cannot write a strong `image-2` prompt on their own.

## What It Does

- turns rough Chinese or English requests into structured English prompts for `gpt-image-2`
- gathers official-priority reference images
- extracts identity anchors such as hair, eyes, outfit silhouette, and signature accessories
- runs a lock-first workflow before final scene generation
- supports fixed output profiles such as `poster-2k`, `scene-2k`, `square-2k`, and optional 4K variants
- produces several concrete style directions when the user is vague instead of asking a long questionnaire

## Install

### Option 1: install as a Codex skill

Windows PowerShell:

```powershell
git clone <your-repo-url> "$env:USERPROFILE\.codex\skills\anime-fanart-imagegen"
```

macOS or Linux:

```bash
git clone <your-repo-url> ~/.codex/skills/anime-fanart-imagegen
```

Restart Codex after installation.

### Option 2: vendor into another repo

Copy this folder into any repository and keep the structure intact:

```text
anime-fanart-imagegen/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

If you vendor it under a different parent directory, keep the folder name `anime-fanart-imagegen` so trigger references stay predictable.

## Typical Use

### Name only

```text
$anime-fanart-imagegen Anna Yanami
```

Default behavior:

1. infer the series if needed
2. gather official-priority references
3. extract identity anchors
4. create a lock prompt
5. generate a recommended `poster-2k` output

### Rough idea in natural language

```text
Use $anime-fanart-imagegen for Anna Yanami. Put her on a rainy rooftop at dusk and make it feel like an official poster.
```

### User cannot describe the image well

```text
Use $anime-fanart-imagegen for Anna Yanami. I only want it to feel softer and more premium. You decide the rest.
```

Default behavior:

1. infer the missing slots
2. propose `3` concrete directions
3. recommend one default
4. generate or prepare the final prompt

## Local Script Workflow

Use the Python CLI when you need reproducible `gpt-image-2` outputs, named profiles, metadata sidecars, or a lock-first API workflow.

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your API key:

```bash
export OPENAI_API_KEY="..."
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "..."
```

### Lock pass

```bash
python scripts/anime_fanart.py lock \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --image refs/yanami/01-face.png \
  --image refs/yanami/02-fullbody.png \
  --out output/yanami-lock.png
```

### Final generation

```bash
python scripts/anime_fanart.py generate \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --lock-image output/yanami-lock.png \
  --image refs/yanami/02-fullbody.png \
  --profile poster-2k \
  --prompt "Use case: poster-key-visual
Primary request: Anna Yanami sitting on an old school staircase during lunch, eating bento with a playful smile
Style/medium: polished character illustration matching the canonical source visuals in the reference pack
Composition/framing: vertical poster composition
Constraints: preserve recognizability, canonical school uniform, no text, no watermark" \
  --out output/yanami-poster.png
```

Use `--dry-run` first when you want to inspect the request payload without calling the API.

## Distribution Notes

- `SKILL.md` is the authoritative behavior contract for Codex.
- `agents/openai.yaml` controls how the skill appears in the UI.
- `references/` contains the reusable prompt, QA, quality, and UX guidance.
- `scripts/anime_fanart.py` is repo-local and does not depend on this repository living at a fixed absolute path.

## Defaults

- `poster-2k`: vertical hero art
- `scene-2k`: horizontal scene composition
- `square-2k`: square crop
- `banner-2k`: panoramic cover art

4K profiles are available, but should be treated as opt-in final-delivery profiles.

## Notes

- Do not promise exact reproduction of a copyrighted frame or composition.
- Do not expose `OPENAI_API_KEY` in commits, issues, screenshots, or generated metadata.
- This skill is tuned for identity preservation first and stylization second.
