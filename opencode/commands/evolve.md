---
description: Analyze instincts and suggest or generate evolved structures
agent: build
---

# Evolve Command

Analyze and evolve instincts in continuous-learning-v2: $ARGUMENTS

## Your Task

Run:

```bash
python3 "<path_to_skills>/continuous-learning-v2/scripts/instinct-cli.py" evolve $ARGUMENTS
```

`<path_to_skills>` maybe:

- `~/.agents/skills`
- `~/.config/opencode/skills`
- `./.agents/skills`
- ...

## Supported Args (v2.1)

- no args: analysis only
- `--generate`: also generate files under `evolved/{skills,commands,agents}`

## Behavior Notes

- Uses project + global instincts for analysis.
- Shows skill/command/agent candidates from trigger and domain clustering.
- Shows project -> global promotion candidates.
- With `--generate`, output path is:
  - project context: `<project_path>/evolved/`
