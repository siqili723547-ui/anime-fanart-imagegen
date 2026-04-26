# Discovery Loop

Use this file when the user is not ready to choose a final prompt. The goal is to help them discover what they want through lightweight comparison, not through a long form.

## Design Principle

Treat every suggestion as a probe. A probe is a small, meaningful direction the user can react to.

Do not ask the user to name technical parameters unless they already use that language. Instead, show semantically different possibilities and learn from their reactions.

Do not lock concrete picture content too early. In early discovery, avoid naming specific locations, props, poses, or story beats unless the user already supplied them. First discover the user's abstract preference, then translate it into concrete image candidates later.

## Source-Informed Heuristics

- Prompt expansion: short prompts often need interpretation, embellishment, and structure before generation.
- Reference control: style and structure references can carry taste better than text when the user has an image in mind.
- Branching support: diverse prompt suggestions help users overcome uncertainty and express intent.
- Mixed-initiative refinement: alternate between agent suggestions and user reactions instead of forcing the user to author the whole prompt.

## State To Maintain

Keep this state mentally across turns. Do not print it unless useful.

```text
known:
  character:
  source:
  identity_anchors:
  hard_constraints:
liked:
  moods:
  abstract_preferences:
  scene_families:
  crops:
  styles:
  references:
disliked:
  avoid_moods:
  avoid_scene_families:
  avoid_specific_content:
  avoid_styles:
open:
  purpose:
  crop:
  style_strength:
  picture_content:
  scene_density:
next_probe:
```

Update the state from natural language:

- "A but softer" -> keep A's abstract direction, lower contrast, warmer or hazier light
- "more like C" -> transfer C's mood, purpose, or style strength, not its concrete picture content unless the user mentions it
- "too generic" -> increase specificity later through scene logic, prop logic, or character-specific symbolism
- "too far" -> reduce style strength and reassert canonical baseline
- "more premium" -> cleaner staging, lower prop count, controlled lighting, stronger composition hierarchy
- "more emotional" -> increase emotional intensity first; decide pose, facial expression, lighting direction, and symbolic environment in the picture-content phase
- "not like her" -> return to likeness-first lock and canonical outfit

## Loop Structure

### 1. Orient

State the current interpretation in one sentence.

```text
I am treating this as: <character/source>, with <identity anchors>, and the current goal is <goal>.
```

### 2. Probe Abstract Preference First

Offer `3-5` abstract probes. Make them semantically far apart, but do not bind them to exact picture content yet.

Good probe axes:

- purpose: shareable finished image, wallpaper, avatar, reference sheet, mood exploration
- emotional direction: calm, warm, lonely, dramatic, playful, mysterious, premium
- crop: face, half-body, full-body, wide environment
- style strength: canon-close, lightly stylized, bold reinterpretation
- character distance: intimate close-up, character-forward, environment-forward, symbolic
- story energy: still, quiet narrative, dramatic narrative, motion

Avoid early specifics:

- exact locations
- exact props
- exact poses
- exact weather or time of day
- exact story beats

Use these only after the user has picked an abstract direction or supplied the content themselves.

Bad probes:

- three variants that are all vertical posters
- synonym swaps such as "cinematic", "beautiful", "premium" without composition changes
- choices that change identity anchors before the user asks for reinterpretation
- choices that pre-decide the picture content while the user is still exploring taste

### 2b. Translate To Picture Content Later

After the user picks an abstract probe, offer `2-4` picture-content candidates that fit that preference.

At this stage, concrete content is useful:

- location
- prop
- pose
- time of day
- weather
- symbolic motif
- camera distance

Keep one candidate conservative, one emotionally stronger, and one more surprising.

### 3. Capture

Ask for a low-effort reaction.

```text
Reply with one: A/B/C/D, "A+C", "A but more like C", "mix B+C", "explore more", "back", "none", or any mood word.
```

If the user has entered exploration mode, do not end exploration just because they picked an option. Treat each pick as a new locked preference and continue exploring inside it until the user explicitly says they are done.

### 4. Narrow

After a reaction, narrow instead of expanding again.

Use this decision rule:

- if the user chooses one abstract probe -> offer picture-content candidates or ask permission to choose one
- if the user likes two probes -> merge only one feature from the second into the first
- if the user combines options, keep the first option as the base unless they say otherwise, then borrow only the named trait from the second option
- if the user says none -> change the probe axis, not all axes
- if the user says explore more -> stay at the same decision level and offer new alternatives that avoid repeating prior probes
- if the user says back -> return one decision level up and preserve learned likes/dislikes
- if the user gives a mood word -> map it to emotional direction first; defer pose and scene content until the picture-content phase
- if the user asks for surprise -> pick the strongest route and explain in one sentence

Do not auto-commit after narrowing during active exploration. A narrowed choice becomes the new current branch, then offer the next useful exploration dimension.

Commit only when the user says one of:

- "ok"
- "looks good"
- "this one"
- "可以了"
- "就这个"
- "生成"
- "stop exploring"
- "use this"

### 5. Commit

Before generation, show the selected direction in one short sentence, then produce a modular prompt spec and the compiled final prompt.

Do not ask another broad question at this point. The next action should be:

```text
Reply "generate", "explore more", "back", or give one correction.
```

Always keep `explore more` available until the image is generated. The user should never feel trapped by the latest recommendation.

Use `prompt-modules.md` for finalization after exploration. The compiled prompt should be derived from modules, not written as an unstructured one-off paragraph.

