# Anime Fanart Imagegen Skill / 动漫同人图像生成 Skill

English: A portable Codex skill for turning rough anime fanart ideas into an identity-aware, editable image-generation workflow.

中文：这是一个可移植的 Codex Skill，用来把模糊的动漫同人图想法转成可探索、可锁定角色识别度、可模块化编辑的图像生成流程。

## What It Does / 功能定位

English:

- Guides the user through multi-turn direction exploration before generation.
- Keeps known characters recognizable by separating identity anchors from scene choices.
- Uses modular prompt fields (`M1`-`M12`) so users can revise one part without rewriting the whole prompt.
- Requires explicit generation confirmation before calling image generation.
- Supports two execution paths: Codex built-in `image_gen` by default, and local Python scripts for stricter local-reference workflows.

中文：

- 在生成图片前先引导用户多轮探索方向、情绪、构图和风格。
- 把角色身份锚点和场景创意分开，降低角色漂移。
- 使用 `M1`-`M12` 模块化提示词，方便只改某一部分。
- 只有用户明确说出生成口令后才生成图片。
- 默认使用 Codex 内置 `image_gen`；需要本地参考图、可复现 payload、锁脸图流程时再使用 Python 脚本。

## Core Rule / 核心规则

English: Do not call any image-generation tool until the user says exactly:

中文：在用户没有明确说出下面这句话之前，不调用任何图像生成工具：

```text
开始生成图片
```

English: Before that phrase appears, the skill should help the user explore options, refine direction cards, and finalize the `M1`-`M12` prompt modules.

中文：在这句话出现之前，Skill 应该帮助用户探索方向卡、细化选择，并确认 `M1`-`M12` 模块化提示词。

## Install / 安装

Preferred install / 推荐安装：

```bash
npx skills add https://github.com/siqili723547-ui/anime-fanart-imagegen -g
```

Manual install on macOS/Linux / macOS 或 Linux 手动安装：

```bash
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen ~/.codex/skills/anime-fanart-imagegen
```

Manual install on Windows PowerShell / Windows PowerShell 手动安装：

```powershell
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen "$env:USERPROFILE\.codex\skills\anime-fanart-imagegen"
```

English: Restart Codex after installation. If `npx skills find anime-fanart-imagegen` cannot find this skill, use direct GitHub URL installation. `skills find` depends on the public skill index, and this repository may be usable before it appears there.

中文：安装后请重启 Codex。如果 `npx skills find anime-fanart-imagegen` 搜不到它，请直接使用 GitHub URL 安装。`skills find` 依赖公开索引，仓库本身可以先通过直链安装使用。

## Quick Start in Codex / Codex 快速开始

English example:

```text
$anime-fanart-imagegen Asuka
AF
more options
A+C
开始生成图片
```

中文示例：

```text
$anime-fanart-imagegen 明日香
AF
再来几个方向
A+C
开始生成图片
```

What should happen / 预期行为：

- English: The skill should first show direction choices instead of asking the user to write a full prompt.
- 中文：Skill 应该先给方向选择，而不是要求用户一开始就写完整提示词。
- English: The user can select options such as `A+C`, `B`, or "closer to F".
- 中文：用户可以输入 `A+C`、`B`、`更接近 F` 这类选择。
- English: The flow can continue for more exploration rounds before generation.
- 中文：在生成前可以继续探索多个分支。
- English: Final generation should happen only after the exact confirmation phrase.
- 中文：最终生成必须等到明确口令出现后才执行。

## Workflow Details / 工作流细节

English:

- Exploration is the default path. The assistant should help users choose a direction before compiling the final prompt.
- The default exploration target is `10` rounds before proactively offering the generation phrase, unless the user explicitly asks to skip exploration.
- Direction cards normally show `4-5` concrete options, and `5-6` options when the user asks for more or wants a different set.
- Users can mix options, such as `A+C`, or ask for a direction to be closer to another option.
- Large modules (`M1`-`M12`) can expose smaller submodules. For broad areas such as scene, composition, lighting, and finish, the assistant should first let the user choose which submodule to refine.
- For real existing-character work, identity-sensitive flows should use an identity lock pass. The accepted lock image constrains identity only; it should not force the final pose, crop, background, lighting, or render style.
- After generation, feedback should map back to the matching module instead of restarting the prompt from scratch.

