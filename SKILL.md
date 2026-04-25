---
name: anime-fanart-imagegen
description: Generate anime fan posters, scenes, and character art for existing anime or game characters with strong identity preservation. Use when the user wants Chinese-to-English prompt shaping, official-priority reference image gathering, character likeness locking, fixed output standards such as 2K or 4K, or fanart of a known character/IP that should stay recognizable without copying a reference composition.
---

# Anime Fanart Imagegen

Generate high-quality anime fanart for known characters while keeping the character recognizable.

Default to a two-stage workflow: build a reference pack, lock the character identity, then generate the final poster or scene. Use the built-in `image_gen` tool only for loose ideation. If the user cares about likeness, resolution, file format, or repeatable quality profiles, use the bundled `scripts/anime_fanart.py` workflow instead.

## Quick Start

1. Decide whether the request is about a known character/IP. If yes, use this skill.
2. Gather `3-5` reference images. Prefer user-provided images first. Otherwise search official sources with the workflow below.
3. Extract the character anchors: hairstyle, hair color, eye color, face vibe, canonical outfit silhouette, key color accents, and signature prop or accessory.
4. Produce three English prompt options by default:
   - poster key visual
   - narrative scene
   - character render
5. Run `lock` first to confirm the character reads correctly.
6. Only after the lock image passes, run `generate` or `run` for the final output.

Read `references/reference-sourcing.md` before you search. Read `references/prompt-recipes.md` before you draft prompts. Read `references/quality-standards.md` before choosing a resolution profile.

## Zero-Friction Default

If the user only gives a character name, do not ask for a full prompt up front. Use this default behavior:

- infer the series from official or high-confidence sources
- search for official-priority references
- default to the anime/game version that is easiest to verify
- build a character anchor list
- create a lock prompt first
- generate one `poster-2k` fan poster unless the user asked for a scene, square image, or 4K

Only ask a clarifying question if the character name is genuinely ambiguous across multiple works or versions.

Example user input:

```text
$anime-fanart-imagegen Anna Yanami
```

Default interpretation:

```text
Create a 2K anime fan poster for Anna Yanami from Too Many Losing Heroines!, using official-priority references, preserving recognizability, and avoiding copied reference composition.
```

## Decision Path

### Use the built-in `image_gen` tool when

- The user only wants quick ideation or rough variations.
- Exact resolution and output format do not matter yet.
- Character likeness is important but not strict enough to justify a lock pass.

### Use `scripts/anime_fanart.py` when

- The user says the character must look like the reference character.
- The user wants 2K, 4K, PNG, or a fixed deliverable size.
- The user wants a reproducible lock-first workflow.
- You have local reference images or official images downloaded into the workspace.

## Reference Workflow

### 1. Build a reference pack

Use `references/reference-sourcing.md`.

Default source priority:
- user-provided references
- official anime or game site
- publisher or distributor promo pages
- trusted character pages that embed official art or anime screenshots

Default exclusions:
- fanart sites
- booru sites
- Pinterest
- social media reposts
- aggregation pages with no clear official source

Save local references under a stable folder such as:

```text
refs/<character-slug>/
```

Try to cover these roles:
- `face`
- `full-body`
- `outfit-color`
- `prop-accessory`
- `anime-lighting` or `scene`

If the user supplied references, treat them as the top-priority definition of the character version. Use automatically found images only to fill missing information. Do not let supplemental images override the user-selected version.

### 2. Extract the anchors

Write down the minimum identity anchors before generating:
- character name
- series/franchise
- hairstyle and hair color
- eye color and eye shape
- face vibe and age impression
- canonical outfit silhouette
- dominant colors
- signature prop or accessory
- any non-negotiable notes from the user

If the user wants the person to look like the character but not copy the reference composition, explicitly separate:
- identity anchors to preserve
- composition and scene details that may change

### 3. Draft prompt options

Use English for the generation prompt even when the user speaks Chinese.

Default output is a three-option pack:
- poster
- scene
- render

Use the exact structure in `references/prompt-recipes.md`. Keep the character name and the extracted anchors in the prompt together. This gives you a fallback if the model under-recognizes the name.

### 4. Lock the character first

Run the lock pass before any final scene:

```powershell
python "$env:CODEX_HOME\\skills\\anime-fanart-imagegen\\scripts\\anime_fanart.py" lock `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --image "refs\\yanami-anna-anime\\01-face-icon.png" `
  --image "refs\\yanami-anna-anime\\02-fullbody-character.png" `
  --image "refs\\yanami-anna-anime\\03-love-visual.jpg" `
  --out "output\\yanami-lock.png"
```

Use the lock output as the first input for the final render. The lock pass should keep:
- face and hair identity
- canonical outfit silhouette
- signature colors
- signature accessories

The lock pass should not try to solve a busy scene.

### 5. Generate the final image

After the lock image passes:

```powershell
python "$env:CODEX_HOME\\skills\\anime-fanart-imagegen\\scripts\\anime_fanart.py" generate `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --image "output\\yanami-lock.png" `
  --image "refs\\yanami-anna-anime\\02-fullbody-character.png" `
  --prompt "Use case: poster-key-visual
Primary request: anime key visual of Anna Yanami standing on a rainy school rooftop at dusk
Style/medium: polished anime illustration matching the TV anime adaptation
Composition/framing: vertical poster composition, full body, cinematic camera
Lighting/mood: cool dusk light with reflected neon highlights
Constraints: preserve Anna Yanami's recognizable face, hairstyle, blue-themed canonical school-uniform silhouette, and playful-but-sly expression; original composition; no text; no watermark" `
  --profile poster-2k `
  --out "output\\yanami-poster.png"
```

If you want the lock and final generation in one command, use `run`.

## Likeness Rules

- Preserve identity anchors, not the exact reference composition.
- Default to the canonical outfit. Do not change outfits unless the user explicitly asks.
- Keep the lock image simple. Complexity belongs in the final scene.
- If the character starts drifting, go back to the lock image instead of rewriting the entire prompt.
- Change one thing at a time during retries.

Use `references/recovery.md` when:
- the face is off
- the outfit drifts
- the colors drift
- the scene becomes too busy
- the final image stops looking like the locked character

## Quality Rules

Read `references/quality-standards.md` before choosing a profile.

Defaults:
- `poster-2k`
- `scene-2k`
- `square-2k`

Only use 4K profiles when the user explicitly asks for them. Keep in mind that higher-than-`2560x1440` total pixel outputs are treated as experimental in current OpenAI docs.

Do not promise transparent backgrounds with `gpt-image-2`. This model currently does not support them.

## Validation

Use `references/qa-checklist.md` after each important output.

A lock image passes only if all of these are true:
- hairstyle and hair color are correct
- canonical outfit silhouette is correct
- dominant colors are correct
- no extra limbs, eyes, or fingers
- the character still reads as the intended person at a glance

If the lock image fails, do not move on to the final poster or scene.

## Script Surface

The bundled script supports these subcommands:
- `lock`
- `generate`
- `run`

Use `--dry-run` first when you want to inspect the payload without making an API call.

The script writes a JSON sidecar next to each output image with:
- model snapshot
- profile
- size
- quality
- output format
- prompt
- source image list
- timestamp

## Reference Map

- `references/reference-sourcing.md`: where and how to find official-priority references
- `references/prompt-recipes.md`: English prompt templates for poster, scene, and render outputs
- `references/quality-standards.md`: profile names, sizes, and guardrails
- `references/recovery.md`: what to change when identity or quality drifts
- `references/qa-checklist.md`: acceptance checks before final delivery
- `scripts/anime_fanart.py`: `gpt-image-2` lock and generation workflow