If the user asks the agent to decide unresolved modules or chooses a module option, use `prompt-modules.md` Auto-Integration After Decisions: output the full updated module list and compiled English prompt, not just the changed module.

## Active Exploration Mode

Use active exploration mode after the user says "explore more", "continue exploring", "再探索", or otherwise asks to keep discovering.

In active exploration mode:

- do not produce a final prompt by default
- do not ask "is this okay?" after every choice
- treat each selected option as a preference update
- keep the current branch fixed unless the user says `back`
- explore one new dimension per turn
- stop only when the user explicitly approves, asks to generate, or asks to stop

Rotate exploration dimensions to avoid repetition:

1. emotional intensity
2. viewing distance or crop
3. motion versus stillness
4. realism versus symbolism
5. canon closeness versus reinterpretation
6. detail density
7. color temperature
8. character agency: passive, observing, acting, arriving, leaving

After each turn, end with:

```text
Reply A-F, combine like "A+C" or "A 但更像 C", "explore more", "back", or "可以了".
```

## Exploration Modes

Use one of these modes depending on the user's uncertainty.

### Fast Track

Use when the user wants low effort.

- one recommended route
- one prompt
- one next action

### Taste Finder

Use when the user says they do not know what they want.

- `4-6` abstract taste cards
- no final prompt until they pick or react
- each card should avoid exact picture content
- each card should differ by purpose, emotional direction, character distance, or style strength

### Reference-Led

Use when the user has images, screenshots, pins, or "like this" examples.

- ask for or use the reference
- separate identity reference from style reference
- decide whether the reference should affect face, outfit, composition, color, or mood

### Contrast Test

Use when the user is stuck between options.

- offer two opposite directions
- ask which is closer
- then interpolate

Example:

```text
A. Canon-close, quiet, face-first
B. More cinematic, environment-first, stronger mood
```

### Mutation

Use after the user likes a result but wants refinement.

Change exactly one thing:

- crop
- lighting
- emotional intensity
- scene density
- style strength
- outfit freedom

### Explore More

Use when the user explicitly asks for more options, says "再探索", or seems unconvinced by the current set.

- stay at the current decision level
- preserve likes and dislikes
- avoid repeating previous options
- change the probe axis if the last set felt too narrow
- offer `3-5` new alternatives
- include `back` and `generate` as exits when relevant

Examples:

- after abstract taste cards -> provide new abstract taste cards, not picture content
- after picture-content candidates -> provide new picture-content candidates within the chosen abstract direction
- after final prompt -> provide alternate prompt directions or return to picture-content candidates
- after the user names a module, such as "再探索 M9" -> use module-level exploration from `prompt-modules.md`

## Probe Card Template

Use this for early discovery:

```text
A. <name>: <purpose>, <emotional direction>, <character distance>, <style strength>. Best if you want <plain-language outcome>.
B. <name>: ...
C. <name>: ...

Reply A/B/C, "mix A+C", "none", or one mood word.
```

Do not include specific picture content in early probe cards.

## Mixing Options

Always tell the user they can mix options.

Interpret mixed choices conservatively:

- `A+C` -> use A as the base, borrow the most distinctive trait from C
- `A 但更像 C` -> keep A's purpose/content, move style, mood, or intensity toward C
- `A+B+C` -> ask which one is the base if the combination would affect more than two modules
- `不要 A 的 X，只要 C 的 Y` -> update only the named traits

Do not blindly merge every detail from both options. A clean hybrid is better than an overloaded prompt.

## Picture-Content Template

Use this after the user chooses an abstract preference:

```text
Direction locked: <abstract preference>.

Now choose picture content:
A. Conservative: <specific but safe image idea>
B. Stronger emotion: <specific image idea with more mood>
C. More surprising: <specific image idea with more novelty>

Reply A/B/C, "mix A+C", "explore more", "back", or "you choose".
```

## Finalization Template

```text
Selected direction: <one sentence>.

Prompt modules:
M1 身份锚点: ...
M2 原作基线: ...
M3 用途目标: ...
M4 改编边界: ...
M5 情绪方向: ...
M6 角色状态: ...
M7 画面内容: ...
M8 构图画幅: ...
M9 光线色彩: ...
M10 风格质感: ...
M11 正向约束: ...
M12 避免项: ...

English prompt:
<image-2-ready English prompt>

Next:
- 生成
- 改某一模块，例如 "改 M9 光线色彩"
- 再探索某一模块，例如 "再探索 M7"
- 探索更多维度
- 返回
```

## Universal Exits

Every discovery response should include at least two of these exits, and finalization responses should include all three:

- `generate`: commit to the current prompt
- `explore more`: stay at this level and show different alternatives
- `back`: return to the previous level

Do not hide these exits in prose. Put them in the final next-action line.

If the user asks to explore a specific module, the next-action line should stay module-scoped, for example:

```text
Next: reply A-C, mix like "A+C", "继续探索 M9", "返回", or "可以了".
```

If the user asks to explore more dimensions after a modular prompt spec, use `prompt-modules.md` More-Dimensions Exploration and keep the current prompt unchanged until they select a dimension.

## Guardrails

- Never turn discovery into a survey.
- Never show more than `6` probes at once.
- Do not expose advanced technical axes before the user shows they want control.
- Preserve identity anchors across probes unless the user asks for reinterpretation.
- When unsure, vary purpose, emotional direction, character distance, and style strength before choosing exact picture content.
- Do not turn early taste discovery into a list of specific scene ideas.
- Always offer an escape from the current branch: explore more, back, or generate.
- Keep user agency visible: recommendations are defaults, not hidden decisions.
