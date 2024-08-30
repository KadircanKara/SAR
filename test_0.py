from FileManagement import load_pickle
from Distance import *
from Smoothness import *
from Connectivity import *
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

scenario = "MOO_NSGA2_time_conn_g_8_a_50_n_8_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0"
solutions = load_pickle(f"Results/Solutions/{scenario}-SolutionObjects.pkl")
random_sol = solutions[0][0]
F = load_pickle(f"Results/Objectives/{scenario}-ObjectiveValues.pkl")
model = random_sol.info.model
drone_speed_violations = []
smoothness_penalties = []
percentage_connectivities = []
mission_times = []

print(model["G"] + model["H"])

for x in solutions:
    sol = x[0]
    percentage_connectivities.append(sol.percentage_connectivity)
    drone_speed_violations.append(calculate_drone_speed_violations(sol))
    smoothness_penalties.append(calculate_path_smoothness_penalties(sol))

# Speed Violations Check
speed_violations_info_df = pd.DataFrame(data={"Drone Speed Violations":drone_speed_violations})
speed_violations_info_df["Total Speed Violations"] = speed_violations_info_df["Drone Speed Violations"].apply(lambda x: sum(x))
speed_violations_info_df["Max Speed Violations"] = speed_violations_info_df["Drone Speed Violations"].apply(lambda x: max(x))
speed_violations_info_df = pd.concat([speed_violations_info_df, F], axis=1)

# Smoothness Penalties Check
print(smoothness_penalties[0].keys())
traceback_penalties = [x["Traceback"] for x in smoothness_penalties]
ugly_path_penalties = [x["Ugly Step"] for x in smoothness_penalties]
triangle_penalties = [x["Triangle"] for x in smoothness_penalties]
smoothness_penalties = [(np.array(traceback_penalties[i]) + np.array(ugly_path_penalties[i]) + np.array(triangle_penalties[i]).tolist()) for i in range(len(traceback_penalties))]

traceback_penalties_df = pd.DataFrame(data={"Drone Traceback Penalties":traceback_penalties})
ugly_path_penalties_df = pd.DataFrame(data={"Drone Ugly Step Penalties":ugly_path_penalties})
triangle_penalties_df = pd.DataFrame(data={"Drone Triangle Penalties":triangle_penalties})
smoothness_penalties_df = pd.DataFrame(data={"Drone Smoothness Penalties":smoothness_penalties})

traceback_penalties_df["Total Traceback Penalties"] = traceback_penalties_df["Drone Traceback Penalties"].apply(lambda x: sum(x))
traceback_penalties_df["Max Traceback Penalties"] = traceback_penalties_df["Drone Traceback Penalties"].apply(lambda x: max(x))
ugly_path_penalties_df["Total Ugly Step Penalties"] = ugly_path_penalties_df["Drone Ugly Step Penalties"].apply(lambda x: sum(x))
ugly_path_penalties_df["Max Ugly Step Penalties"] = ugly_path_penalties_df["Drone Ugly Step Penalties"].apply(lambda x: max(x))
triangle_penalties_df["Total Triangle Penalties"] = triangle_penalties_df["Drone Triangle Penalties"].apply(lambda x: sum(x))
triangle_penalties_df["Max Triangle Penalties"] = triangle_penalties_df["Drone Triangle Penalties"].apply(lambda x: max(x))
smoothness_penalties_df["Total Smoothness Penalties"] = smoothness_penalties_df["Drone Smoothness Penalties"].apply(lambda x: sum(x))
smoothness_penalties_df["Max Smoothness Penalties"] = smoothness_penalties_df["Drone Smoothness Penalties"].apply(lambda x: max(x))

# smoothness_penalties_df = pd.concat([traceback_penalties_df, ugly_path_penalties_df, triangle_penalties_df], axis=1)

print(speed_violations_info_df)