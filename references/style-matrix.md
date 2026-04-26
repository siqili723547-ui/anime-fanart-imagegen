# Style Matrix

Use this file when you need more variety without losing the character.

## How to use this file

Build style directions from `4` blocks:
- baseline
- archetype
- finish
- lighting

Keep identity anchors fixed and change only `1-2` style blocks per variant.

## Baseline

- `tv-anime-faithful`: clean cel shading, simplified graphic shapes, adaptation-consistent palette
- `game-render-faithful`: crisper material separation, richer gradient treatment, promo-art finish
- `official-illustration-faithful`: key-visual polish, stronger graphic silhouette, print-poster clarity
- `manga-colorized`: ink-aware line emphasis, flatter value grouping, restrained painterly effects
- `hybrid-promo`: anime character readability with premium illustration finish

## Stylization Delta

- `faithful`: stay close to the reference pack and change mostly composition or mood
- `lightly-stylized`: keep baseline intact, but push lighting, finish, or camera language
- `boldly-reinterpreted`: keep face/outfit/source anchors, but allow finish and atmosphere to shift more noticeably

Use `boldly-reinterpreted` only when the user explicitly wants stronger style.

## Archetypes

- `poster-key-visual`: signature pose, readable silhouette, strong focal center
- `slice-of-life`: intimate daily-life scene, grounded props, soft narrative energy
- `action-set-piece`: dynamic motion, cleaner gesture readability, reduced background clutter around the face
- `dreamlike-mood-piece`: symbolic or atmospheric environment, soft haze, fewer hard props
- `fashion-editorial`: controlled pose, wardrobe emphasis, premium poster finish
- `seasonal-illustration`: sakura, rain, summer heat, autumn gold, winter blue-hour mood
- `festival-scene`: matsuri, school festival, idol-stage, city-night event energy
- `banner-panorama`: wide crop, environment-forward composition, character still dominant

## Finish

- `clean-cel`: flatter color grouping, anime-cut clarity
- `polished-key-visual`: glossy promotional illustration finish
- `soft-filmic`: slightly softer edges with cinematic grading
- `painted-anime-poster`: richer brush texture while staying anime-readable
- `game-promo-render`: cleaner material read, sharper local contrast, premium splash-art vibe

## Lighting Packs

- `neutral-daylight`: safest for likeness checks
- `golden-hour`: warm character-driven poster lighting
- `rainy-neon`: urban reflections, blue-magenta accents, stronger mood
- `winter-blue-hour`: cool ambient light, soft skin contrast, quiet mood
- `spring-haze`: pale bloom, airy atmosphere, romantic softness
- `stage-spotlight`: performance framing, dark surroundings, bright subject isolation
- `moonlit-glow`: restrained highlights, elegant shadow shapes, fantasy-adjacent mood

## Safe Combinations

- faithful poster:
  - `tv-anime-faithful` + `poster-key-visual` + `clean-cel` + `golden-hour`
- premium official-art feel:
  - `official-illustration-faithful` + `poster-key-visual` + `polished-key-visual` + `neutral-daylight`
- game character promo:
  - `game-render-faithful` + `poster-key-visual` + `game-promo-render` + `neutral-daylight`
- daily-life atmosphere:
  - `tv-anime-faithful` + `slice-of-life` + `soft-filmic` + `spring-haze`
- bold but still safe:
  - `official-illustration-faithful` + `dreamlike-mood-piece` + `painted-anime-poster` + `moonlit-glow`
- header / cover art:
  - `hybrid-promo` + `banner-panorama` + `polished-key-visual` + `rainy-neon`

## User Language Translation

- "more cinematic" -> `narrative scene` + `soft-filmic` + directional lighting
- "more premium" -> `fashion-editorial` or `official-illustration-faithful` + `polished-key-visual`
- "more dreamlike" -> `dreamlike-mood-piece` + `spring-haze` or `moonlit-glow`
- "more hot-blooded" -> `action-set-piece` + stronger silhouette contrast + reduced prop clutter
- "more like an official poster" -> `poster-key-visual` + `official-illustration-faithful`
- "more like official game art" -> `game-render-faithful` + `game-promo-render`
- "give me several style options" -> vary `archetype` and `lighting` first, then `finish`

## Failure Modes

- Too many style words:
  - remove overlapping adjectives and keep only one finish term plus one lighting term
- Character drift after stylization:
  - step back one stylization level and reassert the source baseline in `Style/medium`
- Variants all feel the same:
  - change archetype or crop, not just mood adjectives
- Background takes over:
  - keep the face larger in frame and reduce scene events
