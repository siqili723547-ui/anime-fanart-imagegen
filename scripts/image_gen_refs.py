#!/usr/bin/env python3
"""Generate an image from a prompt and local reference images.

This is a small, general-purpose wrapper around the image edit API. Use it when
the built-in chat `image_gen` tool is not enough because a local file must be
sent as a real image input.
"""

from __future__ import annotations

import argparse

from anime_fanart import (
    DEFAULT_MODEL,
    DEFAULT_MODERATION,
    SIZE_HELP,
    _execute_generation,
    _profile_help,
    _profile_for_args,
    _read_prompt,
    _reference_paths,
    _resolve_output_path,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an image using local reference images as real inputs"
    )
    parser.add_argument(
        "--image",
        action="append",
        required=True,
        help="Local reference image path. Repeat to provide multiple inputs.",
    )
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--profile", default="poster-safe", help=_profile_help())
    parser.add_argument("--size", help=SIZE_HELP)
    parser.add_argument("--quality")
    parser.add_argument("--output-format")
    parser.add_argument("--output-compression", type=int)
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=(
            "Image model to use (matches the workflow defaults; override with --model "
            "or ANIME_FANART_MODEL env var)."
        ),
    )
    parser.add_argument("--moderation", default=DEFAULT_MODERATION)
    parser.add_argument("--out", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=3)
    args = parser.parse_args()

    if args.max_attempts < 1 or args.max_attempts > 10:
        parser.error("--max-attempts must be between 1 and 10.")

    image_paths = _reference_paths(args.image)
    profile = _profile_for_args(
        args.profile,
        args.size,
        args.quality,
        args.output_format,
    )
    output_path = _resolve_output_path(args.out, profile["output_format"])
    prompt = _read_prompt(args.prompt, args.prompt_file)

    return _execute_generation(
        command="image-gen-refs",
        character="",
        series="",
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
    )


if __name__ == "__main__":
    raise SystemExit(main())
