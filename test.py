from PathInfo import *

from PathOptimizationModel import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PathSolution import *
from FileManagement import load_pickle
from PathAnimation import PathAnimation

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import os
import sympy as sp

jw = sp.Symbol('jw')
j = sp.Symbol('j')

test = ( (1/(3-2*j+jw)) - (1/(3+2*j+jw)) + (1/(3+2*j-jw)) - (1/(3-2*j-jw)) ) / (2*j)

solutions = sp.simplify(test)

print(solutions)

# test = np.array([ [1,2,3,4,5,6] ]).T    
# print(test)
# print(type(test[0]))

# test = load_pickle("Results/Solutions/SOO_GA_T_g_8_a_50_n_4_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-SolutionObjects.pkl")
# print(test[0].max_mean_tbv)
# for sol in test:
#     print(sol.max_mean_tbv)
#     sol.get_visit_times()
#     sol.calculate_tbv()
#     sol.calculate_mean_tbv()

# print(test[0].max_mean_tbv)
# print(test)
# print(test[0])
# print(type(test[0]))

# test = pd.read_pickle("Results/Objectives/MOO_NSGA2_TCDT_g_8_a_50_n_12_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")["Mission Time"].max()
# print(test)

# F = pd.read_pickle("Results/Objectives/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
# print(f"Objective Values:\n{F}")

# best_time_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Best-Mission_Time-Solution.pkl")
# worst_time_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Worst-Mission_Time-Solution.pkl")
# print(f"Best-Worst Time: {best_time_sol.mission_time}, {worst_time_sol.mission_time}")
# print(f"Best Time Solution time, conn, tbv values: {best_time_sol.mission_time}, {best_time_sol.percentage_connectivity}, {best_time_sol.max_mean_tbv}")
# best_conn_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Best-Percentage_Connectivity-Solution.pkl")
# worst_conn_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Worst-Percentage_Connectivity-Solution.pkl")
# print(f"Best-Worst Conn: {best_conn_sol.percentage_connectivity}, {worst_conn_sol.percentage_connectivity}")
# print(f"Best Conn Solution time, conn, tbv values: {best_conn_sol.mission_time}, {best_conn_sol.percentage_connectivity}, {best_conn_sol.max_mean_tbv}")
# best_tbv_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Best-Max_Mean_TBV_as_Objective-Solution.pkl")
# worst_tbv_sol = pd.read_pickle("Results/Solutions/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Worst-Max_Mean_TBV_as_Objective-Solution.pkl")
# print(f"Best-Worst TBV: {best_tbv_sol.max_mean_tbv}, {worst_tbv_sol.max_mean_tbv}")
# print(f"Best TBV Solution time, conn, tbv values: {best_tbv_sol.mission_time}, {best_tbv_sol.percentage_connectivity}, {best_tbv_sol.max_mean_tbv}")
# # X = pd.read_pickle("Results/Objectives/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-SolutionObjects.pkl")



"""# Check if files in results_backup folder are working properly
no_tbv = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
tbv = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_tbv_g_8_a_50_n_8_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")

print(no_tbv["Mission Time"].min())
print(tbv["Mission Time"].min())
"""
"""
F = load_pickle("Results/Objectives/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_12_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
# res = load_pickle("Results/Res/MOO_NSGA3_time_conn_disconn_tbv_g_8_a_50_n_12_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Res.pkl")
print(min(F["Mission Time"]))
# print(res)
"""

"""
visits = [1, 2, 3]
drones = [4, 8, 12, 16]

data = {
    "Number of Drones": drones * len(visits) * 2,
    "Number of Visits": sum([[v] * len(drones) for v in visits] * 2, []),
    "Model": ["Model 1"] * (len(drones) * len(visits)) + ["Model 2"] * (len(drones) * len(visits)),
    "Performance": np.random.rand(len(drones) * len(visits) * 2)  # replace with actual values
}

df = pd.DataFrame(data)

# Plot line plot comparison
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="Number of Drones", y="Performance", hue="Model", style="Model", markers=True)
plt.title("Performance Comparison for Different Number of Visits")
plt.xlabel("Number of Drones")
plt.ylabel("Performance Metric")
plt.legend(title="Model")
plt.show()
"""
"""F = load_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_tbv_g_8_a_50_n_20_v_2.5_r_2*sqrt(2)_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
shape = F.shape

print(shape)
"""


"""# Initialize the PathInfo object
info = PathInfo(test_setup_scenario)

scenario = str(info)
directions = ["Best", "Mid", "Worst"]
objectives = [x.replace(" ", "_") for x in info.model["F"]]

# Iterate through each objective
for obj in objectives:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create subplots with 1 row and 3 columns
    fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
    # title = f"{direction} {obj.replace('_',' ')} Paths"
    animations = []  # Store all animations to prevent garbage collection

    for ax, direction in zip(axes, directions):
        ax.set_title(f"{direction} {obj.replace('_',' ')} Paths")
        sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
        anim_object = PathAnimation(sol, fig, ax)
        anim = FuncAnimation(
            fig, anim_object.update, frames=anim_object.paths[0].shape[1],
            init_func=anim_object.initialize_figure, blit=False, interval=0
        )
        animations.append(anim)  # Store the animation object

    plt.tight_layout()
    plt.show()"""