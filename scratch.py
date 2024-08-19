import os

from numpy.lib.function_base import insert
os.system('clear')
import numpy as np
import pandas as pd
from scipy import io
import pickle
from scipy.signal import convolve
import random

from PathOptimizationModel import moo_model_with_disconn, distance_soo_model
from PathSolution import PathSolution
from PathInfo import PathInfo
from Time import get_real_paths
from Connectivity import *
from FileManagement import load_pickle
from PathInput import test_setup_scenario
from PathAnimation import *

scenario = str(PathInfo(test_setup_scenario))
direction = "Best"
obj = "Percentage_Connectivity"
sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
print(sol.percentage_connectivity)
anim = PathAnimation(sol)
anim()
F = load_pickle(f"Results/Objectives/{scenario}-ObjectiveValues.pkl")
print(F)






# test_anim = load_pickle(f"Results/Animations/{scenario}_{direction}{obj}_Animation.pkl")
# test_anim()