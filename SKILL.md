---
name: anime-fanart-imagegen
description: Generate anime fan posters, scenes, stylized illustrations, and character renders for existing anime, game, visual-novel, or adjacent Japanese-style IP characters with strong identity preservation. Use when the user has only a rough idea in Chinese, cannot write a strong prompt, wants the agent to infer likely directions, gather official-priority references, lock character likeness, expand fuzzy intent into image-2-ready English prompts, explore style options without identity drift, or deliver repeatable 2K or 4K outputs for a known character/IP without copying a reference composition.
---

# Anime Fanart Imagegen

Generate high-quality anime fanart for known characters while keeping the character recognizable.

Default to a two-stage workflow: build a reference pack, lock the character identity, then generate the final poster or scene. Use the built-in `image_gen` tool only for loose ideation. If the user cares about likeness, resolution, file format, or repeatable quality profiles, use the bundled `scripts/anime_fanart.py` workflow instead.

Optimize for a low-friction user experience. Assume many users know the character and the vibe they want, but do not know how to convert that into a complete prompt. Do that conversion for them. For vague first-turn requests, guide before rendering with an intent router first, then expose creative controls only if the user wants to steer. Do not bounce the work back by asking for a fully written prompt, a full shot list, or a long style questionnaire unless there is a real ambiguity that blocks identity or deliverable selection.

## Quick Start

1. Decide whether the request is about a known character/IP. If yes, use this skill.
2. Gather `3-5` reference images. Prefer user-provided images first. Otherwise search official sources with the workflow below.
3. Extract the character anchors: hairstyle, hair color, eye color, face vibe, canonical outfit silhouette, key color accents, signature prop or accessory, and the canonical visual baseline from the reference pack.
4. Produce three English prompt options by default with controlled spread:
   - faithful key visual
   - scene-driven variation
   - stylized reinterpretation that still preserves the character anchors
5. Run `lock` first to confirm the character reads correctly.
6. Only after the lock image passes, run `generate` or `run` for the final output.

Read `references/reference-sourcing.md` before you search. Read `references/prompt-recipes.md` before you draft prompts. Read `references/quality-standards.md` before choosing a resolution profile.
Read `references/style-matrix.md` before prompt drafting when the user wants richer styles, the current prompts feel repetitive, or you need to vary look without losing recognizability.
Read `references/frictionless-ux.md` before deciding how to handle vague, incomplete, or "you decide" input.
Read `references/discovery-loop.md` when the user is still unsure after the first guide, asks for more options, reacts with "not quite", or needs help discovering what they want through multiple turns.
Read `references/prompt-modules.md` before finalizing a prompt after multi-turn exploration, or whenever the user may want to change only part of the result later.

## UX Contract

Treat this skill as a prompt-and-direction engine, not just a rendering engine.

- accept rough Chinese requests as valid input
- reconstruct the missing prompt structure yourself
- present concrete visual directions instead of asking broad open-ended questions
- keep the question budget at `0-1` by default
- for vague first-turn requests such as "I want to make an image of X", route by user intent first and wait for the user's choice unless they explicitly asked to generate immediately
- when the user remains unsure, switch from menu selection to a discovery loop: branch, compare, capture preference, narrow, then prompt
- if the user says "you decide", "freestyle it", or "I can't describe it clearly", choose a strong safe default and move forward
- convert vague adjectives into explicit visual decisions before calling `image-2`
- after multi-turn exploration, finalize as a modular prompt spec first, then compile it into the English prompt

The user should feel that they only need to provide taste signals, not production-ready prompt language.

## Zero-Friction Default

If the user only gives a character name, do not ask for a full prompt up front. Use this default behavior:

- infer the series from official or high-confidence sources
- search for official-priority references
- default to the anime/game version that is easiest to verify
- build a character anchor list
- infer the canonical visual baseline from the strongest references instead of forcing a TV-anime look
- create a lock prompt first
- generate one `poster-2k` fan poster unless the user asked for a scene, square image, or 4K
- if the user asks for "more styles", "different vibes", or "give me several style options", produce `3-5` style directions first and only then choose one to render

