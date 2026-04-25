# QA Checklist

Run this checklist before you call the output final.

## Identity

- Does the face read as the intended character immediately?
- Are hair style and hair color correct?
- Are eye color and eye shape close enough?
- Is the canonical outfit silhouette preserved?
- Are the dominant colors correct?
- Are the signature prop or accessory cues present when needed?

## Anatomy

- No extra limbs
- No extra fingers
- No extra eyes or broken facial structure
- No obvious proportion collapse

## Scene

- The face is still readable at the chosen composition size.
- Background complexity does not overpower the character.
- The user-requested mood and scene are present.
- The image is original in composition and not a copy of one reference image.

## Output Standard

- Profile matches the requested deliverable
- Size matches the selected profile or validated custom size
- Output format matches the deliverable request
- Metadata sidecar exists and records the model snapshot and sources

## Stop Conditions

Do not call the image final if:
- the lock image failed
- the final image no longer matches the lock image
- the character version drifted because references were mixed
