LATEX_PROJECT_BASE_PATH = "/home/pepijn/Documents/uni/y5/thesis/writing/overleaf/"
RUNTIME_DIR = "/home/pepijn/Documents/uni/y5/thesis/amalur/amalur-experiments/results/full_1/daic"
FIGURE_WIDTH_INCHES = 8.0
MODEL_OPERATORS = ["KMeans", "Logistic Regression", "Linear Regression", "Gaussian"]

import sys
# sys.path.append(f"{RUNTIME_DIR}/src")
sys.path.append("/home/pepijn/Documents/uni/y5/thesis/amalur/amalur-experiments/results/full_1/src/")

from util import read_data_chars

def save_table(table, path):
    print(table)
    with open(f"{LATEX_PROJECT_BASE_PATH}/{path}", "w+") as f:
        f.write("% LTeX: enabled=false\n")
        f.write(table)
