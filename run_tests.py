"""
Runs the AST parser on all 10 sample files and prints the results.
"""

import os
from ast_parser import find_sensitive_nodes

sample_folder = "sample_files"
sample_files = [
    "sample_01.py", "sample_02.py", "sample_03.py", "sample_04.py",
    "sample_05.py", "sample_06.py", "sample_07.py", "sample_08.py",
    "sample_09.py", "sample_10.py"
]

total = 0

print("AST Parser - Week 3 Test Run")
print("=" * 50)

for filename in sample_files:
    filepath = os.path.join(sample_folder, filename)
    findings = find_sensitive_nodes(filepath)
    total += len(findings)

    print("\nFile: " + filename)
    print("Findings: " + str(len(findings)))

    if len(findings) == 0:
        print("  No sensitive nodes found.")
    else:
        for f in findings:
            print("  Line " + str(f["line"]) + " [" + f["type"] + "] " + f["name"])
            print("    " + f["snippet"])

print("\n" + "=" * 50)
print("Total findings: " + str(total))
