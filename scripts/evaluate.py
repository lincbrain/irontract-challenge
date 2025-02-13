#!/usr/bin/env python3

import argparse
import os

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import pandas as pd
from sklearn.metrics import auc


def load_nifti_data(filepath):
    """Load a NIfTI file using nibabel and return its data as a NumPy array."""
    img = nib.load(filepath)
    return img.get_fdata()


def compute_tpr_fpr(gt_data, pred_data, mask_data):
    """
    Compute TPR and FPR for a single binary prediction compared to ground truth,
    restricted to voxels where mask_data == 1.
    Both gt_data and pred_data are expected to contain 0 or 1 only.
    """
    # Restrict to the masked region
    mask_indices = mask_data == 1

    # Flatten the relevant voxels
    gt = gt_data[mask_indices].flatten()
    pred = pred_data[mask_indices].flatten()

    # Compute confusion matrix components
    tp = np.sum((pred == 1) & (gt == 1))
    tn = np.sum((pred == 0) & (gt == 0))
    fp = np.sum((pred == 1) & (gt == 0))
    fn = np.sum((pred == 0) & (gt == 1))

    # Avoid division by zero
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    return tpr, fpr


def plot(new_fprs, new_tprs, historical_file, output_plot):
    plt.figure(figsize=(12, 8))
    
    if historical_file:
        csv_file = historical_file
        df = pd.read_csv(csv_file)
        submissions = df['dataset'].unique()

        for submission in submissions:
            subset = df[df['dataset'] == submission]
            plt.plot(subset['fpr'], subset['tpr'], label=submission)
    plt.plot(new_fprs, new_tprs, label='New Submission', color='black')
    # Customize the plot
    plt.title("FPR vs. TPR for All Submissions", fontsize=16)
    plt.xlabel("False Positive Rate (FPR)", fontsize=12)
    plt.ylabel("True Positive Rate (TPR)", fontsize=12)
    plt.legend(title="Submission", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_plot, dpi=150, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate submission NIfTI files (binary 0/1) vs. ground truth.")
    parser.add_argument("--mask-file", required=True,
                        help="Path to the NIfTI mask file.")
    parser.add_argument("--gt-file", required=True,
                        help="Path to the NIfTI ground-truth file (binary 0/1).")
    parser.add_argument("--submission-folder", required=True,
                        help="Folder containing participant NIfTI predictions.")
    parser.add_argument("--output-plot", default="roc_curve.png",
                        help="Filename for the saved ROC curve plot.")
    parser.add_argument("--output-stats", default="results.txt",
                        help="Filename to save the computed AUC and points.")
    parser.add_argument("--threshold", type=float, default=0.3,
                        help="Threshold for fpr.")

    args = parser.parse_args()

    # 1. Load mask and ground truth data
    mask_data = load_nifti_data(args.mask_file)
    gt_data = load_nifti_data(args.gt_file)

    # 2. Iterate over all NIfTI files in the submissions folder
    submission_files = [
        f for f in os.listdir(args.submission_folder)
        if f.lower().endswith(".nii") or f.lower().endswith(".nii.gz")
    ]

    # Lists to store all TPR/FPR points
    tpr_list = []
    fpr_list = []

    for sub_file in submission_files:
        sub_path = os.path.join(args.submission_folder, sub_file)
        pred_data = load_nifti_data(sub_path)

        # 3. Compute TPR and FPR for this submission
        tpr, fpr = compute_tpr_fpr(gt_data, pred_data, mask_data)
        if fpr > 0.3:
            continue
        tpr_list.append(tpr)
        fpr_list.append(fpr)

        print(f"File: {sub_file} => TPR={tpr:.3f}, FPR={fpr:.3f}")

    # 4. Sort the points by FPR (typical approach for computing AUC in ROC space)
    #    Each submission is a single threshold => each is a single point
    #    We'll form a piecewise curve from these points.
    points = sorted(zip(fpr_list, tpr_list), key=lambda x: x[0])
    sorted_fprs = [p[0] for p in points]
    sorted_tprs = [p[1] for p in points]

    # 5. Compute area under the curve (AUC) using a standard trapezoidal rule
    #    from scikit-learn
    roc_auc = auc(sorted_fprs, sorted_tprs)

    # 6. Plot the ROC curve
    plot(sorted_fprs, sorted_tprs, 'data/2021.csv', args.output_plot)

    # 7. Save results
    with open(args.output_stats, "w") as f:
        f.write("Submission Results (TPR, FPR):\n")
        for (fpr, tpr), sub_file in zip(points, submission_files):
            f.write(f"{sub_file}: TPR={tpr:.4f}, FPR={fpr:.4f}\n")
        f.write(f"\nArea Under Curve (AUC): {roc_auc:.4f}\n")

    print(f"\nDone! AUC = {roc_auc:.4f}")
    print(f"ROC curve saved to {args.output_plot}")
    print(f"Results saved to {args.output_stats}")


if __name__ == "__main__":
    main()