中文：

- 默认路径是先探索，不急着直接生成。助手应先帮助用户确定方向，再整理最终提示词。
- 默认探索目标是 `10` 轮；除非用户明确要求跳过探索，否则不要过早主动催促生成。
- 方向卡通常给 `4-5` 个具体选项；当用户说“再来几个”或“换一组”时，给 `5-6` 个新方向。
- 用户可以混合选择，例如 `A+C`，也可以说“更接近另一个选项”。
- 大模块 `M1`-`M12` 可以继续拆成小模块。像画面内容、构图、光线、风格质感这类大模块，应先让用户选择要细化的小模块。
- 对真实已有角色，重视相似度时应走 identity lock。已确认的锁脸图只约束身份，不应该限制最终姿势、裁切、背景、光影和渲染风格。
- 生成后的反馈应回到对应模块继续修正，而不是从零重写提示词。

## Repository Layout / 仓库结构

- `SKILL.md`: primary skill contract and runtime behavior / Skill 主说明与运行约束。
- `agents/openai.yaml`: Codex UI metadata and default prompt wiring / Codex UI 元数据与默认提示词入口。
- `references/`: discovery loop, UX rules, prompt modules, quality rules, and recovery guidance / 探索流程、交互规则、提示词模块、质量标准和恢复策略。
- `scripts/anime_fanart.py`: main local CLI for lock, generate, and lock+generate workflows / 本地完整 CLI，支持锁脸、生成、锁脸后生成。
- `scripts/generate_from_lock.py`: convenience CLI for generating from an accepted lock image / 使用已接受锁脸图继续生成的快捷入口。
- `scripts/image_gen_refs.py`: lightweight CLI for image generation from local reference images / 使用本地参考图生成的轻量入口。
- `scripts/test_anime_fanart.py`: minimal regression tests for scripts and workflow assumptions / 脚本与流程假设的最小回归测试。

## Python Environment / Python 环境

English: Python scripts are optional. Use them only when you need local reference images, repeatable API payloads, or strict lock-image control.

中文：Python 脚本是可选高级路径。只有在需要本地参考图、可复现 API payload、严格锁脸图控制时才需要使用。

Use Python 3.11+ / 使用 Python 3.11 或更高版本。

Install dependencies / 安装依赖：

```bash
pip install -r requirements.txt
```

Install the OpenAI SDK if needed / 如有需要安装 OpenAI SDK：

```bash
uv pip install openai
```

Set an API key for local script generation / 为本地脚本设置 API key：

```bash
export OPENAI_API_KEY="..."
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "..."
```

Default model / 默认模型：

```text
gpt-image-2.0
```

English: Override it with `--model` only when your local environment requires a different image model name.

中文：只有当你的本地环境必须使用其他图像模型名时，才通过 `--model` 覆盖。

## CLI Commands / CLI 命令

Create a character lock image / 创建角色锁脸图：

```bash
python scripts/anime_fanart.py lock \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --image refs/asuka/face.png \
  --image refs/asuka/fullbody.png \
  --out output/asuka-lock.png
```

Generate final image from prompt / 根据最终提示词生成图片：

```bash
python scripts/anime_fanart.py generate \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --image refs/asuka/fullbody.png \
  --prompt "<final English prompt>" \
  --out output/asuka-final.png
```

Generate with an accepted lock image / 使用已确认锁脸图生成：

```bash
python scripts/generate_from_lock.py \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/rei-lock-accepted.png \
  --profile poster-safe \
  --prompt-file output/rei-final-prompt.txt \
  --out output/rei-final-from-lock.png
```

General local-reference generation / 使用本地参考图生成：

