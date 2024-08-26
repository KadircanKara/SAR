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
from FileManagement import load_pickle
from PathInput import test_setup_scenario
from PathAnimation import *

info = PathInfo(test_setup_scenario)
model = info.model
scenario = str(info)
direction = "Best"
obj = "Mean_Disconnected_Time"
sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
print(sol.percentage_connectivity)
fig, axis = plt.subplots()
fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
title = f"{direction} {obj.replace('_',' ')} Paths"
axis.set_title(title)
anim_object = PathAnimation(sol, fig, axis)
anim = FuncAnimation(anim_object.fig, anim_object.update, frames=anim_object.paths[0].shape[1],
                             init_func=anim_object.initialize_figure, blit=True, interval=50)
plt.show()
# F = load_pickle(f"Results/Objectives/{scenario}-ObjectiveValues.pkl")
# for column in F:
#     values = F[column]
#     print(f"min {column}: {min(values)} ")
#     print(f"max {column}: {max(values)} ")
#     print(f"min {column}: {median_low(values)} ")






# test_anim = load_pickle(f"Results/Animations/{scenario}_{direction}{obj}_Animation.pkl")
# test_anim()