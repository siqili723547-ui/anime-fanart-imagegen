#!/usr/bin/env python3
"""Generate final art from an accepted local lock image.

This is the convenience entry point for the common workflow:

1. Pick an accepted identity/baseline image.
2. Send that file as the first real image input to the image edit API.
3. Generate the final poster, scene, avatar, or wallpaper from a prompt.

The lock image is identity-only evidence. It should keep the character from
drifting, while the written prompt remains responsible for the final pose,
scene, crop, lighting, mood, and finish.

Use --dry-run to verify that the lock image path is present in the request
payload before spending an API call.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from anime_fanart import (
    DEFAULT_MODEL,
    DEFAULT_MODERATION,
    SIZE_HELP,
    _die,
    _execute_generation,
    _final_prompt,
    _profile_for_args,
    _profile_help,
    _read_prompt,
    _reference_paths,
    _resolve_output_path,
)


def _image_paths_with_lock(
    lock_image: str, extra_images: Optional[Sequence[str]]
) -> Tuple[Path, List[Path]]:
    raw_paths = [lock_image, *(extra_images or [])]
    resolved = _reference_paths(raw_paths)
    lock_path = resolved[0]

    ordered: List[Path] = [lock_path]
    seen = {lock_path.resolve()}
    for path in resolved[1:]:
        real_path = path.resolve()
        if real_path in seen:
            continue
        seen.add(real_path)
        ordered.append(path)
    return lock_path, ordered


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an image while sending an accepted lock image as the first "
            "real image input to the OpenAI image edit API."
        )
    )
    parser.add_argument("--character", required=True)
    parser.add_argument("--series")
    parser.add_argument(
        "--lock-image",
        required=True,
        help=(
            "Accepted baseline/identity image. This is sent as image input #1 "
            "and treated as identity-only evidence."
        ),
    )
    parser.add_argument(
        "--image",
        action="append",
        help=(
            "Optional extra reference image path. Repeat to provide more inputs. "
            "These are sent after --lock-image."
        ),
    )
    parser.add_argument("--identity-notes")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--profile", default="poster-safe", help=_profile_help())
    parser.add_argument("--size", help=SIZE_HELP)
    parser.add_argument("--quality")
    parser.add_argument("--output-format")
    parser.add_argument("--output-compression", type=int)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--moderation", default=DEFAULT_MODERATION)
    parser.add_argument("--out", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()

    if args.max_attempts < 1 or args.max_attempts > 10:
        parser.error("--max-attempts must be between 1 and 10.")

    lock_image, image_paths = _image_paths_with_lock(args.lock_image, args.image)
    profile = _profile_for_args(
        args.profile,
        args.size,
        args.quality,
        args.output_format,
    )
    output_path = _resolve_output_path(args.out, profile["output_format"])
    if output_path.resolve() == lock_image.resolve():
        _die("--out must not overwrite --lock-image.")

    prompt = _final_prompt(
        _read_prompt(args.prompt, args.prompt_file),
        args.character,
        args.series or "",
        args.identity_notes,
        use_lock_image=True,
    )

    return _execute_generation(
        command="generate-from-lock",
        character=args.character,
        series=args.series or "",
        prompt=prompt,
        image_paths=image_paths,
        output_path=output_path,
        profile_name=profile["profile"],
        size=profile["size"],
        quality=profile["quality"],
        output_format=profile["output_format"],
        model=args.model,
        moderation=args.moderation,
        output_compression=args.output_compression,
        dry_run=args.dry_run,
        max_attempts=args.max_attempts,
        force=args.force,
        lock_image=lock_image,
    )


if __name__ == "__main__":
    raise SystemExit(main())
