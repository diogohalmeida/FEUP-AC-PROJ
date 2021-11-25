import pandas as pd
import sys

filepath = sys.argv[1]

perfect = pd.read_csv("submissions/results_1_1.csv")

ours = pd.read_csv(filepath)

perfect_pred = perfect["Predicted"]

ours_pred = ours["Predicted"]

diff = abs(perfect_pred - ours_pred)

print(f"sum:\t {diff.sum()}")
print(diff.describe())