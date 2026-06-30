import os.path

import numpy as np
import pandas as pd
import argparse
from scipy.stats import spearmanr

from sklearn.metrics import roc_auc_score

parser = argparse.ArgumentParser()

parser.add_argument("--path", type=str, required=True)
parser.add_argument("--name", type=str, required=True)
parser.add_argument("--answer_file", type=str, required=True)
parser.add_argument("--predict_file", type=str, required=True)

parser.add_argument("--value", type=str, default="place_id")

args = parser.parse_args()

actual = pd.read_csv(args.answer_file)
submission = pd.read_csv(args.predict_file)


def mean_spearmanr(y_true, y_pred):
    """
    Compute mean column-wise Spearman rank correlation coefficient
    """
    assert (
        y_true.shape == y_pred.shape
    ), "The shapes of true and predicted values do not match"
    correlations = []
    for col in range(y_true.shape[1]):
        corr, _ = spearmanr(y_true[:, col], y_pred[:, col])
        correlations.append(corr)
    return sum(correlations) / len(correlations)


# Extract ground truth labels and predictions
actual_values = actual.iloc[
    :, 1:
].values  # Assuming first column is qa_id, followed by actual labels
predicted_values = submission.iloc[
    :, 1:
].values  # Assuming first column is qa_id, followed by predicted labels
# Compute MAP@3
performance = mean_spearmanr(actual_values, predicted_values)


with open(os.path.join(args.path, args.name, "result.txt"), "w") as f:
    f.write(str(performance))
