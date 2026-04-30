# Discovery Loop

Use this file when the user is not ready to choose a final prompt. The goal is to help them discover what they want through lightweight comparison, not through a long form.

## Design Principle

Treat every suggestion as a probe. A probe is a small, meaningful direction the user can react to.

Do not ask the user to name technical parameters unless they already use that language. Show semantically different possibilities and learn from reactions.

Do not lock concrete picture content too early. In early discovery, avoid exact locations, props, poses, weather, and story beats unless the user supplied them. First discover the user's abstract preference, then translate it into concrete image candidates.

## Progressive Exploration Ladder

Exploration should feel like a funnel. Do not offer unrelated directions from
different levels in the same turn. Move from broad taste to concrete image
decisions in this order:

```text
L0 身份基线: character, source, version, identity anchors
L1 用途画幅: poster / wallpaper / avatar / banner / render
L2 方向感: canon-close / cinematic-emotional / style-exploration / symbolic
L3 画面内容: scene family, location type, action or stillness, motif
L4 构图距离: face / half-body / full-body / wide, camera angle, hierarchy
L5 光色氛围: time, lighting direction, palette, emotional intensity
L6 风格质感: finish, line/paint/render feel, detail density, canon risk
L7 定稿: M1-M12 modules and compiled English prompt
```

Rules:

- Start at the earliest unresolved layer. If the user only gives a character,
  start at `L1` or `L2`; if they already gave a scene, record it and start at the
  next unresolved layer.
- Every exploration reply should show one short state line:
  `当前层级: Lx <name> / 已锁定: <1-3 choices>`.
- Each turn should ask about one layer only. Offer `4-5` choices at that layer by
  default; use `5-6` when the user asks for "再给几个", "换一组", or "都不满意".
  Use only `3` choices for quick mode or narrow module edits.
- After a user picks an option, lock that layer and advance exactly one layer.
- For `L3`-`L6` and any broad `M1`-`M12` module, the first turn should be a
  small-module picker by default instead of a final creative choice. Let the user
  select which submodules to explore, then expand the selected submodules in
  order. Choosing small modules counts as an exploration round but does not lock
  a final prompt value yet. Skip the picker only when the user names a specific
  submodule, asks for a quick fix, or already supplied that decision.
- `再探索`, "再给几个", "换一组", and "都不满意" mean stay on the current
  layer and show different choices.
- `返回` means go back one layer while preserving earlier locked choices.
- `A+C` mixes choices inside the current layer; it should not jump to a later
  layer.
- Only jump layers when the user explicitly provides a later decision, such as a
  concrete scene or exact crop. Even then, keep earlier locked choices visible.

## Minimum Exploration Depth

The default path is exploration-first. For users who did not explicitly choose
`B` / "不要探索" / "直接给提示词", do not proactively offer the copyable
`开始生成图片` CTA until the current task has reached at least `10` exploration
rounds.

Count one exploration round whenever the user:

- picks one displayed option
- mixes options such as `A+C` or `A 但更像 C`
- says `再探索`
- delegates a choice with `你选`
- gives a taste reaction that changes the branch
- chooses a module or dimension probe

Every default-path exploration reply should show `已探索: N/10` near the final
next-action line. Before `N >= 10`, the final next-action line should offer
selection, mixing, `再探索`, `返回`, `你选`, or `可以了`, but should not proactively
mention `开始生成图片`. After `N >= 10`, finalization responses may end with:

```text
已探索: 10/10，可以定稿。
下一步：回复「开始生成图片」即可出图；或回复「再探索」继续看方向。
```

If the user explicitly says `开始生成图片` before round 10, obey the hard generation
gate after a short preflight note. If the user explicitly asks to skip exploration,
use the direct prompt path and do not apply this depth gate.

Default 10-round rhythm:

1. `L2` broad direction: canon-close / cinematic / style-exploration
2. `L2` direction refinement: character distance, emotional intensity, or mix
3. `L3` scene family: where the image lives without overloading details
4. `L3` picture motif: action/stillness, prop logic, or symbolic hook
5. `L4` crop and character distance: face / half-body / full-body / wide
6. `L4` composition hierarchy: what the viewer notices first
7. `L5` lighting/color submodules: subject light / background light / ambient light / light color / shadow texture
8. `L5` selected submodule detail: offer options for the first selected light/color submodule
9. `L6` finish submodules and canon risk: line finish / render texture / detail density / source-faithful vs stylized
10. `L7` final module pass: show unresolved choices, let user edit or approve

