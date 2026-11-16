<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/bts-logo-white.svg">
    <img src="docs/brand/bts-logo.svg" alt="BTS" width="150">
  </picture>
</p>

<h1 align="center">BTS Plugin Marketplace</h1>

<p align="center">
  Plugins and skills for BTS teams that build with Claude Code and other AI agents.
</p>

<p align="center">
  <a href="https://github.com/BTS-USA/bts-plugin-marketplace/actions/workflows/test.yml"><img src="https://github.com/BTS-USA/bts-plugin-marketplace/actions/workflows/test.yml/badge.svg" alt="Tests"></a>
  <img src="https://img.shields.io/badge/Claude_Code-plugin_marketplace-CA1C68" alt="Claude Code plugin marketplace">
  <img src="https://img.shields.io/badge/Agent_Skills-compatible-24282B" alt="Agent Skills compatible">
</p>

<!-- project-info:start -->
## Project Info
- **What:** A Claude Code plugin marketplace. Each plugin is a set of agent skills.
- **Why:** Give BTS teams one place to install, pin and update the skills they use.
- **For:** BTS designers and developers who work with AI agents
- **By:** Joshua Duffill
- **Type:** Internal tool
- **Status:** Prototype
- **Last reviewed:** 2026-11-13
<!-- project-info:end -->

