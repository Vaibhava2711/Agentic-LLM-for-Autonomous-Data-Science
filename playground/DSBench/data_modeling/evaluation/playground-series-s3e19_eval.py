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

parser.add_argument("--value", type=str, default="Machine failure")

args = parser.parse_args()

answers = pd.read_csv(args.answer_file)
predictions = pd.read_csv(args.predict_file)

# Extract predictions and ground truth labels
predicted_values = predictions["num_sold"].values
actual_values = answers["num_sold"].values  # Use answers column


smape = np.mean(
    2
    * np.abs(predicted_values - actual_values)
    / (np.abs(actual_values) + np.abs(predicted_values))
)
performance = smape
with open(os.path.join(args.path, args.name, "result.txt"), "w") as f:
    f.write(str(performance))
