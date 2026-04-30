# Anime Fanart Imagegen

Portable Codex skill for anime fanart prompt discovery and `gpt-image-2` generation.

面向 Codex 的动漫角色生图 skill，用于提示词探索和 `gpt-image-2` 生成。

The skill is designed for the common case where a user knows the character, but cannot describe the exact image or write a strong prompt. It guides the user through lightweight choices, keeps character identity stable, produces a modular prompt spec, and compiles the final English prompt for image generation.

这个 skill 面向一种很常见的情况：用户知道想画哪个角色，但说不清具体画面，也写不出高质量提示词。它会通过低成本选择引导用户探索方向，保持角色识别度，输出模块化提示词，并最终编译成可用于生图的英文 prompt。

## What It Solves / 解决的问题

Most image generation failures here are workflow problems, not only model problems.

这类生图失败很多时候不是模型能力问题，而是用户流程问题。

- The user only gives a character name.
- 用户只给了一个角色名。
- The user cannot describe the final image clearly.
- 用户说不清最终想要什么画面。
- The first set of options is too narrow.
- 第一轮可选方向太窄。
- Exploration stops too early.
- 探索过程停止得太早。
- The final prompt is hard to revise.
- 最终提示词不好局部修改。
- Changing one detail forces the whole prompt to be rewritten.
- 改一个细节就要重写整段提示词。

This skill turns that into a guided flow.

这个 skill 把这些问题转成一个可持续推进的引导流程。

- Start from a character name or rough idea.
- 从角色名或模糊想法开始。
- Infer the source, version, and identity anchors.
- 推断角色来源、版本和身份锚点。
- Put exploration first, so users can choose directions instead of writing prompts.
- 把探索放在第一位，让用户先选方向，而不是自己写 prompt。
- Keep the default exploration path going for at least 10 rounds before proactively suggesting image generation.
- 默认探索路径至少推进 10 轮后，才主动提示用户可以开始生成图片。
- Allow option mixing such as `A+C`, `AF`, or `B but closer to F`.
- 支持 `A+C`、`AF`、`B 但更像 F` 这类混合选择。
- Keep exploring inside the current branch until the user approves.
- 在当前选择分支下继续探索，直到用户确认。
- Finalize as editable modules before generation.
- 生成前先整理成可编辑模块。
- Allow module-level changes and module-level exploration later.
- 后续可以只改某个模块，或只在某个模块里继续探索。

## Core Workflow / 核心流程

1. Identify the character and source.
2. Gather or use official-priority references.
3. Extract identity anchors: hair, eyes, outfit silhouette, colors, accessories, and source visual baseline.
4. Put exploration first with low-friction direction choices when the request is vague.
5. Explore progressively for at least 10 default-path rounds before proactively offering generation.
6. Explore mood, style, crop, and picture content without changing identity anchors.
7. For real existing-character outputs, create or reuse an accepted identity-lock baseline before final generation.
8. After the baseline is accepted, resume guided prompt selection for the final image; the baseline is identity-only evidence, not the final art direction.
   A single post-lock direction choice only locks `L2` and advances to `L3`; it must not skip directly to the final prompt.
   Broad modules should expose small-module pickers first: `L3/M7`, `L4/M8`, `L5/M9`, and `L6/M10`.
9. Produce a modular prompt spec.
10. Compile the final English `gpt-image-2` prompt.
11. Generate only after the user says `开始生成图片`. Default to the built-in `image_gen` path; use the optional script/API workflows only when local file inputs, fixed profiles, repeatable payloads, or stricter local-reference control are explicitly needed.

中文流程：

1. 识别角色和来源作品。
2. 收集或使用官方优先的参考图。
3. 提取身份锚点：发型、眼睛、服装轮廓、颜色、配饰和原作视觉基线。
4. 当用户表达模糊时，把探索放在第一位，用低摩擦方向卡引导。
5. 默认探索路径至少推进 10 轮后，才主动提示用户可以生成图片。
6. 在不改变身份锚点的前提下探索情绪、风格、画幅和画面内容。
7. 真实现有角色出图前，先创建或复用一个已接受的身份锁定基准图。
8. 基准图通过后，继续引导用户选择最终成图提示词；基准图只锁身份，不决定最终画面方向。
   用户选中一个基准图后的方向卡时，只锁定 L2 方向感，然后进入 L3，不能直接跳到最终提示词。
   进入大模块时先给小模块选择器：`L3/M7`、`L4/M8`、`L5/M9`、`L6/M10`。
9. 输出模块化提示词。
10. 编译最终英文 `gpt-image-2` prompt。
11. 用户说出 `开始生成图片` 后，才可以直接生成或使用锁脸优先的脚本流程获得更稳定的角色相似度。

