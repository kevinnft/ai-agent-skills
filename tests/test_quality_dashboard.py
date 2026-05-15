"""Tests for scripts/quality-dashboard.py.

QualityDashboard hits the GitHub API on init, so we don't construct it here.
We test imports, dataclass shapes, and the no-token sys.exit guard.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("qd_mod", ROOT / "scripts" / "quality-dashboard.py")
qd = importlib.util.module_from_spec(spec)
sys.modules["qd_mod"] = qd
spec.loader.exec_module(qd)


class TestImports:
    def test_module_loaded(self):
        for name in ("QualityDashboard", "HealthCheck", "Metrics", "QualityScore"):
            assert hasattr(qd, name), f"missing {name}"


class TestDataclasses:
    def test_health_check_constructable(self):
        hc = qd.HealthCheck(name="readme", status=True, message="exists", severity="info")
        assert hc.name == "readme" and hc.status is True

    def test_metrics_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(qd.Metrics)

    def test_quality_score_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(qd.QualityScore)


class TestNoTokenExits:
    def test_init_without_token_calls_sys_exit(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        with pytest.raises(SystemExit):
            qd.QualityDashboard("kevinnft/ai-agent-skills", token=None)
