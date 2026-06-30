import os.path

import numpy as np
import pandas as pd
import argparse
from sklearn.metrics import f1_score


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

parser.add_argument("--value", type=str, default="target")

args = parser.parse_args()


answers = pd.read_csv(args.answer_file)
predictions = pd.read_csv(args.predict_file)

performance = f1_score(answers[args.value], predictions[args.value])

with open(os.path.join(args.path, args.name, "result.txt"), "w") as f:
    f.write(str(performance))
