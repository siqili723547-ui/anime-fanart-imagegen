# Prompt Modules

Use this file when finalizing a prompt after exploration, when the user asks to finalize after several choices, or when the user wants to change only part of an existing direction.

Hard generation gate: the modular prompt spec can be finalized without
generating an image. Only the exact phrase `开始生成图片` permits image
generation. Other approvals such as "生成", "可以了", "就这个", picking an
option, or asking the agent to decide only update modules and the compiled
English prompt.

Until the user says `开始生成图片`, keep the user in guided exploration. Use two
response modes:

- **Exploration state**: for "再探索", module probes, option mixing, and
  dimension queues, keep the reply lightweight. Show the current branch, the
  targeted module or dimension, `4-6` choices, and the next action. Do not print
  the full `M1`-`M12` list or the compiled English prompt unless the user asks
  for the full prompt.
- **Finalization state**: when the user says "可以了", "就这个", "生成",
  `开始生成图片`, asks for the full prompt, or reaches generation preflight,
  output the full current `提示词模块` list (`M1`-`M12`) and the full compiled
  English prompt.

Every exploration or finalization response must still end with concrete next
actions. Exploration replies should keep a visible `探索更多维度` path.
On the default exploration path, do not proactively offer the copyable
`开始生成图片` CTA until `exploration_rounds >= 10`. Before that, finalization may
show modules if the user asks, but the next action should emphasize continuing
exploration or editing. After round 10, finalization replies should end with the
copyable `开始生成图片` CTA and optional edit/explore exits. Do not treat a finished
English prompt as the end of the workflow.

For module or dimension choices, use the same guidance microcopy as discovery:
visible options use letters, numeric aliases are accepted silently, and every
choice block says how to reply plus what will happen next. Module-level
exploration should explicitly say that only the targeted module changes.
When offering module or dimension choices, mark exactly one option as `推荐` and
add `影响` or `风险` notes so the user can choose without understanding module
internals.

## Final Confirmation Card

When finalizing for Chinese users, put a short `最终确认卡` before the module list.
It helps the user confirm the result without reading the full English prompt.

The confirmation card is not prompt state. It is a UI summary derived from
`M1`-`M12`. The only editable source of truth is the module list. If the user
says "改确认卡里的画面", "风险控制再强一点", "风格换一下", or similar, map the request
back to the relevant modules, update those modules, then recompile the English
prompt.

Use this shape:

```text
最终确认卡:
角色: <character + source + version>
画面: <one-sentence visible image summary from M3/M7/M8>
风格: <emotion + lighting + finish summary from M5/M9/M10>
风险控制: <identity/canon/avoid safeguards from M1/M2/M4/M11/M12>
```

Keep it short: `4` lines, no more than one sentence per line. Do not put unique
details in the confirmation card that are absent from `M1`-`M12`.

## Revision Feedback Loop

Use this when the user reacts to a generated image or current prompt with
feedback such as "不满意", "人物不像", "脸不像", "不够像", "更像原作",
"光影不满意", "色调不对", "背景太乱", "构图不行", "风格太 AI", or any
concrete complaint.

Rules:

- Do not restart the workflow or ask the user to rewrite the full prompt.
- Map the complaint to the smallest relevant module set, then continue from the
  current module state.
- If the complaint is ambiguous, show concrete correction choices inside the
  mapped module instead of rewriting immediately.
- After applying a correction in exploration state, show the changed module(s),
  the new local wording, and the next actions. If the correction finalizes the
  prompt or the user asks to generate, output the full current `提示词模块` list
  (`M1`-`M12`) and the full compiled English prompt.
- End by asking whether they want more changes, and include visible next actions:
  `开始生成图片`, continue editing the same module, edit another module, explore
  more dimensions, or return.

Common feedback mapping:

- face, likeness, hair, eyes, "人物不像", "脸不像", "不够像", "更像原作":
  `M1`, `M2`, `M4`, `M8`, `M10`, sometimes `M12`
