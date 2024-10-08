from PathOptimizationModel import time_conn_disconn_nsga2_model
from FileManagement import load_pickle
from FilePaths import solutions_filepath

from math import sqrt
import sympy as sp

print(load_pickle(f'{solutions_filepath}MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_2_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-Best-Mission_Time-Solution.pkl').info.model)

"""dirs = ["Best", "Mid", "Worst"]

r_values = [2, sp.sqrt(8), 4]
objs = [x.replace(" ","_") for x in time_conn_disconn_nsga2_model["F"]]
minv_values = [1,2,3]

all_solution_filenames = []
extreme_point_solution_filenames = []

for r in r_values:
    for obj in objs:
        for minv in minv_values:
            all_solution_objects = load_pickle(f'{solutions_filepath}MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_{r}_minv_{minv}_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-SolutionObjects.pkl')
            for sol in all_solution_objects:
                sol[0].info.model = time_conn_disconn_nsga2_model
            # all_solution_filenames.append(f'MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_{r}_minv_{minv}_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-SolutionObjects.pkl')
            for dir in dirs:
                sol = load_pickle(f'{solutions_filepath}MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_{r}_minv_{minv}_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-{dir}-{obj}-Solution.pkl')
                sol.info.model = time_conn_disconn_nsga2_model
                # extreme_point_solution_filenames.append(f'MOO_NSGA2_time_conn_disconn_g_8_a_50_n_12_v_2.5_r_{r}_minv_{minv}_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-{dir}-{obj}-Solution.pkl')"""