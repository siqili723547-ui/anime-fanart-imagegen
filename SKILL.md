---
name: anime-fanart-imagegen
description: Generate anime fan posters, scenes, stylized illustrations, and character renders for existing anime, game, visual-novel, or adjacent Japanese-style IP characters with strong identity preservation. Use when the user has only a rough idea in Chinese, cannot write a strong prompt, wants the agent to infer likely directions, gather official-priority references, lock character likeness, expand fuzzy intent into image-2-ready English prompts, explore style options without identity drift, or deliver repeatable 2K, 4K, or fixed-profile outputs for a known character/IP without copying a reference composition.
---

# Anime Fanart Imagegen

Generate high-quality anime fanart for known characters while keeping the character recognizable.

Treat this skill as a prompt-and-direction engine, not only a rendering engine. The user should only need to provide taste signals; the agent converts them into structured decisions, a modular Chinese prompt spec, and a final English `gpt-image-2` prompt.

Primary UX promise: make exploration the default. A user who cannot describe the
image should be able to pick from concrete direction cards instead of writing a
prompt. Put exploration first in first-turn choices, keep the default path in
exploration for at least `10` rounds before proactively offering generation, then
compile the prompt only after the user chooses, mixes, or delegates a direction.

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
- Label visible choices with letters (`A`, `B`, `C`) and accept numeric aliases
  (`1`, `2`, `3`) silently. Do not use numbers as the primary labels because
  they conflict with `已探索: N/10`, `L2/L3` layers, and `M1`-`M12` modules.
- Every exploration choice block should end with three short guidance lines:
  `怎么选`, `接下来`, and `已探索`. `怎么选` explains the valid replies; `接下来`
  says what the next round will refine; `已探索` shows progress. Avoid vague
  "what do you want" prompts.
- Every exploration choice block should mark exactly one option as `推荐` and
  explain why in one short sentence. The recommendation is a visible default, not
  a hidden decision; the user can still pick, mix, or ask for more options.
- Add a short `风险` or `影响` label to each option. For image directions, risk
  means likely identity drift, scene complexity, or prompt ambiguity; use
  `低/中/高` in plain Chinese.
- Do not make default exploration a repeated three-choice funnel. Normal
  exploration layers should offer `4-5` real creative options; use `5-6` when
  the user says "再给几个", "换一组", or "都不满意". Reserve `3` options for quick
  mode or narrow module edits.
- Keep identity anchors fixed while exploring style, mood, crop, and scene.
- Exploration must feel progressive, not scattered. Use a fixed ladder: identity
  baseline -> broad direction -> picture content -> crop/composition ->
  lighting/color -> style/finish -> final modules. Each exploration reply should
  show the current layer, what is already locked, and the next small choice.
- Every major prompt module `M1`-`M12` may expose small modules. First let the
  user choose which small modules to explore, then expand the selected small
  modules one by one. Do not jump straight from a big module like "光影" into
  fixed final lighting presets. Example: under `M9 光线色彩`, first offer
  submodules such as `人物打光`, `背景光`, `环境光`, `光线颜色`, and `阴影质感`;
  after the user selects one or more, offer rich creative options only for the
  first selected submodule and keep the rest queued. Use
  `references/prompt-modules.md` for the full `M1`-`M12` small-module map.
- In the default discovery path, `L3 画面内容`, `L4 构图距离`, `L5 光色氛围`,
  and `L6 风格质感` should all start with small-module pickers unless the user
  already selected a specific submodule. Do not reserve small-module selection
  only for lighting.
- Small-module selection is a control surface, not the final prompt itself.
  Show plain Chinese submodule names and what they affect; avoid forcing every
  submodule into the final prompt unless the user selects it or delegates with
  "你选".
- Default exploration depth: track `exploration_rounds` for the current task.
  Count a round whenever the user picks an option, mixes options, says "再探索",
  delegates with "你选", gives a taste reaction that changes the branch, or
  chooses a module/dimension probe. Before `exploration_rounds >= 10`, do not
  proactively offer the copyable `开始生成图片` CTA; keep the final next-action line
  focused on the next exploration step and show progress as `已探索: N/10`.