Complete dogfood tests for existing characters must include the lock pass. A
final poster generated without an accepted lock image is only a prompt-quality
demo, not a valid identity-preservation test.

## Installation / 安装

Install as a Codex skill.

安装为 Codex skill。

Windows PowerShell:

```powershell
git clone <repo-url> "$env:USERPROFILE\.codex\skills\anime-fanart-imagegen"
```

macOS or Linux:

```bash
git clone <repo-url> ~/.codex/skills/anime-fanart-imagegen
```

Restart Codex after installation.

安装后重启 Codex。

## Out-of-the-box Tutorial / 开箱即用教程

Use this after installation. It is a first-run smoke test for the guided workflow, not a replacement for the reference sections below.

完成安装后使用这一段。它是第一次运行的冒烟测试，不替代后面的交互模型和模块说明。

No local reference images or `OPENAI_API_KEY` are required for this guided prompt test.

这个引导式 prompt 测试不需要本地参考图，也不需要 `OPENAI_API_KEY`。

### Copy-paste flow / 复制流程

Send these messages in Codex one by one.

在 Codex 里逐条发送：

```text
$anime-fanart-imagegen Asuka
```

```text
AF
```

```text
再探索
```

```text
A+C
```

```text
可以了
```

```text
开始生成图片
```

Expected checkpoints:

预期检查点：

- After the character name, the skill should show a compact intent router instead of asking for a full prompt.
- 输入角色名后，skill 应该给出简洁意图路由，而不是要求用户写完整 prompt。
- After `AF`, it should explore direction and style together.
- 输入 `AF` 后，它应该同时探索方向和风格。
- After `再探索`, it should stay in the current branch and offer new alternatives.
- 输入 `再探索` 后，它应该留在当前分支下给出新方向。
- After `可以了`, it should output editable modules plus a compiled English prompt.
- 输入 `可以了` 后，它应该输出可编辑模块和编译好的英文 prompt。

## Interaction Model / 交互模型

If a user directly asks to generate a poster, cover, wallpaper, or key visual,
the skill first offers exploration: four concrete directions to choose from,
with direct prompt preparation as the secondary path.

如果用户直接要求生成海报、封面、壁纸或 key visual，skill 会先询问是否先给 4 个方向让用户选择，
并把“直接给一版可生成提示词”作为次级路径。

```text
我理解你要做 <角色/作品 + 海报方向>。
你想 A. 先给我 4 个方向让我选（推荐），还是 B. 直接给我一版可生成提示词？
```

If the user chooses A, the four cards should be clearly different and written
as user-facing creative choices, not internal axis labels:

- `A 保守原作向`: safest canon-close result
- `B 情绪电影向`: stronger mood and cinematic framing
- `C 角色符号向`: stronger source-specific motif and identity hook
- `D 风格探索向`: more stylized but still identity-safe

Each card should include a short `画面感`, `差异点`, `角色钩子`, and `适合`
line. The cards should differ on purpose, emotion, crop, style strength, or
character distance, and include one character-specific hook from the source.

During exploration, responses should stay lightweight: current branch, changed
dimension, a few choices, and the next action. Full `M1`-`M12` modules and the
compiled English prompt appear when the user is ready to finalize, asks for the
full prompt, or says `开始生成图片`.

Choice guidance should be explicit and repeatable: show lettered options (`A`,
`B`, `C`), accept numeric aliases silently, and end exploration blocks with
`怎么选`, `接下来`, and `已探索`. This keeps each round easy to answer without
making the user understand modules, layers, or prompt terms.

Every exploration choice set should also include one visible `推荐` option and
short `风险` or `影响` notes. The recommendation gives users a low-effort default;
the risk label tells them whether an option is safer for likeness, stronger in
mood, or more likely to drift.

Default exploration should not collapse into repeated three-choice menus. Normal
rounds should offer `4-5` real creative options, and when the user says
`再给几个`, `换一组`, or `都不满意`, the skill should stay on the same layer and
provide `5-6` new alternatives.

Every major prompt module can expose small modules first. For example, `M1 身份锚点`
can split into hair, eyes/face, outfit silhouette, signature accessories, and
non-negotiable anchors; `M9 光线色彩` can split into `人物打光`, `背景光`,
`环境光`, `光线颜色`, `阴影质感`, and `角色原色保护`. The user can select multiple
small modules, and the skill expands them one at a time instead of forcing a
fixed preset.

For vague/default-path requests, track `已探索: N/10`. Do not proactively show the
copyable `开始生成图片` CTA until round 10. Users can still explicitly choose the
direct prompt path or type `开始生成图片`; the 10-round rule only prevents the skill
from pushing generation too early.

