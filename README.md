# Anime Fanart Imagegen Skill

A portable Codex skill that guides users through **iterative prompt exploration** for
anime-character image generation and keeps identity stable across generations.

The workflow is designed for cases where users know the character they want but
need help turning a rough idea into a strong, editable prompt specification.

## Highlights

- Supports guided, multi-turn exploration before generation.
- Uses references (or generated baselines) as identity anchors.
- Keeps prompts modular (`M1`-`M12`) so users can revise one aspect at a time.
- Generates final output only after the user is ready (or explicitly asks to generate).
- Provides two execution paths:
  - Codex built-in image generation flow (recommended default).
  - Local Python scripts for repeatable payloads, local references, and strict reference-control flows.

## Key Principle

For this skill, image generation should not jump to completion too early.

- Let the user explore direction, mood, and composition first.
- Preserve identity anchors separately from scene/composition decisions.
- Let users edit module-level choices (`M1`-`M12`) before final generation.
- Treat confirmation cards as a summary, not the source of truth. The module state is the source of truth.

## Install

```bash
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen ~/.codex/skills/anime-fanart-imagegen
```

On Windows PowerShell:

```powershell
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen "$env:USERPROFILE\.codex\skills\anime-fanart-imagegen"
```

Restart Codex after installation.

Preferred install (recommended):

```bash
npx skills add https://github.com/siqili723547-ui/anime-fanart-imagegen -g
```

If `npx skills find anime-fanart-imagegen` still cannot find it, use the direct clone command above and restart Codex manually. `skills find` depends on the public skill index; direct GitHub URL installation is the supported path for this repository until that index includes the skill.

## Quick Start (Codex)

After installation, the normal in-chat flow is:

1. Start from character intent (for example `Asuka`).
2. Choose exploration options.
3. Continue branching until the final direction is clear.
4. Confirm modular prompt spec.
5. Generate only when user confirms.

### Basic smoke test in Codex

Send in chat:

```text
$anime-fanart-imagegen Asuka
AF
再来
A+C
开始生成
```

What to check:

- You get a short intent router instead of requiring a full prompt up front.
- You can mix options like `A+C` or `B but closer to F`.
- You can explore further without losing branch context.
- Final output appears only after confirmation phrase.

## Repository Layout

- `SKILL.md` — primary skill contract and runtime behavior.
- `agents/openai.yaml` — UI metadata / default prompt wiring.
- `references/` — workflow, discovery loop, quality, prompts, and recovery rules.
- `scripts/anime_fanart.py` — main CLI for lock → generate/lock+generate flow.
- `scripts/image_gen_refs.py` — image generation from local reference images.
- `scripts/generate_from_lock.py` — generate final image with accepted lock as image input #1.

## 中文快速上手

安装后，可直接在 Codex 中使用以下流程：

```text
$anime-fanart-imagegen 明日香
AF
再来
A+C
开始生成
```

中文分支建议动作：

- 先给角色名或关键词：`明日香`
- 收到默认选项后可继续输入 `AF`、`再来`、`A+C` 等进行探索
- 不要在还没到位时马上下命令，等确认后再说 `开始生成`
- 需要继续扩展细节时继续沿当前分支输入 `再来`、`换个方向`
- 想改模块时可直接说 `只改M9光线`、`只改M8构图`

本地脚本也支持中文场景的同名参数（参数名为英文，中文内容可写在 prompt 文件中）：

```bash
python scripts/anime_fanart.py generate \
  --character "明日香·兰克莱·索留" \
  --series "新世纪福音战士" \
  --image refs/asuka/face.png \
  --prompt-file output/zh-final-prompt.txt \
  --out output/zh-asuka-final.png
```

## Python Environment

Use Python 3.11+.

Install dependencies:

```bash
pip install -r requirements.txt
```

Install OpenAI SDK:

```bash
uv pip install openai
```

Set key for local script workflow:

```bash
export OPENAI_API_KEY="..."
```

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = "..."
```

This repository defaults local scripts to `gpt-image-2.0`. Override it with `--model` only when your local environment requires a different image model name.

## CLI Commands

### 1) Create a character lock image

```bash
python scripts/anime_fanart.py lock \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --image refs/asuka/face.png \
  --image refs/asuka/fullbody.png \
  --out output/asuka-lock.png
```

- Purpose: create a clean identity baseline.
- Profile defaults: `square-safe` unless overridden.
- Use this before final generation when you need strong identity continuity.

### 2) Generate final image from prompt

```bash
python scripts/anime_fanart.py generate \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --image refs/asuka/fullbody.png \
  --prompt "<final English prompt>" \
  --out output/asuka-final.png
```

Optional: provide a lock image to anchor identity.

```bash
python scripts/anime_fanart.py generate \
  --character "Asuka Langley Soryu" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/asuka-lock.png \
  --image refs/asuka/fullbody.png \
  --prompt-file output/asuka-final-prompt.txt \
  --out output/asuka-final.png
```

- The lock image is identity-only evidence; final prompt still controls mood, crop, scene, and finish.

### 3) Run lock + final generation in one step

```bash
python scripts/anime_fanart.py run \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --image refs/rei/face.png \
  --image refs/rei/style.png \
  --prompt "<final English prompt>" \
  --lock-out output/rei-lock.png \
  --out output/rei-final.png
```

### 4) Generate with accepted lock image (convenience entry)

```bash
python scripts/generate_from_lock.py \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/rei-lock-accepted.png \
  --profile poster-safe \
  --prompt-file output/rei-final-prompt.txt \
  --out output/rei-final-from-lock.png
```

### 5) General local-reference generation

```bash
python scripts/image_gen_refs.py \
  --image refs/any/style.png \
  --image refs/any/ref2.jpg \
  --prompt "<prompt>" \
  --out output/result.png
```

### Dry run (recommended before spending API calls)

All scripts support `--dry-run` and print request metadata/payload for inspection.

```bash
python scripts/generate_from_lock.py \
  --character "Rei Ayanami" \
  --series "Neon Genesis Evangelion" \
  --lock-image output/rei-lock-accepted.png \
  --prompt-file output/rei-final-prompt.txt \
  --out output/rei-final-from-lock.png \
  --dry-run
```

For lock workflows, verify the payload order in dry-run output:
`source_images[0]` and image #1 should be the accepted lock image.

## Output Profiles

Default profiles are API-safe presets:

- `poster-safe`: `1024x1536`
- `scene-safe`: `1536x1024`
- `square-safe`: `1024x1024`
- `banner-safe`: `1536x1024`

Legacy aliases:

- `poster-2k` -> `poster-safe`
- `scene-2k` -> `scene-safe`
- `square-2k` -> `square-safe`
- `banner-2k` -> `banner-safe`

To request true 2K/4K, pass explicit `--size` (must satisfy model constraints).

## Size Constraints (gpt-image-2.0)

- both edges must be multiples of 16
- longest edge `<= 3840`
- aspect ratio `<= 3:1`
- total pixels in `[655,360, 8,294,400]`
- outputs above `2560x1440` are treated as experimental by this repository.

## Metadata and outputs

Each successful generation writes:

- the image file
- a sidecar JSON (`*.json`) with request metadata

## Distribution

Keep directory structure intact when vendoring to another repository:

`anime-fanart-imagegen/`

This preserves skill import and file-path compatibility.