- For existing-character dogfood tests and final outputs where recognizability
  matters, the complete flow must include an identity lock pass before the final
  poster/scene pass. If no accepted lock or baseline image exists, do not present
  a final poster as a complete test result; first prepare the lock prompt and,
  after the user permits generation with `开始生成图片`, generate a neutral
  identity-lock image for approval.
- If the main ladder reaches style/finish before round 10, continue with
  high-value refinement rounds instead of pushing generation: likeness safety,
  composition readability, scene density, light/color tuning, finish strength,
  or avoid terms.
- If the user explicitly asks to skip exploration (`B`, "不要探索", "直接给提示词")
  or already says the exact phrase `开始生成图片`, respect that explicit exit. The
  `10`-round rule controls proactive prompting on the default path; it must not
  block a clear user override.
- Hard generation gate: never call any image-generation tool unless the user message contains the exact phrase `开始生成图片`.
- Treat option letters, "生成", "出图", "直接生成", "按这个生成", "可以了", "就这个", "you decide", and selected ready directions as guidance or prompt-finalization only, not permission to generate images.
- Until the user says `开始生成图片`, keep guiding exploration of more dimensions. Use a lightweight exploration state for "再探索", "再给几个", "换一组", "都不满意", option mixing, module probes, and direction cards: show the current branch, the changed module or dimension, `4-6` concrete choices, and the next action only.
- Use the full finalization state only when the user says "可以了", "就这个", "生成", `开始生成图片`, asks for the full prompt, or reaches generation preflight. In finalization state, show the full current `提示词模块` list (`M1`-`M12`) and the full compiled English prompt before the next-action line.
- Before every image-generation tool call, tell the user that if the image is unsatisfying they can name the part to change, and that feedback will continue through the matching prompt module instead of restarting.
- When the user gives post-image feedback such as "人物不像", "脸不像", "不够像", "更像原作", "光影不满意", "背景太乱", or "风格太 AI", map it to the relevant module(s), revise the full prompt state, show full modules and the full compiled English prompt, then ask whether they want more changes or `开始生成图片`.
- After multi-turn exploration, finalize as modules first, then compile the English prompt.

## First-Turn Routing

If the first turn or a new task explicitly asks to generate a poster, cover,
wallpaper, or key visual, but does not choose a workflow, do not render yet.
Ask one confirmation question before preparing the prompt:

```text
我理解你要做 <character/source + requested poster direction>。
你想 A. 先给我 4 个方向让我选（推荐），还是 B. 直接给我一版可生成提示词？
```

If the user chooses `A`, says "引导", "给我几个方向", "先看看方向",
"完善提示词", "不知道怎么写 prompt", or equivalent, show four user-facing
direction cards before finalizing modules and prompt. If the user chooses `B`,
says "直接给提示词", "不要探索", "无需引导", "直接生成", or equivalent,
infer missing slots conservatively and prepare the final modules and English
prompt, but do not generate. Use this fixed shape for the exploration path:

```text
当前层级: L2 方向感 / 已锁定: <character/source + identity baseline>.

A. 保守原作向
画面感: <一句用户能立刻想象的画面>.
差异点: <3-5 个用户能看懂的差异，例如用途 / 情绪 / 构图 / 风格强度 / 角色距离>.
角色钩子: <与角色或作品强相关的视觉母题>.
适合: <用白话说明适合什么结果>.
风险: <低/中/高 + 一句原因>.

B. 情绪电影向
画面感: <一句用户能立刻想象的画面>.
差异点: <3-5 个用户能看懂的差异>.
角色钩子: <与角色或作品强相关的视觉母题>.
适合: <用白话说明适合什么结果>.
风险: <低/中/高 + 一句原因>.

C. 角色符号向
画面感: <一句用户能立刻想象的画面>.
差异点: <3-5 个用户能看懂的差异>.
角色钩子: <与角色或作品强相关的视觉母题>.
适合: <用白话说明适合什么结果>.
风险: <低/中/高 + 一句原因>.

D. 风格探索向
画面感: <一句用户能立刻想象的画面>.
差异点: <3-5 个用户能看懂的差异>.
角色钩子: <与角色或作品强相关的视觉母题>.
适合: <用白话说明适合什么结果>.
风险: <低/中/高 + 一句原因>.

推荐: <A-D + 一句原因，通常优先兼顾像角色和画面完成度>.
怎么选: 回 A-D（也接受 1-4）；不确定就回"推荐"或"你选"；想融合就回"A+C"；都不满意就回"再给几个"或"换一组"。
接下来: 我会锁定方向感，然后进入画面内容；不会直接生成。
已探索: 1/10
```

