import ast

def extract_functions(code):
    tree = ast.parse(code)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
    return funcs

def safe_replace(original, new_code):
    try:
        ast.parse(new_code)
        return new_code
    except:
        print("❌ New code invalid — keeping original")
        return original
