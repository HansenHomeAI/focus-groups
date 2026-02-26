# OpenClaw Orchestration (How to run Focus Groups)

This repo is intentionally **orchestrator-agnostic**.

It provides:
- a **run spec** format (`run_spec.json`)
- a **filesystem layout** for agent outputs (`agents/<k>/...`)
- a **compile** step to aggregate outputs (`REPORT.json`)

## Why

OpenClaw subagents are managed by Franklin/OpenClaw runtime (not by this CLI directly).
So the typical flow is:

1) Prepare a run folder:

```bash
focus-groups prep prompt.md --agents 10
# outputs a folder like .runs/20260226-120000
```

2) Franklin/OpenClaw spawns N subagents, each with:
- the same prompt + shared context pack
- explicit instructions to output structured JSON

3) Franklin writes the results into:

```
.runs/<run_id>/agents/<agent_id>/finding.json
.runs/<run_id>/agents/<agent_id>/finding.md
```

4) Franklin then runs a deliberation pass (either as another subagent, or as a single synthesis step) and writes:

```
.runs/<run_id>/deliberation/consensus.md
.runs/<run_id>/deliberation/dissent.md
.runs/<run_id>/deliberation/open_questions.md
```

5) Compile:

```bash
focus-groups compile .runs/<run_id>
```

## Artifact contract (recommended)

Each agent writes `finding.json` with:
- `agent_id`
- `role` (e.g. "sfm", "aws", "metrics", "skeptic")
- `findings_md`
- `citations` (URLs)
- `risks` (bullets)
- `recommendations` (bullets)

This keeps the deliberation grounded.