Each card must differ from the others on at least `3` of these axes: purpose,
emotion, crop, style strength, and character distance. Each card must include
one character-specific hook from the source, such as a relationship, signature
object, world location, theme metaphor, or original visual motif. Do not expose
axis names as the main card content; translate them into plain Chinese choices.

Example card:

```text
A. 保守原作向
画面感: 露西站在夜之城冷色霓虹边缘，脸部清楚、姿态克制，整体像官方宣传视觉。
差异点: 成品海报 / 冷静疏离 / 半身到三分之二身 / 接近原作 / 角色优先。
角色钩子: 月球梦、白色短发、黑色网跑服与夜之城霓虹形成对照。
适合: 你想先要一张稳、像本人、可直接用的图。
风险: 低，最稳但惊喜少。
```

If the user already says "不要问", "无需引导", "直接生成", or equivalent in the
same request, treat that as workflow `B` for prompt preparation only. Generate
only if the same or later user message contains `开始生成图片`.

If the user only gives a character name or says something like "我要生成 X 图片", do not generate immediately.

First show a compact guide:

1. interpreted character and source
2. inferred identity anchors
3. exploration-first intent router
4. recommended exploration path or direction cards
5. optional quick tweak chips
6. one-line next action

Do not put a full English prompt in the first response by default. On the
default exploration path, keep advancing the progressive ladder and provide the
ready English prompt after `exploration_rounds >= 10`, when the user asks for
`B` direct prompting, says "不要探索", asks for the full prompt, or explicitly
enters finalization.

Default intent router:

```text
A. 探索方向（推荐，不用写 prompt）
B. 成品图
C. 壁纸或封面
D. 头像或肖像
E. 最大化角色相似度
F. 改变风格
G. 我来决定
```

The user may reply with one option, multiple options, or a natural-language reaction.

Examples:

- `AF`
- `A`
- `A+C`
- `B 但更像 F`
- `开始生成图片`
- `再探索`

Interpret the first selected option as the base when the user mixes options, unless they say otherwise.

## Discovery Loop

Use `references/discovery-loop.md` when the user is unsure, asks for more options, says "再探索", combines choices, or reacts with "不够泛化", "继续探索", "不是这个", or "还有吗".

Do not reset the conversation. Maintain a lightweight preference state:

- `known`: character, source, identity anchors, hard constraints
- `liked`: moods, scene families, crops, styles, references
- `disliked`: directions to avoid
- `open`: unresolved choices
- `exploration_rounds`: number of exploration turns completed on the default path
- `next_probe`: smallest useful next comparison

Exploration rules:

- In early exploration, avoid locking exact picture content too soon.
- Follow the progressive ladder from `discovery-loop.md`: first broad direction,
  then picture content, then crop/composition, then lighting/color, then
  style/finish, then final modules.
- After the user chooses one layer, advance only one layer unless they explicitly
  ask to jump ahead.
- If the user says "再探索", stay at the current layer and show different
  alternatives for that same layer.
- If the user chooses an option during active exploration, treat it as a locked preference and continue inside that branch.
- When the user says "可以了", "就这个", "use this", or equivalent approval before `exploration_rounds >= 10`, finalize the prompt if requested but do not push generation; end with edit/explore exits and a note that deeper exploration is still available. After `exploration_rounds >= 10`, finalization may end with the copyable `开始生成图片` CTA plus optional edit/explore exits. Generate only when the user says `开始生成图片`.
- Always mention that mixing is allowed, such as `A+C` or `A 但更像 C`.

Every discovery response should keep visible exits and explain the next round:

```text
推荐: <one option + short reason>.
怎么选: 回 A-F（也接受 1-6）；可混合如"A+C"；不确定回"推荐"或"你选"；都不满意回"再给几个"或"换一组"；想退一步回"返回"。
接下来: 我会锁定当前小节，并进入 <next layer/dimension>；不会直接生成。
已探索: <N>/10
未满 10 轮时继续探索；满 10 轮后再主动提示生成口令。
```

## Modular Prompt Spec

Use `references/prompt-modules.md` when the user says "可以了", asks to finalize after exploration, asks to revise only part of a prompt, asks to explore a specific module, or asks the agent to decide unresolved modules.

For Chinese users, output three layers:

1. `最终确认卡`: short Chinese summary for fast user confirmation
2. `提示词模块`: editable Chinese module list with stable module IDs
3. `英文生成提示词`: final English `image-2` prompt assembled from those modules

The confirmation card is a read-only UI summary, not the source of truth. The
only editable prompt state is `M1`-`M12`; if the user asks to change something in
the confirmation card, map that request to the matching module(s), update the
modules, then recompile the English prompt.

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

If the user asks the agent to decide unresolved modules, or after the user picks
a module option, integrate the decision into the current prompt state. While the
user is still exploring, return a lightweight update with the changed module or
dimension, the selected value, and next actions. When the user says "可以了",
"就这个", "生成", `开始生成图片`, asks for the full prompt, or reaches
generation preflight, switch to finalization state and show the full module spec
plus compiled English prompt.

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

## Identity Confidence Gate

Treat text prompts as soft constraints. A detailed description can still produce
a generic nearby design, especially when the scene, style, lighting, or outfit
freedom is stronger than the character evidence.

Choose the identity confidence level before generation:

- `prompt-only`: quick ideation; acceptable when likeness is not the main goal
- `reference-constrained`: use user or official-priority references; required
  when the user expects the character to be recognizable
- `locked`: run a lock pass first and use the lock image as the first image for
  the final pass; required when the user says likeness, face accuracy, "must
  look like", or provides reference images for identity

For a real existing-character test, default to `locked` unless the test is
explicitly labeled as prompt-only ideation. A test that jumps directly to the
final poster without an accepted lock image should be reported as an incomplete
flow test, not as evidence that the skill preserves identity.

Once an accepted lock or baseline image exists for the current character
version, use it as an identity reference for every final generation direction,
including posters, wallpapers, avatars, style changes, and mood explorations.
Do not make the user choose `E` again just to keep the baseline active. Option
`E` means "maximize likeness": generate or re-check the lock before final
generation, use stricter acceptance, and recover identity drift more
aggressively.

Do not let the lock pass replace the user's creative-direction workflow. For a
normal task, guide the user from the character into intent, mood, composition,
style, and final modules first. Use the lock or baseline image as an identity
gate before final generation, not as the final art direction. If the user asks
to test the lock image first, generate and confirm it, then return to the
module workflow for the final image.

After a baseline or lock image is generated, accepted, re-uploaded, or named by
the user, treat it as `accepted_lock_image` and immediately resume prompt
selection. Do not ask the user to write the final prompt from scratch. Show
lettered direction cards or the next unresolved ladder layer, with the lock
state visible, for example:

```text
当前层级: L2/L3 最终成图方向 / 已锁定: <character/source> identity uses accepted lock image only.

A. 稳定原作主视觉: ...
B. 情绪电影海报: ...
C. 壁纸场景版: ...
D. 风格探索版: ...

推荐: <one option + reason>.
怎么选: 回 A-D；可混合如 "A+B"；不确定回 "你选"；想先改基准图回 "修基准图"。
接下来: 我会把所选方向整理进 M1-M12，基准图只约束身份，不限制最终姿势、场景、光影和风格。
```

If the user attaches or references a baseline image and asks for final art, use
that image as identity evidence, then guide final prompt selection unless the
same message explicitly asks for the direct prompt path. The baseline image
should reduce identity drift; it must not replace the user's choice of final
composition, mood, use case, or style.

