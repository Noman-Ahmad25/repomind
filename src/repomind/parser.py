from pathlib import Path
from typing import Dict
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

def count_node_types(node, target_type: str) -> int: # type: ignore
    """Recursively count specific AST nodes."""
    count = 1 if node.type == target_type else 0
    for child in node.children:
        count += count_node_types(child, target_type)
    return count

def analyze_repository_structure(local_path: str) -> Dict[str, int]:
    """Parse the repository and extract metadata using Tree-Sitter."""
    # Initialize the Python Tree-Sitter grammar
    py_language = Language(tspython.language())
    parser = Parser(py_language)
    
    class_count = 0
    function_count = 0
    file_count = 0
    
    repo_dir = Path(local_path)
    
    # Scan all Python files in the cloned repository
    for py_file in repo_dir.rglob("*.py"):
        # FIX: Exclude virtual environments and package directories
        if 'venv' in str(py_file) or '.git' in str(py_file) or 'node_modules' in str(py_file):
            continue
            
        file_count += 1
        try:
            content = py_file.read_bytes()
            tree = parser.parse(content)
            
            class_count += count_node_types(tree.root_node, "class_definition")
            function_count += count_node_types(tree.root_node, "function_definition")
        except Exception:
            # Skip unparseable files safely
            continue
        
    return {
        "files": file_count,
        "classes": class_count,
        "functions": function_count
    }