import ast
from repomind.analyzer_metrics import FunctionAnalyzer

def test_function_complexity_and_nesting() -> None:
    """Ensure the AST analyzer correctly counts complexity and nesting depth."""
    
    # A fake python function with 1 loop and 1 nested if (Complexity: 3, Nesting: 2)
    source_code = """
def sample_function(x, y):
    for i in range(x):
        if i > y:
            print("Nested!")
    """
    
    # Parse the code into an AST tree
    tree = ast.parse(source_code)
    function_node = tree.body[0] # Get the 'sample_function' node
    
    # Run your analyzer!
    analyzer = FunctionAnalyzer()
    analyzer.visit(function_node)
    
    # Assert your deterministic math is flawless
    assert analyzer.params == 2        # (x, y)
    assert analyzer.complexity == 3    # Base(1) + For(1) + If(1)
    assert analyzer.max_nesting == 2   # For -> If