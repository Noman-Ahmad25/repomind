# src/repomind/prioritizer.py
from typing import Any

def calculate_impact(findings: dict[str, Any], criticality_multiplier: float = 1.5) -> float:
    """Calculate an architectural impact score based on findings metrics."""
    # Base score from metrics
    raw_score = findings["complexity"] + (findings["nesting"] * 2)
    
    # Scale by criticality
    return float(raw_score * criticality_multiplier)

def get_top_issues(all_findings: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    """Sort findings by the calculated impact score and return top results."""
    # Sort findings by the calculated impact score
    sorted_issues = sorted(
        all_findings, 
        key=lambda x: calculate_impact(x), 
        reverse=True
    )
    return sorted_issues[:limit]
