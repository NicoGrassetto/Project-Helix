# Agent Catalog

This folder contains general-purpose agent definitions for Project Helix.

## Agent files
- research-planner.md
- literature-mapper.md
- data-readiness.md
- experiment-designer.md
- reproducibility.md
- compute-orchestrator.md
- results-interpreter.md
- visualization.md
- writing-copilot.md
- citation-claim-verifier.md
- peer-reviewer.md
- ethics-risk.md
- project-operations.md
- publication-packaging.md

## Suggested handoff order
1. research-planner.md
2. data-readiness.md
3. experiment-designer.md
4. compute-orchestrator.md
5. results-interpreter.md
6. writing-copilot.md
7. citation-claim-verifier.md
8. peer-reviewer.md
9. reproducibility.md
10. publication-packaging.md

## Usage notes
- These definitions are field-agnostic by design.
- Adapt inputs and guardrails per domain as needed.
- Keep outputs stored in version control when possible.

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
