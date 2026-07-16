"""
Pattern detection engine for Week 4.
Takes findings from the AST parser and checks whether the actual values
look like real secrets or just placeholders.
"""

import re

# Regex patterns that match known real secret formats
REAL_SECRET_PATTERNS = [
    ("AWS Access Key",    r"AKIA[0-9A-Z]{16}"),
    ("AWS Secret Key",    r"[A-Za-z0-9/+=]{40}"),
    ("GitHub Token",      r"gh[pso]_[A-Za-z0-9]{36}"),
    ("Stripe Key",        r"(sk|pk)_(test|live)_[A-Za-z0-9]{24,}"),
    ("JWT",               r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
    ("Generic Long Key",  r"[A-Za-z0-9+/!@#$%^&*\-_]{20,}"),
]

# Words that suggest a value is just a placeholder, not a real secret
PLACEHOLDER_WORDS = [
    "your", "here", "example", "todo", "change", "replace",
    "placeholder", "insert", "enter", "put", "add", "xxx",
    "test", "fake", "dummy", "sample", "demo"
]


def looks_like_placeholder(value):
    value_lower = value.lower()
    for word in PLACEHOLDER_WORDS:
        if word in value_lower:
            return True
    if value.startswith("<") and value.endswith(">"):
        return True
    return False


def check_value(value):
    if not value or len(value) < 6:
        return None
    if looks_like_placeholder(value):
        return None
    for name, pattern in REAL_SECRET_PATTERNS:
        if re.search(pattern, value):
            return name
    return None


def scan_file(filepath):
    from ast_parser import find_sensitive_nodes

    findings = find_sensitive_nodes(filepath)
    results = []

    for f in findings:
        value = f.get("value", "")
        match = check_value(value)
        results.append({
            "line": f["line"],
            "type": f["type"],
            "name": f["name"],
            "value": value,
            "pattern_match": match,
            "flagged": match is not None,
            "snippet": f["snippet"]
        })

    return results


def report(filepath, results):
    flagged = [r for r in results if r["flagged"]]
    print("\nFile: " + filepath)
    print("Total nodes found : " + str(len(results)))
    print("Flagged as real   : " + str(len(flagged)))
    if flagged:
        for r in flagged:
            print("  Line " + str(r["line"]) + " [" + r["type"] + "] " + r["name"])
            print("    Pattern : " + str(r["pattern_match"]))
            print("    Snippet : " + r["snippet"])
    else:
        print("  No real secrets detected.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pattern_detector.py <file.py>")
        sys.exit(1)
    for path in sys.argv[1:]:
        results = scan_file(path)
        report(path, results)
