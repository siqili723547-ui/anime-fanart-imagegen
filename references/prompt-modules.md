# Prompt Modules

Use this file when finalizing a prompt after exploration or when the user wants to change only part of an existing direction.

When talking to a Chinese-speaking user, show module names and edit instructions in Chinese. Keep the compiled generation prompt in English.

## Principle

Separate decision state from the final prose prompt.

The final English prompt is compiled from modules. The user should be able to change one module without redoing the whole discovery flow.

## Required Modules

Use these stable labels internally. For Chinese users, show the Chinese display names.

```text
M1 Identity / 身份锚点
M2 Canon Baseline / 原作基线
M3 Intent / Use Case / 用途目标
M4 Reinterpretation Boundary / 改编边界
M5 Emotional Direction / 情绪方向
M6 Character Agency / 角色状态
M7 Picture Content / 画面内容
M8 Composition / Crop / 构图画幅
M9 Light / Color / 光线色彩
M10 Finish / Style / 风格质感
M11 Constraints / 正向约束
M12 Avoid / 避免项
```

For faithful outputs, `M4 Reinterpretation Boundary` can be `canon-close`.

For AU outputs, `M4` must explicitly state what may change and what must remain recognizable.

## Module Meanings

### M1 Identity

Character name, series, and identity anchors.

Examples:

- hair, eyes, face vibe
- outfit silhouette
- signature prop or accessory
- non-negotiable recognition cues

### M2 Canon Baseline

The source visual logic that prevents style drift.

Examples:

- TV anime promotional art baseline
- official game render baseline
- visual novel illustration baseline
- manga-colorized baseline

### M3 Intent / Use Case

What the image is for.

Examples:

- poster-key-visual
- wallpaper
- avatar
- character-render
- banner
- mood exploration

### M4 Reinterpretation Boundary

How far the image can move from canon.

Examples:

- canon-close
- lightly stylized
- strong AU
- outfit redesign allowed
- setting can change, identity anchors must stay fixed

### M5 Emotional Direction

The primary emotional target.

Examples:

- quiet and restrained
- melancholic but hopeful
- dreamlike and symbolic
- dramatic and heroic
- warm and nostalgic

### M6 Character Agency

What the character is doing at an abstract level.

Examples:

- still and observing
- arriving
- leaving
- protecting
- repairing
- crossing through
- presenting herself

### M7 Picture Content

Concrete scene, setting, props, and symbolic motifs.

This module should stay empty or abstract until the user has reached the picture-content phase.

### M8 Composition / Crop

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

### M9 Light / Color

Lighting and palette.

Examples:

- dawn gold and pale blue
- silver-gray and cold white
- dark blue with muted gold
- rose dusk
- white and pale gold
- broken prismatic memory fragments

### M10 Finish / Style

Rendering finish and medium.

Examples:

- polished anime key visual
- soft filmic anime illustration
- premium painted anime poster
- clean character render
- fashion editorial finish

### M11 Constraints

Positive requirements.

Examples:

- preserve recognizability
- preserve canonical outfit cues
- no text
- no watermark
- original composition

### M12 Avoid

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

When finalizing for Chinese users, show this:

```text
提示词模块：
M1 身份锚点：...
M2 原作基线：...
M3 用途目标：...
M4 改编边界：...
M5 情绪方向：...
M6 角色状态：...
M7 画面内容：...
M8 构图画幅：...
M9 光线色彩：...
M10 风格质感：...
M11 正向约束：...
M12 避免项：...

英文生成提示词：
<English prompt>

下一步你可以：
- 生成：直接使用当前英文提示词
- 改模块：例如「改 M9 光线色彩」「换 M7 画面内容」「M4 更接近原作」
- 再探索某模块：例如「再探索 M9」「继续探索 M7」「M8 多给几个」
- 探索更多维度：例如「探索更多维度」「还有哪些维度可以调」
- 返回：回到上一层选择
```

For English-speaking users, use the English labels from the required module list.

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
- offer `3-6` alternatives only for the requested module
- include one conservative option, one stronger option, and one more surprising option when possible
- do not rewrite the compiled prompt until the user picks a module option or says "你选"
- after the user picks, update only that module and directly dependent compiled-prompt lines

Chinese response shape:

```text
保持其他模块不变，只再探索 M9 光线色彩：

A. <option>: <what changes and what it feels like>
B. <option>: ...
C. <option>: ...

下一步：回 A-C，也可以混合如「A+C」「A 但更像 C」，或说「继续探索 M9」「返回」「可以了」。
```

If the user says "继续探索 M9", stay within M9 and offer a new set that avoids repeating the previous options.

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

Chinese response shape:

```text
当前提示词不变。还可以继续探索这些维度：

A. 情绪强度：更克制 / 更强烈 / 更治愈 / 更孤独
B. 画面密度：极简 / 适中 / 丰富 / 史诗
C. 符号比例：更写实 / 更多意象 / 更抽象
D. 角色距离：脸更近 / 半身 / 全身 / 环境更大
E. 服装自由度：接近原作 / 轻改 / 完全 AU
F. 镜头语言：静态 / 行进中 / 俯视 / 仰视 / 电影海报

下一步：回 A-F，也可以混合如「A+C」「A 但更像 C」，或说「再探索 M9」「生成」「返回」。
```

If the user selects one, continue exploring only that dimension and note which module it affects.

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

After every modular prompt spec, always show a short interaction prompt. Do not assume users know modules are editable.

Chinese default:

```text
你现在可以继续精修，不需要重写整段提示词：
- 想直接出图：回「生成」
- 想改某一块：回「改 M9 光线色彩」「换 M7 画面内容」
- 想只在某一块里继续找方向：回「再探索 M9」「继续探索 M6」
- 想混合两个选项：回「A+C」「A 但更像 C」
- 想看看还有哪些可调方向：回「探索更多维度」
- 想退回上一步：回「返回」
```

Keep this prompt short. It should appear after the compiled English prompt, not before it.

## Module Exploration Axes

Use module-specific axes so exploration stays relevant.

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
- re-render the full `提示词模块` list
- recompile the full `英文生成提示词`
- include a short `已整合` note before the modules
- include the post-finalization interaction prompt after the compiled prompt

Do not answer with only the changed module. The user needs the integrated current version.

Chinese response shape:

```text
已整合这次选择，当前版本如下。

提示词模块：
M1 身份锚点：...
...
M12 避免项：...

英文生成提示词：
<English prompt>

你现在可以继续精修，不需要重写整段提示词：
- 想直接出图：回「生成」
- 想改某一块：回「改 M9 光线色彩」「换 M7 画面内容」
- 想只在某一块里继续找方向：回「再探索 M9」「继续探索 M6」
- 想看看还有哪些可调方向：回「探索更多维度」
- 想退回上一步：回「返回」
```

Examples:

- user says "你来确定剩下未锁定的模块" -> decide unresolved modules, then output full integrated modules and prompt
- user picks "M9 A" -> update M9, then output full integrated modules and prompt
- user says "可以了" after active exploration -> lock current branch, then output full integrated modules and prompt

## Versioning

If the user compares versions, label them:

```text
Version A
Version B
```

Keep module diffs compact:

```text
已修改：
M9 光线色彩：黎明金蓝 -> 银灰冷白
M6 角色状态：正在抵达 -> 正在保护
```
