import ast

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # Base complexity is 1
        self.max_nesting = 0
        self.current_nesting = 0
        self.params = 0

    def visit_FunctionDef(self, node):
        self.params = len(node.args.args)
        self.generic_visit(node)

    def visit_If(self, node):
        self._increment_complexity_and_nesting(node)

    def visit_For(self, node):
        self._increment_complexity_and_nesting(node)

    def visit_While(self, node):
        self._increment_complexity_and_nesting(node)

    def _increment_complexity_and_nesting(self, node):
        self.complexity += 1
        self.current_nesting += 1
        self.max_nesting = max(self.max_nesting, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1

def analyze_function_body(source_code: str):
    try:
        tree = ast.parse(source_code)
        analyzer = FunctionAnalyzer()
        analyzer.visit(tree)
        return {
            "complexity": analyzer.complexity,
            "nesting": analyzer.max_nesting,
            "params": analyzer.params
        }
    except SyntaxError:
        return {"complexity": 0, "nesting": 0, "params": 0}