- outfit, costume drift, too much AU: `M4`, `M7`, `M12`
- lighting too flat, too dark, too bright, AI glow: `M9`, sometimes `M10`
- color tone wrong, too cold, too purple, too saturated: `M9`
- background clutter, wrong motifs, unwanted objects: `M7`, `M8`, `M12`
- crop, distance, framing, poster balance: `M8`
- expression, mood, agency, pose intent: `M5`, `M6`
- too official, too fanart, too digital, too AI, not hand-drawn enough: `M10`,
  sometimes `M4`

Chinese response shape after applying a revision:

```text
已更新: <one sentence naming the revised module(s) and intent>.

提示词模块
M1 身份锚点: ...
...
M12 避免项: ...

英文生成提示词:
<English prompt>

- 想继续改同一块: 回"继续改 M9"
- 想改另一块: 回"改 M8 构图画幅"
- 想看看还有哪些可调方向: 回"探索更多维度"
- 想退回上一步: 回"返回"
已探索: <N>/10
若已满 10 轮、已经出过图、或用户已明确要求生成，下一步：回复「开始生成图片」即可出图；否则继续「再探索」看方向。
```

If the user says `开始生成图片`, send the pre-generation note before calling the
image tool: mention the current version briefly, then say that after the image
they can name any unsatisfying part and the next revision will continue through
the matching module.

When talking to a Chinese-speaking user, show module names, edit instructions, and next actions in Chinese. Keep the compiled generation prompt in English.

## Principle

Separate decision state from final prompt prose.

The final English prompt is compiled from modules. The user should be able to change one module without redoing the whole discovery flow.

## Required Modules

Use these stable labels. For Chinese users, show the Chinese label first and keep the module ID visible.

```text
M1 身份锚点 / Identity
M2 原作基线 / Canon Baseline
M3 用途目标 / Intent and Use Case
M4 改编边界 / Reinterpretation Boundary
M5 情绪方向 / Emotional Direction
M6 角色状态 / Character Agency
M7 画面内容 / Picture Content
M8 构图画幅 / Composition and Crop
M9 光线色彩 / Light and Color
M10 风格质感 / Finish and Style
M11 正向约束 / Constraints
M12 避免项 / Avoid
```

For faithful outputs, `M4` can be `接近原作 / canon-close`.

For AU outputs, `M4` must explicitly state what may change and what must remain recognizable.

## Module Meanings

### M1 身份锚点

Character name, series, and recognition anchors.

Examples:

- hair, eyes, face vibe
- outfit silhouette
- signature prop or accessory
- non-negotiable recognition cues

If an accepted lock or baseline image exists, mention it here only as an
identity reference. It may lock face, hair, eyes, makeup, outfit silhouette,
dominant colors, and signature cues. It must not override `M5`-`M10` unless the
user explicitly asks to reuse its mood, pose, crop, lighting, or finish.
This applies to every final direction, not only "maximize likeness" routes.
Choosing `E` makes the identity gate stricter; it is not required to keep an
already accepted baseline active.

### M2 原作基线

The source visual logic that prevents style drift.

Examples:

- TV anime promotional art baseline
- official game render baseline
- visual novel illustration baseline
- manga-colorized baseline

### M3 用途目标

What the image is for.

Examples:

- poster-key-visual
- wallpaper
- avatar
- character-render
- banner
- mood exploration

### M4 改编边界

How far the image can move from canon.

Examples:

- 接近原作
- 轻度风格化
- 强 AU
- 允许服装重设计
- 场景可变，身份锚点必须固定

### M5 情绪方向

The primary emotional target.

Examples:

- 克制安静
- 忧郁但有希望
- 梦幻象征
- 戏剧化英雄感
- 温暖怀旧

### M6 角色状态

What the character is doing at an abstract level.

Examples:

- 静止观察
- 正在抵达
- 正在离开
- 正在保护
- 正在修复
- 正在穿行
- 正在展示自己

### M7 画面内容

Concrete scene, setting, props, and symbolic motifs.

Keep this module empty or abstract until the user reaches the picture-content phase.

### M8 构图画幅

Framing and visual hierarchy.

Examples:

- close portrait
- half-body
- three-quarter body
- full-body
- wide environment
- vertical poster
- horizontal wallpaper
- square avatar
- panoramic banner

### M9 光线色彩

Lighting and palette.

Examples:

- 黎明金色和浅蓝
- 银灰和冷白
- 深蓝和暗金
- 玫瑰色黄昏
- 纯白和淡金
- 破碎棱镜记忆光

