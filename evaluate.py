"""
Evaluates the pattern detector against 20 hand-labeled test cases.
Prints a precision/recall table and confusion matrix.
"""

import os
from pattern_detector import scan_file
from labels import LABELS

TEST_FOLDER = "test_cases"

tp = 0  # predicted positive, actually positive
fp = 0  # predicted positive, actually negative
tn = 0  # predicted negative, actually negative
fn = 0  # predicted negative, actually positive

print("Evaluation Results — 20 Hand-Labeled Test Cases")
print("=" * 65)
print(f"{'File':<12} {'Predicted':>10} {'Actual':>8} {'Result':>10}")
print("-" * 65)

for filename, true_label in LABELS.items():
    filepath = os.path.join(TEST_FOLDER, filename)
    results = scan_file(filepath)

    # File is flagged if ANY result has a pattern match
    predicted = 1 if any(r["flagged"] for r in results) else 0

    if predicted == 1 and true_label == 1:
        outcome = "True Positive"
        tp += 1
    elif predicted == 1 and true_label == 0:
        outcome = "False Positive"
        fp += 1
    elif predicted == 0 and true_label == 0:
        outcome = "True Negative"
        tn += 1
    else:
        outcome = "False Negative"
        fn += 1

    predicted_str = "Sensitive" if predicted == 1 else "Clean"
    actual_str = "Sensitive" if true_label == 1 else "Clean"
    print(f"{filename:<12} {predicted_str:>10} {actual_str:>8} {outcome:>15}")

print("=" * 65)

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall    = tp / (tp + fn) if (tp + fn) > 0 else 0
f1        = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print("\nConfusion Matrix:")
print(f"  True Positives  : {tp}")
print(f"  False Positives : {fp}")
print(f"  True Negatives  : {tn}")
print(f"  False Negatives : {fn}")

print("\nScores:")
print(f"  Precision : {precision:.2f}")
print(f"  Recall    : {recall:.2f}")
print(f"  F1 Score  : {f1:.2f}")
