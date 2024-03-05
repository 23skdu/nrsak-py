#!/usr/bin/env python3
import argparse
import subprocess
import sys
def install(package):
 subprocess.check_call([sys.executable, "-m", "pip3", "install", package])
required_packages = [
 "numpy", "pandas", "matplotlib", "tensorflow", "scikit-learn", "plotly"
]
for package in required_packages:
 try:
   __import__(package)
 except ImportError:
   install(package)

import numpy as np
import pandas as d
import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend such as 'Agg'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go
import os

parser = argparse.ArgumentParser()
parser.add_argument("a")
args = parser.parse_args()
print(args.echo)