Do not finalize the full prompt immediately after the user picks one post-lock
direction card such as `A`, `B`, `C`, or `A+C`. Treat that selection as the
locked `L2 方向感` only, increment `exploration_rounds`, and advance to `L3
画面内容`. Continue the normal progressive ladder and default 10-round
exploration depth unless the user explicitly asks for the direct prompt path or
the exact generation phrase `开始生成图片`.

When advancing into a broad prompt module on that ladder, show the module's
small-module picker first instead of concrete final alternatives. In practice:
`L3` starts with `M7 画面内容` small modules, `L4` starts with `M8 构图画幅`
small modules, `L5` starts with `M9 光线色彩` small modules, and `L6` starts
with `M10 风格质感` small modules. Only after the user selects one or more small
modules should the assistant expand the first selected small module and keep
the rest as an ordered queue.

Treat an accepted lock image as identity evidence only. It may define face,
hair, eyes, makeup, outfit silhouette, color hierarchy, and signature cues. It
must not define the final pose, crop, lighting, background, rendering finish,
body emphasis, composition, scene, or mood unless the user explicitly chooses
those from the lock image.

If likeness is important, do not try to fix drift by only adding more prompt
adjectives. Strengthen the evidence instead: reduce optional style language,
put the cleanest face reference first, keep the character larger in frame, use
neutral or simple lighting for the lock pass, and retry from the lock image.

Before accepting a lock or final output, compare it against the reference pack
and ask: would the character be recognized without reading the prompt? If not,
the identity gate failed even if the image is technically polished.

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

Before choosing a generation method, verify that the latest user message
contains the exact phrase `开始生成图片`. If it does not, do not call
`image_gen`, `scripts/anime_fanart.py`, `scripts/image_gen_refs.py`, or
`scripts/generate_from_lock.py`; continue guiding, refining, or finalizing the
prompt, and keep offering the next useful dimensions to explore.

Immediately before calling any image-generation tool, send a short
pre-generation note that names the current prompt version and says the user can
continue by naming unsatisfying parts after the image, for example face,
likeness, lighting, color tone, outfit, background, composition, emotion, or
style. Do not put this note after the image-generation call.

If the user gives feedback after a generated image, use
`references/prompt-modules.md` Revision Feedback Loop to continue from the
current modules. Do not ask the user to rewrite the whole prompt.
If the feedback is "人物不像", "脸不像", "不够像", "更像", or equivalent,
enter identity-first recovery: reduce scene/style pressure, make the face and
canonical outfit more readable, and edit `M1`, `M2`, `M4`, `M8`, `M10`, and
`M12` as needed before offering another `开始生成图片` pass.

Default to the built-in `image_gen` tool for image generation. Do this even
when likeness matters, unless the user explicitly asks for a local file output,
fixed profile, API/script workflow, or real local image inputs. `OPENAI_API_KEY`
is optional for the skill, not a prerequisite for the default workflow.

Use the built-in `image_gen` tool when:

- the user asks to generate an image in the chat
- the user wants quick ideation or normal final art
- exact local file output, fixed profile, or repeatable API payloads are not
  required
- the accepted baseline can be represented by current conversation context,
  attached images, or explicit identity anchors

Use `scripts/image_gen_refs.py` when:

- the user wants the convenience of image generation but a local baseline or
  reference image must be sent as a real image input
- the task is not necessarily the full anime lock workflow
- the built-in chat `image_gen` tool would only receive text and therefore
  cannot actually see the local image file
- the user accepts that this local-file path requires `OPENAI_API_KEY`

Use `scripts/generate_from_lock.py` when:

- the user already has an accepted local baseline or lock image
- that lock image must be sent as the first real image input
- the final prompt should treat the lock image as identity-only evidence
- the written prompt should remain free to control pose, crop, scene, lighting,
  mood, background, and finish
- the task does not need to create a new lock image first
- the user accepts that this local-file path requires `OPENAI_API_KEY`

Use `scripts/anime_fanart.py` when:

- the user explicitly wants the API/script workflow for stricter local-file
  reference control
- the user wants PNG, a stable named profile, a validated custom `gpt-image-2`
  size, or repeatable metadata
