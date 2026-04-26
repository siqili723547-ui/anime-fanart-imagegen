# Quality Standards

Use these named profiles instead of inventing a size each time.

## Defaults

| Profile | Size | Quality | Format | Use |
| --- | --- | --- | --- | --- |
| `preview` | `1024x1024` | `medium` | `png` | fast checks and rough ideation |
| `poster-2k` | `1440x2560` | `high` | `png` | default vertical poster |
| `scene-2k` | `2560x1440` | `high` | `png` | default horizontal scene |
| `square-2k` | `1920x1920` | `high` | `png` | default square render |
| `banner-2k` | `3072x1024` | `high` | `png` | extra-wide header, cover, or panoramic key visual |
| `poster-4k` | `2160x3840` | `high` | `png` | explicit 4K vertical poster |
| `scene-4k` | `3840x2160` | `high` | `png` | explicit 4K horizontal scene |
| `banner-4k` | `3840x1280` | `high` | `png` | explicit 4K panoramic banner |

## Why these defaults exist

- `poster-2k`, `scene-2k`, `square-2k`, and `banner-2k` give stable default deliverables for common poster, scene, square, and cover-art use cases.
- `poster-4k`, `scene-4k`, and `banner-4k` are valid but should be opt-in only.

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
