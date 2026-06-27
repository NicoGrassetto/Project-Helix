# Agent Catalog

This folder contains the agent definitions for Project Helix.

## Agent files
- infrastructure-setup.md — accompanies IT teams in deploying Azure Machine Learning compute infrastructure for scientists, walking through every Bicep parameter.

## Usage notes
- Keep outputs stored in version control when possible.

## Microsoft Learn MCP server
The `infrastructure-setup` agent grounds its parameter explanations in official
Microsoft documentation through the **Microsoft Learn MCP server**:

- Endpoint: `https://learn.microsoft.com/api/mcp` (remote, streamable HTTP, no auth)
- Tools: `microsoft_docs_search`, `microsoft_docs_fetch`, `microsoft_code_sample_search`

Project-level configuration is committed for the tools that support it:

- **Claude Code** -> `.mcp.json` (repo root)
- **opencode** -> `opencode.json` (repo root)

Codex reads MCP servers only from its global config. Add this to
`~/.codex/config.toml`:

```toml
[mcp_servers.microsoft-learn]
url = "https://learn.microsoft.com/api/mcp"
```

## Automatic sync to other tools
This folder is the single source of truth for agent definitions. On every push
to `main` that touches `.github/agents/**`, the `Sync agents` GitHub Actions
workflow (`.github/workflows/sync-agents.yml`) runs `.github/scripts/sync_agents.py`
to regenerate tool-native copies and commits them back to the branch:

- `.claude/agents/<name>.md` — Claude Code subagent (YAML frontmatter)
- `.opencode/agents/<name>.md` — opencode subagent (YAML frontmatter)
- `.codex/prompts/<name>.md` — Codex CLI custom prompt

Do not edit the generated files directly; they carry a `GENERATED FILE` marker
and are overwritten (or pruned, if the source agent is deleted) on each sync.
You can also run the script locally: `python .github/scripts/sync_agents.py`.
