import os.path

import numpy as np
import pandas as pd
import argparse
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score


# Compute multiclass log loss
def multiclass_logloss(actuals, predictions):
    epsilon = 1e-15  # Avoid numerical instability in logarithm
    predictions = np.clip(
        predictions, epsilon, 1 - epsilon
    )  # Clip predicted probabilities to prevent log of zero
    predictions /= predictions.sum(axis=1)[:, np.newaxis]  # Normalize to ensure probabilities sum to 1
    log_pred = np.log(predictions)
    loss = -np.sum(actuals * log_pred) / len(actuals)
    return loss


parser = argparse.ArgumentParser()

parser.add_argument("--path", type=str, required=True)
parser.add_argument("--name", type=str, required=True)
parser.add_argument("--answer_file", type=str, required=True)
parser.add_argument("--predict_file", type=str, required=True)

parser.add_argument("--value", type=str, default="NObeyesdad")

args = parser.parse_args()

actual = pd.read_csv(args.answer_file)
submission = pd.read_csv(args.predict_file)

# Define target evaluation classes
categories = [
    "Pastry",
    "Z_Scratch",
    "K_Scatch",
    "Stains",
    "Dirtiness",
    "Bumps",
    "Other_Faults",
]

# Extract data and compute ROC-AUC score per class
auc_scores = {}
for category in categories:
    y_true = actual[category].values
    y_pred = submission[category].values
    auc_scores[category] = roc_auc_score(y_true, y_pred)

# Compute average AUC score
performance = sum(auc_scores.values()) / len(auc_scores)

with open(os.path.join(args.path, args.name, "result.txt"), "w") as f:
    f.write(str(performance))