If the user resolves several layers quickly, do not jump to the generation CTA
early. Use the remaining rounds for high-value refinement: likeness safety,
composition readability, scene density, light/color, finish, or avoid terms. Keep
each round small and concrete so the user can imagine the resulting picture.

## Guidance Microcopy

Choice guidance is part of the product experience. It should make the next click
obvious without explaining the whole system.

Use letters as the visible option labels (`A`, `B`, `C`). Accept numeric aliases
silently (`1` = `A`, `2` = `B`, `3` = `C`) but do not display numbers as primary
labels because they conflict with `已探索: N/10`, `L2/L3`, and `M1`-`M12`.

Every exploration choice block must end with this shape:

```text
推荐: <one option + short reason>.
怎么选: 回 A-D（也接受 1-4）；不确定就回"推荐"或"你选"；想融合就回"A+C"；都不满意就回"再给几个"或"换一组"。
接下来: 我会锁定 <current decision>，然后进入 <next layer>; 不会直接生成。
已探索: <N>/10
```

For `A-F` lists, change `A-D / 1-4` to `A-F / 1-6`. Keep the guidance to one or
two short lines; do not add a paragraph of instructions.

Layer-specific `接下来` lines:

- `L2 方向感`: `我会锁定方向感，然后进入画面内容；不会直接生成。`
- `L3 画面内容`: `我会锁定画面内容，然后进入构图距离；不会直接生成。`
- `L4 构图距离`: `我会锁定构图距离，然后进入光色氛围；不会直接生成。`
- `L5 光色氛围`: `我会锁定光色氛围，然后进入风格质感；不会直接生成。`
- `L6 风格质感`: `我会锁定成片质感，然后做最终模块检查；未满 10 轮会继续补关键细节。`
- module/dimension exploration: `我只更新这一小节，其他已锁定内容保持不变。`

Recommendation and risk labels:

- Every choice set must include exactly one `推荐` line. Prefer the option that
  best balances character likeness, visual clarity, and exploration value.
- Every option should include a compact `风险` or `影响` note. Use `低/中/高` for
  visual/image risk, or plain impact wording for module edits.
- Risk is not a safety warning. It tells the user whether the option may reduce
  likeness, overload the background, make the face less readable, or push style
  farther from canon.
- Do not make options overly specific too early. At `L2` and early `L3`, each
  option should leave room for later composition, lighting, and finish choices.

## State To Maintain

Keep this state mentally across turns. Do not print it unless useful.

```text
known:
  character:
  source:
  identity_anchors:
  hard_constraints:
liked:
  moods:
  abstract_preferences:
  scene_families:
  crops:
  styles:
  references:
disliked:
  avoid_moods:
  avoid_scene_families:
  avoid_specific_content:
  avoid_styles:
open:
  current_layer:
  exploration_rounds:
  purpose:
  crop:
  style_strength:
  picture_content:
  scene_density:
next_probe:
```

Update the state from natural language:

- "A but softer" -> keep A's abstract direction, lower contrast, warmer or hazier light
- "more like C" -> transfer C's mood, purpose, or style strength, not its concrete picture content unless the user mentions it
- "too generic" -> increase specificity later through scene logic, prop logic, or character-specific symbolism
- "too far" -> reduce style strength and reassert canonical baseline
- "more premium" -> cleaner staging, lower prop count, controlled lighting, stronger composition hierarchy
- "more emotional" -> increase emotional intensity first; decide pose, facial expression, lighting direction, and symbolic environment in the picture-content phase
- "not like her" -> return to likeness-first lock and canonical outfit

## Loop Structure

### 1. Orient

State the current interpretation in one sentence.

```text
I am treating this as: <character/source>, with <identity anchors>, and the current goal is <goal>.
```

### 2. Probe Abstract Preference First

Offer `4-6` abstract probes at `L2 方向感`. Make them semantically different,
but do not bind them to exact picture content yet.

Every probe set must include character-specific hooks. When the character and
source are known, each card should include at least one hook from that source:
a relationship, signature object, world location, theme metaphor, or original
visual motif. Keep the hook abstract in early discovery, so the direction feels
specific to the character without locking an exact scene too soon.

Good probe axes:

