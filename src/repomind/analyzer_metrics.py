import ast
from repomind.validator import check_try_node_exceptions

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self) -> None:
        self.complexity: int = 1  
        self.max_nesting: int = 0
        self.current_nesting: int = 0
        self.params: int = 0
        self.exceptions: list[str] = []
        self.depth: int = 0

    # FIX: Added standard function visitor
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.depth += 1
        if self.depth == 1:
            self.params = len(node.args.args)
            self.generic_visit(node)
        self.depth -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.depth += 1
        if self.depth == 1:
            self.params = len(node.args.args)
            self.generic_visit(node)
        self.depth -= 1

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