If the user gives an incomplete request instead of only a character name, keep the same spirit:

- rough vibe only, such as "make it more romantic" or "make it feel more premium" -> map that language to baseline, archetype, finish, and lighting
- rough scene only, such as "put her on a rooftop at night in the rain" -> keep the canonical identity anchors and build the rest of the prompt
- rough prompt draft -> preserve the user's main intent, but rewrite it into the structured English prompt format
- user-provided images without clear words -> infer the version, baseline, and strongest recurring anchors from the images first
- "help me decide" or "you decide" -> produce a recommended default plus `2-4` nearby alternatives instead of asking them to define the whole look

If a user is vague, default to showing options, not asking a long questionnaire.

Only ask a clarifying question if the character name is genuinely ambiguous across multiple works or versions.

## Guided-First Start

Use this when the user starts with a broad request like "I want to make an image of Violet", "try this skill", "help me make a picture", or "I do not know what prompt to write".

Do not generate immediately in this situation. First produce a one-screen guide:

1. interpreted character and source
2. inferred identity anchors
3. an intent router with broad user goals, such as "make a finished image", "make a wallpaper", "explore vibe", "maximize likeness", "change style", or "surprise me"
4. one recommended path based on the character
5. optional micro-chips for mood, crop, and style strength
6. a ready English prompt for the recommended path
7. simple next actions, such as "reply A/B/C/D/E/F", "say generate", or "add one mood word"

Keep the guide compact. The user should be able to choose by replying with one intent letter, one mood phrase, or "generate".

Skip this guided-first start only when the user explicitly says to render now, provides a complete prompt, selects a previous direction, or asks for a batch of generated images.

## Discovery Loop

Use `references/discovery-loop.md` after the first guide if the user says anything like:

- "still not sure"
- "more options"
- "not this"
- "I like part of A and part of C"
- "make it closer"
- "make it more surprising"
- "show me different directions"

Do not reset the conversation. Maintain a lightweight preference state:

- `known`: character, source, identity anchors, hard constraints
- `liked`: words, scenes, moods, crops, or references the user responded to positively
- `disliked`: directions to avoid
- `open`: unresolved choices
- `next_probe`: the smallest useful comparison to ask or offer next

Iterate in this order:

1. preserve known identity anchors
2. branch into semantically different abstract probes
3. let the user react in natural language
4. translate the reaction into updated preference state
5. only then offer concrete picture-content candidates
6. narrow to one candidate prompt
7. generate only after the user selects, approves, or asks you to choose

The goal is not to expose all controls. The goal is to help the user discover taste through comparison.

Always keep a visible exit in discovery responses:

- `generate`: use the current prompt
- `explore more`: stay at the current level and show different alternatives
- `back`: return one level up

If the user says "再探索", treat it as `explore more`.

When the user is actively exploring, do not stop exploration after they choose an option. Treat the choice as a newly locked preference and continue exploring inside that branch. Stop only when the user clearly says "可以了", "就这个", "生成", "use this", or equivalent approval.

Always mention that option mixing is allowed during exploration, such as "A+C" or "A 但更像 C". Interpret the first option as the base and borrow one clear trait from the second unless the user says otherwise.

## Modular Prompt Spec

Use `references/prompt-modules.md` when the user says "可以了", asks to generate after exploration, or wants to revise only part of a prompt.

Output two layers:

1. `提示词模块`: editable Chinese module list with stable module IDs when the user speaks Chinese
2. `英文生成提示词`: the final English `image-2` prompt assembled from those modules

Keep modules independent enough that the user can say things like:

- "change only lighting"
- "keep AU, change emotion"
- "keep everything, make it closer to canon"
- "change picture content, keep color and mood"
- "只改 M9 光线色彩"
- "换 M7 画面内容"
- "M4 更接近原作"
- "再探索 M9"
- "只在 M7 里继续探索"

Do not rewrite the whole direction when a module-level edit is enough.

If the user requests module-level exploration, keep all other modules fixed and offer alternatives only inside that module.

After showing a modular prompt spec, always include a short next-step prompt that explicitly tells the user they can generate, edit one module, explore one module, explore more dimensions, or go back.

