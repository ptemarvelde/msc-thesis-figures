import socket
import matplotlib.pyplot as plt
plt.style.use('./std-colors.mplstyle')

hostname = socket.gethostname()



LATEX_PROJECT_BASE_PATH = "/home/pepijn/Documents/uni/y5/thesis/writing/overleaf/"
RESULT_DIR = "/home/pepijn/Documents/uni/y5/thesis/amalur/amalur-experiments/results/full_1"
if hostname != "pepijn-desktop":
    print("Running on laptop")
    LATEX_PROJECT_BASE_PATH = "/mnt/c/Users/ptema/Documents/uni/y5/writing/overleaf/"
    RESULT_DIR = "/mnt/c/Users/ptema/Documents/uni/y5/amalur-experiments/results/full_1"

FIGURE_WIDTH_INCHES = 8.0
MODEL_OPERATORS = ["KMeans", "Logistic Regression", "Linear Regression", "Gaussian"]

import sys
sys.path.append(f"{RESULT_DIR}/")

from src.util import read_data_chars

def save_table(table, path):
    print(table)
    with open(f"{LATEX_PROJECT_BASE_PATH}/{path}", "w+") as f:
        f.write("% LTeX: enabled=false\n")
        f.write(table)