- purpose: finished image, wallpaper, avatar, reference sheet, mood exploration
- emotional direction: calm, warm, lonely, dramatic, playful, mysterious, premium
- crop: face, half-body, full-body, wide environment
- style strength: canon-close, lightly stylized, bold reinterpretation
- character distance: intimate close-up, character-forward, environment-forward, symbolic
- story energy: still, quiet narrative, dramatic narrative, motion

Avoid early specifics:

- exact locations
- exact props
- exact poses
- exact weather or time of day
- exact story beats

### 3. Translate To Picture Content Later

After the user picks an abstract probe, advance to `L3 画面内容` and first offer
the picture-content small-module picker. Do not jump straight to concrete
picture-content candidates unless the user already named a specific scene or
asked for a quick preset.

At this stage, concrete content becomes useful only inside the selected
small-module:

- location
- prop
- pose
- time of day
- weather
- symbolic motif
- camera distance

Keep one candidate conservative, one emotionally stronger, and one more surprising.

### 4. Capture

Ask for a low-effort reaction.

```text
推荐: <one option + short reason>.
怎么选: 回 A-F（也接受 1-6）；可混合如"A+C"或"A 但更像 C"；不确定回"推荐"或"你选"；都不满意回"再给几个"或"换一组"。
接下来: 我会锁定当前小节，并进入下一层；不会直接生成。
已探索: <N>/10
```

If the user has entered active exploration mode, do not end exploration just because they picked an option. Treat each pick as a new locked preference and continue exploring inside it until the user explicitly says they are done.

### 5. Narrow

After a reaction, narrow instead of expanding everything again.

Decision rule:

- if the user chooses one abstract probe -> increment `exploration_rounds`, then offer picture-content candidates or ask permission to choose one
- if the user likes two probes -> merge only one feature from the second into the first
- if the user combines options -> keep the first option as the base unless they say otherwise
- if the user says none -> change the probe axis, not all axes
- if the user says "再探索", "再给几个", "换一组", or "都不满意" -> increment `exploration_rounds`, stay at the same decision level, and offer new alternatives that avoid repeating prior probes
- if the user says "返回" -> return one decision level up and preserve learned likes/dislikes
- if the user gives a mood word -> map it to emotional direction first; defer pose and scene content until the picture-content phase
- if the user asks for surprise -> pick the strongest route and explain in one sentence

Do not auto-commit after narrowing during active exploration. A narrowed choice
becomes the current branch, then offer the next unresolved ladder layer.

Finalize the current prompt, but keep exploration open, when the user says one of:

- "ok"
- "looks good"
- "this one"
- "可以了"
- "就这个"
- "生成" (finalize the prompt only; do not generate)
- "开始生成图片"
- "stop exploring"
- "use this"

### 6. Commit

Before generation, show the selected direction in one short sentence, then produce a modular prompt spec and the compiled final prompt. Do not call an image-generation tool unless the user said `开始生成图片`. If the user did not say `开始生成图片` and `exploration_rounds < 10`, keep guiding exploration after the compiled prompt by offering the next useful dimension or a `探索更多维度` path without the generation CTA. If `exploration_rounds >= 10`, use the copyable generation CTA.

Use `prompt-modules.md` for finalization after exploration. The compiled prompt should be derived from modules, not written as an unstructured one-off paragraph.

If the user asks the agent to decide unresolved modules or chooses a module option, use `prompt-modules.md` Auto-Integration After Decisions: output the full updated module list and compiled English prompt, not just the changed module.
This also applies to dimension queues: after each queued selection is integrated,
show the full `M1`-`M12` module list and full compiled English prompt before
offering the next queued dimension or more-dimension choices.

## Active Exploration Mode

Use active exploration mode after the user says "explore more", "continue exploring", "再探索", or otherwise asks to keep discovering.

In active exploration mode:

- do not produce a final prompt by default
- do not ask "is this okay?" after every choice
- treat each selected option as a preference update
- keep the current branch fixed unless the user says `返回`
- explore one new dimension per turn
- if the user explicitly approves without saying `开始生成图片` before `exploration_rounds >= 10`, finalize modules if useful but end with edit/explore exits and `已探索: N/10`; after `exploration_rounds >= 10`, end with the copyable `开始生成图片` CTA plus optional edit/explore exits
- stop only when the user says `开始生成图片` or asks to stop

Use the ladder before rotating dimensions. Only rotate within the current layer
when the user asks for `再探索`, or after finalization when they ask to keep
exploring.

Within-layer small-module examples:

- `L2 方向感`: canon closeness, emotion, character distance, symbolism
- `L3 画面内容`: 场景类型, 角色行为, 叙事瞬间, 角色符号, 背景密度, 道具逻辑
- `L4 构图距离`: 角色距离, 镜头角度, 画幅比例, 视觉重心, 前中后景层次, 留白/标题空间
- `L5 光色氛围`: 人物打光, 背景光, 环境光, 光线颜色, 阴影质感, 角色原色保护
- `L6 风格质感`: 线条质感, 上色方式, 渲染精度, 材质细节, 后期颗粒/胶片感, 原作贴近度

After each turn, end with:

```text
推荐: <one option + short reason>.
怎么选: 回 A-F（也接受 1-6）；可混合如"A+C"或"A 但更像 C"；不确定回"推荐"或"你选"；都不满意回"再给几个"或"换一组"；想退一步回"返回"。
接下来: 我会锁定当前小节，并继续下一层；不会直接生成。
已探索: <N>/10
```

## Exploration Modes

### Fast Track

Use when the user wants low effort.

- one recommended route
- one prompt
- one next action

### Taste Finder

Use when the user says they do not know what they want.

- `4-6` abstract taste cards
- no final prompt until they pick or react
- each card should avoid exact picture content
- each card should differ by purpose, emotional direction, character distance, or style strength

### Reference-Led

Use when the user has images, screenshots, pins, or "like this" examples.

- ask for or use the reference
- separate identity reference from style reference
- decide whether the reference should affect face, outfit, composition, color, or mood

### Contrast Test

Use when the user is stuck between options.

- offer two opposite directions
- ask which is closer
- then interpolate

Example:

```text
A. Canon-close, quiet, face-first
B. More cinematic, environment-first, stronger mood
```

### Mutation

Use after the user likes a result but wants refinement.

Change exactly one thing:

- crop
- lighting
- emotional intensity
- scene density
- style strength
- outfit freedom

### Explore More

Use when the user explicitly asks for more options, says "再探索", or seems unconvinced by the current set.

- stay at the current decision level
- preserve likes and dislikes
- avoid repeating previous options
- change the probe axis if the last set felt too narrow
- offer `5-6` new alternatives when the user asks for more; avoid repeating the
  previous set and include at least one safer, one more emotional, one more
  character-specific, and one more surprising route
- include `返回` as an exit; include `开始生成图片` only after `exploration_rounds >= 10` or when the user explicitly asks for it

Examples:

- after abstract taste cards -> provide new abstract taste cards, not picture content
- after picture-content candidates -> provide new picture-content candidates within the chosen abstract direction
- after final prompt -> provide alternate prompt directions or return to picture-content candidates
- after the user names a module, such as "再探索 M9" -> use module-level exploration from `prompt-modules.md`

## Probe Card Template

Use this for early discovery:

```text
当前层级: L2 方向感 / 已锁定: <identity baseline>.

A. <方向名>
画面感: <一句用户能立刻想象的画面>.
差异点: <3-5 个用户能看懂的差异，例如用途 / 情绪 / 构图 / 风格强度 / 角色距离>.
角色钩子: <与角色或作品强相关的视觉母题>.
适合: <用白话说明适合什么结果>.
风险: <低/中/高 + 一句原因>.

B. <方向名>
画面感: ...
差异点: ...
角色钩子: ...
适合: ...
风险: ...

C. <方向名>
画面感: ...
差异点: ...
角色钩子: ...
适合: ...
风险: ...

D. <方向名>
画面感: ...
差异点: ...
角色钩子: ...
适合: ...
风险: ...

推荐: <one option + short reason>.
怎么选: 回 A-D（也接受 1-4）；不确定就回"推荐"或"你选"；想融合就回"A+C"；都不满意就回"再给几个"或"换一组"。
接下来: 我会锁定方向感，然后进入画面内容；不会直接生成。
已探索: <N>/10
```

Do not include specific picture content in early probe cards. Translate internal
axes into plain user-facing Chinese; cards should feel like creative directions,
not parameter dumps.

## Mixing Options

Always tell the user they can mix options.

Interpret mixed choices conservatively:

- `A+C` -> use A as the base, borrow the most distinctive trait from C
- `A 但更像 C` -> keep A's purpose/content, move style, mood, or intensity toward C
- `A+B+C` -> ask which one is the base if the combination would affect more than two modules
- `不要 A 的 X，只要 C 的 Y` -> update only the named traits

Do not blindly merge every detail from both options. A clean hybrid is better than an overloaded prompt.

