from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_DIR / "scripts" / "prepare_video.py"
SPEC = importlib.util.spec_from_file_location("prepare_video", SCRIPT_PATH)
PREPARE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(PREPARE)


class BrowserCookieResolutionTest(unittest.TestCase):
    def test_resolves_chrome_against_operator_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir)
            chrome_root = home / "Library" / "Application Support" / "Google" / "Chrome"
            chrome_root.mkdir(parents=True)

            result = PREPARE.resolve_browser_cookie_spec("chrome", home)

            self.assertEqual(result, f"chrome:{chrome_root}")

    def test_keeps_explicit_browser_spec(self) -> None:
        explicit = "chrome:/Users/example/Library/Application Support/Google/Chrome"
        self.assertEqual(PREPARE.resolve_browser_cookie_spec(explicit), explicit)


class DownloadAttemptEvidenceTest(unittest.TestCase):
    def test_preserves_cookie_and_anonymous_errors_separately(self) -> None:
        failures = [
            subprocess.CompletedProcess([], 1, "", "cookie database not found"),
            subprocess.CompletedProcess([], 1, "", "fresh cookies needed"),
        ]
        with tempfile.TemporaryDirectory() as temp_dir, patch.object(
            PREPARE.shutil, "which", return_value="/usr/local/bin/yt-dlp"
        ), patch.object(PREPARE, "resolve_browser_cookie_spec", return_value="chrome:/real/profile"), patch.object(
            PREPARE, "run", side_effect=failures
        ):
            result = PREPARE.prepare_url(
                "https://www.douyin.com/video/123",
                Path(temp_dir),
                no_download=False,
                cookies_browser="chrome",
            )

        self.assertFalse(result["ok"])
        self.assertEqual(result["cookies_browser"], "chrome:/real/profile")
        self.assertEqual(result["attempts"][0]["error"], "cookie database not found")
        self.assertEqual(result["attempts"][1]["error"], "fresh cookies needed")


if __name__ == "__main__":
    unittest.main()
