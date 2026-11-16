#!/usr/bin/env python3
"""Copy the skills listed in sources.json from their upstream repos into plugins/<plugin>/skills/.

  python tools/vendor_skill.py                 # every skill in sources.json
  python tools/vendor_skill.py taste-skill     # the named skills only
  python tools/vendor_skill.py --check         # report the skills that changed upstream; exit 1 if any did

Each run replaces the skill folder with the upstream folder at `ref`. It writes the commit to sources.json
as `sha` and the git tree id of the folder as `tree`. --check compares `tree` with the upstream folder, so
a commit that does not touch the skill is not an update. Local edits to a vendored skill are lost, so
keep BTS-made skills out of sources.json.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "sources.json")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SAFE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9._/-]*$")  # cannot start with "-", so git never reads it as an option
LICENCE = ("LICENSE", "LICENCE", "COPYING")


def check(name, src):
    """Reject values that can leave plugins/ or reach git as an option. Return the destination folder."""
    for label, value in (("skill", name), ("plugin", src.get("plugin", ""))):
        if not NAME.match(value):
            raise ValueError(f"{label} name {value!r} must be kebab-case")
    path = src.get("path", "")
    if not SAFE.match(path) or ".." in path.split("/"):
        raise ValueError(f"{name}: path {path!r} must be a folder inside the repo, such as skills/{name}")
    if not SAFE.match(src.get("ref", "")):
        raise ValueError(f"{name}: ref {src.get('ref')!r} must be a branch or tag name")
    if not re.match(r"^https://[^\s]+$", src.get("repo", "")):
        raise ValueError(f"{name}: repo {src.get('repo')!r} must be an https:// URL")
    return os.path.join(ROOT, "plugins", src["plugin"], "skills", name)


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def clone(src, tmp, mode):
    # Shallow and blobless: a 300 MB repo costs only its file list, plus the one folder for a copy.
    git("clone", "--quiet", "--depth", "1", "--filter=blob:none", mode, "--branch", src["ref"], src["repo"], tmp)
    return git("rev-parse", f"HEAD:{src['path']}", cwd=tmp)


def changed(name, src):
    """True when the upstream folder is not the folder that sources.json records."""
    check(name, src)
    tmp = tempfile.mkdtemp(prefix="vendor-skill-")
    try:
        return clone(src, tmp, "--no-checkout") != src.get("tree")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def vendor(name, src):
    dest = check(name, src)
    tmp = tempfile.mkdtemp(prefix="vendor-skill-")
    try:
        tree = clone(src, tmp, "--sparse")
        git("sparse-checkout", "set", src["path"], cwd=tmp)
        upstream = os.path.join(tmp, *src["path"].split("/"))
        if not os.path.isfile(os.path.join(upstream, "SKILL.md")):
            raise ValueError(f"{name}: no SKILL.md at {src['path']} in {src['repo']} ({src['ref']})")
        shutil.rmtree(dest, ignore_errors=True)
        shutil.copytree(upstream, dest, symlinks=True)  # keep links as links: never read a file outside the clone
        # The licence must go with the copy. Use the repo's files when the skill folder has none.
        if not any(f.upper().startswith(LICENCE) for f in os.listdir(dest)):
            for f in os.listdir(tmp):
                if f.upper().startswith(LICENCE + ("NOTICE",)) and os.path.isfile(os.path.join(tmp, f)):
                    shutil.copy(os.path.join(tmp, f), dest)
        src["sha"], src["tree"] = git("rev-parse", "HEAD", cwd=tmp), tree
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(args):
    names = [a for a in args if a != "--check"]
    with open(SOURCES, encoding="utf-8") as fh:
        sources = json.load(fh)
    unknown = [n for n in names if n not in sources]
    if unknown:
        sys.exit(f"not in sources.json: {', '.join(unknown)}")
    stale = []
    for name in names or sorted(sources):
        try:
            if "--check" in args:
                if changed(name, sources[name]):
                    stale.append(name)
                print(f"{name}: {'UPDATE available' if name in stale else 'up to date'}")
                continue
            vendor(name, sources[name])
        except subprocess.CalledProcessError as err:
            sys.exit(f"{name}: git failed: {err.stderr.strip()}")
        except ValueError as err:
            sys.exit(str(err))
        with open(SOURCES, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(sources, fh, indent=2)
            fh.write("\n")
        print(f"{name}: {sources[name]['sha'][:12]} -> plugins/{sources[name]['plugin']}/skills/{name}")
    if stale:
        sys.exit(f"\nTo update: python tools/vendor_skill.py {' '.join(stale)}")


if __name__ == "__main__":
    main(sys.argv[1:])
