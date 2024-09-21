from matplotlib import pyplot as plt
from FilePaths import *
from FileManagement import load_pickle
from PathSolution import *
from PathInfo import *
from TimeBetweenVisits import calculate_mean_tbv

import os

minv_scenarios = []
minv_objs = []
minv_sols = []

obj_dir = os.listdir(objective_values_filepath)
sol_dir = os.listdir(solutions_filepath)
for minv in range(1,4):
    minv_scenarios.append(np.array([x.split("-")[0] for x in obj_dir if (f"minv_{minv}" in x) and ("time_conn_disconn" in x)]))
    minv_objs.append(np.array([x for x in obj_dir if (f"minv_{minv}" in x) and ("time_conn_disconn" in x)]))
    minv_sols.append(np.array([x for x in sol_dir if (f"minv_{minv}" in x) and ("time_conn_disconn" in x)]))

# print(load_pickle(f"Results/Objectives/{minv_objs[0][0]}"))
# for x in minv_objs[0]:
#     print(min(load_pickle(f"Results/Objectives/{x}")["Mission Time"]))


# Plot Mission Time and Percentage Connectivity for different number of visits for r = 2
r=2
number_of_drones = [4,8,12,16]
# 1 Visit
n_4_r_2_v_1_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_4_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_8_r_2_v_1_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_12_r_2_v_1_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_16_r_2_v_1_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_16_v_2.5_r_2_minv_1_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")

n_4_r_2_v_1_best_mission_time, n_4_r_2_v_1_best_percentage_connectivity = min(n_4_r_2_v_1_objective_values["Mission Time"]), max(n_4_r_2_v_1_objective_values["Percentage Connectivity"])
n_8_r_2_v_1_best_mission_time, n_8_r_2_v_1_best_percentage_connectivity = min(n_8_r_2_v_1_objective_values["Mission Time"]), max(n_8_r_2_v_1_objective_values["Percentage Connectivity"])
n_12_r_2_v_1_best_mission_time, n_12_r_2_v_1_best_percentage_connectivity = min(n_12_r_2_v_1_objective_values["Mission Time"]), max(n_12_r_2_v_1_objective_values["Percentage Connectivity"])
n_16_r_2_v_1_best_mission_time, n_16_r_2_v_1_best_percentage_connectivity = min(n_16_r_2_v_1_objective_values["Mission Time"]), max(n_16_r_2_v_1_objective_values["Percentage Connectivity"])

v_1_r_2_best_mission_times = [n_4_r_2_v_1_best_mission_time, n_8_r_2_v_1_best_mission_time, n_12_r_2_v_1_best_mission_time, n_16_r_2_v_1_best_mission_time]
v_1_r_2_best_percentage_connectivities = [n_4_r_2_v_1_best_percentage_connectivity, n_8_r_2_v_1_best_percentage_connectivity, n_12_r_2_v_1_best_percentage_connectivity, n_16_r_2_v_1_best_percentage_connectivity]

# 2 Visits
n_4_r_2_v_2_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_4_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_8_r_2_v_2_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_12_r_2_v_2_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_16_r_2_v_2_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_16_v_2.5_r_2_minv_2_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")


n_4_r_2_v_2_best_mission_time, n_4_r_2_v_2_best_percentage_connectivity = min(n_4_r_2_v_2_objective_values["Mission Time"]), max(n_4_r_2_v_2_objective_values["Percentage Connectivity"])
n_8_r_2_v_2_best_mission_time, n_8_r_2_v_2_best_percentage_connectivity = min(n_8_r_2_v_2_objective_values["Mission Time"]), max(n_8_r_2_v_2_objective_values["Percentage Connectivity"])
n_12_r_2_v_2_best_mission_time, n_12_r_2_v_2_best_percentage_connectivity = min(n_12_r_2_v_2_objective_values["Mission Time"]), max(n_12_r_2_v_2_objective_values["Percentage Connectivity"])
n_16_r_2_v_2_best_mission_time, n_16_r_2_v_2_best_percentage_connectivity = min(n_16_r_2_v_2_objective_values["Mission Time"]), max(n_16_r_2_v_2_objective_values["Percentage Connectivity"])