When the user asks the agent to decide unresolved modules, or after the user picks a module option, immediately integrate the decision into the full module list and regenerate the compiled English prompt. Do not return only a partial module update.

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

## Intent Reconstruction

When the user cannot describe the final image well, infer the hidden slots instead of asking them to fill every slot manually.

Reconstruct these fields silently unless one of them is truly ambiguous:

- subject identity
- series or version
- deliverable type: poster, scene, render, banner
- crop and size profile
- scene density
- lighting
- finish
- stylization delta
- non-negotiable constraints

Use these defaults when the user does not care:

- deliverable: `poster-2k` for hero art, `scene-2k` for wallpaper-like scenes, `square-2k` for avatar-ish or social crops, `banner-2k` for headers and panoramic hero art
- scene density: simple-to-medium before busy
- lighting: `neutral-daylight` for likeness checks, then `golden-hour`, `spring-haze`, or `rainy-neon` depending on the user's mood words
- stylization delta: `faithful` first, `lightly-stylized` only after the canonical baseline is explicit
- outfit: canonical outfit unless the user asked for a redesign

If the user input is vague, respond with a compact interpretation pack:

1. one-line interpreted brief in Chinese
2. intent router across broad user goals
3. one recommended path
4. optional micro-chips for quick steering
5. one English prompt for the recommended path
6. short next actions the user can answer with one intent letter, one mood word, or "generate"

Do not make the user reverse-engineer prompt craft vocabulary. Translate their taste signals into production language yourself.

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
- `style-baseline`
- `anime-lighting`, `game-lighting`, or `scene`

If the user supplied references, treat them as the top-priority definition of the character version. Use automatically found images only to fill missing information. Do not let supplemental images override the user-selected version.

### 2. Extract the anchors

Write down the minimum identity anchors before generating:
- character name
- series/franchise
- source visual baseline, such as TV anime, game render, or official illustration
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

Default output is a three-option pack with intentional spread:
- faithful baseline: safest recognizable option that stays closest to the reference pack
- scene-first variation: same character anchors, different composition and environment emphasis
- stylized variation: same character anchors, wider shift in finish, lighting, or mood

### Style Decision Framework

When prompts start sounding interchangeable, vary them across explicit axes instead of rewriting everything from scratch.

Keep these fixed unless the user asked otherwise:
- character identity anchors
- canonical outfit silhouette
- canonical color hierarchy
- core source visual baseline

Vary these axes deliberately:
- visual baseline: TV anime, game render, official illustration, manga-colorized look, or mixed-media promo art
- stylization delta: faithful, lightly stylized, or bold reinterpretation
- scene archetype: poster, slice-of-life, action set piece, dreamlike mood piece, fashion editorial, seasonal illustration, festival scene, stage performance
- framing: close portrait, half-body, full-body, wide scene, banner-like panoramic crop
- finish: cel-shaded, polished illustration, glossy key visual, painterly anime poster, soft filmic grading
- lighting: neutral daylight, warm sunset, rainy neon, winter blue hour, spring haze, stage spotlight, moonlit glow

Change `1-2` axes at a time during retries. If you change baseline, finish, lighting, and composition all at once, identity drift becomes much harder to diagnose.

Use `references/style-matrix.md` to map user language such as:
- "premium" or "editorial" -> fashion editorial + clean controlled lighting
- "more cinematic" or "more atmospheric" -> narrative scene + cinematic framing + directional light
- "dreamier" or "ethereal" -> dreamlike mood piece + soft haze + restrained prop count
- "more like official game promo art" -> game-faithful render + hard-surface clarity + official UI-free promo look

When the user says "I don't know what style I want" or gives only mood language, do not stop at adjectives. Convert them into explicit choices:

- mood word -> lighting pack
- taste word -> finish
- intended use, such as wallpaper/avatar/poster -> crop and profile
- "make it feel like official art" or "like a promo poster" -> baseline + archetype
- "make it more premium" or "more refined" -> cleaner staging, lower prop count, premium finish, more controlled light
- "make it moodier" -> environment and lighting change first, not identity change

