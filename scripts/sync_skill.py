#!/usr/bin/env python3
"""Copy skills/pa-cafe/SKILL.md from the PA Cafe Agent Skills discovery index.

The single source is pa-cafe/pa-cafe public/.well-known/agent-skills/pa-cafe/SKILL.md,
served at <base>/.well-known/agent-skills/pa-cafe/SKILL.md and listed with a sha256
digest in <base>/.well-known/agent-skills/index.json
(https://github.com/cloudflare/agent-skills-discovery-rfc, v0.2.0).

Exit 0 with changed=false when the index is not published yet (404, or the site's
single-page fallback answering HTML). Exit 1 when the index or file is malformed or
the digest does not match, so nothing unverified is written.
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SKILL = "pa-cafe"
TARGET = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", SKILL, "SKILL.md"))


def output(**values):
    path = os.environ.get("GITHUB_OUTPUT")
    lines = [f"{key}={value}" for key, value in values.items()]
    if path:
        with open(path, "a") as f:
            f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "pa-cafe-plugin-sync"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.headers.get("Content-Type", ""), response.read()


def main():
    base = os.environ.get("PA_CAFE_BASE_URL", "https://pacafe.dnplus.dev").rstrip("/")
    index_url = f"{base}/.well-known/agent-skills/index.json"
    try:
        content_type, body = fetch(index_url)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        content_type, body = "", None
    if body is None or "application/json" not in content_type:
        print(f"::warning::{index_url} is not published yet (got {content_type or '404'}); nothing to sync")
        output(changed="false")
        return

    index = json.loads(body)
    entry = next((s for s in index.get("skills", []) if s.get("name") == SKILL), None)
    if not entry or entry.get("type") != "skill-md" or not str(entry.get("digest", "")).startswith("sha256:"):
        sys.exit(f"::error::{index_url} has no skill-md entry named {SKILL} with a sha256 digest")

    skill_url = urllib.parse.urljoin(index_url, entry["url"])
    _, skill = fetch(skill_url)
    digest = "sha256:" + hashlib.sha256(skill).hexdigest()
    if digest != entry["digest"]:
        sys.exit(f"::error::{skill_url} digest {digest} does not match the index ({entry['digest']})")
    head = skill.split(b"\n---\n", 1)[0].decode() + "\n"
    if not head.startswith("---\n") or f"\nname: {SKILL}\n" not in head:
        sys.exit(f"::error::{skill_url} has no frontmatter name: {SKILL}")

    with open(TARGET, "rb") as f:
        current = f.read()
    if current == skill:
        print(f"{TARGET} already matches {digest}")
        output(changed="false", digest=digest)
        return
    with open(TARGET, "wb") as f:
        f.write(skill)
    print(f"Updated {TARGET} from {skill_url} ({digest})")
    output(changed="true", digest=digest, source=skill_url)


if __name__ == "__main__":
    main()
