import os

os.system('clear')


# from PathInfo import PathInfo
# from Connectivity import *
# from Distance import *
# from Smoothness import *
from FileManagement import load_pickle
# from PathInput import *
from PathAnimation import *
from PathAlgorithm import *
# pd.DataFrame.sort_values()
# F = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl").sort_values(by="Mission Time")
info = PathInfo(scenario=scenario, pop_size=pop_size, gen_size=gen_size, model=model)
model = info.model
scenario = str(info)
F = load_pickle(f"Results/Objectives/{scenario}-ObjectiveValues.pkl").sort_values("Mission Time")
print(F.to_string(index=False))
direction = "Best"
obj = "Mission_Time"
sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
# print(f"Percentage Connectivity: {sol.percentage_connectivity}\nDrone Speed Violations: {calculate_drone_speed_violations(sol)}\nDrone Tracebacks: {calculate_drone_tracebacks(sol)}")
fig, axis = plt.subplots()
fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
title = f"{direction} {obj.replace('_',' ')} Paths"
axis.set_title(title)
anim_object = PathAnimation(sol, fig, axis)
anim = anim_object()
plt.show()