Prefer three distinct directions over seven weakly separated synonyms.

Use the exact structure in `references/prompt-recipes.md`. Keep the character name and the extracted anchors in the prompt together. This gives you a fallback if the model under-recognizes the name.

Default this skill to single-character identity locking. For multi-character scenes, lock the hero character first and treat the other character(s) as best-effort unless the user explicitly wants a per-character lock workflow.

If the user request is under-specified, do not invent a random style. Start from the canonical baseline, then expand outward in this order:
1. faithful baseline
2. composition change
3. lighting or mood change
4. finish change
5. baseline reinterpretation

Only use step 5 when the user explicitly asked for stronger stylization or reinterpretation.

### 4. Lock the character first

Run the lock pass before any final scene.

If you are already inside the skill directory, prefer the repo-local command form below. If you are invoking the script from another working directory, resolve the installed skill directory first and then call the same script.

```powershell
python scripts\\anime_fanart.py lock `
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
python scripts\\anime_fanart.py generate `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --lock-image "output\\yanami-lock.png" `
  --image "refs\\yanami-anna-anime\\02-fullbody-character.png" `
  --prompt "Use case: poster-key-visual
Primary request: anime key visual of Anna Yanami standing on a rainy school rooftop at dusk
Style/medium: polished character illustration matching the canonical source visuals in the reference pack
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
- Match the reference pack's canonical source visuals. Do not force a game character into a TV-anime baseline unless the user explicitly asks for that reinterpretation.
- If the user wants a different style, preserve identity first and move style second. Describe the stylization as a delta from the canonical baseline rather than replacing the baseline entirely.
- Keep the lock image simple. Complexity belongs in the final scene.
- If the character starts drifting, go back to the lock image instead of rewriting the entire prompt.
- Change one thing at a time during retries.

## Style Expansion Rules

- Use strong style language only after the identity anchors are explicit.
- Prefer composable style phrases over vague adjectives. "rainy neon city dusk with glossy anime key visual finish" is better than "very cool cinematic style".
- Keep the prompt internally consistent. Do not mix "TV-anime cel shading", "photoreal film still", and "oil painting" unless the user explicitly wants a hybrid experiment.
- For faithful outputs, let the reference pack define the finish.
- For bolder outputs, keep one anchor in each bucket:
  - face or expression anchor
  - outfit/color anchor
  - source-baseline anchor
- If the user asks for many variants, make them meaningfully different by changing archetype, lighting, or finish, not by swapping synonyms.

When the user's raw wording is weak, do not mirror weak wording into the final prompt. Upgrade it. Replace vague wording with:

- clear subject action or pose
- concrete framing
- one finish phrase
- one lighting phrase
- one scene description with restrained prop count
- concise avoid terms for the actual likely failure modes

## Multi-Character Scope

- This skill is optimized for one locked character at a time.
- For two-character or group scenes, lock the primary character first and treat additional characters as lower-confidence unless you build separate lock images for each one.
- If both characters must read precisely, prefer separate lock passes and then compose the final scene.

Use `references/recovery.md` when:
- the face is off
- the outfit drifts
- the colors drift
- the scene becomes too busy
- the final image stops looking like the locked character
- the result is technically polished but all variants look the same
- the stylization got stronger and recognizability collapsed

## Quality Rules

Read `references/quality-standards.md` before choosing a profile.

Defaults:
- `poster-2k`
- `scene-2k`
- `square-2k`
- `banner-2k` for extra-wide hero art, headers, or panoramic key visuals

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
- `references/frictionless-ux.md`: how to handle vague requests, low-question intake, and prompt reconstruction
- `references/discovery-loop.md`: iterative branching and narrowing when the user does not know what they want yet
- `references/prompt-modules.md`: modular prompt spec format for changing small parts after exploration
- `references/style-matrix.md`: style axes, safe combinations, and user-language translation for varied looks
- `references/quality-standards.md`: profile names, sizes, and guardrails
- `references/recovery.md`: what to change when identity or quality drifts
- `references/qa-checklist.md`: acceptance checks before final delivery
- `scripts/anime_fanart.py`: `gpt-image-2` lock and generation workflow
