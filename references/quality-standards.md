# Quality Standards

Use these named profiles for reliable defaults. Use manual `--size` only when
the user explicitly asks for 2K, 4K, or another custom delivery size.

## Defaults

| Profile | Size | Quality | Format | Use |
| --- | --- | --- | --- | --- |
| `preview` | `1024x1024` | `medium` | `png` | fast checks and rough ideation |
| `poster-safe` | `1024x1536` | `high` | `png` | stable vertical poster source |
| `scene-safe` | `1536x1024` | `high` | `png` | stable horizontal scene source |
| `square-safe` | `1024x1024` | `high` | `png` | stable square source |
| `banner-safe` | `1536x1024` | `high` | `png` | stable cover source |

## Why these defaults exist

- `poster-safe`, `scene-safe`, `square-safe`, and `banner-safe` keep the default script path compatible with the narrower Image API reference schema.
- Explicit 2K or 4K delivery remains available through manual `--size`, but large outputs should be opt-in only because they cost more and may be experimental.
- Legacy names such as `poster-2k` still map to the matching `*-safe` profile for compatibility, but they are aliases only and must not be described as true 2K output.

## Size constraints for `gpt-image-2`

When you override a size manually, use `auto` or keep all of these true:

- longest edge `<= 3840`
- width and height are multiples of `16`
- long side to short side ratio `<= 3:1`
- total pixels between `655,360` and `8,294,400`

The current `gpt-image-2` guide lists 2K and 4K examples, but outputs above
`2560x1440` total pixels are experimental. Use 4K only when the user explicitly
needs final delivery at that size.

## Output format rules

- Default to `png`.
- Use `webp` or `jpeg` only when the user explicitly wants smaller web delivery files.
- Only pass `output_compression` for `webp` or `jpeg`.

## Transparency

Do not promise transparent backgrounds in this skill. `gpt-image-2` currently does not support transparent background output.
