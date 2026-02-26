from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


def _md_score(md: str) -> dict[str, int]:
    """Lightweight proxy metrics for 'truth-seeking' output quality.

    These are intentionally heuristic and cheap:
    - citations: count of URLs and explicit evidence-id refs
    - assumptions / uncertainty language
    - counterexamples / dissent markers
    - tests / falsifiers

    This is not a substitute for ground-truth evaluation.
    """
    url_count = len(re.findall(r"https?://\S+", md))
    evidence_refs = len(re.findall(r"\bE\d+\b|\bC-\d+\b|\bR-\d+\b", md))

    assumptions = len(re.findall(r"\bassum\w+\b", md, flags=re.IGNORECASE))
    uncertainty = len(re.findall(r"\b(confidence|uncertain|probab|likely|risk|could be wrong)\b", md, flags=re.IGNORECASE))
    counter = len(re.findall(r"\b(counterexample|counter-?evidence|devil|red team|steelman|minority|dissent)\b", md, flags=re.IGNORECASE))
    tests = len(re.findall(r"\b(falsif|test|experiment|measure|metric|gate|CI)\b", md, flags=re.IGNORECASE))

    return {
        "url_count": url_count,
        "evidence_refs": evidence_refs,
        "assumptions": assumptions,
        "uncertainty": uncertainty,
        "counter": counter,
        "tests": tests,
    }


def diff_reports(baseline: dict[str, Any], improved: dict[str, Any]) -> dict[str, Any]:
    base_cons = baseline.get("consensus_md", "") or ""
    imp_cons = improved.get("consensus_md", "") or ""

    base = _md_score(base_cons)
    imp = _md_score(imp_cons)

    delta = {k: imp[k] - base[k] for k in base}

    return {
        "baseline": base,
        "improved": imp,
        "delta": delta,
    }
