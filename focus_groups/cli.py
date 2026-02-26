from __future__ import annotations

import json
from pathlib import Path
import typer

app = typer.Typer(no_args_is_help=True)


@app.command()
def run(
    prompt_file: Path = typer.Argument(..., exists=True, dir_okay=False),
    agents: int = typer.Option(10, "--agents"),
    out_dir: Path = typer.Option(Path(".runs"), "--out"),
):
    """Run a focus group session (stub).

    v0 just writes a run manifest; next step is to spawn OpenClaw subagents.
    """
    prompt = prompt_file.read_text(encoding="utf-8")
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "prompt_file": str(prompt_file),
        "agents": agents,
        "status": "stub",
        "prompt_preview": prompt[:4000],
    }
    (out_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    typer.echo(f"Wrote {out_dir/'run_manifest.json'}")


if __name__ == "__main__":
    app()
