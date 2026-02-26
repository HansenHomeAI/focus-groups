from __future__ import annotations

from pathlib import Path
from typing import Literal
from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    prompt: str
    agents: int = 10
    # NOTE: The harness is designed to be executed by an external orchestrator (e.g., OpenClaw)
    # that actually runs the agents. This repo stores the run spec + artifacts.
    mode: Literal["prep-only"] = "prep-only"
    context_paths: list[str] = Field(default_factory=list)


class AgentFinding(BaseModel):
    agent_id: str
    role: str
    findings_md: str
    citations: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class DeliberationOutput(BaseModel):
    consensus_md: str
    dissent_md: str = ""
    open_questions_md: str = ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
