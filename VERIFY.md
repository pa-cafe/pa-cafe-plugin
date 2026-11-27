# Local verification 2026-10-14 (Asia/Taipei)
- plugin.json vs agent-plugins 1.0.0 plugin.schema.json: PASS (jsonschema)
- mcp.json vs agent-plugins 1.0.0 mcp.schema.json: PASS
- .cursor-plugin/plugin.json vs cursor/plugins schemas/plugin.schema.json: PASS
- tools/list (Grok Bot authenticated MCP connection): 17 tools, names match README
- Unauthenticated POST /mcp/external: 401 + OAuth discovery; AS metadata has DCR, PKCE S256, auth method none
- Installed copy: ~/.cursor/plugins/local/pa-cafe (real dir, box)
- NOT proven: Cursor loader (@anysphere/cursor-plugins not on npm, no Cursor binary on box), Customize UI, logo render, OAuth inside Cursor, dual-manifest precedence in Cursor

# Update 2026-10-15
- README tool list rebuilt from server source (dnplus/pa-cafe@b609123): 31 tools.
  memory_* (removed in dnplus/pa-cafe#97) and team_* (removed in #99) are gone;
  notice_list / notice_post / notice_update added.
- Live tools/list NOT re-run: unauthenticated POST https://pacafe.dnplus.dev/mcp
  returns 401, and no authenticated connection was available.
