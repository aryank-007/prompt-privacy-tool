"""
CLI tool — Week 6.
Full pipeline: raw code file in → redacted clean output out.
Usage: python cli.py <file.py>
"""

import sys
import os
from pattern_detector import scan_file
from redactor import redact_file, get_placeholder


def print_banner():
    print("=" * 60)
    print("   Prompt Privacy Tool — AST-Driven Secret Scanner")
    print("=" * 60)


def run(filepath):
    if not os.path.exists(filepath):
        print("Error: file not found — " + filepath)
        sys.exit(1)

    print_banner()
    print("Scanning : " + filepath)
    print()

    original, redacted, flagged = redact_file(filepath)

    # Summary
    results = scan_file(filepath)
    total_nodes = len(results)
    total_flagged = len(flagged)

    print("SCAN SUMMARY")
    print("-" * 60)
    print("Sensitive nodes found : " + str(total_nodes))
    print("Real secrets detected : " + str(total_flagged))
    print()

    if total_flagged == 0:
        print("No real secrets detected. Your code is safe to share.")
        print()
        print("CLEAN OUTPUT")
        print("-" * 60)
        print(original)
        return

    # Show what was redacted
    print("REDACTIONS APPLIED")
    print("-" * 60)
    for f in flagged:
        placeholder = get_placeholder(f["name"])
        print("  Line " + str(f["line"]) + "  [" + f["type"] + "]  " + f["name"])
        print("    Before : " + f["value"])
        print("    After  : " + placeholder)
    print()

    # Print clean output
    print("CLEAN OUTPUT (safe to paste into AI assistant)")
    print("-" * 60)
    print(redacted)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py <file.py>")
        sys.exit(1)
    run(sys.argv[1])
