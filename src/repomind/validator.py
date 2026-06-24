# src/repomind/validator.py
import json

def load_rules(config_path="rules.json"):
    with open(config_path, "r") as f:
        return json.load(f)

def evaluate_function(metrics, rules):
    findings = []
    
    # Check complexity
    if metrics["complexity"] > rules["metrics"]["complexity"]["critical"]:
        findings.append({"type": "HIGH_COMPLEXITY", "severity": 10})
        
    # Check nesting
    if metrics["nesting"] > rules["metrics"]["nesting"]["critical"]:
        findings.append({"type": "DEEP_NESTING", "severity": 8})
        
    return findings

def visit_Try(self, node):
        # Check for broad exceptions: except Exception:
        for handler in node.handlers:
            if isinstance(handler.type, ast.Name) and handler.type.id == 'Exception':
                self.findings.append("BROAD_EXCEPTION")
            # Check for empty exceptions: except: pass
            if not handler.type and any(isinstance(child, ast.Pass) for child in handler.body):
                self.findings.append("EMPTY_EXCEPTION")
        self.generic_visit(node)