### M10 风格质感

Rendering finish and medium.

Examples:

- polished anime key visual
- soft filmic anime illustration
- premium painted anime poster
- clean character render
- fashion editorial finish

### M11 正向约束

Positive requirements.

Examples:

- preserve recognizability
- preserve canonical outfit cues
- no text
- no watermark
- original composition

### M12 避免项

Likely failure modes to avoid.

Examples:

- face drift
- random costume redesign
- generic fantasy design
- copied frame
- extra fingers
- duplicate limbs
- background clutter

## Output Format

When finalizing for Chinese users, show this shape:

```text
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
<English prompt>

- 想改某一块: 回"改 M9 光线色彩"、"换 M7 画面内容"、"M4 更接近原作"
- 想只在某一块里继续找方向: 回"再探索 M9"、"继续探索 M7"、"M8 多给几个"
- 想看看还有哪些可调方向: 回"探索更多维度"、"还有哪些维度可以调"
- 想退回上一步: 回"返回"
已探索: <N>/10
若已满 10 轮或用户已明确要求生成，下一步：回复「开始生成图片」即可出图；否则继续「再探索」看方向。
```

For English-speaking users, use the English labels from the module list.

## Compilation Rules

Compile modules into the structure from `prompt-recipes.md`.

Mapping:

- `Use case` <- M3
- `Primary request` <- M3 + M4 + M5 + M6 + M7
- `Character` <- M1
- `Identity anchors` <- M1
- `Style/medium` <- M2 + M10 + M4
- `Composition/framing` <- M8
- `Lighting/mood` <- M5 + M9
- `Background/scene` <- M7
- `Constraints` <- M11
- `Avoid` <- M12

If a lock image is present, compile it as identity-only evidence. Add language
such as: "Use the accepted lock image only for identity; do not copy its pose,
crop, lighting, background, rendering finish, body emphasis, or composition."
Keep the final art direction governed by `M5`-`M10`.
If the user changes from poster to wallpaper, avatar, style exploration, or any
other final direction, keep the accepted lock image in the compiled prompt as
identity-only evidence unless the user explicitly rejects that baseline.

## Edit Rules

When the user asks to change a module:

- change only that module and any directly dependent wording in the compiled prompt
- preserve all other modules
- mention which module changed
- do not restart discovery unless the new request conflicts with locked identity or hard constraints
- if the user is Chinese-speaking, confirm the changed module in Chinese and keep the regenerated compiled prompt in English

## Module-Level Exploration

Use this when the user says things like:

- "再探索 M9"
- "探索光线色彩"
- "M7 多给几个"
- "这个模块再看看"
- "只在构图里再探索"

Rules:

- keep all other modules fixed
- if the requested module is broad or rich, first offer a small-module picker
  instead of final alternatives. This applies to any `M1`-`M12` module with
  multiple control surfaces, not only lighting or style.
- small modules are user-selected control surfaces. They are not final prompt
  values until the user chooses an option inside that small module.
- if the user selects multiple small modules, process them as an ordered queue:
  expand the first selected small module, update the module after selection, then
  continue to the next queued small module.
- offer `4-6` alternatives for the requested module by default; use `3` only for
  very narrow fixes
- include one conservative option, one stronger option, and one more surprising option when possible
- do not rewrite the compiled prompt until the user picks a module option or says "你选"
- after the user picks, update only that module and directly dependent compiled-prompt lines

Generic Chinese response shape:

```text
保持其他模块不变，先选要探索的 <Mx 模块名> 小模块:

A. <小模块名>: <它会影响什么，使用用户能理解的话>.
B. <小模块名>: <它会影响什么>.
C. <小模块名>: <它会影响什么>.
D. <小模块名>: <它会影响什么>.
E. <小模块名>: <它会影响什么>.
F. 你来搭配: 我选 2-3 个最适合当前方向的小模块。

推荐: <2-3 个小模块 + short reason>.
怎么选: 回 A-F（也接受 1-6）；可多选如"ADE"；不确定回"推荐"或"你选"；想退一步回"返回"。
接下来: 我会先展开你选的第一个小模块，其他小模块排队。
```

