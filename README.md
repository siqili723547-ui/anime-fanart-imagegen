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
- Route the user by intent instead of technical prompt terms.
- 用用户意图做路由，而不是要求用户理解提示词术语。
- Allow option mixing such as `A+C`, `DF`, or `B but closer to F`.
- 支持 `A+C`、`DF`、`B 但更像 F` 这类混合选择。
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
4. Guide the user with low-friction choices when the request is vague.
5. Explore mood, style, crop, and picture content without changing identity anchors.
6. Produce a modular prompt spec.
7. Compile the final English `gpt-image-2` prompt.
8. Generate directly, or run the lock-first script workflow for stricter likeness.

中文流程：

1. 识别角色和来源作品。
2. 收集或使用官方优先的参考图。
3. 提取身份锚点：发型、眼睛、服装轮廓、颜色、配饰和原作视觉基线。
4. 当用户表达模糊时，用低摩擦选项引导。
5. 在不改变身份锚点的前提下探索情绪、风格、画幅和画面内容。
6. 输出模块化提示词。
7. 编译最终英文 `gpt-image-2` prompt。
8. 直接生成，或使用锁脸优先的脚本流程获得更稳定的角色相似度。

## Quick Start / 快速开始

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

Use the skill.

使用方式：

```text
$anime-fanart-imagegen Asuka
```

The skill should not ask for a complete prompt. It should infer what it can, show a compact intent router, recommend a path, and provide a ready English prompt or continue exploration.

skill 不应该要求用户先写完整 prompt。它应该先推断可推断的信息，给出紧凑的意图路由，推荐一个方向，并提供可用英文 prompt 或继续探索。

## Interaction Model / 交互模型

For vague requests, the skill starts with broad intent instead of technical controls.

面对模糊请求时，skill 会先询问用户目标，而不是直接暴露复杂参数。

```text
A. Finished image / 成品图
B. Wallpaper or cover / 壁纸或封面
C. Avatar or portrait / 头像或肖像
D. Explore vibe / 探索氛围
E. Maximize likeness / 最大化角色相似度
F. Change style / 改变风格
G. Let the agent decide / 让 agent 决定
```

Users can reply with one option or mix options.

用户可以选择一个选项，也可以混合选择。

```text
D
DF
A+C
B but closer to F
B 但更像 F
```

If the user asks to explore more, the skill stays inside the current branch and offers new alternatives. It should stop only when the user says the direction is ready or asks to generate.

如果用户要求“再探索”，skill 会留在当前分支下给出新的替代方向。只有当用户明确说“可以了”“生成”或等价表达时，探索才停止。

## Modular Prompt Spec / 模块化提示词

After exploration, the skill outputs a module list plus the compiled English prompt.

探索结束后，skill 会输出模块列表和编译后的英文提示词。

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

## Local Script Workflow / 本地脚本流程

Use the Python CLI when you need repeatable outputs, fixed profiles, metadata sidecars, or a lock-first API workflow.

如果需要可复现输出、固定尺寸配置、JSON 元数据，或锁脸优先的 API 流程，可以使用 Python CLI。

Install dependencies:

安装依赖：

```bash
pip install -r requirements.txt
```

Set your API key:

设置 API key：

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
  --profile poster-2k \
  --prompt "<compiled English image-2 prompt>" \
  --out output/asuka-poster.png
```

Use `--dry-run` to inspect the request payload without calling the API.

使用 `--dry-run` 可以只检查请求内容，不实际调用 API。

## Output Profiles / 输出配置

- `poster-2k`: vertical hero art / 竖版角色主视觉
- `scene-2k`: horizontal scene or wallpaper / 横版场景或壁纸
- `square-2k`: avatar, social image, or square crop / 头像、社交图或方图
- `banner-2k`: wide cover or header image / 宽幅封面或头图

4K profiles are available, but should be treated as opt-in final delivery profiles.

4K 配置可用，但建议只在最终交付阶段明确启用。

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

## Distribution / 分发

This repository is meant to be portable. To vendor it into another repository, copy the whole folder and keep the directory structure intact.

这个仓库设计为可迁移。复制到其他仓库时，保留整个目录和内部结构即可。

Keep the folder name `anime-fanart-imagegen` when possible so skill references remain predictable.

建议尽量保留目录名 `anime-fanart-imagegen`，这样 skill 引用更稳定。

## Notes / 注意事项

- Preserve identity anchors instead of copying a reference composition.
- 保留角色身份锚点，而不是复制参考图构图。
- Do not promise exact reproduction of copyrighted frames or layouts.
- 不承诺精确复刻受版权保护的画面、分镜或版式。
- Treat user-provided references as the highest-priority version definition.
- 用户提供的参考图优先级最高，应作为角色版本定义。
- Do not commit `OPENAI_API_KEY` or generated metadata containing secrets.
- 不要提交 `OPENAI_API_KEY`，也不要提交包含密钥的生成元数据。
