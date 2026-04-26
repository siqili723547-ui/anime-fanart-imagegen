# Frictionless UX

Use this file when the user wants a strong result from `image-2` but cannot clearly describe the image, cannot write a solid prompt, or explicitly says "you decide".

## Goal

Make the workflow feel low-effort for the user and high-control for the agent.

The user should not need to know prompt engineering vocabulary. Convert rough taste signals into explicit image decisions.

## Default Interaction Rule

Prefer this order:

1. infer what can be inferred
2. route by user intent
3. recommend one default path
4. offer micro-chips or discovery probes only if needed
5. prepare the final prompt
6. render only after the user asks to generate, selects a direction, or has already provided a complete prompt

Do not start with a long list of questions.

Keep the default question budget at `0-1`.

Ask only when one of these is genuinely blocking:

- the character name is ambiguous
- the version is ambiguous and changes the design materially
- the requested deliverable is incompatible with the default crop
- the user supplied contradictory references

## Guided-First Rule

For vague first-turn requests, guide before rendering.

Examples:

```text
I want to make an image of Violet.
```

```text
Try this skill with Violet Evergarden.
```

```text
I cannot describe what I want yet.
```

Default behavior:

- identify the character and likely source
- infer the canonical visual baseline
- show an intent router across broad user goals
- recommend one path that is likely to produce a strong first result
- show optional micro-chips for quick steering
- provide a ready English prompt for the recommended path
- ask for a low-effort next action such as `A`, `B`, `C`, `generate`, or one mood word

Do not call the image tool during this first guided response unless the user explicitly says "generate now", "directly render", "no need to ask", or selects an existing direction.

## Intake Modes

### 1. Name-only

Example:

```text
Anna Yanami
```

Default behavior:

- infer the series
- gather references
- build anchors
- choose a faithful poster or render
- produce a recommended prompt and `2-3` nearby alternatives

### 2. Mood-only

Example:

```text
Make it dreamier and moodier.
```

Default behavior:

- keep the character baseline fixed
- map mood to lighting, finish, and scene density
- produce several style directions that differ in atmosphere, not identity

### 3. Rough scene

Example:

```text
Put her on a rooftop at night in the rain, and make it feel like an official poster.
```

Default behavior:

- keep the character anchors fixed
- translate "official poster" into baseline plus archetype
- turn the rough scene into a structured English prompt

### 4. Rough prompt draft

Example:

```text
A very pretty poster with a blue palette. Make it feel refined.
```

Default behavior:

- preserve the user's intent
- replace weak adjectives with concrete finish, framing, and lighting decisions
- add the missing constraints and avoid terms

### 5. Reference-only

Example:

User provides several images with little text.

Default behavior:

- infer the specific version from the references
- extract recurring anchors
- ask at most one question only if the references conflict

### 6. "You decide"

Example:

```text
You decide what suits her best.
```

Default behavior:

- choose the safest strong default
- explain the interpreted brief in one line
- optionally include `2-3` nearby variants
- do not push the decision back to the user

## Hidden Slots To Fill

When the user is vague, infer these slots yourself:

- identity: character, series, version
- output type: poster, scene, render, banner
- crop: vertical, horizontal, square, wide
- focus: portrait, half-body, full-body, wide scene
- archetype: poster-key-visual, slice-of-life, action-set-piece, dreamlike-mood-piece, fashion-editorial, banner-panorama
- baseline: tv-anime-faithful, game-render-faithful, official-illustration-faithful, manga-colorized, hybrid-promo
- finish: clean-cel, polished-key-visual, soft-filmic, painted-anime-poster, game-promo-render
- lighting: neutral-daylight, golden-hour, rainy-neon, winter-blue-hour, spring-haze, stage-spotlight, moonlit-glow
- stylization delta: faithful, lightly-stylized, boldly-reinterpreted
- constraints: recognizability, outfit fidelity, no text, no watermark

## Intent Router

Use the intent router as the default selection UX. It asks what outcome the user wants, not which art parameters they understand.

### Intent options

- `A Finished image`: user wants a strong all-purpose result for sharing
- `B Wallpaper or cover`: user wants a scene, banner, desktop image, or social header
- `C Avatar or portrait`: user wants the face large and recognizable
- `D Explore vibe`: user is unsure and wants taste discovery before generation
- `E Maximize likeness`: user cares most that the character reads correctly
- `F Change style`: user wants reinterpretation, AU, fashion, cinematic, painterly, game-promo, or another style shift
- `G Surprise me`: user wants the agent to choose a high-confidence route

### Intent routing behavior

- `A Finished image` -> recommend a polished poster or character-forward key visual
- `B Wallpaper or cover` -> recommend horizontal or panoramic scene-first composition
- `C Avatar or portrait` -> recommend face-first portrait or half-body image
- `D Explore vibe` -> return `4-6` vibe chips before writing the final prompt
- `E Maximize likeness` -> start with identity lock and neutral lighting
- `F Change style` -> ask for or infer style strength, then preserve face/outfit/source anchors
- `G Surprise me` -> choose the strongest low-risk route and state the choice briefly

For vague first-turn requests, show this router before any technical axes. Technical axes are advanced controls, not the default interface.

## Micro-Chips

Use micro-chips to let the user steer without learning prompt vocabulary. Show only one short line of chips unless the user asks for more.

### Mood chips

- faithful
- softer
- more cinematic
- dreamier
- more melancholic
- brighter
- more premium
- more dynamic
- darker

### Composition chips

- close-up
- half-body
- full-body
- wide scene
- vertical
- horizontal
- square
- banner

