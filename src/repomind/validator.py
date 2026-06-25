# src/repomind/validator.py
import json
import ast
from typing import Any

def load_rules(config_path: str = "rules.json") -> dict[str, Any]:
    with open(config_path, "r") as f:
        return dict(json.load(f))

def evaluate_function(metrics: dict[str, Any], rules: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    
    # Check complexity
    if metrics["complexity"] > rules["metrics"]["complexity"]["critical"]:
        findings.append({"type": "HIGH_COMPLEXITY", "severity": "High"})
        
    # Check nesting
    if metrics["nesting"] > rules["metrics"]["nesting"]["critical"]:
        findings.append({"type": "DEEP_NESTING", "severity": "High"})
        
    # --- NEW: Check Security Exceptions ---
    flaws = metrics.get("exception_flaws", [])
    for flaw in flaws:
        if flaw == "BROAD_EXCEPTION":
            findings.append({"type": "BROAD_EXCEPTION", "severity": "Medium"})
        elif flaw == "EMPTY_EXCEPTION":
            findings.append({"type": "EMPTY_EXCEPTION", "severity": "High"})
            
    return findings

def check_try_node_exceptions(node: ast.Try, findings_list: list[str]) -> None:
    """Helper utility to check for bad exception handling patterns within Try blocks."""
    # Check for broad exceptions: except Exception:
    for handler in node.handlers:
        if isinstance(handler.type, ast.Name) and handler.type.id == 'Exception':
            findings_list.append("BROAD_EXCEPTION")
        # Check for empty exceptions: except: pass
        if not handler.type and any(isinstance(child, ast.Pass) for child in handler.body):
            findings_list.append("EMPTY_EXCEPTION")
