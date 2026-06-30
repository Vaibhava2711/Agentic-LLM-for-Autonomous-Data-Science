import os.path

import numpy as np
import pandas as pd
import argparse
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error

from sklearn.metrics import roc_auc_score

parser = argparse.ArgumentParser()

parser.add_argument("--path", type=str, required=True)
parser.add_argument("--name", type=str, required=True)
parser.add_argument("--answer_file", type=str, required=True)
parser.add_argument("--predict_file", type=str, required=True)

parser.add_argument("--value", type=str, default="defects")

args = parser.parse_args()

answers = pd.read_csv(args.answer_file)
predictions = pd.read_csv(args.predict_file)

answers.sort_values(by=["id"])
predictions.sort_values(by=["id"])
# Extract predictions and ground truth labels
predicted_values = predictions["defects"].values
actual_values = answers["defects"].values  # Use answers column

# Compute RMSE
rmse = roc_auc_score(actual_values, predicted_values)

performance = rmse
with open(os.path.join(args.path, args.name, "result.txt"), "w") as f:
    f.write(str(performance))
