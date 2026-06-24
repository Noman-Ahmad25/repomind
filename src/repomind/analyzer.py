from tree_sitter import Language, Parser
import tree_sitter_python as tspython

# Load the language once for efficiency
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def walk_tree_for_functions(node, file_path, registry):
    """Recursively walk the AST to find function definitions."""
    if node.type == 'function_definition':
        # Find the identifier (the function's name)
        name_node = None
        for child in node.children:
            if child.type == 'identifier':
                name_node = child
                break
        
        if name_node:
            start_line = node.start_point[0]
            end_line = node.end_point[0]
            
            # Handle text decoding safely across tree-sitter versions
            func_name = name_node.text
            if isinstance(func_name, bytes):
                func_name = func_name.decode('utf-8')
                
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

def get_function_registry(file_path: str):
    """Parses a single file and returns its function registry."""
    with open(file_path, "rb") as f:
        tree = parser.parse(f.read())
        
    registry = []
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