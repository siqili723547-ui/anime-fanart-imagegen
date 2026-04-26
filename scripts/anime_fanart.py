#!/usr/bin/env python3
"""Reference-driven anime fanart workflow for GPT Image 2.

This CLI is intended for identity-sensitive fanart where the user wants a known
character to stay recognizable across prompt iterations.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

DEFAULT_MODEL = "gpt-image-2-2026-04-21"
DEFAULT_OUTPUT_FORMAT = "png"
DEFAULT_MODERATION = "auto"
LOCK_PROFILE = "square-2k"
MIN_PIXELS = 655_360
MAX_PIXELS = 8_294_400
MAX_EDGE = 3840
MAX_RATIO = 3.0
NON_EXPERIMENTAL_PIXEL_THRESHOLD = 2560 * 1440
MAX_REFERENCE_IMAGES = 16
MAX_IMAGE_BYTES = 50 * 1024 * 1024
ALLOWED_QUALITIES = {"low", "medium", "high", "auto"}
ALLOWED_OUTPUT_FORMATS = {"png", "jpeg", "jpg", "webp"}
DEFAULT_FINAL_CONSTRAINTS = (
    "preserve character identity and recognizability; preserve the canonical outfit "
    "silhouette unless the user explicitly asked for a new outfit; original composition; "
    "no watermark"
)


@dataclass(frozen=True)
class Profile:
    name: str
    size: str
    quality: str
    output_format: str


PROFILES: Dict[str, Profile] = {
    "preview": Profile("preview", "1024x1024", "medium", "png"),
    "poster-2k": Profile("poster-2k", "1440x2560", "high", "png"),
    "scene-2k": Profile("scene-2k", "2560x1440", "high", "png"),
    "square-2k": Profile("square-2k", "1920x1920", "high", "png"),
    "banner-2k": Profile("banner-2k", "3072x1024", "high", "png"),
    "poster-4k": Profile("poster-4k", "2160x3840", "high", "png"),
    "scene-4k": Profile("scene-4k", "3840x2160", "high", "png"),
    "banner-4k": Profile("banner-4k", "3840x1280", "high", "png"),
}


def _die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def _warn(message: str) -> None:
    print(f"Warning: {message}", file=sys.stderr)


def _dependency_hint() -> str:
    return "Install the OpenAI SDK in the active environment with `uv pip install openai`."


def _ensure_api_key(dry_run: bool) -> None:
    if os.getenv("OPENAI_API_KEY"):
        return
    if dry_run:
        _warn("OPENAI_API_KEY is not set; continuing because this is a dry run.")
        return
    _die("OPENAI_API_KEY is not set.")


def _create_client():
    try:
        from openai import OpenAI
    except ImportError:
        _die(f"openai SDK is not installed. {_dependency_hint()}")
    return OpenAI()


def _normalize_output_format(value: Optional[str]) -> str:
    fmt = (value or DEFAULT_OUTPUT_FORMAT).lower()
    if fmt not in ALLOWED_OUTPUT_FORMATS:
        _die("output format must be png, jpeg, jpg, or webp.")
    return "jpeg" if fmt == "jpg" else fmt


def _validate_quality(value: str) -> None:
    if value not in ALLOWED_QUALITIES:
        _die("quality must be one of low, medium, high, or auto.")


def _parse_size(size: str) -> Tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", size.strip().lower())
    if not match:
        _die("size must look like WIDTHxHEIGHT, for example 1440x2560.")
    return int(match.group(1)), int(match.group(2))


def _validate_size(size: str) -> None:
    width, height = _parse_size(size)
    if width % 16 != 0 or height % 16 != 0:
        _die("width and height must both be multiples of 16.")
    if max(width, height) > MAX_EDGE:
        _die(f"the longest edge must be <= {MAX_EDGE}.")
    ratio = max(width, height) / min(width, height)
    if ratio > MAX_RATIO:
        _die("the aspect ratio must be <= 3:1.")
    pixels = width * height
    if pixels < MIN_PIXELS or pixels > MAX_PIXELS:
        _die(
            f"total pixels must be between {MIN_PIXELS:,} and {MAX_PIXELS:,}."
        )


def _profile_for_args(profile_name: str, size_override: Optional[str], quality_override: Optional[str], output_format_override: Optional[str]) -> Dict[str, str]:
    if profile_name not in PROFILES:
        choices = ", ".join(sorted(PROFILES))
        _die(f"unknown profile {profile_name!r}. Choose one of: {choices}")
    profile = PROFILES[profile_name]
    size = size_override or profile.size
    quality = quality_override or profile.quality
    output_format = _normalize_output_format(output_format_override or profile.output_format)
    _validate_size(size)
    _validate_quality(quality)
    pixels = _parse_size(size)[0] * _parse_size(size)[1]
    if pixels > NON_EXPERIMENTAL_PIXEL_THRESHOLD:
        _warn(
            "this size is above the current non-experimental pixel threshold in the "
            "OpenAI image generation guide."
        )
    return {
        "profile": profile.name,
        "size": size,
        "quality": quality,
        "output_format": output_format,
    }


def _resolve_output_path(out: str, output_format: str) -> Path:
    path = Path(out)
    if path.suffix == "":
        path = path.with_suffix("." + output_format)
    return path


def _assert_writable(path: Path, force: bool) -> None:
    if path.exists() and not force:
        _die(f"output already exists: {path} (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)


def _reference_paths(paths: Iterable[str]) -> List[Path]:
    resolved: List[Path] = []
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            _die(f"reference image not found: {path}")
        if path.stat().st_size > MAX_IMAGE_BYTES:
            _die(f"reference image exceeds 50MB: {path}")
        resolved.append(path)
    if not resolved:
        _die("at least one --image is required for this workflow.")
    if len(resolved) > MAX_REFERENCE_IMAGES:
        _die(f"too many reference images; max is {MAX_REFERENCE_IMAGES}.")
    return resolved


def _read_prompt(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt and prompt_file:
        _die("use --prompt or --prompt-file, not both.")
    if prompt_file:
        path = Path(prompt_file)
        if not path.exists():
            _die(f"prompt file not found: {path}")
        text = path.read_text(encoding="utf-8").strip()
    else:
        text = (prompt or "").strip()
    if not text:
        _die("missing prompt.")
    return text


def _lock_prompt(character: str, series: str, identity_notes: Optional[str]) -> str:
    series_line = f" from {series}" if series else ""
    notes = f"\nIdentity anchors: {identity_notes}" if identity_notes else ""
    return (
        f"Use case: character-lock\n"
        f"Primary request: create a clean identity-lock image for {character}{series_line}\n"
        f"Style/medium: polished character art matching the canonical source visuals in the reference pack\n"
        f"Composition/framing: simple centered portrait or full-body neutral standing pose, plain or lightly graded background{notes}\n"
        f"Constraints: preserve recognizability; keep the canonical outfit silhouette; do not copy any single reference composition; no text; no watermark\n"
        f"Avoid: busy scenery, dramatic perspective distortion, face drift, random costume changes, anatomy errors"
    )


def _final_prompt(base_prompt: str, character: str, series: str, identity_notes: Optional[str]) -> str:
    identity_line = f"Identity anchors: {identity_notes}\n" if identity_notes else ""
    series_line = f" from {series}" if series else ""
    prompt_body = base_prompt.strip()
    if not re.search(r"(?im)^constraints\s*:", prompt_body):
        prompt_body = f"{prompt_body}\nConstraints: {DEFAULT_FINAL_CONSTRAINTS}"
    return (
        f"Character: {character}{series_line}\n"
        f"{identity_line}"
        f"{prompt_body}"
    )


def _open_binary_files(paths: Sequence[Path]) -> ExitStack:
    stack = ExitStack()
    handles = [stack.enter_context(path.open("rb")) for path in paths]
    stack.handles = handles  # type: ignore[attr-defined]
    return stack


def _decode_write_image(image_b64: str, output_path: Path) -> None:
    output_path.write_bytes(base64.b64decode(image_b64))


def _metadata_path(output_path: Path) -> Path:
    return output_path.with_suffix(output_path.suffix + ".json")


def _write_metadata(output_path: Path, metadata: Dict[str, Any], force: bool) -> None:
    sidecar = _metadata_path(output_path)
    _assert_writable(sidecar, force)
    sidecar.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def _request_metadata(
    *,
    command: str,
    character: str,
    series: str,
    profile: str,
    size: str,
    quality: str,
    output_format: str,
    prompt: str,
    model: str,
    output_path: Path,
    image_paths: Sequence[Path],
    lock_image: Optional[Path] = None,
) -> Dict[str, Any]:
    return {
        "command": command,
        "character": character,
        "series": series,
        "profile": profile,
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "model": model,
        "prompt": prompt,
        "output_path": str(output_path),
        "source_images": [str(path) for path in image_paths],
        "lock_image": str(lock_image) if lock_image else None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def _transient_error(exc: Exception) -> bool:
    name = exc.__class__.__name__.lower()
    message = str(exc).lower()
    if "ratelimit" in name or "rate_limit" in name or "429" in message:
        return True
    return "timeout" in name or "timeout" in message or "tempor" in name


def _retry_after(exc: Exception) -> float:
    for attr in ("retry_after", "retry_after_seconds"):
        value = getattr(exc, attr, None)
        if isinstance(value, (int, float)) and value > 0:
            return float(value)
    return 4.0


def _call_image_edit(
    *,
    model: str,
    prompt: str,
    image_paths: Sequence[Path],
    size: str,
    quality: str,
    output_format: str,
    moderation: str,
    output_compression: Optional[int],
    dry_run: bool,
    max_attempts: int,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": output_format,
        "moderation": moderation,
    }
    if output_compression is not None:
        if output_format == "png":
            _die("output compression is only valid for jpeg or webp outputs.")
        if not 0 <= output_compression <= 100:
            _die("output compression must be between 0 and 100.")
        payload["output_compression"] = output_compression

    if dry_run:
        payload["image"] = [str(path) for path in image_paths]
        return {"dry_run": True, "payload": payload}

    client = _create_client()
    with _open_binary_files(image_paths) as stack:
        request = dict(payload)
        request["image"] = stack.handles if len(stack.handles) > 1 else stack.handles[0]  # type: ignore[attr-defined]
        last_exc: Optional[Exception] = None
        for attempt in range(1, max_attempts + 1):
            try:
                return client.images.edit(**request)
            except Exception as exc:
                last_exc = exc
                if attempt == max_attempts or not _transient_error(exc):
                    raise
                wait_s = _retry_after(exc)
                _warn(
                    f"attempt {attempt}/{max_attempts} failed with {exc.__class__.__name__}; retrying in {wait_s:.1f}s"
                )
                time.sleep(wait_s)
        raise last_exc or RuntimeError("image edit failed")


def _execute_generation(
    *,
    command: str,
    character: str,
    series: str,
    prompt: str,
    image_paths: Sequence[Path],
    output_path: Path,
    profile_name: str,
    size: str,
    quality: str,
    output_format: str,
    model: str,
    moderation: str,
    output_compression: Optional[int],
    dry_run: bool,
    max_attempts: int,
    force: bool,
    lock_image: Optional[Path] = None,
) -> int:
    _assert_writable(output_path, force)
    payload_result = _call_image_edit(
        model=model,
        prompt=prompt,
        image_paths=image_paths,
        size=size,
        quality=quality,
        output_format=output_format,
        moderation=moderation,
        output_compression=output_compression,
        dry_run=dry_run,
        max_attempts=max_attempts,
    )
    metadata = _request_metadata(
        command=command,
        character=character,
        series=series,
        profile=profile_name,
        size=size,
        quality=quality,
        output_format=output_format,
        prompt=prompt,
        model=model,
        output_path=output_path,
        image_paths=image_paths,
        lock_image=lock_image,
    )
    if dry_run:
        metadata["dry_run_payload"] = payload_result["payload"]
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
        return 0

    _decode_write_image(payload_result.data[0].b64_json, output_path)
    _write_metadata(output_path, metadata, force)
    print(f"Wrote {output_path}")
    print(f"Wrote {_metadata_path(output_path)}")
    return 0


def _cmd_lock(args: argparse.Namespace) -> int:
    refs = _reference_paths(args.image)
    profile = _profile_for_args(args.profile, args.size, args.quality, args.output_format)
    output_path = _resolve_output_path(args.out, profile["output_format"])
    prompt = _lock_prompt(args.character, args.series, args.identity_notes)
    return _execute_generation(
        command="lock",
        character=args.character,
        series=args.series or "",
        prompt=prompt,
        image_paths=refs,
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


def _cmd_generate(args: argparse.Namespace) -> int:
    refs = _reference_paths(args.image)
    profile = _profile_for_args(args.profile, args.size, args.quality, args.output_format)
    output_path = _resolve_output_path(args.out, profile["output_format"])
    prompt = _final_prompt(
        _read_prompt(args.prompt, args.prompt_file),
        args.character,
        args.series or "",
        args.identity_notes,
    )
    lock_image = Path(args.lock_image) if args.lock_image else None
    if lock_image:
        if not lock_image.exists():
            _die(f"lock image not found: {lock_image}")
        refs = [lock_image, *refs]
    return _execute_generation(
        command="generate",
        character=args.character,
        series=args.series or "",
        prompt=prompt,
        image_paths=refs,
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


def _cmd_run(args: argparse.Namespace) -> int:
    refs = _reference_paths(args.image)
    lock_profile = _profile_for_args(args.lock_profile, None, None, None)
    lock_out = _resolve_output_path(args.lock_out, lock_profile["output_format"])
    lock_prompt = _lock_prompt(args.character, args.series, args.identity_notes)

    lock_result = _execute_generation(
        command="lock",
        character=args.character,
        series=args.series or "",
        prompt=lock_prompt,
        image_paths=refs,
        output_path=lock_out,
        profile_name=lock_profile["profile"],
        size=lock_profile["size"],
        quality=lock_profile["quality"],
        output_format=lock_profile["output_format"],
        model=args.model,
        moderation=args.moderation,
        output_compression=None,
        dry_run=args.dry_run,
        max_attempts=args.max_attempts,
        force=args.force,
    )
    if lock_result != 0:
        return lock_result

    final_profile = _profile_for_args(args.profile, args.size, args.quality, args.output_format)
    final_out = _resolve_output_path(args.out, final_profile["output_format"])
    final_prompt = _final_prompt(
        _read_prompt(args.prompt, args.prompt_file),
        args.character,
        args.series or "",
        args.identity_notes,
    )
    final_refs = [lock_out, *refs]
    return _execute_generation(
        command="run",
        character=args.character,
        series=args.series or "",
        prompt=final_prompt,
        image_paths=final_refs,
        output_path=final_out,
        profile_name=final_profile["profile"],
        size=final_profile["size"],
        quality=final_profile["quality"],
        output_format=final_profile["output_format"],
        model=args.model,
        moderation=args.moderation,
        output_compression=args.output_compression,
        dry_run=args.dry_run,
        max_attempts=args.max_attempts,
        force=args.force,
        lock_image=lock_out,
    )


def _add_shared_args(parser: argparse.ArgumentParser, *, require_prompt: bool) -> None:
    parser.add_argument("--character", required=True)
    parser.add_argument("--series")
    parser.add_argument("--image", action="append", required=True)
    parser.add_argument("--identity-notes")
    if require_prompt:
        parser.add_argument("--prompt")
        parser.add_argument("--prompt-file")
    parser.add_argument("--profile", default="poster-2k")
    parser.add_argument("--size")
    parser.add_argument("--quality")
    parser.add_argument("--output-format")
    parser.add_argument("--output-compression", type=int)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--moderation", default=DEFAULT_MODERATION)
    parser.add_argument("--out", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=3)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reference-driven anime fanart generation with GPT Image 2"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    lock_parser = subparsers.add_parser("lock", help="Create a clean character lock image")
    _add_shared_args(lock_parser, require_prompt=False)
    lock_parser.set_defaults(func=_cmd_lock, profile=LOCK_PROFILE)

    gen_parser = subparsers.add_parser("generate", help="Generate a final image from a prompt")
    _add_shared_args(gen_parser, require_prompt=True)
    gen_parser.add_argument("--lock-image")
    gen_parser.set_defaults(func=_cmd_generate)

    run_parser = subparsers.add_parser("run", help="Run lock and final generation in sequence")
    _add_shared_args(run_parser, require_prompt=True)
    run_parser.add_argument("--lock-profile", default=LOCK_PROFILE)
    run_parser.add_argument("--lock-out", required=True)
    run_parser.set_defaults(func=_cmd_run)

    args = parser.parse_args()
    _ensure_api_key(args.dry_run)
    if args.max_attempts < 1 or args.max_attempts > 10:
        _die("--max-attempts must be between 1 and 10.")
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
