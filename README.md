# Anime Fanart Imagegen

Codex skill for generating anime fan posters, scenes, and character art for existing anime or game characters with stronger identity preservation.

The skill is designed for workflows where the character should stay recognizable without copying a reference image composition. It supports Chinese-to-English prompt shaping, official-priority reference sourcing, character lock passes, and fixed output profiles such as 2K and optional 4K.

## What It Does

- Builds a small reference pack from user-provided or official-priority images.
- Extracts character identity anchors such as hair, eyes, outfit silhouette, palette, and props.
- Produces English prompts for poster, narrative scene, and character render variants.
- Uses a lock-first workflow before final poster or scene generation.
- Provides a `gpt-image-2` CLI workflow with named quality profiles.

## Install

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/anime-fanart-imagegen
```

Then invoke it in Codex with:

```text
Use $anime-fanart-imagegen to generate a 2K anime fan poster for <character> from <series>.
```

## API Mode

The bundled script requires the OpenAI Python SDK and `OPENAI_API_KEY`:

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="..."
```

Example dry run:

```bash
python scripts/anime_fanart.py lock \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --image refs/yanami/01-face.png \
  --image refs/yanami/02-fullbody.png \
  --out output/yanami-lock.png \
  --dry-run
```

## Important Notes

Do not publish copyrighted reference images, screenshots, generated images, or private API keys in this repository. Keep local reference packs under `refs/` and generated outputs under `output/`; both are ignored by `.gitignore`.

This skill helps preserve likeness through references and prompt structure, but it cannot guarantee perfect reproduction of a copyrighted character or a specific frame.
