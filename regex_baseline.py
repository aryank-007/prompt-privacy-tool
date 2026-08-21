"""
Regex-only baseline for Week 9.
Scans files as plain text using regex patterns — no AST parsing.
Used to compare against the AST-driven approach.
"""

import re
import sys
import os

# Sensitive variable names to look for in assignments
SENSITIVE_NAMES = [
    "api_key", "api_secret", "apikey",
    "password", "passwd", "pwd",
    "secret", "secret_key",
    "token", "access_token", "auth_token",
    "credential", "credentials",
    "private_key", "client_secret",
    "db_password", "aws_secret", "aws_access_key",
    "account_secret",
]

# Known credential format patterns
CREDENTIAL_PATTERNS = [
    ("AWS Access Key",  r"AKIA[0-9A-Z]{16}"),
    ("AWS Secret Key",  r"[A-Za-z0-9/+=]{40}"),
    ("GitHub Token",    r"gh[pso]_[A-Za-z0-9]{36}"),
    ("Stripe Key",      r"(sk|pk)_(test|live)_[A-Za-z0-9]{24,}"),
    ("JWT",             r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"),
]


def scan_file(filepath):
    with open(filepath, "r") as f:
        text = f.read()

    findings = []

    # Pattern 1: sensitive_name = "value_of_6+_chars"
    for name in SENSITIVE_NAMES:
        pattern = name + r'\s*=\s*["\']([^"\']{6,})["\']'
        for match in re.finditer(pattern, text):
            findings.append({
                "type": "Name Match",
                "name": name,
                "value": match.group(1),
                "flagged": True,
            })

    # Pattern 2: known credential format anywhere in the file
    for cred_name, pattern in CREDENTIAL_PATTERNS:
        if re.search(pattern, text):
            findings.append({
                "type": "Credential Pattern",
                "name": cred_name,
                "value": "",
                "flagged": True,
            })

    return findings


def is_flagged(filepath):
    return len(scan_file(filepath)) > 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python regex_baseline.py <file.py>")
        sys.exit(1)
    for path in sys.argv[1:]:
        result = scan_file(path)
        print("File: " + path)
        print("Flagged: " + str(len(result) > 0))
        for r in result:
            print("  [" + r["type"] + "] " + r["name"])