```bash
python scripts/image_gen_refs.py \
  --image refs/any/style.png \
  --image refs/any/ref2.jpg \
  --prompt "<prompt>" \
  --out output/result.png
```

Chinese content can be passed through argument values or prompt files / 中文内容可以写在参数或 prompt 文件里：

```bash
python scripts/anime_fanart.py generate \
  --character "明日香·兰格雷·惣流" \
  --series "新世纪福音战士" \
  --image refs/asuka/face.png \
  --prompt-file output/zh-final-prompt.txt \
  --out output/zh-asuka-final.png
```

## Dry Run / 试运行

English: All scripts support `--dry-run`. Use it before spending API calls.

中文：所有脚本都支持 `--dry-run`。建议在真正消耗 API 调用前先检查 payload。

```bash
python scripts/generate_from_lock.py \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/rei-lock-accepted.png \
  --prompt-file output/rei-final-prompt.txt \
  --out output/rei-final-from-lock.png \
  --dry-run
```

English: For lock workflows, verify that `source_images[0]` is the accepted lock image.

中文：锁脸图流程里，请确认 `source_images[0]` 是已接受的锁脸图。

## Output Profiles / 输出规格

Default profiles / 默认规格：

- `preview`: `1024x1024`, medium quality.
- `poster-safe`: `1024x1536`, high quality.
- `scene-safe`: `1536x1024`, high quality.
- `square-safe`: `1024x1024`, high quality.
- `banner-safe`: `1536x1024`, high quality.

Legacy aliases / 旧别名：

- `poster-2k` -> `poster-safe`
- `scene-2k` -> `scene-safe`
- `square-2k` -> `square-safe`
- `banner-2k` -> `banner-safe`

English: To request true 2K or 4K output, pass explicit `--size` and keep model constraints in mind.

中文：如果需要真正的 2K 或 4K 输出，请显式传入 `--size`，并确保符合模型尺寸约束。

## Size Constraints / 尺寸约束

For `gpt-image-2.0` / 针对 `gpt-image-2.0`：

- Both edges must be multiples of 16 / 宽高都必须是 16 的倍数。
- Longest edge must be `<= 3840` / 最长边必须 `<= 3840`。
- Aspect ratio must be `<= 3:1` / 宽高比必须 `<= 3:1`。
- Total pixels must be in `[655,360, 8,294,400]` / 总像素必须在 `[655,360, 8,294,400]` 范围内。
- Outputs above `2560x1440` are treated as experimental by this repository / 本仓库把高于 `2560x1440` 的输出视为实验路径。

## Tests / 测试

Run the minimal script tests / 运行最小脚本测试：

```bash
python -m unittest scripts.test_anime_fanart
```

Covered behavior / 覆盖内容：

- Default model remains `gpt-image-2.0` / 默认模型保持为 `gpt-image-2.0`。
- `--dry-run` behavior / `--dry-run` 行为。
- Size validation / 尺寸校验。
- Lock image ordering / 锁脸图排序。
- Prompt identity conflict detection / 提示词身份冲突检测。
- Missing `OPENAI_API_KEY` behavior / 缺少 `OPENAI_API_KEY` 时的行为。

## Metadata and Outputs / 元数据与输出

English: Each successful local generation writes the image file and a sidecar JSON metadata file.

中文：每次本地脚本成功生成后，会写入图片文件和一个旁路 JSON 元数据文件。

Ignored local folders / 已忽略的本地目录：

- `refs/`: local reference packs / 本地参考图包。
- `output/`: generated results / 生成结果。
- `generated_images/`: generated images / 生成图片。
- `__pycache__/`: Python cache files / Python 缓存文件。

## Distribution / 分发

English: Keep this directory structure intact when vendoring or installing the skill.

中文：复制或安装这个 Skill 时，请保持目录结构完整。

```text
anime-fanart-imagegen/
```

English: This preserves skill import paths, reference files, and script compatibility.

中文：这样可以保持 Skill 导入路径、参考文档和脚本路径兼容。
