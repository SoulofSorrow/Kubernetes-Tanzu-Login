@AGENTS.md

## Claude Code specifics

- Project skills live in `.claude/skills/`. Invoke the matching skill before
  starting a task it covers.
- `.claude/settings.json` allows the `ast.parse` syntax check, asks before
  starting the GUI and denies reading `~/.kube/`.
