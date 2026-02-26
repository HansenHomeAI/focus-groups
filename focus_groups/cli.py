from __future__ import annotations

import json
import time
from pathlib import Path

import typer

from .models import RunConfig, write_text

app = typer.Typer(no_args_is_help=True)


def _new_run_id() -> str:
    # Include milliseconds to avoid collisions when running prep repeatedly.
    return time.strftime("%Y%m%d-%H%M%S") + f"-{int((time.time() % 1)*1000):03d}"


@app.command()
def prep(
    prompt_file: Path = typer.Argument(..., exists=True, dir_okay=False),
    agents: int = typer.Option(10, "--agents"),
    out_root: Path = typer.Option(Path(".runs"), "--out"),
    context: list[Path] = typer.Option(None, "--context", exists=True),
):
    """Prepare a run folder + run_spec.json.

    This repo is intentionally 'orchestrator-agnostic': an external orchestrator
    (e.g., OpenClaw Franklin) runs the agents and writes artifacts into this folder.
    """
    run_id = _new_run_id()
    run_dir = out_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    prompt = prompt_file.read_text(encoding="utf-8")
    cfg = RunConfig(
        prompt=prompt,
        agents=agents,
        context_paths=[str(p) for p in (context or [])],
    )
    (run_dir / "run_spec.json").write_text(cfg.model_dump_json(indent=2), encoding="utf-8")

    write_text(run_dir / "PROMPT.md", prompt)
    write_text(run_dir / "README.md", f"# Focus Groups Run {run_id}\n\n- agents: {agents}\n")

    typer.echo(str(run_dir))


@app.command()
def compile(
    run_dir: Path = typer.Argument(..., exists=True, file_okay=False),
):
    """Compile artifacts into a single report (requires agent outputs present)."""
    agents_dir = run_dir / "agents"
    findings = []
    if agents_dir.exists():
        for p in sorted(agents_dir.glob("*/finding.json")):
            findings.append(json.loads(p.read_text(encoding="utf-8")))

    consensus = (run_dir / "deliberation" / "consensus.md").read_text(encoding="utf-8") if (run_dir / "deliberation" / "consensus.md").exists() else ""
    dissent = (run_dir / "deliberation" / "dissent.md").read_text(encoding="utf-8") if (run_dir / "deliberation" / "dissent.md").exists() else ""
    oq = (run_dir / "deliberation" / "open_questions.md").read_text(encoding="utf-8") if (run_dir / "deliberation" / "open_questions.md").exists() else ""

    report = {
        "run_dir": str(run_dir),
        "agents": findings,
        "consensus_md": consensus,
        "dissent_md": dissent,
        "open_questions_md": oq,
    }
    out = run_dir / "REPORT.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    typer.echo(str(out))


if __name__ == "__main__":
    app()