### Style strength chips

- keep close to canon
- lightly stylized
- bold reinterpretation
- outfit unchanged
- outfit redesign allowed

## Progressive Disclosure

Do not show every control at once.

Use this order:

1. intent router
2. recommendation and ready prompt
3. micro-chips
4. advanced creative-control axes only if the user asks to customize

This makes the first response broadly useful without feeling like a form.

## Creative-Control Axes

Use these axes only as advanced controls. Do not show the full axis grid by default.

### 1. Use case

- `poster`: vertical hero art or key visual
- `wallpaper`: horizontal scene or cinematic frame
- `avatar`: face-forward square or portrait crop
- `banner`: wide header or cover image
- `character-sheet`: clean full-body render

### 2. Scene family

- `canonical-world`: location and props close to the source work
- `quiet-daily`: small everyday moment
- `cinematic-drama`: emotional scene with strong light and framing
- `symbolic`: abstract or poetic visual motif
- `fashion-editorial`: controlled pose and premium print feel
- `seasonal`: spring, summer, autumn, winter, rain, festival, snow
- `action-or-motion`: movement, wind, battle, performance, or gesture
- `crossover-au`: alternate outfit or setting, only if the user allows reinterpretation

### 3. Mood

- `faithful-calm`
- `warm-nostalgic`
- `melancholic`
- `dreamlike`
- `dramatic`
- `bright-playful`
- `mysterious`
- `premium-refined`

### 4. Style strength

- `identity-first`: safest likeness, smallest style movement
- `lightly-stylized`: different lighting or finish, same design logic
- `bold-reinterpretation`: stronger atmosphere or setting, identity anchors must be restated

### 5. Fidelity priority

- `face-first`: maximize face and hair recognizability
- `outfit-first`: preserve canonical costume silhouette
- `scene-first`: let the environment carry more of the image
- `mood-first`: prioritize emotional atmosphere

## Safe Defaults

Use these when the user did not specify them:

- poster-like hero image -> `poster-2k`
- wallpaper-like scene -> `scene-2k`
- icon/avatar/social crop -> `square-2k`
- header/cover/wide illustration -> `banner-2k`
- likeness-first pass -> `neutral-daylight`
- romantic or soft mood -> `spring-haze`
- premium or polished -> `polished-key-visual`
- official-poster feel -> `official-illustration-faithful` + `poster-key-visual`
- "you decide" -> faithful or lightly stylized, not bold reinterpretation

## Output Pattern For Vague Requests

When the request is underspecified, produce a compact pack in this order:

1. interpreted brief in Chinese
2. intent router with broad user goals
3. recommended path
4. optional micro-chips
5. English prompt for the recommended path
6. one-line next action

Do not make the user choose from many technical axes on the first turn. Use technical axes only after they ask for custom control.

## Intent Router Template

Use this shape for vague first-turn requests:

```text
I will treat this as: <character> from <series>, <version/baseline>.

What do you want first?
A. Finished image
B. Wallpaper or cover
C. Avatar or portrait
D. Explore vibe
E. Maximize likeness
F. Change style
G. Surprise me

Recommended: <one route and why in one short sentence>
Quick tweaks: <5-8 chips, for example "softer / cinematic / dreamier / closer to canon / horizontal / face-first">

Prompt:
<output-ready English prompt>

Next: reply A-G, say "generate", say "explore more", or add one tweak word.
```

If the user chooses `D Explore vibe`, return abstract taste cards instead of generating. Do not decide exact picture content in that response.

## Taste Cards

Use taste cards only after the user asks to explore or seems undecided after the intent router.

Each card should combine:

- mood
- purpose
- crop
- style strength
- character distance
- one reason it fits the character

Keep the cards diverse. Avoid making all cards poster-like. Avoid specific locations, props, poses, weather, or story beats until the user chooses a taste card.

For deeper multi-turn exploration, use `discovery-loop.md` instead of adding more menu options to this file.

## Prompt Upgrade Rules

When rewriting weak user language into an `image-2` prompt:

- keep the character name and series explicit
- keep identity anchors near the top
- state the source baseline explicitly
- define composition clearly
- define lighting in visual terms
- keep the scene simple enough for the face to stay readable
- use concise avoid terms targeted at likely failure modes

### Replace weak wording

- "pretty" -> choose a pose, a clean composition, and a finish
- "moody" -> choose a lighting pack and restrained environment cues
- "premium" -> lower prop count, cleaner silhouette, premium finish
- "like official art" -> official-illustration-faithful or game-render-faithful baseline
- "refined" -> better staging and finish, not more random detail

### Avoid these mistakes

- mirroring the user's vague words without adding visual structure
- piling on synonyms for style
- changing identity and style at the same time
- making the background more complex than the user's actual intent requires
- using strong stylization before the canonical baseline is established

## Compact Chinese Response Template

Use a format like this when the user is unclear:

```text
Interpreted brief: <one-line interpreted brief>

What do you want first?
A. Finished image
B. Wallpaper or cover
C. Avatar or portrait
D. Explore vibe
E. Maximize likeness
F. Change style
G. Surprise me

Recommended: <one route>
Quick tweaks: <chips>

Prompt: <ready English prompt>
```

Then provide the English prompt or execute the generation workflow.

## Escalation Rule

If the first result is technically good but emotionally off, do not ask the user to rewrite the whole prompt. Keep the identity anchors fixed and change only one of:

- archetype
- crop
- lighting
- finish
- scene density

This keeps retries easy for the user to react to.
