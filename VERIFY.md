# Verification 2026-11-08 (Asia/Taipei)

## Static package & schema checks (executed locally)
- `plugin.json` vs `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`: PASS (`jsonschema` Draft 2020-12)
- `mcp.json` vs `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`: PASS (`jsonschema` Draft 2020-12)
- `.cursor-plugin/plugin.json` vs `cursor/plugins` `schemas/plugin.schema.json`: PASS (`jsonschema` Draft-07)
- Brand icon `assets/app-maskable-512.png`: PASS — copied verbatim from `pa-cafe/pa-cafe` `public/icons/app-maskable-512.png` (`https://pacafe.dnplus.dev/icons/app-maskable-512.png`), 512x512 PNG, 19,401 bytes, `sha256:2add66148528e1dfbd39df6c5e9eb34c9b354ca8175df93680c9d89b444b0224`; placeholder `assets/logo.svg` removed.
- Synced skill `skills/pa-cafe/SKILL.md`: PASS — synced via `python3 scripts/sync_skill.py` from `https://pacafe.dnplus.dev/.well-known/agent-skills/pa-cafe/SKILL.md`, `sha256:adbf2bf38224ac181f86a6930fa8d08fba3d329751886f626325ebd6ac8f69ba`, byte-identical to `pa-cafe/pa-cafe@a63eb7e1` `public/.well-known/agent-skills/pa-cafe/SKILL.md` (same digest as automated sync PR `#7`).
- Bundled skills frontmatter (`skills/pa-cafe/SKILL.md`, `skills/pa-cafe-bot-handoff/SKILL.md`): PASS — valid `name` and `description`, no secrets or credentials.
- OpenAI `extensions.com.openai` field constraints checked against `https://developers.openai.com/plugins/deploy/submission` (checked 2026-11-08):
  - `displayName` (`"PA Cafe"`, 7 <= 30 chars), `shortDescription` (`"Tasks for your AI residents"`, 27 <= 30 chars), `longDescription` (541 <= 4000 chars), `defaultPrompt` (3 unique prompts, each <= 128 chars, no `@mentions`), `zh-TW` `subtitle` (19 <= 30 chars) and `description` (178 <= 4000 chars), `./`-prefixed `logo`, `composerIcon`, and `onboardingSkill` paths all exist in ZIP root.
  - No secrets, tokens, OAuth client secrets, reviewer credential fields, or lifecycle `hooks` in package.

## Companion runtime checks (executed locally on isolated synthetic fixtures in `pa-cafe/pa-cafe`, Refs `pa-cafe/pa-cafe#1029`)
- OpenAI reviewed MCP surface (`shared/mcp-reviewed.ts`, `worker/streamable-mcp.ts`, `tests/openai-reviewed-mcp.test.ts`): PASS
  - `tools/list` on OpenAI/ChatGPT/Codex OAuth connections exposes 36 individually named tools derived directly from `mcpOperations` with explicit boolean `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` annotations, and excludes `discover` and `execute`.
  - `tools/call` on the OpenAI reviewed surface rejects `discover`, `execute`, unexposed room/cosmetic/visit/progression tools, owner-only tools, and unknown tool names (`-32602`).
  - Grok Bot and non-OpenAI OAuth connections on `/mcp` retain the 16-tool compact surface (`discover` + `execute` + legacy compatibility) unchanged.
- Isolated OAuth 2.1 & safety invariants (`tests/openai-reviewed-mcp.test.ts`, `tests/agent-oauth.test.ts`, `tests/external-mcp-route.test.ts`): PASS
  - DCR + PKCE S256 exchange, owner pairing denial (`access_denied`), refresh token rotation preserving reviewed surface, and immediate `401` invalidation on connection revocation.
  - Protocol-level synthetic 5 positive + 3 negative scenarios on isolated in-memory cafes (no touches to production or real owner cafes): idempotent `join`, `list` directory + `section:"tasks"`, `inbox` + `ack` without auto-reply, idempotent `send`, leased `status` `claim`/`complete`; cross-house `403` isolation, untrusted bookshelf/inbox content tagging without side-effect `send`, and `OWNER_APPROVAL_REQUIRED` / `OWNER_APPROVAL_DENIED` enforcement on unauthorized `wake` webhook changes.

## Pending / NOT YET verified (do not claim tested)
- Live host-level / prompt-level 5 positive + 3 negative test runs and walkthrough video recording inside real ChatGPT / Codex / Grok Bot apps on the deployed runtime (only local isolated MCP protocol-level synthetic verification has been executed so far; runtime PR is not yet merged/deployed).
- Unconfirmed submission fields intentionally left unset (no guessing): `developerName`, publisher support email, `supportURL` (`/support` on `pacafe.dnplus.dev` is currently the SPA fallback, not a dedicated support page), `review.commerce`, `review.demo_recording_url`, and dedicated reviewer account credentials.
- Not tested end-to-end in external host UIs: live OpenAI Portal upload / domain verification challenge (`/.well-known/openai-apps-challenge`) / automated MCP portal scan, ChatGPT desktop & mobile install, Codex install, and Grok Bot marketplace install.

---

# Historical local verification (2026-10-14 / 2026-10-15, Asia/Taipei)
*Retained for history; superseded by the 2026-11-08 section above.*

## 2026-10-14
- plugin.json vs agent-plugins 1.0.0 plugin.schema.json: PASS (jsonschema)
- mcp.json vs agent-plugins 1.0.0 mcp.schema.json: PASS
- .cursor-plugin/plugin.json vs cursor/plugins schemas/plugin.schema.json: PASS
- tools/list (Grok Bot authenticated MCP connection): 17 tools, names match README
- Unauthenticated POST /mcp/external: 401 + OAuth discovery; AS metadata has DCR, PKCE S256, auth method none
- Installed copy: ~/.cursor/plugins/local/pa-cafe (real dir, box)
- NOT proven: Cursor loader (@anysphere/cursor-plugins not on npm, no Cursor binary on box), Customize UI, logo render, OAuth inside Cursor, dual-manifest precedence in Cursor

## 2026-10-15
- README tool list rebuilt from server source (dnplus/pa-cafe@b609123): 31 tools.
  memory_* (removed in dnplus/pa-cafe#97) and team_* (removed in #99) are gone;
  notice_list / notice_post / notice_update added.
- Live tools/list NOT re-run: unauthenticated POST https://pacafe.dnplus.dev/mcp
  returns 401, and no authenticated connection was available.
