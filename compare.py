"""
Week 9: Side-by-side comparison of the AST tool vs the regex baseline
on all 50 labeled test cases.
"""

import os
from pattern_detector import scan_file as ast_scan
from regex_baseline import is_flagged as regex_flagged
from labels import LABELS

TEST_FOLDER = "test_cases"

ast_tp = ast_fp = ast_tn = ast_fn = 0
reg_tp = reg_fp = reg_tn = reg_fn = 0

print("AST Tool vs Regex Baseline - 50 Test Cases")
print("=" * 75)
print(f"{'File':<12} {'Actual':>10} {'AST Result':>15} {'Regex Result':>15} {'Diff':>10}")
print("-" * 75)

for filename, true_label in LABELS.items():
    filepath = os.path.join(TEST_FOLDER, filename)

    ast_predicted  = 1 if any(r["flagged"] for r in ast_scan(filepath)) else 0
    regex_predicted = 1 if regex_flagged(filepath) else 0

    actual_str = "Sensitive" if true_label == 1 else "Clean"

    def outcome(predicted, actual):
        if predicted == 1 and actual == 1: return "TP"
        if predicted == 1 and actual == 0: return "FP"
        if predicted == 0 and actual == 0: return "TN"
        return "FN"

    ast_out   = outcome(ast_predicted, true_label)
    regex_out = outcome(regex_predicted, true_label)

    if ast_out == "TP":   ast_tp += 1
    elif ast_out == "FP": ast_fp += 1
    elif ast_out == "TN": ast_tn += 1
    else:                 ast_fn += 1

    if regex_out == "TP":   reg_tp += 1
    elif regex_out == "FP": reg_fp += 1
    elif regex_out == "TN": reg_tn += 1
    else:                   reg_fn += 1

    diff = "" if ast_out == regex_out else "<-- differs"
    print(f"{filename:<12} {actual_str:>10} {ast_out:>15} {regex_out:>15} {diff:>10}")

print("=" * 75)

def scores(tp, fp, tn, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

ap, ar, af = scores(ast_tp, ast_fp, ast_tn, ast_fn)
rp, rr, rf = scores(reg_tp, reg_fp, reg_tn, reg_fn)

print("\nComparison Summary")
print("-" * 50)
print(f"{'Metric':<20} {'AST Tool':>12} {'Regex Only':>12}")
print("-" * 50)
print(f"{'True Positives':<20} {ast_tp:>12} {reg_tp:>12}")
print(f"{'False Positives':<20} {ast_fp:>12} {reg_fp:>12}")
print(f"{'True Negatives':<20} {ast_tn:>12} {reg_tn:>12}")
print(f"{'False Negatives':<20} {ast_fn:>12} {reg_fn:>12}")
print("-" * 50)
print(f"{'Precision':<20} {ap:>12.2f} {rp:>12.2f}")
print(f"{'Recall':<20} {ar:>12.2f} {rr:>12.2f}")
print(f"{'F1 Score':<20} {af:>12.2f} {rf:>12.2f}")