v_2_r_2_best_mission_times = [n_4_r_2_v_2_best_mission_time, n_8_r_2_v_2_best_mission_time, n_12_r_2_v_2_best_mission_time, n_16_r_2_v_2_best_mission_time]
v_2__r_2_best_percentage_connectivities = [n_4_r_2_v_2_best_percentage_connectivity, n_8_r_2_v_2_best_percentage_connectivity, n_12_r_2_v_2_best_percentage_connectivity, n_16_r_2_v_2_best_percentage_connectivity]

# 3 Visits
n_4_r_2_v_3_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_4_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_8_r_2_v_3_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_12_r_2_v_3_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
n_16_r_2_v_3_objective_values = pd.read_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_g_8_a_50_n_16_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")

n_4_r_2_v_3_best_mission_time, n_4_r_2_v_3_best_percentage_connectivity = min(n_4_r_2_v_3_objective_values["Mission Time"]), max(n_4_r_2_v_3_objective_values["Percentage Connectivity"])
n_8_r_2_v_3_best_mission_time, n_8_r_2_v_3_best_percentage_connectivity = min(n_8_r_2_v_3_objective_values["Mission Time"]), max(n_8_r_2_v_3_objective_values["Percentage Connectivity"])
n_12_r_2_v_3_best_mission_time, n_12_r_2_v_3_best_percentage_connectivity = min(n_12_r_2_v_3_objective_values["Mission Time"]), max(n_12_r_2_v_3_objective_values["Percentage Connectivity"])
n_16_r_2_v_3_best_mission_time, n_16_r_2_v_3_best_percentage_connectivity = min(n_16_r_2_v_3_objective_values["Mission Time"]), max(n_16_r_2_v_3_objective_values["Percentage Connectivity"])

v_3_r_2_best_mission_times = [n_4_r_2_v_3_best_mission_time, n_8_r_2_v_3_best_mission_time, n_12_r_2_v_3_best_mission_time, n_16_r_2_v_3_best_mission_time]
v_3__r_2_best_percentage_connectivities = [n_4_r_2_v_3_best_percentage_connectivity, n_8_r_2_v_3_best_percentage_connectivity, n_12_r_2_v_3_best_percentage_connectivity, n_16_r_2_v_3_best_percentage_connectivity]

# Plot
# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xticks(number_of_drones)
ax.grid()
# Plot each scatter plot and connect them with lines
ax.scatter(number_of_drones, v_1_r_2_best_mission_times, color='red', label='1 Visit')
ax.plot(number_of_drones, v_1_r_2_best_mission_times, color='red')
ax.scatter(number_of_drones, v_2_r_2_best_mission_times, color='green', label='2 Visits')
ax.plot(number_of_drones, v_2_r_2_best_mission_times, color='green')
ax.scatter(number_of_drones, v_3_r_2_best_mission_times, color='blue', label='3 Visits')
ax.plot(number_of_drones, v_3_r_2_best_mission_times, color='blue')
# Add a legend to the plot
ax.legend()
# Add axis labels and a title
ax.set_xlabel('Number of Drones')
ax.set_ylabel('Mission Time')
ax.set_title('Mission Time for Different Number of Visits')

# Create a figure and axis
fig, ax = plt.subplots()
ax.set_xticks(number_of_drones)
ax.grid()
# Plot each scatter plot and connect them with lines
ax.scatter(number_of_drones, v_1_r_2_best_percentage_connectivities, color='red', label='1 Visit')
ax.plot(number_of_drones, v_1_r_2_best_percentage_connectivities, color='red')
ax.scatter(number_of_drones, v_2__r_2_best_percentage_connectivities, color='green', label='2 Visits')
ax.plot(number_of_drones, v_2__r_2_best_percentage_connectivities, color='green')
ax.scatter(number_of_drones, v_3__r_2_best_percentage_connectivities, color='blue', label='3 Visits')
ax.plot(number_of_drones, v_3__r_2_best_percentage_connectivities, color='blue')
# Add a legend to the plot
ax.legend()
# Add axis labels and a title
ax.set_xlabel('Number of Drones')
ax.set_ylabel('Percentage Connectivity')
ax.set_title('Percentage Connectivity for Different Number of Visits')

