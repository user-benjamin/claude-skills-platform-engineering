#!/usr/bin/env python3
"""Validate skills and shared templates for structural correctness.

Catches the classes of drift that have actually bitten us:
  - a skill that references a template which doesn't exist (broken `cat` lookup)
  - a template that no skill references (orphan)
  - SKILL.md frontmatter that's missing or whose name doesn't match the directory
  - a skill directory with no README.md (the CONTRIBUTING quality bar)

Errors fail CI (exit 1). Warnings are printed but don't fail (exit 0), so that
genuinely-optional drift (e.g. an orphan template kept as a scaffold) is
surfaced without blocking merges.

Run from anywhere: `python3 scripts/lint-skills.py`
No third-party dependencies — stdlib only.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
TEMPLATES_DIR = REPO_ROOT / "templates"

# Matches the shell-injection lookups skills use to inline a template, e.g.
#   !`cat ~/.claude/templates/adr.md`
TEMPLATE_REF = re.compile(r"~/\.claude/templates/([A-Za-z0-9._-]+\.md)")

errors: list[str] = []
warnings: list[str] = []


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Return the key/value pairs in a leading `---` fenced block, or None.

    Deliberately simple: this validates presence and exact-match of scalar
    fields like `name`, not full YAML. Anything fancier isn't needed here.
    """
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"FATAL: skills dir not found at {SKILLS_DIR}", file=sys.stderr)
        return 1

    referenced_templates: set[str] = set()
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

    if not skill_dirs:
        errors.append(f"no skill directories found under {SKILLS_DIR}")

    for skill in skill_dirs:
        name = skill.name
        skill_md = skill / "SKILL.md"
        readme = skill / "README.md"

        if not skill_md.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue

        if not readme.is_file():
            errors.append(f"{name}: missing README.md")

        text = skill_md.read_text(encoding="utf-8")

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{name}/SKILL.md: missing or malformed frontmatter block")
        else:
            if not fm.get("name"):
                errors.append(f"{name}/SKILL.md: frontmatter missing `name`")
            elif fm["name"] != name:
                errors.append(
                    f"{name}/SKILL.md: frontmatter name '{fm['name']}' "
                    f"does not match directory '{name}'"
                )
            if not fm.get("description"):
                errors.append(f"{name}/SKILL.md: frontmatter missing `description`")

        for ref in TEMPLATE_REF.findall(text):
            referenced_templates.add(ref)
            if not (TEMPLATES_DIR / ref).is_file():
                errors.append(
                    f"{name}/SKILL.md: references templates/{ref}, "
                    f"which does not exist"
                )

    # Orphan templates: present on disk but referenced by no skill. A warning,
    # not an error — a template may be kept deliberately as a scaffold.
    if TEMPLATES_DIR.is_dir():
        for tmpl in sorted(TEMPLATES_DIR.glob("*.md")):
            if tmpl.name not in referenced_templates:
                warnings.append(
                    f"templates/{tmpl.name}: not referenced by any skill (orphan)"
                )

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    checked = len(skill_dirs)
    print(
        f"\nChecked {checked} skill(s): "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
