from __future__ import annotations

import argparse
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import List
from unittest import mock

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

import anime_fanart
import generate_from_lock
import image_gen_refs


def _write_file(path: Path, data: bytes | str = b"x") -> Path:
    payload = data.encode("utf-8") if isinstance(data, str) else data
    path.write_bytes(payload)
    return path


class AnimeFanartTests(unittest.TestCase):
    def test_default_model_is_gpt_image_2(self) -> None:
        self.assertEqual(anime_fanart.DEFAULT_MODEL, "gpt-image-2.0")

    def test_validate_size_uses_openai_constraints(self) -> None:
        self.assertEqual(anime_fanart._validate_size("1024x1536"), "1024x1536")
        self.assertEqual(anime_fanart._validate_size("auto"), "auto")
        with self.assertRaises(SystemExit):
            anime_fanart._validate_size("1025x1024")

    def test_check_prompt_identity_conflict_is_detected(self) -> None:
        prompt_ok = "Character: Asuka Langley Soryu from Neon Genesis Evangelion\nstyle: sharp anime render"
        anime_fanart._check_prompt_identity(prompt_ok, "Asuka Langley Soryu", "Neon Genesis Evangelion")
        conflict = "Character: Rei Ayanami from Neon Genesis Evangelion"
        with self.assertRaises(SystemExit):
            anime_fanart._check_prompt_identity(
                conflict, "Asuka Langley Soryu", "Neon Genesis Evangelion"
            )

    def test_missing_openai_api_key_guard(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            anime_fanart._ensure_api_key(dry_run=True)
            with self.assertRaises(SystemExit):
                anime_fanart._ensure_api_key(dry_run=False)

    def test_execute_generation_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            image = _write_file(td_path / "input.png", b"img")
            output = td_path / "out.png"

            status = anime_fanart._execute_generation(
                command="generate",
                character="Asuka Langley Soryu",
                series="Neon Genesis Evangelion",
                prompt="heroic anime scene",
                image_paths=[image],
                output_path=output,
                profile_name="poster-safe",
                size="1024x1536",
                quality="high",
                output_format="png",
                model=anime_fanart.DEFAULT_MODEL,
                moderation="auto",
                output_compression=None,
                dry_run=True,
                max_attempts=1,
                force=True,
            )
            self.assertEqual(status, 0)
            self.assertFalse(output.exists())

    def test_anime_fanart_generate_honors_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            image = _write_file(td_path / "input.png", b"img")
            output = td_path / "generate.png"
            args = argparse.Namespace(
                character="Asuka Langley Soryu",
                series="Neon Genesis Evangelion",
                image=[str(image)],
                identity_notes=None,
                prompt="heroic anime scene",
                prompt_file=None,
                profile="poster-safe",
                size=None,
                quality=None,
                output_format=None,
                output_compression=None,
                model=anime_fanart.DEFAULT_MODEL,
                moderation="auto",
                out=str(output),
                dry_run=True,
                force=True,
                max_attempts=1,
                lock_image=None,
            )
            with mock.patch("anime_fanart._execute_generation", return_value=0) as mock_exec:
                status = anime_fanart._cmd_generate(args)
                self.assertEqual(status, 0)
                self.assertTrue(mock_exec.call_args.kwargs["dry_run"])


class ImageGenRefsTests(unittest.TestCase):
    def test_image_gen_refs_main_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            image = _write_file(td_path / "input.png", b"img")
            output = td_path / "out.png"

            argv: List[str] = [
                "prog",
                "--image",
                str(image),
                "--prompt",
                "anime hero with neon lighting",
                "--out",
                str(output),
                "--dry-run",
                "--force",
            ]

            with mock.patch.object(sys, "argv", argv):
                with mock.patch(
                    "image_gen_refs._reference_paths", return_value=[image]
                ):
                    with mock.patch(
                        "image_gen_refs._read_prompt",
                        return_value="anime hero with neon lighting",
                    ):
                        with mock.patch(
                            "image_gen_refs._profile_for_args",
                            return_value={
                                "profile": "poster-safe",
                                "size": "1024x1536",
                                "quality": "high",
                                "output_format": "png",
                            },
                        ):
                            with mock.patch.object(
                                image_gen_refs, "_resolve_output_path", return_value=output
                            ):
                                with mock.patch(
                                    "image_gen_refs._execute_generation",
                                    return_value=0,
                                ) as mock_exec:
                                    status = image_gen_refs.main()
                                    self.assertEqual(status, 0)
                                    self.assertTrue(mock_exec.call_args.kwargs["dry_run"])


class GenerateFromLockTests(unittest.TestCase):
    def test_image_lock_is_first_and_unique(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            lock = _write_file(td_path / "lock.png", b"img")
            extra1 = _write_file(td_path / "ref1.png", b"img")
            extra2 = _write_file(td_path / "ref2.png", b"img")

            lock_path, ordered = generate_from_lock._image_paths_with_lock(
                str(lock), [str(extra1), str(lock), str(extra2)]
            )
            self.assertEqual(lock_path, lock)
            self.assertEqual(ordered, [lock, extra1, extra2])

    def test_generate_from_lock_main_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            lock = _write_file(td_path / "lock.png", b"img")
            ref = _write_file(td_path / "ref.png", b"img")
            output = td_path / "final.png"

            argv: List[str] = [
                "prog",
                "--character",
                "Asuka Langley Soryu",
                "--series",
                "Neon Genesis Evangelion",
                "--lock-image",
                str(lock),
                "--image",
                str(ref),
                "--prompt",
                "character: Asuka Langley Soryu from Neon Genesis Evangelion, full scene",
                "--out",
                str(output),
                "--dry-run",
                "--force",
            ]

            with mock.patch.object(sys, "argv", argv):
                with mock.patch(
                    "generate_from_lock._final_prompt",
                    return_value="character: Asuka Langley Soryu from Neon Genesis Evangelion, full scene",
                ):
                    with mock.patch(
                        "generate_from_lock._profile_for_args",
                        return_value={
                            "profile": "poster-safe",
                            "size": "1024x1536",
                            "quality": "high",
                            "output_format": "png",
                        },
                    ):
                        with mock.patch.object(
                            generate_from_lock, "_resolve_output_path", return_value=output
                        ):
                            with mock.patch(
                                "generate_from_lock._read_prompt",
                                return_value="character: Asuka Langley Soryu from Neon Genesis Evangelion, full scene",
                            ):
                                with mock.patch(
                                    "generate_from_lock._execute_generation",
                                    return_value=0,
                                ) as mock_exec:
                                    status = generate_from_lock.main()
                                    self.assertEqual(status, 0)
                                    self.assertTrue(mock_exec.call_args.kwargs["dry_run"])
                                    self.assertEqual(
                                        mock_exec.call_args.kwargs["image_paths"][0], lock
                                    )


if __name__ == "__main__":
    unittest.main()
