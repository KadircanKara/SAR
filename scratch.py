import os

from numpy.lib.function_base import insert
os.system('clear')
import numpy as np
import pandas as pd
from scipy import io
import pickle
from scipy.signal import convolve
import random

from statistics import median_low

from PathOptimizationModel import moo_model_with_disconn, distance_soo_model
from PathSolution import PathSolution
from PathInfo import PathInfo
from Time import get_real_paths
from Connectivity import *
from Distance import *
from Smoothness import *
from FileManagement import load_pickle
from PathInput import test_setup_scenario
from PathAnimation import *

info = PathInfo(test_setup_scenario)
model = info.model
scenario = str(info)
direction = "Best"
obj = "Mission_Time"
sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
print(f"Percentage Connectivity: {sol.percentage_connectivity}\nDrone Speed Violations: {calculate_drone_speed_violations(sol)}\nDrone Tracebacks: {calculate_drone_tracebacks(sol)}")
fig, axis = plt.subplots()
fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
title = f"{direction} {obj.replace('_',' ')} Paths"
axis.set_title(title)
anim_object = PathAnimation(sol, fig, axis)
anim = anim_object()
# plt.show()