**Contents:** [Install](#install) · [Plugins](#plugins) · [Layout](#layout) · [Add a skill](#add-a-skill) ·
[Add a plugin](#add-a-plugin) · [Update a skill](#update-a-skill) · [Checks](#checks) · [Credits](#credits-and-licences)

---

## Install

### Claude Code

Add the marketplace one time. Then install the plugins that you want.

```
/plugin marketplace add BTS-USA/bts-plugin-marketplace
/plugin install bts-design@bts-plugin-marketplace
```

Claude Code 2.1.275 and later can do the two steps in one line:

```
/plugin install bts-design --marketplace BTS-USA/bts-plugin-marketplace
```

### Other agents

A skill is a folder with a `SKILL.md` file. Codex CLI, Gemini CLI, Cursor and other agents that support
Agent Skills can read the same folder. Copy the skill folder into the skills directory of your agent.

```bash
git clone https://github.com/BTS-USA/bts-plugin-marketplace.git
cp -r bts-plugin-marketplace/plugins/bts-design/skills/logo-design ~/.claude/skills/logo-design
```

---

## Plugins

| Plugin | Purpose | Skills |
| --- | --- | --- |
| [`bts-design`](plugins/bts-design) | Design work: identity, websites, motion, reviews and image references | 13 |

### bts-design

| Skill | Use it to | Needs | Upstream | Licence |
| --- | --- | --- | --- | --- |
| [`logo-design`](plugins/bts-design/skills/logo-design) | Design, review and deliver a logo. The skill covers the brief, the concepts, SVG construction, tests, a presentation board and brand guidelines. It includes a library of 1,400+ reference logos. | Python 3.9+ | [kaankiziltug/logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) | MIT |
| [`taste-skill`](plugins/bts-design/skills/taste-skill) | Build or redesign a website with art direction. The skill checks the page in a real browser. | Node 22+, Chrome or Edge | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | MIT |
| [`imagegen-frontend-web`](plugins/bts-design/skills/imagegen-frontend-web) | Make one reference image for each section of a website. | An agent that can generate images | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/imagegen-frontend-web) | MIT |
| [`imagegen-frontend-mobile`](plugins/bts-design/skills/imagegen-frontend-mobile) | Make screen concepts for a mobile app, shown in a phone frame. | An agent that can generate images | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/imagegen-frontend-mobile) | MIT |
| [`image-to-code-skill`](plugins/bts-design/skills/image-to-code-skill) | Make the design image first. Then build the page from the image. | An agent that can generate images | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/image-to-code-skill) | MIT |
| [`redesign-skill`](plugins/bts-design/skills/redesign-skill) | Audit a website or an app that exists. Then improve its design. | — | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/redesign-skill) | MIT |
| [`brandkit`](plugins/bts-design/skills/brandkit) | Make brand-kit boards, logo systems and identity decks as images. | An agent that can generate images | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/brandkit) | MIT |
| [`emil-design-eng`](plugins/bts-design/skills/emil-design-eng) | Apply rules for UI polish, component design and animation decisions. | — | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/emil-design-eng) | MIT |
| [`ui-animation`](plugins/bts-design/skills/ui-animation) | Implement, review and measure UI motion. Scripts measure the motion in a screen recording. | Python with `opencv-python`, `numpy`, `scipy`; `ffmpeg` (for the scripts only) | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/ui-animation) | MIT |
| [`review-animations`](plugins/bts-design/skills/review-animations) | Review animation code against a high standard. | — | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/review-animations) | MIT |
| [`web-design-guidelines`](plugins/bts-design/skills/web-design-guidelines) | Review UI code against the Web Interface Guidelines of Vercel. | — | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/web-design-guidelines) | MIT |
| [`reference-design-contract`](plugins/bts-design/skills/reference-design-contract) | Turn screenshots, URLs and notes into a `DESIGN.md` file. | — | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/reference-design-contract) | Apache-2.0 |
| [`pptx-html-fidelity-audit`](plugins/bts-design/skills/pptx-html-fidelity-audit) | Compare a `python-pptx` export with its HTML deck. Find the layout differences. | Python with `python-pptx` | [nexu-io/open-design](https://github.com/nexu-io/open-design/tree/main/skills/pptx-html-fidelity-audit) | Apache-2.0 |

---

## Layout

```
.claude-plugin/marketplace.json     the list of plugins
plugins/
  bts-design/
    .claude-plugin/plugin.json      the plugin manifest
    skills/
      logo-design/                  one folder for each skill
      taste-skill/
      ...                           13 skills in all
sources.json                        where each vendored skill comes from
tools/vendor_skill.py               copies the skills in sources.json from their upstream repos
tests/test_marketplace.py           checks that the files above agree
docs/brand/                         BTS logos for this README
```

A *vendored skill* is a copy of a skill folder from another repo. `sources.json` records the repo, the folder,
the branch, the commit and the git tree id of each copy.

---

## Add a skill

### From a GitHub repo

1. Add an entry to `sources.json`. The key is the name of the skill folder.

   ```json
   "frontend-design": {
     "plugin": "bts-design",
     "repo": "https://github.com/nexu-io/open-design",
     "path": "skills/frontend-design",
     "ref": "main"
   }
   ```

2. Run the script with the name of the skill.

   ```bash
   python tools/vendor_skill.py frontend-design
   ```

   The script copies the folder into `plugins/bts-design/skills/`. It also copies the licence of the repo if the
   skill folder has none. Then it writes the commit to `sources.json` as `sha`.

3. Add a row to the skill table in this README.
4. Run the [checks](#checks).

The script downloads only the folder that you name. A large repo is not a problem.

### A skill that BTS wrote

1. Put the skill folder in `plugins/<plugin>/skills/<skill-name>/`. The folder must contain a `SKILL.md` file
   with `name` and `description` in its frontmatter.
2. Do not add the skill to `sources.json`. The script replaces each folder that `sources.json` lists.
3. Add a row to the skill table in this README.

---

## Add a plugin

### A plugin in this repo

1. Create `plugins/<plugin-name>/.claude-plugin/plugin.json`. Use
   [`plugins/bts-design/.claude-plugin/plugin.json`](plugins/bts-design/.claude-plugin/plugin.json) as the example.
2. Add the plugin to `plugins` in [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json). Set
   `source` to `./plugins/<plugin-name>`.
3. Add skills to `plugins/<plugin-name>/skills/` as the section above shows.

The plugin manifests have no `version` field. Claude Code then uses the commit as the version. Thus each commit
on `main` is an update for the persons who installed the plugin.

### A plugin in a different repo

A plugin that is complete in its own repo needs no copy here. Add an entry to `plugins` in
`.claude-plugin/marketplace.json` that points to the repo.

```json
{
  "name": "example-plugin",
  "source": { "source": "github", "repo": "BTS-USA/example-plugin" },
  "description": "One sentence about the plugin."
}
```

---

## Update a skill

First, find the skills that changed in their upstream repos.

```bash
python tools/vendor_skill.py --check         # all the skills in sources.json
python tools/vendor_skill.py --check taste-skill
```

The check prints `UPDATE available` or `up to date` for each skill. Its exit code is 1 when a skill changed.
The check compares the skill folder only. A commit to a different part of the upstream repo is not an update.

Then copy the new version.

```bash
python tools/vendor_skill.py taste-skill     # one skill
python tools/vendor_skill.py                 # all the skills in sources.json
```

The script replaces the folder with the upstream folder at `ref`. Read the diff before you commit. Local edits
to a vendored skill do not survive an update.

---

## Checks

```bash
python -m unittest discover -s tests -v      # the same check that CI runs
claude plugin validate .                     # the manifest check of Claude Code
```

The tests make sure that:

- each folder in `plugins/` is in `marketplace.json` and has a manifest,
- each skill has a `SKILL.md` file with `name` and `description`,
- each entry in `sources.json` has a vendored folder, a commit and a licence file.

---

## Credits and licences

The skills in this marketplace are the work of their authors. BTS collects them here and does not change them.

- **logo-design** is by [kaankiziltug](https://github.com/kaankiziltug). This repo started as a fork of
  [logo-design-skill](https://github.com/kaankiziltug/logo-design-skill).
- **taste-skill** is by [Leonxlnx](https://github.com/Leonxlnx).
- The other skills come from the [open-design](https://github.com/nexu-io/open-design) collection by nexu-io.
  Their authors are Leonxlnx, Matt Pocock, Matthew Blode, Vercel Labs and nexu-io. The `LICENSE` file in each
  folder names the author.

Each skill folder contains its own `LICENSE` file. That file applies to that skill.

The logo library in `logo-design` contains trademarks of other companies. Read [TRADEMARKS.md](TRADEMARKS.md)
before you use them.