- the workflow needs repeatable lock-first generation
- local reference images must be sent as real API image inputs
- prior attempts looked polished but unlike the intended character

If a script workflow is selected but `OPENAI_API_KEY` is missing, treat the key
as an optional upgrade blocker only for that script path. Run `--dry-run` when
useful, report that local-file API generation is unavailable, and offer to
continue with the default built-in `image_gen` path using the compiled prompt,
attached images if present, and identity anchors. Do not make API key setup the
preferred or required path unless the user asks for the script/API workflow.

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
  --profile poster-safe `
  --prompt "<compiled English image-2 prompt>" `
  --out "output\yanami-poster.png"
```

When using a lock image for final generation, explicitly state that the lock
image is identity-only. The final image should follow the selected modules for
scene, mood, lighting, crop, finish, and composition rather than copying the
lock image's baseline pose or render style.

Use `--dry-run` first when inspecting payloads without calling the API.

Generate from an accepted local lock image:

```powershell
python scripts\generate_from_lock.py `
  --character "Anna Yanami" `
  --series "Too Many Losing Heroines!" `
  --lock-image "output\yanami-lock.png" `
  --profile poster-safe `
  --prompt-file "output\yanami-final-prompt.txt" `
  --out "output\yanami-poster-from-lock.png"
```

This wrapper always sends `--lock-image` as image input #1 and prepends an
identity-only lock note to the prompt. The lock image should keep the character
from drifting, while the written prompt still controls pose, crop, scene,
lighting, mood, background, and finish. Use `--dry-run` to verify that
`source_images[0]` and `dry_run_payload.image[0]` are the lock image before
calling the API.

Local reference-image wrapper:

```powershell
python scripts\image_gen_refs.py `
  --image "output\lucy-lock-baseline-v1.png" `
  --prompt-file "output\lucy-final-prompt.txt" `
  --profile poster-safe `
  --out "output\lucy-final-poster.png"
```

This wrapper sends each `--image` path as a real image input to the image edit
API. It is the local-file equivalent of "give this photo to image generation."

## Quality Rules

Defaults use API-reference-compatible named profiles so the first script path
stays reliable:

- `poster-safe`: `1024x1536` stable vertical poster source
- `scene-safe`: `1536x1024` stable horizontal scene source
- `square-safe`: `1024x1024` stable square source
- `banner-safe`: `1536x1024` stable cover source

For explicit 2K or 4K delivery, use a manual `--size` rather than a named
profile. Manual sizes may use `auto` or any `gpt-image-2` size that satisfies
the current Image API constraints: longest edge `<= 3840`, both edges multiples
of `16`, aspect ratio `<= 3:1`, and total pixels between `655,360` and
`8,294,400`. Treat outputs above `2560x1440` total pixels as experimental.
Legacy profile names such as `poster-2k` are compatibility aliases only. If a
user requests actual 2K or 4K output, pass `--size` explicitly instead of using
one of those legacy aliases.

Do not promise transparent backgrounds with `gpt-image-2`.

A lock image passes only if:

- the face reads as the intended character before reading the prompt
- hairstyle and hair color are correct
- eye color and eye shape are close enough
- canonical outfit silhouette is correct
- dominant colors are correct
- no extra limbs, eyes, or fingers
- the character reads correctly at a glance

If the lock image fails, fix the lock. Do not move on to the final poster or scene.
If the final image no longer matches the accepted lock image, treat it as
identity drift: put the lock image first, reduce the reference set to the
cleanest `1-3` images, simplify style or scene pressure, and retry one variable
at a time.
If the final image copies the lock image's pose, crop, lighting, or finish too
closely, treat it as lock overfitting: keep the lock image for identity, but
make `M7`, `M8`, `M9`, and `M10` more explicit and add an avoid term for copying
the lock composition or render style.

## Recovery Rules

Use `references/recovery.md` when:

- face is off
- outfit drifts
- colors drift
- scene becomes too busy
- final image stops looking like the locked character
- variants look technically polished but too similar
- stylization gets stronger and recognizability collapses
- user says "人物不像", "脸不像", "不够像", "更像", or equivalent likeness feedback

Change one thing at a time during retries.
