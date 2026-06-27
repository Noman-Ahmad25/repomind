from pathlib import Path
import ast
from typing import Dict, Any, Callable, TypedDict  
from repomind.analyzer import get_function_registry, get_code_slice
from repomind.analyzer_metrics import analyze_function_body, UsageTracker, ImportVisitor
from repomind.validator import evaluate_function

# Add TypedDict

# Define a structured type for the context dictionary
class ProjectContext(TypedDict):
    languages: set[str]
    frameworks: set[str]
    project_type: str

class RepositoryScanner:
    def __init__(self, repo_path: str, rules: Dict[str, Any]):
        self.repo_path = Path(repo_path)
        self.rules = rules
        self.ignored_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".next"}
        
        self.findings: list[Dict[str, Any]] = []
        self.structure = {"files": 0, "functions": 0, "classes": 0}
        
        # FIX 1: Use the TypedDict instead of a generic Union dict
        self.context: ProjectContext = {
            "languages": set(),
            "frameworks": set(),
            "project_type": "Unknown"
        }
        
        # FIX 2: Add specific type arguments to Callable
        self.analyzers: Dict[str, Callable[[Path], None]] = {
            ".py": self._analyze_python,
        }

    def scan(self) -> None:
        """Walk the repository exactly once and route files dynamically."""
        for file_path in self.repo_path.rglob("*"):
            if any(part in self.ignored_dirs for part in file_path.parts):
                continue
                
            if file_path.is_file():
                ext = file_path.suffix.lower()
                
                # 1. Update Project Signature
                self._update_signature(file_path.name, ext)
                
                # 2. Route to AST Engine if supported
                if ext in self.analyzers:
                    self.structure["files"] += 1
                    try:
                        self.analyzers[ext](file_path)
                    except Exception:
                        continue
                        
        self._finalize_context()

    def _update_signature(self, filename: str, ext: str) -> None:
        """Build the ecosystem context."""
        if ext == ".py": 
            self.context["languages"].add("Python")
        if ext in [".js", ".jsx"]: 
            self.context["languages"].add("JavaScript")
        if filename == "package.json": 
            self.context["frameworks"].add("Node Ecosystem")
        if filename in ["requirements.txt", "pyproject.toml"]: 
            self.context["frameworks"].add("Python Ecosystem")

    def _finalize_context(self) -> None:
        """Determine project type based on collected evidence."""
        if "JavaScript" in self.context["languages"] and "Python" not in self.context["languages"]:
            self.context["project_type"] = "Frontend/Node"
        elif "Python" in self.context["languages"]:
            self.context["project_type"] = "Python Backend/Script"

    def _analyze_python(self, file_path: Path) -> None:
        """The Python-specific AST engine, God File detector, and Unused Import detector."""
        
        # 1. Read file and setup visitors
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                source_code = f.read()
            tree = ast.parse(source_code)
        except Exception:
            return

        # 2. Extract Imports (from ImportVisitor)
        import_visitor = ImportVisitor()
        import_visitor.visit(tree)
        imported_names = set(import_visitor.imports.keys())

        # 3. Track Usage (from UsageTracker)
        usage_tracker = UsageTracker()
        usage_tracker.visit(tree)
        used_names = usage_tracker.used_names

        # 4. Perform Set Subtraction: Detect Unused Imports
        # We filter out common internal names or standard boilerplate
        unused = imported_names - used_names
        for name in unused:
            self.findings.append({
                "file": str(file_path),
                "function": "Module Level",
                "complexity": 0,
                "nesting": 0,
                "findings": [{"type": "UNUSED_IMPORT", "severity": "Low", "detail": name}]
            })

        # 5. Existing Function Analysis logic...
        file_registry = get_function_registry(str(file_path))
        
        self.structure["functions"] += len(file_registry)
        
        for func in file_registry:
            code_slice = get_code_slice(func['file'], func['start_line'], func['end_line'])
            metrics = analyze_function_body(code_slice)
            findings = evaluate_function(metrics, self.rules)
            
            if findings:
                self.findings.append({**func, **metrics, "findings": findings})