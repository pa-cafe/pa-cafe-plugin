#!/usr/bin/env python3
"""Fail when the README poll interval differs from the one in skills/pa-cafe/SKILL.md.

The number is INBOX_POLL_INTERVAL_SECONDS in pa-cafe/pa-cafe shared/domain.ts. The
skill copy is synced from PA Cafe, so it only has the rule after the cafe releases it.
Until then this prints a notice and exits 0.
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PATTERN = re.compile(r"once\s+every\s+(\d+)\s+seconds")


def intervals(relative):
    with open(os.path.join(ROOT, relative), encoding="utf-8") as f:
        return {int(n) for n in PATTERN.findall(f.read())}


def main():
    readme = intervals("README.md")
    if not readme:
        sys.exit("::error::README.md has no 'once every N seconds' poll rule")
    skill = intervals("skills/pa-cafe/SKILL.md")
    if not skill:
        print("::notice::skills/pa-cafe/SKILL.md does not have the poll rule yet; "
              "the daily sync brings it after PA Cafe releases it")
        return
    if readme != skill:
        sys.exit(f"::error::README.md says {sorted(readme)} seconds but skills/pa-cafe/SKILL.md says "
                 f"{sorted(skill)}; the source is INBOX_POLL_INTERVAL_SECONDS in pa-cafe/pa-cafe shared/domain.ts")
    print(f"README.md and skills/pa-cafe/SKILL.md both say once every {readme.pop()} seconds")


if __name__ == "__main__":
    main()
