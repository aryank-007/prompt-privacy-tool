"""
Redaction layer for Week 5.
Takes a Python source file, detects real secrets using the pattern detector,
and returns a sanitized version with secrets replaced by safe placeholders.
"""

import os
import sys
from pattern_detector import scan_file


def get_placeholder(name):
    name = name.lower()
    if "password" in name or "passwd" in name or "pwd" in name:
        return "[REDACTED_PASSWORD]"
    if "api_key" in name or "apikey" in name:
        return "[REDACTED_API_KEY]"
    if "token" in name:
        return "[REDACTED_TOKEN]"
    if "aws" in name:
        return "[REDACTED_AWS_CREDENTIAL]"
    if "private_key" in name:
        return "[REDACTED_PRIVATE_KEY]"
    if "secret" in name:
        return "[REDACTED_SECRET]"
    if "credential" in name:
        return "[REDACTED_CREDENTIAL]"
    if "auth" in name:
        return "[REDACTED_AUTH]"
    return "[REDACTED_SECRET]"


def redact_source(source, findings):
    redacted = source
    for f in findings:
        if not f["flagged"] or not f["value"]:
            continue
        value = f["value"]
        placeholder = get_placeholder(f["name"])
        redacted = redacted.replace('"' + value + '"', '"' + placeholder + '"')
        redacted = redacted.replace("'" + value + "'", "'" + placeholder + "'")
    return redacted


def redact_file(filepath):
    with open(filepath, "r") as f:
        source = f.read()

    findings = scan_file(filepath)
    flagged = [f for f in findings if f["flagged"]]
    redacted = redact_source(source, flagged)

    return source, redacted, flagged


def show_diff(filename, original, redacted):
    original_lines = original.splitlines()
    redacted_lines = redacted.splitlines()

    print("\nFile: " + filename)
    print("-" * 50)
    changed = False
    for i, (orig, redc) in enumerate(zip(original_lines, redacted_lines)):
        if orig != redc:
            print("  Line " + str(i + 1) + " BEFORE: " + orig.strip())
            print("  Line " + str(i + 1) + " AFTER : " + redc.strip())
            changed = True
    if not changed:
        print("  No changes — no real secrets found.")


def save_redacted(filepath, redacted_source):
    folder = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    out_path = os.path.join(folder, "redacted_" + filename)
    with open(out_path, "w") as f:
        f.write(redacted_source)
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python redactor.py <file.py> [file2.py ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        original, redacted, flagged = redact_file(path)
        show_diff(path, original, redacted)

        if flagged:
            out = save_redacted(path, redacted)
            print("  Saved redacted file: " + out)
