import ast
from repomind.validator import check_try_node_exceptions
from typing import Union, List


class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.complexity: int = 1  
        self.max_nesting: int = 0
        self.current_nesting: int = 0
        self.params: int = 0
        self.exceptions: list[str] = []
        self.depth: int = 0

    def visit_FunctionDef(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> None:
        """Handles both standard and async function definitions."""
        self.depth += 1
        if self.depth == 1:
            self.params = len(node.args.args)
            self.generic_visit(node)
        self.depth -= 1

    # Dynamically map the async visitor to the standard visitor
    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_If(self, node: ast.If) -> None:
        self._increment_complexity_and_nesting(node)

    def visit_For(self, node: ast.For) -> None:
        self._increment_complexity_and_nesting(node)

    def visit_While(self, node: ast.While) -> None:
        self._increment_complexity_and_nesting(node)
        
    def visit_Try(self, node: ast.Try) -> None:
        self._increment_complexity_and_nesting(node)
        check_try_node_exceptions(node, self.exceptions)

    def _increment_complexity_and_nesting(self, node: ast.AST) -> None:
        self.complexity += 1
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1

def analyze_function_body(source_code: str) -> dict[str, int | list[str]]:
    try:
        tree = ast.parse(source_code)
        analyzer = FunctionAnalyzer()
        analyzer.visit(tree)
        return {
            "complexity": analyzer.complexity,
            "nesting": analyzer.max_nesting,
            "params": analyzer.params,
            "exception_flaws": analyzer.exceptions # Pass to the validator
        }
    except SyntaxError:
        return {"complexity": 0, "nesting": 0, "params": 0, "exception_flaws": []}
    

class ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        # Store a mapping of imported names
        self.imports: dict[str, str] = {} 

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            # Store the imported name (alias.asname if provided, else name)
            name = alias.asname or alias.name
            self.imports[name.split('.')[0]] = "Import"
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            for alias in node.names:
                name = alias.asname or alias.name
                self.imports[name] = node.module.split('.')[0]
        self.generic_visit(node)

class UsageTracker(ast.NodeVisitor):
    """Tracks all identifiers used in function bodies."""
    def __init__(self) -> None:
        self.used_names: set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        self.used_names.add(node.id)
        self.generic_visit(node)

def analyze_file_imports(source_code: str) -> List[str]:
    """Parse a file's AST and return a list of unique module dependencies."""
    try:
        tree = ast.parse(source_code)
        visitor = ImportVisitor()
        visitor.visit(tree)
        return list(visitor.imports)
    except SyntaxError:
        return []