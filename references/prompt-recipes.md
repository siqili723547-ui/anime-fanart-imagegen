# Prompt Recipes

These are output-ready English prompt templates. Use them as scaffolding, not as mandatory filler.

## Core Rules

Always include:
- character name
- series
- identity anchors
- scene intent
- source visual baseline
- hard constraints

Keep this order of operations:
1. lock the identity
2. state the baseline
3. describe the scene or pose
4. add finish and lighting
5. close with constraints and avoid terms

When making variants, keep `Character`, `Identity anchors`, and the source-baseline part of `Style/medium` stable. Change only composition, finish, lighting, or scene archetype.

After a multi-turn discovery flow, use `prompt-modules.md` before writing the final prompt. The final English prompt should be compiled from modules so the user can revise one part without restarting exploration.

## Master Skeleton

Use this structure unless a more specific template below is a better fit:

```text
Use case: <poster-key-visual | narrative-scene | character-render | action-set-piece | fashion-editorial | dreamlike-mood-piece | banner-panorama>
Primary request: <describe the scene, action, or pose clearly>
Character: <character name> from <series>
Identity anchors: <hair, eyes, face vibe, outfit silhouette, dominant colors, prop/accessory>
Style/medium: <canonical visual baseline> with <finish language>; preserve the reference pack's source visual logic
Composition/framing: <crop, camera, subject size, staging>
Lighting/mood: <light direction, palette, emotional tone>
Background/scene: <environment or supporting context>
Constraints: preserve recognizability; preserve the canonical outfit silhouette unless the user explicitly asked for a new outfit; original composition; no text; no watermark
Avoid: <specific failure modes for this image>
```

## Faithful Poster Key Visual

```text
Use case: poster-key-visual
Primary request: <describe the poster scene>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished character illustration following the canonical source visuals in the reference pack; if the character is from a game, preserve the game's official design language instead of forcing an anime-TV look
Composition/framing: vertical poster composition, full body or three-quarter body, strong focal pose
Lighting/mood: <lighting and mood>
Background/scene: <environment>
Constraints: preserve recognizability; keep the canonical outfit silhouette unless the user explicitly asked for a new outfit; original composition; no text; no watermark
Avoid: extra limbs, face drift, color drift, random accessories, duplicate props
```

## Slice-of-Life Narrative Scene

```text
Use case: narrative-scene
Primary request: <describe the story beat or daily-life moment>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished character scene illustration matching the canonical source visuals in the reference pack with soft cinematic finishing
Composition/framing: cinematic horizontal or vertical composition, readable staging, character still dominant in frame
Lighting/mood: <gentle daylight, spring haze, rainy window light, cafeteria warmth, etc.>
Background/scene: <environment with a few specific props only>
Constraints: preserve character identity and canonical outfit cues; original composition and scene; no text; no watermark
Avoid: crowded staging that hides the face, face drift, random costume changes, inaccurate palette
```

## Action Set Piece

```text
Use case: action-set-piece
Primary request: <describe the action beat, motion, or confrontation>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: high-energy anime action illustration grounded in the canonical source visuals rather than generic battle shonen styling
Composition/framing: dynamic motion composition with clear silhouette read, decisive gesture, and readable face
Lighting/mood: dramatic directional light, impact highlights, controlled contrast
Background/scene: <minimal but supportive setting that reinforces motion>
Constraints: preserve recognizability and canonical design cues; keep the action readable; original composition; no text; no watermark
Avoid: chaotic background clutter, hidden face, anatomy collapse, random armor or costume redesign
```

## Fashion Editorial / Premium Poster

```text
Use case: fashion-editorial
Primary request: <describe the premium posed illustration or editorial moment>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: premium key visual illustration built on the canonical source visuals with clean editorial polish
Composition/framing: controlled pose, elegant negative space, poster-forward composition
Lighting/mood: sculpted softbox-like light, glossy highlights, premium print-ad feel
Background/scene: restrained graphic backdrop or minimal environment accents
Constraints: preserve recognizability; preserve canonical design logic unless the user explicitly requested wardrobe reinterpretation; no text; no watermark
Avoid: overdecorated scene dressing, random luxury props, off-model face, photoreal skin treatment
```

## Dreamlike / Atmospheric Variation

```text
Use case: dreamlike-mood-piece
Primary request: <describe the atmospheric, surreal, or emotionally symbolic scene>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: stylized anime illustration derived from the canonical source visuals with a restrained dreamlike finish
Composition/framing: character-forward composition with selective background symbolism and clean focal hierarchy
Lighting/mood: moonlit glow, spring haze, underwater light, aurora-like bloom, or other controlled atmospheric effect
Background/scene: symbolic or poetic environment elements that support the mood without replacing character readability
Constraints: preserve character identity; preserve signature outfit and colors; original composition; no text; no watermark
Avoid: over-fogged face, abstract effects covering the eyes, costume drift, too many floating objects
```

## Game-Faithful Character Render

```text
Use case: character-render
Primary request: <describe pose and presentation>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: clean character render matching the canonical source visuals in the reference pack; if the source is a game, preserve crisp material separation and official promo-art logic
Composition/framing: centered full-body or half-body presentation on a simple background
Lighting/mood: neutral showcase lighting or controlled promotional spotlight
Constraints: preserve recognizability; preserve the canonical outfit silhouette and key colors; no text; no watermark
Avoid: background clutter, prop duplication, face drift, anatomy errors
```

## Banner / Panorama

```text
Use case: banner-panorama
Primary request: <describe the panoramic hero image>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished key visual illustration based on the canonical source visuals with environment-forward composition
Composition/framing: wide panoramic crop with the character still large enough to read immediately
Lighting/mood: <lighting and mood>
Background/scene: environment has room to breathe but still supports the hero character
Constraints: preserve recognizability; preserve the canonical outfit silhouette; original composition; no text; no watermark
Avoid: tiny unreadable face, environment dominating the frame, duplicate props, random extra characters
```

## Lock Prompt

Use this for the `lock` pass:

```text
Use case: character-lock
Primary request: create a clean identity-lock image for <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished character art matching the canonical source visuals in the reference pack
Composition/framing: simple centered portrait or full-body neutral standing pose, plain or lightly graded background
Constraints: preserve recognizability; keep the canonical outfit silhouette; do not copy any single reference composition; no text; no watermark
Avoid: busy scenery, dramatic perspective distortion, face drift, random costume changes, anatomy errors
```

## Variant Pack Strategy

When the user asks for multiple styles, use this spread:
- variant 1: faithful baseline
- variant 2: same baseline, different composition or environment
- variant 3: same baseline, different lighting and finish
- variant 4: only if requested, stronger reinterpretation with explicit baseline anchoring
