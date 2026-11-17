"""Checks that the marketplace, its plugins, their skills and sources.json agree with each other."""
import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vendor_skill  # noqa: E402


def load(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return json.load(fh)


class Marketplace(unittest.TestCase):
    def test_every_plugin_folder_is_listed_and_has_a_manifest(self):
        # A plugin with an object source lives in another repo and has no folder here.
        local = {p["name"]: p["source"] for p in load(".claude-plugin", "marketplace.json")["plugins"]
                 if isinstance(p["source"], str)}
        self.assertEqual(sorted(local), sorted(os.listdir(os.path.join(ROOT, "plugins"))))
        for name, source in local.items():
            self.assertEqual(source, f"./plugins/{name}")
            self.assertEqual(load("plugins", name, ".claude-plugin", "plugin.json")["name"], name)

    def test_every_skill_has_frontmatter(self):
        for plugin in os.listdir(os.path.join(ROOT, "plugins")):
            skills = os.path.join(ROOT, "plugins", plugin, "skills")
            for skill in os.listdir(skills) if os.path.isdir(skills) else []:
                with open(os.path.join(skills, skill, "SKILL.md"), encoding="utf-8") as fh:
                    text = fh.read()
                self.assertTrue(text.startswith("---"), skill)
                head = text.split("---", 2)[1]
                for key in ("name", "description"):
                    self.assertRegex(head, rf"(?m)^{key}:\s*\S", f"{plugin}/{skill}")

    def test_sources_match_the_vendored_skills(self):
        for name, src in load("sources.json").items():
            dest = vendor_skill.check(name, src)
            self.assertTrue(os.path.isfile(os.path.join(dest, "SKILL.md")), f"{name} is not vendored")
            for key in ("sha", "tree"):  # tree is what --check compares
                self.assertRegex(src.get(key, ""), r"^[0-9a-f]{40}$", f"{name}: run tools/vendor_skill.py {name}")
            self.assertTrue(any(f.upper().startswith(vendor_skill.LICENCE) for f in os.listdir(dest)),
                            f"{name} has no licence file")

    def test_check_rejects_unsafe_values(self):
        good = {"plugin": "bts-design", "repo": "https://github.com/o/r", "path": "skills/x", "ref": "main"}
        self.assertTrue(vendor_skill.check("x", good).endswith(os.path.join("bts-design", "skills", "x")))
        for key, bad in (("path", "../x"), ("path", "skills/../../x"), ("path", "/etc"), ("path", "-x"),
                         ("plugin", "../x"), ("repo", "--upload-pack=x"), ("repo", "ext::sh -c x"),
                         ("ref", "--x")):
            with self.assertRaises(ValueError, msg=f"{key}={bad}"):
                vendor_skill.check("x", {**good, key: bad})
        with self.assertRaises(ValueError):
            vendor_skill.check("../x", good)


if __name__ == "__main__":
    unittest.main()
