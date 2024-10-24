import os
os.system('clear')
from FileManagement import load_pickle
from PathAnimation import *
from PathAlgorithm import *
from PathOptimizationModel import *
from PathInput import *
from main import scenario

# info = PathInfo(scenario)
# model = info.model
# scenario = str(info)

info:PathInfo = PathInfo(scenario)
scenario_name = str(info)
direction = "Best"
obj = "Percentage_Connectivity" # Max_Mean_TBV_as_Objective
sol = load_pickle(f"Results/Solutions/{scenario_name}-{direction}-{obj}-Solution.pkl")
info:PathInfo = sol.info
# print(f"Percentage Connectivity: {sol.percentage_connectivity}\nDrone Speed Violations: {calculate_drone_speed_violations(sol)}\nDrone Tracebacks: {calculate_drone_tracebacks(sol)}")
fig, axis = plt.subplots()
# fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
title = f"{direction} {obj.replace('_',' ')} Paths"
axis.set_title(title)
anim_object = PathAnimation(sol, fig, axis)
anim = anim_object()
plt.show()