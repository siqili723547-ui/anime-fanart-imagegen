# Recovery Guide

Use this file when the result looks technically good but the character no longer reads correctly.

## Feedback triggers

Enter recovery when the user says "人物不像", "脸不像", "不够像", "更像",
"更像原作", "not like her/him", "more like the character", or equivalent
likeness feedback. Treat this as an identity repair request, not a general
style preference.

- Inspect the latest image when available before rewriting the prompt.
- Keep the current direction unless it is causing the identity drift.
- Do not ask the user to rewrite the whole prompt.
- After the repair, show the full current module list and full compiled English
  prompt, then offer more changes or `开始生成图片`.

## Identity-first repair

When likeness is the problem, strengthen visual evidence and reduce competing
pressure before adding more adjectives:

- Edit `M1` for concrete face, hair, eye, expression, and signature outfit cues.
- Edit `M2` and `M4` to step closer to the canonical source baseline.
- Edit `M8` to crop closer or make the face and outfit details larger.
- Edit `M10` to reduce heavy repaint, fashion, AU, or photoreal language.
- Edit `M12` to explicitly avoid generic nearby designs and prior drift.
- If references are available, put the cleanest face reference first, then the
  clearest full-body or outfit reference, and use only `1-3` strong references.

## When the prompt is already detailed

- Do not keep adding more descriptive clauses as the first fix.
- Treat the failure as weak visual evidence or too much competing style pressure.
- Shorten optional scene, lighting, and finish language before adding new anchors.
- Move the cleanest face reference and accepted lock image earlier in the image list.
- Make the character larger in frame so the face, hair, and outfit silhouette stay readable.

## Likeness retry ladder

Use the smallest stronger step that applies:

1. Reorder references: clean face first, then full-body, then outfit or prop.
2. Reduce the prompt to one finish term, one lighting term, and one scene idea.
3. Rerun the lock pass with neutral lighting and a plain background.
4. Generate the final image with the accepted lock image first and only `1-3` strong references.
5. If it still drifts, step down style strength or crop closer before changing the scene.

## Face drift

- Reduce scene complexity and rerun the lock pass.
- Put the cleanest face reference first in the image list.
- Add a stronger `Identity anchors:` line with hair, eyes, and expression cues.
- Remove optional style flourishes from the prompt.

## Outfit drift

- Reassert the canonical outfit silhouette and dominant colors in `Constraints:`.
- Move the clearest full-body reference earlier in the image list.
- If the user did not explicitly ask for a costume change, say so directly in the prompt.

## Palette drift

- Add a concise color anchor line.
- Remove unrelated mood words that can overpower the canonical palette.
- Prefer a simpler background during the lock step.

## Scene too busy

- Go back to the lock image.
- Keep the character large in frame.
- Reduce the number of props and background events.

## Variants all look the same

- Change the scene archetype or crop before changing synonyms in `Lighting/mood`.
- Keep the identity anchors fixed and vary one of: finish, lighting, or composition.
- Use `references/style-matrix.md` and pick combinations from different archetype families.

## Stylization drift

- Reassert the canonical source visual baseline in `Style/medium`.
- Step down from bold reinterpretation to lightly stylized.
- Remove overlapping style phrases until only one finish term and one lighting term remain.

## Final image no longer matches the lock image

- Use the lock image as the first input image.
- Keep only `1-3` strong references instead of many mixed references.
- Reduce the crop distance or make the face larger before changing identity text.
- Remove AU, fashion, or painterly language unless the user explicitly asked for it.
- Change only one thing between retries.

## Final image copies the lock image too much

- Keep the lock image as the first input only for identity.
- Add an explicit identity-only lock note to `M1` or `M11`.
- Strengthen `M7`, `M8`, `M9`, and `M10` so the final scene, crop, lighting, and
  finish come from the selected modules.
- Add `do not copy the lock image pose, crop, lighting, background, rendering
  finish, body emphasis, or composition` to `M12`.
- Do not regenerate a new lock unless the identity itself is wrong.

## Mixed-version drift

- Do not mix anime version references with original illustration references unless the user explicitly wants a hybrid.
- If mixed references slipped in, rebuild the reference pack using a single visual baseline.
