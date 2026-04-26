---
name: anime-fanart-imagegen
description: Generate anime fan posters, scenes, stylized illustrations, and character renders for existing anime, game, visual-novel, or adjacent Japanese-style IP characters with strong identity preservation. Use when the user has only a rough idea in Chinese, cannot write a strong prompt, wants the agent to infer likely directions, gather official-priority references, lock character likeness, expand fuzzy intent into image-2-ready English prompts, explore style options without identity drift, or deliver repeatable 2K or 4K outputs for a known character/IP without copying a reference composition.
---

# Anime Fanart Imagegen

Generate high-quality anime fanart for known characters while keeping the character recognizable.

Treat this skill as a prompt-and-direction engine, not only a rendering engine. The user should only need to provide taste signals; the agent converts them into structured decisions, a modular Chinese prompt spec, and a final English `gpt-image-2` prompt.

## Read First

Load references only when needed:

- `references/frictionless-ux.md`: vague requests, character-name-only starts, intent router, low-question intake
- `references/discovery-loop.md`: multi-turn exploration, "再探索", option mixing, current-branch exploration
- `references/prompt-modules.md`: final modular prompt spec, single-module edits, module-level exploration, more-dimensions exploration
- `references/style-matrix.md`: style axes, user-language translation, safe style combinations
- `references/reference-sourcing.md`: official-priority reference sourcing
- `references/prompt-recipes.md`: English prompt templates
- `references/quality-standards.md`: output profiles and resolution guardrails
- `references/recovery.md`: identity, outfit, color, scene, and style drift fixes
- `references/qa-checklist.md`: acceptance checks before final delivery

## Core UX Contract

- Accept rough Chinese or English input as valid.
- Do not ask the user to write a complete prompt.
- Infer missing prompt slots when the intent is clear.
- Ask at most one clarifying question unless identity or deliverable selection is blocked.
- Show concrete choices instead of broad open-ended questions.
- Keep identity anchors fixed while exploring style, mood, crop, and scene.
- Generate only after the user asks to generate, selects a ready direction, or explicitly delegates the decision.
- After multi-turn exploration, finalize as modules first, then compile the English prompt.

## First-Turn Routing

If the user only gives a character name or says something like "我要生成 X 图片", do not generate immediately.

First show a compact guide:

1. interpreted character and source
2. inferred identity anchors
3. intent router
4. recommended path
5. optional quick tweak chips
6. ready English prompt for the recommendation
7. one-line next action

Default intent router:

```text
A. 成品图
B. 壁纸或封面
C. 头像或肖像
D. 探索氛围
E. 最大化角色相似度
F. 改变风格
G. 我来决定
```

The user may reply with one option, multiple options, or a natural-language reaction.

Examples:

- `D`
- `DF`
- `A+C`
- `B 但更像 F`
- `生成`
- `再探索`

Interpret the first selected option as the base when the user mixes options, unless they say otherwise.

## Discovery Loop

Use `references/discovery-loop.md` when the user is unsure, asks for more options, says "再探索", combines choices, or reacts with "不够泛化", "继续探索", "不是这个", or "还有吗".

Do not reset the conversation. Maintain a lightweight preference state:

- `known`: character, source, identity anchors, hard constraints
- `liked`: moods, scene families, crops, styles, references
- `disliked`: directions to avoid
- `open`: unresolved choices
- `next_probe`: smallest useful next comparison

Exploration rules:

- In early exploration, avoid locking exact picture content too soon.
- Explore abstract taste first: purpose, emotion, distance, crop, style strength, story energy.
- After the user chooses an abstract direction, then offer picture-content candidates.
- If the user says "再探索", stay at the current decision level and show different alternatives.
- If the user chooses an option during active exploration, treat it as a locked preference and continue inside that branch.
- Stop exploration only when the user says "可以了", "就这个", "生成", "use this", or equivalent approval.
- Always mention that mixing is allowed, such as `A+C` or `A 但更像 C`.

Every discovery response should keep visible exits:

```text
下一步: 回 A-F，可混合如"A+C"，也可以说"再探索"、"返回"、"可以了"或"生成"。
```

## Modular Prompt Spec

Use `references/prompt-modules.md` when the user says "可以了", asks to generate after exploration, asks to revise only part of a prompt, asks to explore a specific module, or asks the agent to decide unresolved modules.

For Chinese users, output two layers:

1. `提示词模块`: editable Chinese module list with stable module IDs
2. `英文生成提示词`: final English `image-2` prompt assembled from those modules

Required modules:

```text
M1 身份锚点
M2 原作基线
M3 用途目标
M4 改编边界
M5 情绪方向
M6 角色状态
M7 画面内容
M8 构图画幅
M9 光线色彩
M10 风格质感
M11 正向约束
M12 避免项
```

After showing modules, always tell the user they can:

- generate
- edit one module
- explore one module
- explore more dimensions
- go back

If the user asks for module-level exploration, keep all other modules fixed and offer alternatives only inside that module.

If the user asks the agent to decide unresolved modules, or after the user picks a module option, immediately integrate the decision into the full module list and regenerate the compiled English prompt. Do not return only a partial module update.

## Reference Workflow

Build a reference pack before strict likeness work.

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

Save local references under a stable folder:

```text
refs/<character-slug>/
```

Try to cover:

- face
- full-body
- outfit color
- prop or accessory
- source visual baseline
- scene or lighting sample

If the user supplied references, treat them as the top-priority definition of the character version.

## Identity Anchors

Write down the minimum identity anchors before generating:

- character name
- series or franchise
- source visual baseline
- hairstyle and hair color
- eye color and eye shape
- face vibe and age impression
- canonical outfit silhouette
- dominant colors
- signature prop or accessory
- non-negotiable notes from the user

Separate what must stay recognizable from what may change.

## Prompt Drafting

Use English for the generation prompt, even when the user speaks Chinese.

Default prompt spread:

- faithful baseline
- scene-first variation
- stylized variation that preserves anchors

Keep these fixed unless the user asks otherwise:

- character identity anchors
- canonical outfit silhouette
- canonical color hierarchy
- source visual baseline

Vary only `1-2` axes at a time:

- visual baseline
- stylization delta
- scene archetype
- framing
- finish
- lighting

For vague input, upgrade weak wording into concrete visual decisions:

- mood word -> lighting and palette
- taste word -> finish and staging
- intended use -> crop and profile
- "official art" -> baseline plus poster archetype
- "premium" -> cleaner staging, lower prop count, controlled lighting
- "more emotional" -> expression, pose, light, and symbolic environment

## Generation Decision

Use the built-in `image_gen` tool when:

- the user only wants quick ideation
- exact resolution and file output do not matter
- likeness matters but does not require a lock pass

Use `scripts/anime_fanart.py` when:

- the character must look like the reference character
- the user wants 2K, 4K, PNG, or a fixed profile
- the workflow needs repeatable lock-first generation
- local reference images are available

If the script workflow is selected but the local environment cannot call the API,
for example because `OPENAI_API_KEY` is missing, do not fall back to direct
`image_gen`. Stop after `--dry-run`, report the blocker, and keep the prepared
prompt, references, and payload ready for the user.

## Script Workflow

Lock first:

```powershell
python scripts\anime_fanart.py lock `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --image "refs\yanami-anna-anime\01-face-icon.png" `
  --image "refs\yanami-anna-anime\02-fullbody-character.png" `
  --out "output\yanami-lock.png"
```

Generate after the lock passes:

```powershell
python scripts\anime_fanart.py generate `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --lock-image "output\yanami-lock.png" `
  --image "refs\yanami-anna-anime\02-fullbody-character.png" `
  --profile poster-2k `
  --prompt "<compiled English image-2 prompt>" `
  --out "output\yanami-poster.png"
```

Use `--dry-run` first when inspecting payloads without calling the API.

## Quality Rules

Defaults:

- `poster-2k`: vertical hero art
- `scene-2k`: horizontal scene composition
- `square-2k`: square crop
- `banner-2k`: panoramic cover art

Only use 4K profiles when the user explicitly asks for them.

Do not promise transparent backgrounds with `gpt-image-2`.

A lock image passes only if:

- hairstyle and hair color are correct
- canonical outfit silhouette is correct
- dominant colors are correct
- no extra limbs, eyes, or fingers
- the character reads correctly at a glance

If the lock image fails, fix the lock. Do not move on to the final poster or scene.

## Recovery Rules

Use `references/recovery.md` when:

- face is off
- outfit drifts
- colors drift
- scene becomes too busy
- final image stops looking like the locked character
- variants look technically polished but too similar
- stylization gets stronger and recognizability collapses

Change one thing at a time during retries.
