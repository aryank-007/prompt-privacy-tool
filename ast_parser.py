"""
AST parser that finds sensitive variable names in Python source code.
Uses Python's built-in ast module - no external libraries needed.
"""

import ast

# Names that suggest a variable holds sensitive information
SENSITIVE_WORDS = [
    "api_key", "api_secret", "apikey",
    "password", "passwd", "pwd",
    "secret", "secret_key",
    "token", "access_token", "auth_token",
    "credential", "credentials",
    "private_key",
    "client_secret",
    "db_password",
    "aws_secret", "aws_access_key",
    "auth",
]


def is_sensitive(name):
    name = name.lower()
    for word in SENSITIVE_WORDS:
        if word in name:
            return True
    return False


def find_sensitive_nodes(filepath):
    with open(filepath, "r") as f:
        source = f.read()

    lines = source.splitlines()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        print("Could not parse " + filepath)
        return []

    findings = []

    for node in ast.walk(tree):

        # Variable assignments: api_key = "abc123"
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and is_sensitive(target.id):
                    value = ""
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        value = node.value.value
                    findings.append({
                        "line": node.lineno,
                        "type": "Assignment",
                        "name": target.id,
                        "value": value,
                        "snippet": lines[node.lineno - 1].strip()
                    })

        # Annotated assignments: api_key: str = "abc123"
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and is_sensitive(node.target.id):
                value = ""
                if node.value and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    value = node.value.value
                findings.append({
                    "line": node.lineno,
                    "type": "Annotated Assignment",
                    "name": node.target.id,
                    "value": value,
                    "snippet": lines[node.lineno - 1].strip()
                })

        # Dictionary keys: {"password": "hunter2"}
        elif isinstance(node, ast.Dict):
            for i, key in enumerate(node.keys):
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    if is_sensitive(key.value):
                        value = ""
                        val_node = node.values[i]
                        if isinstance(val_node, ast.Constant) and isinstance(val_node.value, str):
                            value = val_node.value
                        findings.append({
                            "line": key.lineno,
                            "type": "Dict Key",
                            "name": key.value,
                            "value": value,
                            "snippet": lines[key.lineno - 1].strip()
                        })

        # os.getenv() and os.environ.get() calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("getenv", "get", "environ"):
                    findings.append({
                        "line": node.lineno,
                        "type": "Env Access",
                        "name": node.func.attr,
                        "value": "",
                        "snippet": lines[node.lineno - 1].strip()
                    })
            if isinstance(node.func, ast.Name) and node.func.id == "load_dotenv":
                findings.append({
                    "line": node.lineno,
                    "type": "Env File Load",
                    "name": "load_dotenv",
                    "value": "",
                    "snippet": lines[node.lineno - 1].strip()
                })

        # Function parameters: def login(password, api_key):
        elif isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if is_sensitive(arg.arg):
                    findings.append({
                        "line": node.lineno,
                        "type": "Function Param",
                        "name": arg.arg,
                        "value": "",
                        "snippet": lines[node.lineno - 1].strip()
                    })

    return findings
