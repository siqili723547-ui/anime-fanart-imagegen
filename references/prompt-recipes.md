# Prompt Recipes

These are output-ready English prompt templates. Use them as scaffolding, not as mandatory filler.

Always include:
- character name
- series
- identity anchors
- scene intent
- hard constraints

## Poster Key Visual

```text
Use case: poster-key-visual
Primary request: <describe the poster scene>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished anime illustration matching the anime adaptation
Composition/framing: vertical poster composition, full body or three-quarter body, strong focal pose
Lighting/mood: <lighting and mood>
Background/scene: <environment>
Constraints: preserve recognizability; keep the canonical outfit silhouette unless the user explicitly asked for a new outfit; original composition; no text; no watermark
Avoid: extra limbs, face drift, color drift, random accessories, duplicate props
```

## Narrative Scene

```text
Use case: narrative-scene
Primary request: <describe the story beat or cinematic moment>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished anime scene illustration matching the TV anime adaptation
Composition/framing: cinematic horizontal composition, readable staging, clear subject separation
Lighting/mood: <lighting and mood>
Background/scene: <environment>
Constraints: preserve character identity and canonical outfit cues; original composition and scene; no text; no watermark
Avoid: crowded staging that hides the face, face drift, random costume changes, inaccurate palette
```

## Character Render

```text
Use case: character-render
Primary request: <describe pose and presentation>
Character: <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: clean anime character render matching the anime adaptation
Composition/framing: centered full-body or half-body presentation on a simple background
Lighting/mood: soft neutral studio-like anime lighting
Constraints: preserve recognizability; preserve the canonical outfit silhouette and key colors; no text; no watermark
Avoid: background clutter, prop duplication, face drift, anatomy errors
```

## Lock Prompt

Use this for the `lock` pass:

```text
Use case: character-lock
Primary request: create a clean identity-lock image for <character name> from <series>
Identity anchors: <hair, eyes, outfit silhouette, colors, prop, vibe>
Style/medium: polished anime character art matching the anime adaptation
Composition/framing: simple centered portrait or full-body neutral standing pose, plain or lightly graded background
Constraints: preserve recognizability; keep the canonical outfit silhouette; do not copy any single reference composition; no text; no watermark
Avoid: busy scenery, dramatic perspective distortion, face drift, random costume changes, anatomy errors
```
