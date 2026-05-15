"""Tests for scripts/skills-api.py — skill discovery + search.

skills-api uses module-level REPO_DIR (= cwd at import time). We patch the
constant before instantiating SkillsManager so the test reads our repo's
skills regardless of where pytest is invoked from.
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("api_mod", ROOT / "scripts" / "skills-api.py")
api = importlib.util.module_from_spec(spec)
sys.modules["api_mod"] = api
spec.loader.exec_module(api)


class TestSkillsManager:
    def setup_method(self):
        api.REPO_DIR = ROOT
        api.SKILLS_DIR = ROOT / "skills-test-target"
        api.STATS_FILE = ROOT / ".skills-stats.test.json"
        self.mgr = api.SkillsManager()

    def teardown_method(self):
        f = ROOT / ".skills-stats.test.json"
        if f.exists():
            f.unlink()

    def test_loads_some_skills(self):
        skills = self.mgr.get_all_skills()
        assert len(skills) >= 100, f"expected >=100 skills, got {len(skills)}"

    def test_skill_has_required_fields(self):
        s = self.mgr.get_all_skills()[0]
        assert s.name and s.category and s.path

    def test_categories_nonempty(self):
        cats = self.mgr.get_categories()
        assert len(cats) >= 20

    def test_search_returns_skill_list(self):
        results = self.mgr.search_skills("test-driven")
        assert isinstance(results, list)
        assert all(isinstance(r, api.Skill) for r in results)
