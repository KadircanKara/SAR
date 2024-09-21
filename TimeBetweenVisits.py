from PathSolution import *
from Time import *
from FileManagement import load_pickle

import pandas as pd

def calculate_mean_tbv(sol:PathSolution):
    info = sol.info
    drone_path_matrix = sol.real_time_path_matrix[1:,:]
    visit_times = [[] for _ in range(info.number_of_cells)]
    tbv = visit_times.copy()
    print(f"Path Matrix:\n{drone_path_matrix}")
    for cell in range(info.number_of_cells):
        # print(f"cell {cell} visit steps: {np.where(sol.real_time_path_matrix==cell)[1].tolist()}")
        visit_times[cell] = np.sort(np.where(drone_path_matrix==cell)[1])[:info.min_visits] # Last bit is to exclude hovering steps
        tbv[cell] = np.diff(visit_times[cell])
    return list(map(lambda x: np.mean(x), tbv))

scenario = "MOO_NSGA2_time_conn_disconn_g_8_a_50_n_8_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0"

sols = load_pickle(f"Results/Solutions/{scenario}-SolutionObjects.pkl")
objs = pd.read_pickle(f"Results/Objectives/{scenario}-ObjectiveValues.pkl")
best_time_idx, best_conn_idx = objs["Mission Time"].idxmin(), objs["Percentage Connectivity"].idxmax()
best_time_sol, best_conn_sol = sols[best_time_idx][0], sols[best_conn_idx][0]

print(calculate_mean_tbv(best_time_sol))