M9 example:

```text
保持其他模块不变，先选要探索的 M9 光线色彩小模块:

A. 人物打光: 脸部、头发、身体轮廓、角色识别度。
B. 背景光: 窗光、霓虹、夕阳、舞台光、城市反射等背景记忆点。
C. 环境光: 雾气、雨夜反光、月光、空气感、整体氛围。
D. 光线颜色: 冷暖、主色、角色原色保护、情绪倾向。
E. 阴影质感: 柔阴影、硬阴影、胶片阴影、赛璐璐阴影。
F. 你来搭配: 我选 2-3 个最适合当前方向的小模块。

推荐: <2-3 个小模块 + short reason>.
怎么选: 回 A-F（也接受 1-6）；可多选如"ADE"；不确定回"推荐"或"你选"；想退一步回"返回"。
接下来: 我会先展开你选的第一个小模块，其他小模块排队。
```

After the user chooses a small module, expand that small module:

```text
保持其他模块不变，只再探索 M9 > 人物打光:

A. <option>: <what changes and what it feels like>
B. <option>: ...
C. <option>: ...
D. <option>: ...
影响: A <small/stable>, B <stronger>, C <more experimental>, D <different but still controlled>.

推荐: <one option + short reason>.
怎么选: 回 A-D（也接受 1-4）；不确定回"推荐"或"你选"；想融合就回"A+C"；都不满意回"继续探索 M9"或"再给几个"；想退一步回"返回"。
接下来: 我只更新 M9 的人物打光；如果还有排队的小模块，下一轮继续展开。
```

If the user says "继续探索 M9", stay within M9 and offer a new set that avoids repeating previous options.

## More-Dimensions Exploration

Use this after a modular prompt spec when the user wants to discover additional controls beyond the currently obvious modules.

Triggers:

- "探索更多维度"
- "还有哪些维度可以调"
- "还能改哪里"
- "给我更多可控项"
- "more dimensions"

Behavior:

- keep the current module values unchanged
- suggest `4-8` additional dimensions that could be explored
- group them by usefulness, not by technical category
- do not rewrite the prompt until the user selects a dimension
- after selection, either map it to an existing module or create a temporary sub-module under the closest module
- if the user selects multiple dimensions at once, such as `A+B+C` or `abcefgh`,
  treat them as an ordered edit queue, not a request to synthesize new combined
  directions
- process that queue exactly in the user's order: start with the first selected
  dimension, offer only that dimension's alternatives, and state the remaining
  queued dimensions in the next-action line
- after the user chooses an alternative for the current queued dimension,
  integrate that module change into the current state, then continue to the
  next queued dimension until the queue is empty
- while the queue is still active, show only the changed module, the selected
  alternative, the remaining queue, and the next dimension's alternatives
- when the queue finishes, or when the user says "可以了", "就这个",
  `开始生成图片`, or asks for the full prompt, show the full current module list
  and full compiled English prompt
- only collapse multiple selected dimensions into one combined direction when
  the user explicitly asks for a combined direction or summary

Chinese response shape:

```text
当前提示词不变。还可以继续探索这些维度:

A. 情绪强度: 更克制 / 更强烈 / 更治愈 / 更孤独
B. 画面密度: 极简 / 适中 / 丰富 / 史诗
C. 符号比例: 更写实 / 更多意象 / 更抽象
D. 角色距离: 脸更近 / 半身 / 全身 / 环境更大
E. 服装自由度: 接近原作 / 轻改 / 完全 AU
F. 镜头语言: 静态 / 行进中 / 俯视 / 仰视 / 电影海报

推荐: <one dimension + short reason>.
怎么选: 回 A-F（也接受 1-6）；不确定回"推荐"或"你选"；可按顺序多选如"ACF"；想退一步回"返回"。
接下来: 我会先展开你选的第一个维度，其他维度排队，不会一次混成一团。
已探索: <N>/10
若已满 10 轮，再追加「开始生成图片」CTA。
```

If the user selects one, continue exploring only that dimension and note which module it affects.
If the user selects several dimensions, do not offer cross-dimension composite
directions. Acknowledge the ordered queue and begin with the first dimension.

Common mappings:

- emotional intensity -> M5
- scene density -> M7 or M8
- symbol ratio -> M7 and M10
- character distance -> M8
- outfit freedom -> M4 and M7
- camera language -> M8
- color temperature -> M9
- canon risk -> M2 and M4
- detail priority -> M1, M7, or M10

## Post-Finalization Interaction Prompt

After every modular prompt spec, always show a short interaction prompt. Offer
module edits and optional exploration without pushing the user back into
exploration after they already approved a direction. Do not assume users know
modules are editable.

For finalization and generation-preflight replies, include this copyable CTA as
the final line only when `exploration_rounds >= 10`, when the user explicitly
chose the direct-prompt path, or when the user has already typed
`开始生成图片`:

```text
下一步：回复「开始生成图片」即可出图；或回复「再探索」继续看方向。
```

Chinese default:

```text
- 想改某一块: 回"改 M9 光线色彩"、"换 M7 画面内容"
- 想只在某一块里继续找方向: 回"再探索 M9"、"继续探索 M6"
- 想看看还有哪些可调方向: 回"探索更多维度"
- 想退回上一步: 回"返回"
已探索: <N>/10
若已满 10 轮或用户已明确要求生成，下一步：回复「开始生成图片」即可出图；否则继续「再探索」看方向。
```

Keep this prompt short. It should appear after the compiled English prompt, not before it.

## Module Exploration Axes

Use module-specific axes so exploration stays relevant. For broad modules, first
show small modules, then expand only the selected small modules. This keeps the
prompt rich without turning one turn into a fixed preset.

### Big Module -> Small Module Picker

Use this pattern when the user asks to explore any broad module from `M1`-`M12`.
Narrow requests may still go directly to alternatives, but the default UX should
show small modules first when a module has multiple meaningful control surfaces:

- show `4-6` small modules with plain Chinese labels
- allow multi-select such as `ADE`
- include `你来搭配` when the user wants a low-effort route
- after selection, expand the first selected small module with creative options
- keep the remaining selected small modules as a queue
- do not add unselected small modules to the final prompt unless needed for
  coherence

Suggested small modules:

`M1 身份锚点`
- 发型发色
- 眼睛和脸部气质
- 服装轮廓
- 标志物或配饰
- 角色气质
- 禁改锚点

`M2 原作基线`
- 来源版本
- 线条逻辑
- 色彩逻辑
- 服装设计语言
- 官方宣传感
- 年代或媒介差异

`M3 用途目标`
- 使用场景
- 平台或画幅需求
- 信息层级
- 角色占比
- 完成度标准
- 输出规格倾向

`M4 改编边界`
- 场景自由度
- 服装自由度
- 风格自由度
- 世界观自由度
- 符号化程度
- 禁止改变项

`M5 情绪方向`
- 情绪强度
- 情绪温度
- 角色心理距离
- 观众感受
- 戏剧张力

`M6 角色状态`
- 表情
- 姿态
- 动作
- 手部/道具关系
- 视线方向

`M7 画面内容`
- 场景类型
- 角色行为
- 叙事瞬间
- 角色符号
- 背景密度
- 道具逻辑

`M8 构图画幅`
- 角色距离
- 镜头角度
- 画幅比例
- 视觉重心
- 前中后景层次
- 留白/标题空间

`M9 光线色彩`
- 人物打光
- 背景光
- 环境光
- 光线颜色
- 阴影质感
- 角色原色保护

`M10 风格质感`
- 线条质感
- 上色方式
- 渲染精度
- 材质细节
- 后期颗粒/胶片感
- 原作贴近度

`M11 正向约束`
- 角色相似度优先
- 脸部清晰度
- 服装准确度
- 构图可读性
- 背景控制
- 手部和解剖稳定

`M12 避免项`
- 角色漂移
- 发型或服装错误
- 过度性感化
- 背景喧宾夺主
- AI 痕迹
- 文字水印和多余肢体

### M4 改编边界

- closer to canon
- lightly AU
- strong AU
- symbolic AU
- setting changes only
- outfit redesign allowed

### M5 情绪方向

- calmer
- more melancholic
- warmer
- more hopeful
- more dramatic
- more mysterious
- more romantic
- more solemn

### M6 角色状态

