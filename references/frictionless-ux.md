# Frictionless UX

Use this file when the user wants a strong result from `image-2` but cannot clearly describe the image, cannot write a solid prompt, or explicitly says "you decide".

## Goal

Make the workflow feel low-effort for the user and high-control for the agent.

The user should not need to know prompt engineering vocabulary. Convert rough taste signals into explicit image decisions.

## Default Interaction Rule

Prefer this order:

1. infer what can be inferred
2. put exploration first: offer direction cards or an exploration-first intent router
3. let the user choose, mix, delegate, or ask to skip exploration
4. recommend one default only as a selectable path, not as a hidden decision
5. on the default exploration path, keep exploring for at least `10` rounds before
   proactively offering the generation CTA
6. prepare the final prompt after a direction is chosen or delegated
7. render only after the latest user message contains the exact phrase `开始生成图片`

Hard generation gate: option letters, selected directions, "生成", "出图",
"直接生成", "按这个生成", "可以了", "就这个", "you decide", and complete
prompts are not image-generation permission. They only authorize guidance,
prompt preparation, or prompt finalization. Do not call any image-generation
tool until the user says `开始生成图片`.

Exploration-depth gate: for default-path users, track `exploration_rounds` and
show progress as `已探索: N/10`. Do not proactively offer the copyable
`开始生成图片` CTA before round 10. This gate does not block users who explicitly
choose workflow `B`, say "不要探索" / "直接给提示词", or type the exact
`开始生成图片` phrase themselves.

Do not start with a long list of questions.

Keep the default question budget at `0-1`.

Ask only when one of these is genuinely blocking:

- the character name is ambiguous
- the version is ambiguous and changes the design materially
- the requested deliverable is incompatible with the default crop
- the user supplied contradictory references

## Direct Poster Request Gate

Use this gate when the user directly asks to generate a poster, cover,
wallpaper, or key visual in the first turn or as a new task, for example:

```text
生成有史诗感的蕾姆海报
```

```text
帮我做一张 Saber 封面图
```

Default behavior:

- do not call the image tool yet
- briefly restate the interpreted character, source, and requested deliverable
- ask one two-choice workflow question:

```text
我理解你要做 <character/source + requested poster direction>。
你想 A. 先给我 4 个方向让我选（推荐），还是 B. 直接给我一版可生成提示词？
```

Route the answer:

- `A`, `探索`, `引导`, `给我几个方向`, `先看看方向`, `完善提示词`, `不知道怎么写 prompt`, or equivalent -> show four direction cards before finalizing modules and prompt
- `B`, `直接给提示词`, `不要探索`, `无需引导`, `直接生成`, `按这个生成`, `现在出图`, or equivalent -> infer missing slots conservatively and prepare final modules plus prompt, but do not render

For workflow `A`, use four user-facing direction cards by default:

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

