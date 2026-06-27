# src/repomind/prioritizer.py
from typing import Any

def calculate_impact(findings: dict[str, Any], criticality_multiplier: float = 1.5) -> float:
    """Calculate an architectural impact score based on findings metrics."""
    raw_score = findings.get("complexity", 0) + (findings.get("nesting", 0) * 2)
    return float(raw_score * criticality_multiplier)

def get_top_issues(all_findings: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    """Sort findings by the calculated impact score and return top results."""
    return sorted(all_findings, key=calculate_impact, reverse=True)[:limit]