- still and observing
- arriving
- leaving
- protecting
- repairing
- crossing through
- offering
- carrying

### M7 画面内容

- conservative
- emotionally stronger
- more symbolic
- more cinematic
- more character-focused
- more environment-focused
- more surprising

### M8 构图画幅

- close portrait
- half-body
- three-quarter body
- full-body
- wide environment
- vertical poster
- horizontal wallpaper
- square avatar
- panoramic banner

### M9 光线色彩

- warm dawn
- cold silver
- dark blue and muted gold
- rose dusk
- pure white and pale gold
- prismatic memory fragments
- rainy neon
- winter blue hour

### M10 风格质感

- canon-like anime key visual
- cinematic anime poster
- soft filmic illustration
- premium painted anime
- fashion editorial
- game-promo polish
- symbolic art poster

Examples:

- "change only lighting" -> edit M9 and the `Lighting/mood` line
- "make it closer to canon" -> edit M4 and M10, keep M7 if still compatible
- "different scene" -> edit M7, keep M5/M9/M10
- "more like her" -> edit M1/M2/M4, reduce risky AU language
- "more emotional" -> edit M5 and maybe M6, do not change M7 unless needed

Chinese edit examples:

- "只改光色" -> edit M9
- "画面换一个" -> edit M7
- "更像原作" -> edit M4 and maybe M10
- "更像她" -> edit M1/M2/M4
- "情绪更强" -> edit M5 and maybe M6
- "不要翅膀" -> edit M7 and M12
- "保留其他，只换构图" -> edit M8 only

## Auto-Integration After Decisions

Use this when the user asks the agent to decide unresolved modules, says "你来确定", picks a module option, or otherwise delegates a final choice.

Rules:

- update the affected module values immediately
- remove "未最终锁定" from modules the agent has decided
- if the user is still exploring, reply in exploration state: include a short
  `已整合` note, the changed module(s), the changed compiled-prompt line(s),
  and the next actions
- if the user asks for the full prompt, says "可以了", "就这个", "生成",
  `开始生成图片`, or the queued edits are complete, reply in finalization state:
  re-render the full `提示词模块` list, recompile the full `英文生成提示词`, and
  include the post-finalization interaction prompt after the compiled prompt

Chinese response shape:

```text
已整合这次选择。

变更模块:
M9 光线色彩: ...

英文提示词中对应更新:
Lighting/mood: ...

怎么选: 回"继续探索 M9"看同一模块新方向，回"探索更多维度"换到别的可调项，或回"可以了"定稿。
接下来: 我会继续在当前模块/维度里推进，不会重写整套方向。
已探索: <N>/10
若已满 10 轮，再追加「开始生成图片」CTA。
```

Finalization response shape:

```text
已整合这次选择，当前完整版本如下。

最终确认卡:
角色: <character + source + version>
画面: <one-sentence visible image summary>
风格: <emotion + lighting + finish summary>
风险控制: <identity/canon/avoid safeguards>

提示词模块:
M1 身份锚点: ...
...
M12 避免项: ...

英文生成提示词:
<English prompt>

- 想改某一块: 回"改 M9 光线色彩"、"换 M7 画面内容"
- 想只在某一块里继续找方向: 回"再探索 M9"、"继续探索 M6"
- 想看看还有哪些可调方向: 回"探索更多维度"
- 想退回上一步: 回"返回"
已探索: <N>/10
若已满 10 轮或用户已明确要求生成，下一步：回复「开始生成图片」即可出图；否则继续「再探索」看方向。
```

Examples:

- user says "你来确定剩下未锁定的模块" -> decide unresolved modules, then output full integrated modules and prompt
- user picks "M9 A" while exploring -> update M9 and reply in lightweight exploration state unless they asked for the full prompt
- user says "可以了" after active exploration -> lock current branch, then output full integrated modules and compiled prompt; include the copyable `开始生成图片` CTA only after `exploration_rounds >= 10` or an explicit direct-generation request

## Versioning

If the user compares versions, label them:

```text
Version A
Version B
```

Keep module diffs compact:

```text
已修改:
M9 光线色彩: 从明金蓝 -> 银灰冷白
M6 角色状态: 正在抵达 -> 正在保护
```
