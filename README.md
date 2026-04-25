# Anime Fanart Imagegen

这是一个用于 Codex 的动漫同人图生成 skill，适合生成已有动漫或游戏角色的同人海报、剧情场景和角色图，并尽量保持人物相似度。

它面向“人物要像，但不要照抄参考图构图”的工作流：先整理参考图和人物锚点，再做角色锁定，最后生成海报或场景图。skill 支持中文需求输入、英文生成提示词、官方优先参考图检索、角色锁定流程，以及 2K 和可选 4K 的固定质量档。

## 功能

- 从用户提供的图片或官方优先来源整理小型参考图包。
- 提取角色身份锚点，例如发型、发色、眼睛、服装轮廓、配色和标志性道具。
- 生成适合图片模型使用的英文提示词，默认覆盖海报、剧情场景和角色图三种方向。
- 在最终出图前先做角色锁定图，降低人物跑偏概率。
- 提供基于 `gpt-image-2` 的 CLI 工作流，支持命名质量档。

## 安装

将整个文件夹复制到 Codex 的 skills 目录：

```text
~/.codex/skills/anime-fanart-imagegen
```

然后在 Codex 中这样调用：

```text
使用 $anime-fanart-imagegen，帮我为 <作品名> 的 <角色名> 生成一张 2K 动漫同人海报。
```

如果是在 Windows 上，本地路径通常类似：

```text
C:\Users\<你的用户名>\.codex\skills\anime-fanart-imagegen
```

## API 模式

内置脚本需要 OpenAI Python SDK 和 `OPENAI_API_KEY`：

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="..."
```

Windows PowerShell 示例：

```powershell
$env:OPENAI_API_KEY = "..."
pip install -r requirements.txt
```

先用 `--dry-run` 检查请求参数，不会真实调用 API：

```bash
python scripts/anime_fanart.py lock \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --image refs/yanami/01-face.png \
  --image refs/yanami/02-fullbody.png \
  --out output/yanami-lock.png \
  --dry-run
```

## 推荐流程

1. 准备 `3-5` 张参考图，优先使用用户指定图或官方图。
2. 让 skill 提取角色锚点，包括发型、眼睛、服装、配色、道具和表情气质。
3. 先生成角色锁定图，确认人物相似度。
4. 锁定图通过后，再生成最终海报、剧情场景或角色图。
5. 如果人物跑偏，优先回到锁定图阶段修正，不要直接重写复杂场景。

## 质量档

默认使用 2K 档：

- `poster-2k`: 竖版海报
- `scene-2k`: 横版剧情场景
- `square-2k`: 方图角色图

4K 档只建议在明确需要最终成品时使用：

- `poster-4k`
- `scene-4k`

详细规则见 `references/quality-standards.md`。

## 注意事项

不要把有版权的参考图、动画截图、生成图或私有 API key 提交到这个仓库。建议把本地参考图放在 `refs/`，生成结果放在 `output/`；这两个目录已经被 `.gitignore` 忽略。

这个 skill 可以通过参考图和提示词结构提高人物相似度，但不能保证 100% 复刻某个版权角色或某一帧画面。
