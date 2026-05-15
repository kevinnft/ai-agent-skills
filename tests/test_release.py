"""Tests for scripts/release.py — semver + changelog logic."""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_mod", ROOT / "scripts" / "release.py")
release = importlib.util.module_from_spec(spec)
sys.modules["release_mod"] = release
spec.loader.exec_module(release)


class TestParseVersion:
    def test_simple(self):
        assert release.parse_version("1.2.3") == (1, 2, 3)

    def test_zero(self):
        assert release.parse_version("0.0.0") == (0, 0, 0)

    def test_extra_suffix_ignored(self):
        # regex is non-anchored — "1.2.3-rc1" still parses to (1,2,3)
        assert release.parse_version("1.2.3-rc1") == (1, 2, 3)

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            release.parse_version("not-a-version")


class TestBumpVersion:
    def test_patch(self):
        assert release.bump_version("1.2.3", "patch") == "1.2.4"

    def test_minor(self):
        assert release.bump_version("1.2.3", "minor") == "1.3.0"

    def test_major(self):
        assert release.bump_version("1.2.3", "major") == "2.0.0"

    def test_minor_resets_patch(self):
        assert release.bump_version("1.2.9", "minor") == "1.3.0"

    def test_major_resets_both(self):
        assert release.bump_version("3.7.4", "major") == "4.0.0"


class TestCategorizeCommits:
    def test_feat_in_features(self):
        commits = [{"hash": "abc", "message": "feat: new thing"}]
        cats = release.categorize_commits(commits)
        assert any(c["message"] == "feat: new thing" for c in cats["features"])

    def test_fix_in_fixes(self):
        commits = [{"hash": "abc", "message": "fix: a bug"}]
        cats = release.categorize_commits(commits)
        assert any(c["message"] == "fix: a bug" for c in cats["fixes"])

    def test_unknown_goes_to_other(self):
        commits = [{"hash": "abc", "message": "rewrite the universe"}]
        cats = release.categorize_commits(commits)
        assert any(c["message"] == "rewrite the universe" for c in cats["other"])

    def test_empty_input_yields_empty_buckets(self):
        cats = release.categorize_commits([])
        assert cats["features"] == [] and cats["fixes"] == []
