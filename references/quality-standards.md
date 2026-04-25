# Quality Standards

Use these named profiles instead of inventing a size each time.

## Defaults

| Profile | Size | Quality | Format | Use |
| --- | --- | --- | --- | --- |
| `preview` | `1024x1024` | `medium` | `png` | fast checks and rough ideation |
| `poster-2k` | `1440x2560` | `high` | `png` | default vertical poster |
| `scene-2k` | `2560x1440` | `high` | `png` | default horizontal scene |
| `square-2k` | `1920x1920` | `high` | `png` | default square render |
| `poster-4k` | `2160x3840` | `high` | `png` | explicit 4K vertical poster |
| `scene-4k` | `3840x2160` | `high` | `png` | explicit 4K horizontal scene |

## Why these defaults exist

- `poster-2k`, `scene-2k`, and `square-2k` stay below the current OpenAI guide's experimental threshold for outputs larger than `2560x1440` total pixels.
- `poster-4k` and `scene-4k` are valid but should be opt-in only.

## Size constraints for `gpt-image-2`

When you override a size manually, keep all of these true:
- longest edge `<= 3840`
- width and height are multiples of `16`
- long side to short side ratio `<= 3:1`
- total pixels between `655,360` and `8,294,400`

## Output format rules

- Default to `png`.
- Use `webp` or `jpeg` only when the user explicitly wants smaller web delivery files.
- Only pass `output_compression` for `webp` or `jpeg`.

## Transparency

Do not promise transparent backgrounds in this skill. `gpt-image-2` currently does not support transparent background output.
