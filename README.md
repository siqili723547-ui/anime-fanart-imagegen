# Anime Fanart Imagegen

这是一个用于 Codex 的动漫同人图生成 skill，适合生成已有动漫或游戏角色的同人海报、剧情场景和角色图，并尽量保持人物相似度。

它面向“人物要像，但不要照抄参考图构图”的工作流：先整理参考图和人物锚点，再做角色锁定，最后生成海报或场景图。skill 支持中文需求输入、英文生成提示词、官方优先参考图检索、角色锁定流程，以及 2K 和可选 4K 的固定质量档。

## 功能

- 从用户提供的图片或官方优先来源整理小型参考图包。
- 提取角色身份锚点，例如发型、发色、眼睛、服装轮廓、配色和标志性道具。
- 生成适合图片模型使用的英文提示词，默认覆盖海报、剧情场景和角色图三种方向。
- 在最终出图前先做角色锁定图，降低人物跑偏概率。
- 提供基于 `gpt-image-2` 的 CLI 工作流，支持命名质量档。

## 教程一：最简单的使用教程

### 1. 安装

Windows PowerShell：

```powershell
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen.git "$env:USERPROFILE\.codex\skills\anime-fanart-imagegen"
```

macOS 或 Linux：

```bash
git clone https://github.com/siqili723547-ui/anime-fanart-imagegen.git ~/.codex/skills/anime-fanart-imagegen
```

安装后重启 Codex，或新开一个 Codex 窗口。

### 2. 输入角色名

最简单的用法是只输入角色名：

```text
$anime-fanart-imagegen 八奈见杏菜
```

也可以写成自然语言：

```text
使用 $anime-fanart-imagegen，八奈见杏菜
```

skill 默认会自动执行：

1. 识别角色和作品。
2. 搜索官方优先参考图。
3. 提取人物锚点，例如发型、眼睛、服装、配色和气质。
4. 先做角色锁定，尽量保证人物相似度。
5. 默认生成一张 `2K` 动漫同人海报。

如果角色名不够唯一，补上作品名：

```text
使用 $anime-fanart-imagegen，八奈见杏菜，败犬女主太多了
```

如果想指定场景，在角色名后面加一句需求：

```text
使用 $anime-fanart-imagegen，八奈见杏菜和温水和彦，在旧校舍楼梯一起吃便当
```

## 教程二：完整推荐的使用教程

### 1. 准备参考图

每个角色准备 `3-5` 张图即可：

- `01-face.png`：脸部或半身图
- `02-fullbody.png`：全身图
- `03-outfit.png`：经典服装和主配色
- `04-expression.png`：表情或气质参考
- `05-scene.png`：动画场景或光影参考

参考图只用于锁定“人物是谁”，不是要求模型照抄参考图构图。

如果你已经有参考图，可以把图片拖进 Codex 对话，或提供本地文件夹路径：

```text
参考图目录：
C:\path\to\refs\yanami-anna
C:\path\to\refs\nukumizu-kazuhiko

使用 $anime-fanart-imagegen，先根据参考图锁定人物相似度，再生成双人互动场景。
```

### 2. 在 Codex 里描述需求

不用 API key 的最快完整用法是直接在 Codex 对话里调用 skill，让 Codex 使用内置图片生成能力：

```text
使用 $anime-fanart-imagegen，帮我生成八奈见杏菜和温水和彦在旧校舍楼梯吃便当的双人互动场景。
要求：动画版风格，人物要像，八奈见保持蓝发蓝眼和经典校服，温水保持普通黑发男高中生形象，画面是日常喜剧氛围。
```

### 3. 按推荐流程迭代

推荐流程：

1. 准备或自动搜索参考图。
2. 提取角色锚点，包括发型、眼睛、服装、配色、道具和表情气质。
3. 先生成角色锁定图，确认人物相似度。
4. 锁定图通过后，再生成最终海报、剧情场景或角色图。
5. 如果人物跑偏，优先回到锁定图阶段修正，不要直接重写复杂场景。

### 4. 可选：使用 API 脚本出图

如果你需要固定 `gpt-image-2`、2K/4K、PNG、质量档和元数据记录，可以使用脚本模式。先安装依赖并设置 API key：

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="..."
```

Windows PowerShell：

```powershell
pip install -r requirements.txt
$env:OPENAI_API_KEY = "..."
```

先用 `--dry-run` 检查请求，不会真实调用 API：

```bash
python scripts/anime_fanart.py lock \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --image refs/yanami/01-face.png \
  --image refs/yanami/02-fullbody.png \
  --out output/yanami-lock.png \
  --dry-run
```

真实生成角色锁定图时去掉 `--dry-run`：

```bash
python scripts/anime_fanart.py lock \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --image refs/yanami/01-face.png \
  --image refs/yanami/02-fullbody.png \
  --out output/yanami-lock.png
```

锁定图通过后，再生成最终海报或场景：

```bash
python scripts/anime_fanart.py generate \
  --character "Anna Yanami" \
  --series "Too Many Losing Heroines!" \
  --lock-image output/yanami-lock.png \
  --image refs/yanami/02-fullbody.png \
  --profile poster-2k \
  --prompt "Use case: poster-key-visual
Primary request: Anna Yanami sitting on an old school staircase during lunch, eating bento with a playful smile
Style/medium: polished TV anime illustration
Composition/framing: vertical poster composition
Constraints: preserve recognizability, canonical school uniform, no text, no watermark" \
  --out output/yanami-poster.png
```

## 质量档

默认使用 2K 档：

- `poster-2k`：竖版海报
- `scene-2k`：横版剧情场景
- `square-2k`：方图角色图

4K 档只建议在明确需要最终成品时使用：

- `poster-4k`
- `scene-4k`

详细规则见 `references/quality-standards.md`。

## 注意事项

- 请只在你有权使用参考图和生成结果的场景下使用。
- 不要在公开内容里泄露自己的 `OPENAI_API_KEY`。
- 这个 skill 会尽量提高人物相似度，但不能保证 100% 复刻某个角色或某一帧画面。