Exception for dimension/module selection:

- when the displayed choices are dimensions to edit, modules to explore, or
  other sequential controls rather than competing alternatives for one decision,
  interpret multiple letters as an ordered queue
- `abcefgh` means process A, then B, then C, then E, then F, then G, then H
- handle only the first queued dimension in the current reply, keep the remaining
  queue visible, and continue through the queue after each user choice
- do not synthesize queued dimensions into new combined directions unless the
  user explicitly asks for a combined direction

## Picture-Content Template

Use this after the user chooses an abstract preference:

```text
当前层级: L3 画面内容 / 已锁定: <abstract preference>.

先选这轮想探索哪些画面内容小模块（可多选）:
A. 场景类型: 决定画面发生在哪里，但不急着锁死具体地点。
B. 角色行为: 决定角色是在静止、前进、回头、保护、修复还是展示。
C. 叙事瞬间: 决定画面像一个故事的哪一秒。
D. 角色符号: 决定使用哪些原作母题、关系、物件或主题隐喻。
E. 背景密度: 决定背景是极简、适中、丰富还是史诗。
F. 道具逻辑: 决定哪些道具能强化角色，而不是堆杂物。
影响: 选小模块只是决定接下来探索哪里，不会马上锁死最终画面。

推荐: <2-3 个小模块 + 一句原因，优先兼顾角色钩子和画面想象力>.
怎么选: 回 A-F（也接受 1-6）；可多选如"ACD"；不确定回"推荐"或"你选"；都不满意回"换一组"；想退一步回"返回"。
接下来: 我会先展开你选的第一个画面内容小模块，其他小模块排队；不会直接生成。
已探索: <N>/10
```

After the user selects picture-content submodules, show options only for the
first selected submodule and keep the remaining submodules queued.

## Later-Layer Templates

Use these after `L3` so the user can imagine the picture more clearly one layer
at a time.

### L4 构图距离

```text
当前层级: L4 构图距离 / 已锁定: <direction + picture content>.

先选这轮想探索哪些构图小模块（可多选）:
A. 角色距离: 脸部、半身、三分之二身、全身或大环境。
B. 镜头角度: 平视、俯视、仰视、侧面、回头或电影镜头。
C. 画幅比例: 竖版海报、横版壁纸、方图头像或宽幅 banner。
D. 视觉重心: 观众第一眼看脸、姿态、道具、背景还是标题空间。
E. 前中后景层次: 决定画面深度和背景是否压过角色。
F. 留白/标题空间: 决定能否作为封面、海报或社媒图使用。
影响: 选得越多，构图会更可控；不需要一次全选。

推荐: <2-3 个小模块 + 一句原因，优先保护脸部识别和成图用途>.
怎么选: 回 A-F（也接受 1-6）；可多选如"ACE"；不确定回"推荐"或"你选"；都不满意回"换一组"；想退一步回"返回"。
接下来: 我会先展开你选的第一个构图小模块，其他小模块排队；不会直接生成。
已探索: <N>/10
```

### L5 光色氛围

```text
当前层级: L5 光色氛围 / 已锁定: <direction + picture content + composition>.

先选这轮想探索哪些光影小模块（可多选）:
A. 人物打光: 决定脸、头发、身体轮廓是否清楚，以及角色像不像。
B. 背景光: 决定背景有没有窗光、霓虹、夕阳、舞台光等记忆点。
C. 环境光: 决定空气感、雾气、雨夜反光、月光等氛围。
D. 光线颜色: 决定冷暖、主色、角色原色保护和情绪倾向。
E. 阴影质感: 决定柔阴影、硬阴影、胶片阴影、赛璐璐阴影等质感。
F. 你来搭配: 我按当前方向挑 2-3 个最值得探索的小模块。
影响: 选得越多，后面轮次越丰富；不需要一次全选。

推荐: <2-3 个小模块 + 一句原因，优先能提升画面想象力且不伤角色识别>.
怎么选: 回 A-F（也接受 1-6）；可多选如"ADE"；不确定回"推荐"或"你选"；想看别的小模块就回"换一组"；想退一步回"返回"。
接下来: 我会先展开你选的第一个光影小模块，其他小模块排队；不会直接生成。
已探索: <N>/10
```

After the user selects light/color submodules, show options only for the first
selected submodule and keep the remaining submodules queued:

```text
当前层级: L5 光色氛围 > 人物打光 / 队列: <背景光, 光线颜色>.

A. 脸部清晰主光: <what changes and why it helps likeness>
B. 侧逆光轮廓: <what changes and why it feels more dramatic>
C. 柔和漫反射: <what changes and why it feels gentler>
D. 高对比硬光: <what changes and what risk it adds>

推荐: <one option + short reason>.
怎么选: 回 A-D（也接受 1-4）；可混合如"A+B"；都不满意回"再给几个"；想跳到下个小模块回"下一个"。
接下来: 我会更新人物打光，然后继续队列里的下一个光影小模块。
已探索: <N>/10
```

### L6 风格质感

```text
当前层级: L6 风格质感 / 已锁定: <direction + content + composition + light>.

先选这轮想探索哪些风格质感小模块（可多选）:
A. 线条质感: 接近原作线条、清爽线稿、厚涂边缘或更设计化线条。
B. 上色方式: 赛璐璐、柔和插画、厚涂、电影调色或游戏宣传图质感。
C. 渲染精度: 干净角色图、精致海报、细节丰富或更克制。
D. 材质细节: 皮肤、头发、布料、金属、湿面或发光材质。
E. 后期颗粒/胶片感: 决定是否有胶片、颗粒、轻 bloom 或印刷感。
F. 原作贴近度: 决定最终风格离原作多近，防止风格漂移。
影响: 风格小模块会影响成片观感，也会影响角色相似度风险。

推荐: <2-3 个小模块 + 一句原因，优先兼顾精致度和身份稳定>.
怎么选: 回 A-F（也接受 1-6）；可多选如"BCF"；不确定回"推荐"或"你选"；都不满意回"换一组"；想退一步回"返回"。
接下来: 我会先展开你选的第一个风格质感小模块，其他小模块排队；未满 10 轮会继续补关键细节。
已探索: <N>/10
若已满 10 轮，再追加「开始生成图片」CTA。
```

## Finalization Template

```text
已选方向: <one sentence>.

最终确认卡:
角色: <character + source + version>
画面: <one-sentence visible image summary>
风格: <emotion + lighting + finish summary>
风险控制: <identity/canon/avoid safeguards>

提示词模块:
M1 身份锚点: ...
M2 原作基线: ...
M3 用途目标: ...
M4 改编边界: ...
M5 情绪方向: ...
M6 角色状态: ...
M7 画面内容: ...
M8 构图画幅: ...
M9 光线色彩: ...
M10 风格质感: ...
M11 正向约束: ...
M12 避免项: ...

英文生成提示词:
<image-2-ready English prompt>

已探索: <N>/10
你还可以改某一模块，例如"改 M9 光线色彩"；或回复"探索更多维度"继续调整。
若已满 10 轮或用户已明确要求生成，下一步：回复「开始生成图片」即可出图；否则继续「再探索」看方向。
```

## Universal Exits

Every discovery response should include at least two exits. Before
`exploration_rounds >= 10`, do not proactively include `开始生成图片` as one of
them. Finalization responses after round 10 should include all three:

- `开始生成图片`: commit to the current prompt and permit image generation; proactive CTA only after `exploration_rounds >= 10` unless the user explicitly asks for it
- `再探索`: stay at this level and show different alternatives
- `返回`: return to the previous level

Do not hide these exits in prose. Put them in the final next-action line.

If the user asks to explore a specific module, the next-action line should stay module-scoped.
Default module exploration should use `A-D`; quick module repairs may use `A-C` only
when the user explicitly asks for a fast or minimal change.

```text
怎么选: 回 A-D（也接受 1-4）；想换一组就回"继续探索 M9"或"再给几个"；想退一步回"返回"。
接下来: 我只更新这一小节，其他已锁定内容保持不变。
```

If the user asks to explore more dimensions after a modular prompt spec, use `prompt-modules.md` More-Dimensions Exploration and keep the current prompt unchanged until they select a dimension.

## Guardrails

- Never turn discovery into a survey.
- Never show more than `6` probes at once.
- Do not expose advanced technical axes before the user shows they want control.
- Preserve identity anchors across probes unless the user asks for reinterpretation.
- When unsure, vary purpose, emotional direction, character distance, and style strength before choosing exact picture content.
- Do not turn early taste discovery into a list of specific scene ideas.
- Always offer an escape from the current branch: before round 10 use 再探索, 返回, 你选, or 可以了; after round 10 include 开始生成图片 as the generation CTA.
- Keep user agency visible: recommendations are defaults, not hidden decisions.
