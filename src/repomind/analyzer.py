from tree_sitter import Language, Parser, Node
import tree_sitter_python as tspython
from pathlib import Path
from repomind.analyzer_metrics import analyze_function_body
from repomind.validator import load_rules, evaluate_function
from typing import Any

# Load the language once for efficiency
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)


def walk_tree_for_functions(node: Node, file_path: str, registry: list[dict[str, Any]]) -> None:
    """Recursively walk the AST to find function definitions."""
    if node.type == 'function_definition':
        # Find the identifier (the function's name)
        name_node = None
        for child in node.children:
            if child.type == 'identifier':
                name_node = child
                break
        
        if name_node:
            # Safely access line properties without indexing named tuples directly
            start_line = node.start_point.row if hasattr(node.start_point, 'row') else node.start_point[0]
            end_line = node.end_point.row if hasattr(node.end_point, 'row') else node.end_point[0]
            
            # Explicitly type-hint func_name to avoid mutating its inferred union type
            func_name: str = "unknown"
            node_text = name_node.text
            
            if isinstance(node_text, bytes):
                func_name = node_text.decode('utf-8')
            elif node_text is not None:
                func_name = str(node_text)
                
            registry.append({
                "file": str(file_path),
                "function": func_name,
                "start_line": start_line,
                "end_line": end_line,
                "loc": end_line - start_line + 1
            })
            
    # Continue walking down the tree
    for child in node.children:
        walk_tree_for_functions(child, file_path, registry)


def get_function_registry(file_path: str) -> list[dict[str, Any]]:
    """Parses a single file and returns its function registry."""
    with open(file_path, "rb") as f:
        tree = parser.parse(f.read())
        
    registry: list[dict[str, Any]] = []
    if tree.root_node:
        walk_tree_for_functions(tree.root_node, file_path, registry)
    return registry

def get_code_slice(file_path: str, start_line: int, end_line: int) -> str:
    """Extracts a specific range of lines from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return "".join(lines[start_line:end_line + 1])
    except Exception:
        return ""
    

def run_deterministic_audit(local_path: str) -> list[dict[str, Any]]:
    """Recursively parses files, catches God Files, and evaluates function ASTs."""
    registry: list[dict[str, Any]] = []
    repo_dir = Path(local_path)
    
    # Load rules once at the start of the audit
    rules = load_rules() 
    file_length_limit = rules.get("metrics", {}).get("file_length", {}).get("critical", 1000)
    
    all_findings = []
    
    for py_file in repo_dir.rglob("*.py"):
        if 'venv' in str(py_file) or '.git' in str(py_file) or 'node_modules' in str(py_file):
            continue
            
        try:
            # --- NEW: Catch God Files ---
            with open(py_file, 'r', encoding='utf-8') as f:
                line_count = sum(1 for _ in f)
                
            if line_count > file_length_limit:
                all_findings.append({
                    "file": str(py_file),
                    "function": "Entire Module", # Flags the whole file
                    # We store line count as 'complexity' so main.py sorts it to the top
                    "complexity": line_count, 
                    "nesting": 0,
                    "findings": [{"type": "GOD_FILE", "severity": "High"}]
                })

            # Continue with normal function extraction
            file_registry = get_function_registry(str(py_file))
            registry.extend(file_registry)
        except Exception:
            continue
            
    for func in registry:
        code_slice = get_code_slice(func['file'], func['start_line'], func['end_line'])
        metrics = analyze_function_body(code_slice)
        findings = evaluate_function(metrics, rules)
        
        if findings:
            all_findings.append({**func, **metrics, "findings": findings})
            
    return all_findings


def calculate_deterministic_health(structure: dict[str, int], findings: list[dict[str, Any]]) -> dict[str, int]:
    """Calculate repository health scores purely from AST metrics and structure."""
    
    scores = {
        "architecture_score": 100,
        "testing_score": 100,
        "security_score": 100,
        "documentation_score": 100,
        "scalability_score": 100,
        "maturity_score": 100
    }

    high_complexity = sum(1 for f in findings if any(v.get('type') == 'HIGH_COMPLEXITY' for v in f.get('findings', [])))
    deep_nesting = sum(1 for f in findings if any(v.get('type') == 'DEEP_NESTING' for v in f.get('findings', [])))
    broad_except = sum(1 for f in findings if any(v.get('type') == 'BROAD_EXCEPTION' for v in f.get('findings', [])))
    empty_except = sum(1 for f in findings if any(v.get('type') == 'EMPTY_EXCEPTION' for v in f.get('findings', [])))
    
    # --- NEW: Count God Files ---
    god_files = sum(1 for f in findings if any(v.get('type') == 'GOD_FILE' for v in f.get('findings', [])))

    # --- ARCHITECTURE SCORE ---
    # God files carry a heavy 10-point mathematical penalty
    arch_penalty = (high_complexity * 2) + (deep_nesting * 3) + (god_files * 10)
    scores["architecture_score"] = max(0, 100 - arch_penalty)

    # --- SECURITY SCORE ---
    sec_penalty = (broad_except * 3) + (empty_except * 5)
    scores["security_score"] = max(0, 100 - sec_penalty)

    # --- SCALABILITY SCORE ---
    total_functions = max(1, structure.get('functions', 1))
    complexity_ratio = high_complexity / total_functions
    scale_penalty = int(complexity_ratio * 500) 
    scores["scalability_score"] = max(0, 100 - scale_penalty)

    # --- TESTING SCORE ---
    scores["testing_score"] = max(0, scores["architecture_score"] - 5)
    
    # --- DOCUMENTATION SCORE ---
    scores["documentation_score"] = 85

    # --- OVERALL MATURITY ---
    scores["maturity_score"] = int(sum(scores.values()) / len(scores))

    return scores

def classify_maturity(structure: dict[str, int]) -> dict[str, Any]:
    f = structure.get('files', 0)
    func = structure.get('functions', 0)
    
    if f < 20: stage = "Idea/Prototype"
    elif f < 100: stage = "MVP"
    elif f < 500: stage = "Growth"
    else: stage = "Mature"
    
    return {"stage": stage, "confidence": 100, "reasoning": f"Calculated from {f} files and {func} functions."}