推荐: <A-D + 一句原因>.
怎么选: 回 A-D（也接受 1-4）；不确定就回"推荐"或"你选"；想融合就回"A+C"；都不满意就回"再给几个"或"换一组"。
接下来: 我会锁定方向感，然后进入画面内容；不会直接生成。
已探索: 1/10
```

The four cards must differ on at least `3` of these axes: purpose, emotion,
crop, style strength, and character distance. Each card must include one
character-specific hook from the source, such as a relationship, signature
object, world location, theme metaphor, or original visual motif. Translate the
axes into plain Chinese instead of showing internal field names as the card.
Mark exactly one card as `推荐`, with a short reason, and give every card a
plain `风险: 低/中/高` note about likeness, face readability, scene complexity, or
canon drift.

Example card:

```text
A. 保守原作向
画面感: 露西站在夜之城冷色霓虹边缘，脸部清楚、姿态克制，整体像官方宣传视觉。
差异点: 成品海报 / 冷静疏离 / 半身到三分之二身 / 接近原作 / 角色优先。
角色钩子: 月球梦、白色短发、黑色网跑服与夜之城霓虹形成对照。
适合: 你想先要一张稳、像本人、可直接用的图。
风险: 低，最稳但惊喜少。
```

Do not write the final prompt yet unless the user chooses a card, asks the
agent to choose, or says workflow `B` instead.

If the original request already says "不要问", "无需引导", "直接生成",
"马上出图", or equivalent, treat that as workflow `B` for prompt preparation
only. Generate only if the same or later user message contains `开始生成图片`.
If the character identity or source is ambiguous, combine the identity
clarification with the same single question instead of asking multiple
questions.

## Guided-First Rule

For vague first-turn requests, guide before rendering.

Examples:

```text
I want to make an image of Violet.
```

```text
Try this skill with Violet Evergarden.
```

```text
I cannot describe what I want yet.
```

Default behavior:

- identify the character and likely source
- infer the canonical visual baseline
- show an exploration-first intent router across broad user goals
- recommend exploration as the default route unless the user clearly asked to skip it
- show optional micro-chips for quick steering
- do not provide the full English prompt until the user chooses, mixes, or delegates a direction
- ask for a low-effort next action with `怎么选` and `接下来` lines, such as `A`, `B`, `C`, `你选`, `再探索`, or one mood word; do not proactively mention `开始生成图片` before `exploration_rounds >= 10`

When the user chooses exploration, hand off to `discovery-loop.md` and follow
the progressive ladder. The first exploration reply should start at `L2 方向感`
unless the user already supplied a use case or scene.

During this handoff, initialize `exploration_rounds` and follow the `10`-round
depth gate from `discovery-loop.md`. The first direction-card reply counts as
round 1 and should show `已探索: 1/10`.

Do not call the image tool during this first guided response unless the user
explicitly says `开始生成图片`. Phrases like "generate now", "directly render",
"no need to ask", "直接生成", or selecting an existing direction still mean
prepare or finalize the prompt unless `开始生成图片` is present.

## Intake Modes

### 1. Name-only

Example:

```text
Anna Yanami
```

Default behavior:

- infer the series
- gather references
- build anchors
- show exploration-first direction cards
- include one recommended card, but make it selectable rather than final

### 2. Mood-only

Example:

```text
Make it dreamier and moodier.
```

Default behavior:

- keep the character baseline fixed
- map mood to lighting, finish, and scene density
- produce several style directions that differ in atmosphere, not identity

### 3. Rough scene

Example:

```text
Put her on a rooftop at night in the rain, and make it feel like an official poster.
```

Default behavior:

- keep the character anchors fixed
- translate "official poster" into baseline plus archetype
- turn the rough scene into a structured English prompt

### 4. Rough prompt draft

Example:

```text
A very pretty poster with a blue palette. Make it feel refined.
```

Default behavior:

- preserve the user's intent
- replace weak adjectives with concrete finish, framing, and lighting decisions
- add the missing constraints and avoid terms

### 5. Reference-only

Example:

User provides several images with little text.

Default behavior:

- infer the specific version from the references
- extract recurring anchors
- ask at most one question only if the references conflict

### 6. "You decide"

Example:

```text
You decide what suits her best.
```

Default behavior:

- choose the safest strong default
- explain the interpreted brief in one line
- optionally include `2-3` nearby variants
- do not push the decision back to the user

## Hidden Slots To Fill

When the user is vague, infer these slots yourself:

- identity: character, series, version
- output type: poster, scene, render, banner
- crop: vertical, horizontal, square, wide
- focus: portrait, half-body, full-body, wide scene
- archetype: poster-key-visual, slice-of-life, action-set-piece, dreamlike-mood-piece, fashion-editorial, banner-panorama
- baseline: tv-anime-faithful, game-render-faithful, official-illustration-faithful, manga-colorized, hybrid-promo
- finish: clean-cel, polished-key-visual, soft-filmic, painted-anime-poster, game-promo-render
- lighting: neutral-daylight, golden-hour, rainy-neon, winter-blue-hour, spring-haze, stage-spotlight, moonlit-glow
- stylization delta: faithful, lightly-stylized, boldly-reinterpreted
- constraints: recognizability, outfit fidelity, no text, no watermark

## Intent Router

Use the intent router as the default selection UX. It asks what outcome the user wants, not which art parameters they understand.

### Intent options

- `A Explore directions`: user wants the agent to help discover the best direction before prompt writing
- `B Finished image`: user wants a strong all-purpose result for sharing
- `C Wallpaper or cover`: user wants a scene, banner, desktop image, or social header
- `D Avatar or portrait`: user wants the face large and recognizable
- `E Maximize likeness`: user cares most that the character reads correctly
- `F Change style`: user wants reinterpretation, AU, fashion, cinematic, painterly, game-promo, or another style shift
- `G Surprise me`: user wants the agent to choose a high-confidence route

### Intent routing behavior

- `A Explore directions` -> return `4-6` abstract taste cards before writing the final prompt
- `B Finished image` -> recommend a polished poster or character-forward key visual
- `C Wallpaper or cover` -> recommend horizontal or panoramic scene-first composition
- `D Avatar or portrait` -> recommend face-first portrait or half-body image
- `E Maximize likeness` -> start with identity lock and neutral lighting
- `F Change style` -> ask for or infer style strength, then preserve face/outfit/source anchors
- `G Surprise me` -> choose the strongest low-risk route and state the choice briefly

For vague first-turn requests, show this router before any technical axes. Technical axes are advanced controls, not the default interface.

## Micro-Chips

Use micro-chips to let the user steer without learning prompt vocabulary. Show only one short line of chips unless the user asks for more.

### Mood chips

- faithful
- softer
- more cinematic
- dreamier
- more melancholic
- brighter
- more premium
- more dynamic
- darker

### Composition chips

- close-up
- half-body
- full-body
- wide scene
- vertical
- horizontal
- square
- banner

### Style strength chips

- keep close to canon
- lightly stylized
- bold reinterpretation
- outfit unchanged
- outfit redesign allowed

## Progressive Disclosure

Do not show every control at once.

Use this order:

1. exploration-first intent router
2. direction cards or taste cards
3. recommendation as a selectable default
4. ready prompt only after a direction is chosen or delegated
5. advanced creative-control axes only if the user asks to customize

This makes the first response broadly useful without feeling like a form.

## Creative-Control Axes

Use these axes only as advanced controls. Do not show the full axis grid by default.

### 1. Use case

- `poster`: vertical hero art or key visual
- `wallpaper`: horizontal scene or cinematic frame
- `avatar`: face-forward square or portrait crop
- `banner`: wide header or cover image
- `character-sheet`: clean full-body render

### 2. Scene family

- `canonical-world`: location and props close to the source work
- `quiet-daily`: small everyday moment
- `cinematic-drama`: emotional scene with strong light and framing
- `symbolic`: abstract or poetic visual motif
- `fashion-editorial`: controlled pose and premium print feel
- `seasonal`: spring, summer, autumn, winter, rain, festival, snow
- `action-or-motion`: movement, wind, battle, performance, or gesture
- `crossover-au`: alternate outfit or setting, only if the user allows reinterpretation

### 3. Mood

- `faithful-calm`
- `warm-nostalgic`
- `melancholic`
- `dreamlike`
- `dramatic`
- `bright-playful`
- `mysterious`
- `premium-refined`

### 4. Style strength

- `identity-first`: safest likeness, smallest style movement
- `lightly-stylized`: different lighting or finish, same design logic
- `bold-reinterpretation`: stronger atmosphere or setting, identity anchors must be restated

### 5. Fidelity priority

- `face-first`: maximize face and hair recognizability
- `outfit-first`: preserve canonical costume silhouette
- `scene-first`: let the environment carry more of the image
- `mood-first`: prioritize emotional atmosphere

## Safe Defaults

Use these when the user did not specify them:

- poster-like hero image -> `poster-safe`
- wallpaper-like scene -> `scene-safe`
- icon/avatar/social crop -> `square-safe`
- header/cover/wide illustration -> `banner-safe`
- likeness-first pass -> `neutral-daylight`
- romantic or soft mood -> `spring-haze`
- premium or polished -> `polished-key-visual`
- official-poster feel -> `official-illustration-faithful` + `poster-key-visual`
- "you decide" -> faithful or lightly stylized, not bold reinterpretation

## Output Pattern For Vague Requests

When the request is underspecified, produce a compact pack in this order:

1. interpreted brief in Chinese
2. exploration-first intent router with broad user goals
3. `4-6` direction cards or a recommended exploration path
4. optional micro-chips
5. one-line next action

Do not include the full English prompt in this first response unless the user
asks to skip exploration or says `B` in the direct poster gate.

Do not make the user choose from many technical axes on the first turn. Use technical axes only after they ask for custom control.

## Intent Router Template

Use this shape for vague first-turn requests:

```text
我会先按这个理解: <character> 来自 <series>，版本/视觉基线是 <version/baseline>。

