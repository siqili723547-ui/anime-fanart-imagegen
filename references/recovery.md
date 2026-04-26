# Recovery Guide

Use this file when the result looks technically good but the character no longer reads correctly.

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
- Change only one thing between retries.

## Mixed-version drift

- Do not mix anime version references with original illustration references unless the user explicitly wants a hybrid.
- If mixed references slipped in, rebuild the reference pack using a single visual baseline.