Hard limit: no image-generation tool is called until the user says the exact phrase `开始生成图片`.

硬限制：只有用户说出精确口令 `开始生成图片` 后，才可以调用生图工具。

For vague requests, the skill starts with broad intent instead of technical controls.

面对模糊请求时，skill 会先让用户探索方向，而不是直接暴露复杂参数或要求用户写 prompt。

```text
A. Explore directions / 探索方向（推荐，不用写 prompt）
B. Finished image / 成品图
C. Wallpaper or cover / 壁纸或封面
D. Avatar or portrait / 头像或肖像
E. Maximize likeness / 最大化角色相似度
F. Change style / 改变风格
G. Let the agent decide / 让 agent 决定
```

Users can reply with one option or mix options.

用户可以选择一个选项，也可以混合选择。

```text
A
AF
A+C
B but closer to F
B 但更像 F
```

If the user asks to explore more, the skill stays inside the current branch and offers new alternatives. On the default path, it should avoid pushing final generation until the exploration counter reaches 10. It should generate only after `开始生成图片`.

如果用户要求“再探索”，skill 会留在当前分支下给出新的替代方向。默认路径未满 10 轮时，不主动催用户生成；只有说出 `开始生成图片` 后才生成图片。

## Modular Prompt Spec / 模块化提示词

After exploration, the skill outputs a short confirmation card, a module list, and
the compiled English prompt.

探索结束后，skill 会输出一张中文确认卡、模块列表和编译后的英文提示词。

The confirmation card is only a quick summary. It is not the editable prompt
state. Any change to the card must be mapped back into `M1`-`M12` before the
English prompt is updated.

确认卡只用于快速确认，不是可编辑提示词状态。用户要求修改确认卡内容时，必须先映射回
`M1`-`M12` 模块，再更新英文 prompt。

```text
M1 Identity / 身份锚点
M2 Canon baseline / 原作基线
M3 Intent and use case / 用途目标
M4 Reinterpretation boundary / 改编边界
M5 Emotional direction / 情绪方向
M6 Character agency / 角色状态
M7 Picture content / 画面内容
M8 Composition and crop / 构图画幅
M9 Light and color / 光线色彩
M10 Finish and style / 风格质感
M11 Positive constraints / 正向约束
M12 Avoid / 避免项
```

This lets the user change a small part later.

这样用户后续可以只修改少量模块，而不用重写整段提示词。

Example edits:

修改示例：

```text
change only M9 light and color
只改 M9 光线色彩

explore M7 again
再探索 M7

keep everything else, change M8 composition
保持其他不变，换 M8 构图

explore more dimensions
探索更多维度
```

For Chinese-speaking users, the skill should present module labels and next actions in Chinese, while keeping the generation prompt in English.

面对中文用户时，模块名和下一步操作应该用中文展示，但最终生图 prompt 保持英文。

## Optional Local Script Workflow / 可选本地脚本流程

By default, use the built-in chat `image_gen` flow for image generation. Use the Python CLI only when you need local reference files to be sent as real image inputs, repeatable outputs, fixed profiles, metadata sidecars, or a lock-first API workflow.

默认使用 Codex 内置的 `image_gen` 出图。只有在需要把本地参考图作为真实图像输入、需要可复现输出、固定尺寸配置、JSON 元数据，或锁脸优先的 API 流程时，才使用 Python CLI。

Install dependencies:

安装依赖：

```bash
pip install -r requirements.txt
```

Set your API key only for the optional local script/API workflow:

仅在使用可选本地脚本/API 流程时设置 API key：

```bash
export OPENAI_API_KEY="..."
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "..."
```

Create a character lock image.

创建角色锁定图：

```bash
python scripts/anime_fanart.py lock \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --image refs/asuka/face.png \
  --image refs/asuka/fullbody.png \
  --out output/asuka-lock.png
```

Generate the final image.

生成最终图：

```bash
python scripts/anime_fanart.py generate \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/asuka-lock.png \
  --image refs/asuka/fullbody.png \
  --profile poster-safe \
  --prompt "<compiled English image-2 prompt>" \
  --out output/asuka-poster.png
```

Use `--dry-run` to inspect the request payload without calling the API.

使用 `--dry-run` 可以只检查请求内容，不实际调用 API。

Generate from an accepted local baseline/lock image.

Use this when a Codex-generated baseline image already looks close enough and
you want the next image call to really read that file, not only a text summary
of it. The lock image is always sent as image input #1. Extra `--image` values
are sent after it.

