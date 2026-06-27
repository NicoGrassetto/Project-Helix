#!/usr/bin/env python3
"""Sync agent definitions from .github/agents into tool-native folders.

Source of truth: ``.github/agents/*.md`` (README.md is ignored).

For every source agent this script regenerates one file per target tool,
converting the shared markdown into that tool's native format:

* ``.claude/agents/<name>.md``    - Claude Code subagent (YAML frontmatter)
* ``.opencode/agents/<name>.md``  - opencode subagent (YAML frontmatter)
* ``.codex/prompts/<name>.md``    - Codex CLI custom prompt (plain markdown)

Files in the target folders that no longer have a matching source agent are
removed, so deleting a source agent cleanly deletes its generated copies.

The script is pure stdlib and idempotent: running it twice with no source
changes produces no diff.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

# Repository root = two levels up from this file (.github/scripts/sync_agents.py).
REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / ".github" / "agents"

# Files in the source folder that are not agent definitions.
SOURCE_IGNORE = {"README.md"}

# Marker placed at the top of every generated file so humans know not to edit
# them directly and tooling can recognise files it owns when pruning.
GENERATED_MARKER = "<!-- GENERATED FILE - DO NOT EDIT. Source: .github/agents/{name}.md -->"

# Default model hints per tool. Left as None to let each tool pick its default;
# adjust here if you want to pin specific models.
CLAUDE_MODEL: Optional[str] = None
OPENCODE_MODEL: Optional[str] = None


@dataclass
class Agent:
    """A parsed source agent definition."""

    name: str          # slug derived from the file name, e.g. "research-planner"
    title: str         # the level-1 heading, e.g. "Research Planner Agent"
    description: str    # one-line description used in frontmatter / headers
    body: str          # full original markdown body (without trailing whitespace)


def parse_agent(path: Path) -> Agent:
    """Parse a source markdown file into an :class:`Agent`."""
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not title:
        title = path.stem.replace("-", " ").title()

    description = _extract_description(lines)
    if not description:
        description = title

    return Agent(
        name=path.stem,
        title=title,
        description=description,
        body=raw.strip(),
    )


def _extract_description(lines: list[str]) -> str:
    """Return the first paragraph under the ``## Purpose`` heading.

    Falls back to an empty string when no Purpose section is present.
    """
    in_purpose = False
    collected: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if in_purpose:
                break  # reached the next section
            in_purpose = line[3:].strip().lower() == "purpose"
            continue
        if in_purpose:
            if line.strip() == "":
                if collected:
                    break  # end of the first paragraph
                continue
            collected.append(line.strip())
    return " ".join(collected).strip()


def _yaml_quote(value: str) -> str:
    """Quote a scalar for safe single-line YAML output."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_claude(agent: Agent) -> str:
    """Render a Claude Code subagent file."""
    front = ["---", f"name: {agent.name}", f"description: {_yaml_quote(agent.description)}"]
    if CLAUDE_MODEL:
        front.append(f"model: {CLAUDE_MODEL}")
    front.append("---")
    marker = GENERATED_MARKER.format(name=agent.name)
    return "\n".join(front) + "\n\n" + marker + "\n\n" + agent.body + "\n"


def render_opencode(agent: Agent) -> str:
    """Render an opencode subagent file."""
    front = ["---", f"description: {_yaml_quote(agent.description)}", "mode: subagent"]
    if OPENCODE_MODEL:
        front.append(f"model: {OPENCODE_MODEL}")
    front.append("---")
    marker = GENERATED_MARKER.format(name=agent.name)
    return "\n".join(front) + "\n\n" + marker + "\n\n" + agent.body + "\n"


def render_codex(agent: Agent) -> str:
    """Render a Codex CLI custom prompt file.

    Codex prompts are plain markdown with no required frontmatter, so the
    description is surfaced as an italicised header line above the body.
    """
    marker = GENERATED_MARKER.format(name=agent.name)
    header = f"_{agent.description}_"
    return marker + "\n\n" + header + "\n\n" + agent.body + "\n"


@dataclass
class Target:
    """A tool-specific output destination."""

    subdir: str                        # path relative to repo root
    renderer: Callable[[Agent], str]   # function turning an Agent into file text


TARGETS = [
    Target(".claude/agents", render_claude),
    Target(".opencode/agents", render_opencode),
    Target(".codex/prompts", render_codex),
]


def sync() -> bool:
    """Regenerate all target folders. Returns True if anything changed."""
    if not SOURCE_DIR.is_dir():
        print(f"Source directory not found: {SOURCE_DIR}", file=sys.stderr)
        return False

    agents = [
        parse_agent(path)
        for path in sorted(SOURCE_DIR.glob("*.md"))
        if path.name not in SOURCE_IGNORE
    ]
    expected_names = {agent.name for agent in agents}
    changed = False

    for target in TARGETS:
        out_dir = REPO_ROOT / target.subdir
        out_dir.mkdir(parents=True, exist_ok=True)

        for agent in agents:
            out_path = out_dir / f"{agent.name}.md"
            new_text = target.renderer(agent)
            old_text = out_path.read_text(encoding="utf-8") if out_path.exists() else None
            if old_text != new_text:
                out_path.write_text(new_text, encoding="utf-8")
                print(f"wrote {out_path.relative_to(REPO_ROOT)}")
                changed = True

        # Prune generated files whose source agent no longer exists.
        for stale in out_dir.glob("*.md"):
            if stale.stem not in expected_names and _is_generated(stale):
                stale.unlink()
                print(f"removed {stale.relative_to(REPO_ROOT)}")
                changed = True

    return changed


def _is_generated(path: Path) -> bool:
    """Only delete files this script created (identified by the marker)."""
    try:
        head = path.read_text(encoding="utf-8")[:200]
    except OSError:
        return False
    return "GENERATED FILE - DO NOT EDIT" in head


if __name__ == "__main__":
    did_change = sync()
    if not did_change:
        print("agents already in sync")
    sys.exit(0)