# Plot Pareto Fronts
def plot_pareto_front(mission_time_values, percentage_connectivity_values, title, show=False):
    """
    Plots a Pareto front for two objectives: mission time and percentage connectivity.
    
    Args:
        mission_time_values (list or array): Values for mission time (Objective 1).
        percentage_connectivity_values (list or array): Values for percentage connectivity (Objective 2).
    """
    # Create a figure and axis
    fig, ax = plt.subplots()
    ax.grid()
    # Scatter plot of the two objectives
    ax.scatter(mission_time_values, percentage_connectivity_values, color='blue', label='Pareto Points')
    # Connecting points with lines
    # ax.plot(mission_time_values, percentage_connectivity_values, color='blue')
    # Set labels and title
    ax.set_xlabel('Mission Time')
    ax.set_ylabel('Percentage Connectivity')
    ax.set_title(title)
    # Add a legend
    ax.legend()
    # Optionally, invert y-axis if a higher percentage is better (to show "better" values going up)
    # ax.invert_yaxis()
    if show:
        # Show the plot
        plt.show()

    return None

plot_pareto_front(n_8_r_2_v_1_objective_values["Mission Time"], n_8_r_2_v_1_objective_values["Percentage Connectivity"], "8 Drones, 2 Cell Range, 1 Visit Pareto Front")
plot_pareto_front(n_8_r_2_v_2_objective_values["Mission Time"], n_8_r_2_v_2_objective_values["Percentage Connectivity"], "8 Drones, 2 Cell Range, 2 Visits Pareto Front")
plot_pareto_front(n_8_r_2_v_3_objective_values["Mission Time"], n_8_r_2_v_3_objective_values["Percentage Connectivity"], "8 Drones, 2 Cell Range, 3 Visits Pareto Front")


# Show Plots
plt.show()




# minv_1_best_mission_times, minv_1_best_percentage_connectivities  = [], []
# minv_2_best_mission_times, minv_2_best_percentage_connectivities  = [], []
# minv_3_best_mission_times, minv_3_best_percentage_connectivities  = [], []
# for n in number_of_drones:
#     minv_1_mission_times, minv_1_percentage_connectivities = pd.read_pickle(f"Results/Objectives/{x}")["Mission Time"] for x in minv_objs[0] if (f"n_{n}" in x) and (f"r_{r}" in x)
#     minv_2_mission_times, minv_2_percentage_connectivities =
#     minv_3_mission_times, minv_3_percentage_connectivities =
#     # 1 Visit
#     minv_1_best_mission_times.append(min([pd.read_pickle(f"Results/Objectives/{x}")["Mission Time"] for x in minv_objs[0] if (f"n_{n}" in x) and (f"r_{r}" in x)]))
#     minv_1_best_percentage_connectivities.append(max([pd.read_pickle(f"Results/Objectives/{x}")["Percentage Connectivity"] for x in minv_objs[0] if (f"n_{n}" in x) and (f"r_{r}" in x)]))
#     # 2 Visits
#     minv_2_best_mission_times.append(min([pd.read_pickle(f"Results/Objectives/{x}")["Mission Time"] for x in minv_objs[1] if (f"n_{n}" in x) and (f"r_{r}" in x)]))
#     minv_2_best_percentage_connectivities.append(max([pd.read_pickle(f"Results/Objectives/{x}")["Percentage Connectivity"] for x in minv_objs[1] if (f"n_{n}" in x) and (f"r_{r}" in x)]))
#     # 3 Visits
#     minv_3_best_mission_times.append(min([pd.read_pickle(f"Results/Objectives/{x}")["Mission Time"] for x in minv_objs[2] if (f"n_{n}" in x) and (f"r_{r}" in x)]))
#     minv_3_best_percentage_connectivities.append(max([pd.read_pickle(f"Results/Objectives/{x}")["Percentage Connectivity"] for x in minv_objs[2] if (f"n_{n}" in x) and (f"r_{r}" in x)]))

# print(minv_1_best_mission_times)