The baseline is identity-only evidence: face, hair, eyes, outfit silhouette,
color hierarchy, and signature cues. The final prompt should still control the
pose, crop, camera angle, scene, lighting, mood, background, and finish.

```bash
python scripts/generate_from_lock.py \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/rei-lock-accepted.png \
  --profile poster-safe \
  --prompt-file output/rei-final-prompt.txt \
  --out output/rei-final-from-lock.png
```

PowerShell dry-run example for a baseline saved by Codex:

```powershell
python scripts\generate_from_lock.py `
  --character "Rei Ayanami" `
  --series "Neon Genesis Evangelion" `
  --lock-image "C:\Users\Lsq\.codex\generated_images\<thread-id>\<image-id>.png" `
  --profile poster-safe `
  --prompt-file output\rei-final-prompt.txt `
  --out output\rei-final-from-lock.png `
  --dry-run
```

In the dry-run JSON, verify that `source_images[0]` and
`dry_run_payload.image[0]` are the accepted lock image path. That confirms the
API request will include the real image file.

If the final result copies the baseline pose or crop too closely, strengthen the
scene/composition lines in the prompt rather than replacing the lock image.

## Output Profiles / 输出配置

- `poster-safe`: `1024x1536` stable vertical poster source / 稳妥竖版主视觉源图
- `scene-safe`: `1536x1024` stable horizontal scene source / 稳妥横版场景源图
- `square-safe`: `1024x1024` stable avatar or square source / 稳妥头像或方图源图
- `banner-safe`: `1536x1024` stable cover source / 稳妥封面源图

The named profiles use API-reference-compatible defaults so the first script
path stays reliable. For explicit 2K or 4K delivery, pass a manual `--size`
that satisfies the current `gpt-image-2` constraints: longest edge `<= 3840`,
both edges multiples of `16`, aspect ratio `<= 3:1`, and total pixels between
`655,360` and `8,294,400`. Outputs above `2560x1440` total pixels are treated
as experimental. Legacy names such as `poster-2k` still work as compatibility
aliases, but the script warns and maps them to the matching `*-safe` profile.

命名 profile 使用兼容 API Reference 的稳妥默认尺寸，避免默认脚本路径先失败。
如果用户明确要求 2K 或 4K，使用手动 `--size`，并满足当前 `gpt-image-2`
约束：最长边 `<= 3840`、两边都是 `16` 的倍数、长短边比例 `<= 3:1`，
且总像素在 `655,360` 到 `8,294,400` 之间。超过 `2560x1440` 总像素的输出
按实验性大尺寸处理。`poster-2k` 等旧名称仍作为兼容别名可用，但脚本会提示
它们已映射到对应的 `*-safe` profile。

## Repository Structure / 仓库结构

```text
anime-fanart-imagegen/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

- `SKILL.md`: primary behavior contract for Codex / Codex 的核心行为契约
- `agents/openai.yaml`: UI metadata and default prompt / UI 元数据和默认提示
- `references/frictionless-ux.md`: low-friction intake and intent routing / 低摩擦输入和意图路由
- `references/discovery-loop.md`: multi-turn exploration, option mixing, and branch-local exploration / 多轮探索、选项混合和当前分支内再探索
- `references/prompt-modules.md`: modular prompt format and module-level edits / 模块化提示词和单模块修改
- `references/style-matrix.md`: style axes and user-language translation / 风格轴和用户语言映射
- `references/prompt-recipes.md`: English prompt templates / 英文提示词模板
- `references/reference-sourcing.md`: official-priority reference sourcing / 官方优先参考图检索规则
- `references/quality-standards.md`: profiles and resolution guardrails / 输出配置和分辨率约束
- `references/recovery.md`: recovery rules for identity or quality drift / 角色或质量漂移时的修复规则
- `references/qa-checklist.md`: acceptance checks before final delivery / 最终交付前检查清单
- `scripts/anime_fanart.py`: lock and generation workflow / 锁脸和生成脚本
- `scripts/image_gen_refs.py`: lightweight local-reference wrapper / 轻量本地参考图 wrapper
- `scripts/generate_from_lock.py`: convenience wrapper that sends an accepted lock image as image input #1 / 将已接受基准图作为第一个真实图像输入的便捷脚本

## Distribution / 分发

This repository is meant to be portable. To vendor it into another repository, copy the whole folder and keep the directory structure intact.

这个仓库设计为可迁移。复制到其他仓库时，保留整个目录和内部结构即可。

Keep the folder name `anime-fanart-imagegen` when possible so skill references remain predictable.

建议尽量保留目录名 `anime-fanart-imagegen`，这样 skill 引用更稳定。