你想先做哪种方向？
A. 探索方向（推荐，不用写 prompt）
B. 成品图
C. 壁纸或封面
D. 头像或肖像
E. 最大化角色相似度
F. 改变风格
G. 我来决定

推荐: A，因为你不用先写 prompt，只要从方向里选最接近的。
快速微调: <5-8 chips, for example "更柔和 / 更电影感 / 更梦幻 / 更接近原作 / 横版 / 脸部优先">

怎么选: 回 A-G（也接受 1-7）；不确定就回"推荐"或"你选"；想换一组就回"再探索"；也可以补一个微调词。
接下来: 我会把你的选择转成第一组方向卡；满 10 轮或你要求跳过时再整理英文提示词。
```

If the user chooses `A Explore directions`, return abstract taste cards instead
of generating. Do not decide exact picture content in that response.

## Taste Cards

Use taste cards as the default for `A 探索方向`, after the user asks to explore,
or when the user seems undecided after the intent router.

Taste cards are `L2 方向感`, not final prompt choices. After the user picks or
mixes a taste card, advance to `L3 画面内容`; do not jump directly to lighting,
style, or final prompt unless the user asks.

On the default exploration path, each taste-card selection, mix, or `再探索`
increments `exploration_rounds`. Keep the user in this progressive loop until at
least round 10 before proactively showing the generation CTA.

Each card should combine:

- mood
- purpose
- crop
- style strength
- character distance
- one reason it fits the character

Keep the cards diverse. Avoid making all cards poster-like. Avoid specific locations, props, poses, weather, or story beats until the user chooses a taste card.

For deeper multi-turn exploration, use `discovery-loop.md` instead of adding more menu options to this file.

## Prompt Upgrade Rules

When rewriting weak user language into an `image-2` prompt:

- keep the character name and series explicit
- keep identity anchors near the top
- state the source baseline explicitly
- define composition clearly
- define lighting in visual terms
- keep the scene simple enough for the face to stay readable
- use concise avoid terms targeted at likely failure modes

### Replace weak wording

- "pretty" -> choose a pose, a clean composition, and a finish
- "moody" -> choose a lighting pack and restrained environment cues
- "premium" -> lower prop count, cleaner silhouette, premium finish
- "like official art" -> official-illustration-faithful or game-render-faithful baseline
- "refined" -> better staging and finish, not more random detail

### Avoid these mistakes

- mirroring the user's vague words without adding visual structure
- piling on synonyms for style
- changing identity and style at the same time
- making the background more complex than the user's actual intent requires
- using strong stylization before the canonical baseline is established

## 中文紧凑回复模板

用户表达不清楚时，用这种格式：

```text
理解简述: <一句话说明我理解的角色、作品和目标>

你想先做哪种方向？
A. 探索方向（推荐，不用写 prompt）
B. 成品图
C. 壁纸或封面
D. 头像或肖像
E. 最大化角色相似度
F. 改变风格
G. 我来决定

推荐: A。你不用先写 prompt，只要选最接近的方向。
快速微调: <5-8 个可直接回复的微调词>
```

用户选定或委托一个方向后，默认继续进入递进探索；未满 10 轮时不要主动提示生成口令。用户明确要求跳过探索或已满 10 轮后，再提供英文提示词，并等到用户说出精确口令 `开始生成图片` 后再执行任何生成流程。

## Escalation Rule

If the first result is technically good but emotionally off, do not ask the user to rewrite the whole prompt. Keep the identity anchors fixed and change only one of:

- archetype
- crop
- lighting
- finish
- scene density

This keeps retries easy for the user to react to.
