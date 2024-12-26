from copy import deepcopy
import os
import numpy as np
from FileManagement import load_pickle, save_as_pickle
from FilePaths import *
from TimeBetweenVisits import get_visit_times, calculate_tbv, calculate_mean_tbv

from PathSolution import PathSolution

os.rename

"""Correct Model Names"""
solution_filenames = np.array([f"{solutions_filepath}{x}" for x in os.listdir(solutions_filepath)])
objective_filenames = np.array([f"{objective_values_filepath}{x}" for x in os.listdir(objective_values_filepath)])
runtime_filenames = np.array([f"{runtimes_filepath}{x}" for x in os.listdir(runtimes_filepath)])
animation_filenames = np.array([f"{animations_filepath}{x}" for x in os.listdir(animations_filepath)])
path_filenames = np.array([f"{paths_filepath}{x}" for x in os.listdir(paths_filepath)])
res_filenames = np.array([f"{res_filepath}{x}" for x in os.listdir(res_filepath)])

all_filenames = np.hstack([solution_filenames, objective_filenames, runtime_filenames, animation_filenames, path_filenames, res_filenames]).tolist()

# print(len(all_filenames)==len(solution_filenames)+len(objective_filenames)+len(runtime_filenames)+len(animation_filenames)+len(path_filenames)+len(res_filenames))
for filename in all_filenames:
    # new_filename = deepcopy(filename)
    if "time_conn_disconn_tbv" in filename:
        new_filename = filename.replace("time_conn_disconn_tbv", "TCDT")
    elif "time_conn_disconn" in filename:
        new_filename = filename.replace("time_conn_disconn", "TCD")
    elif "time_conn_ws" in filename:
        new_filename = filename.replace("time_conn_ws", "TC")
    else:
        new_filename = filename
    os.rename(filename, new_filename)
    # new_filename = filename.replace("time_conn_disconn_tbv", "TCDT")
    # new_filename = filename.replace("time_conn_disconn", "TCD")
    # new_filename = filename.replace("time_conn", "TC")
    # print(f"Old Filename: {filename}\nNew Filename: {new_filename}\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
# print(type(filename))

"""Correct mission time for all solutions and modify F"""

# solution_filenames = [x for x in os.listdir("Results/Solutions")]

# for filename in solution_filenames:
# # Load the solution
#     file = load_pickle(f"Results/Solutions/{filename}")
# #     
#     if isinstance(file, np.ndarray):
#         new_file = np.empty(file.shape, dtype=PathSolution)
#         for i, sol in enumerate(file):
#             pass
            
#             get_visit_times(sol[0])
#             calculate_tbv(sol[0])
#             calculate_mean_tbv(sol[0])
#             new_file[i][0] = sol[0]
#             # print(new_file[i][0].max_mean_tbv)
#             # print(sol[0].max_mean_tbv)
#     else:
#         # print(filename, file)
#         get_visit_times(file)
#         calculate_tbv(file)
#         calculate_mean_tbv(file)
#         new_file = file
#         # print(new_file.max_mean_tbv)

#     save_as_pickle(f"Results/Solutions/{filename}", new_file)

#     # Load the file again and see if max_mean_tbv attribute got saved
#     file = load_pickle(f"Results/Solutions/{filename}")
#     if isinstance(file, np.ndarray):
#         for i, sol in enumerate(file):
#             print(file[i][0].max_mean_tbv)
#     else:
#         print(file.mission_time, file.max_mean_tbv)


# info = self.info

# # GET CELL MATRIX
# self.path_matrix = np.zeros((info.number_of_drones+1, self.time_slots), dtype=int) - 1 # number_of_drones+1 bc. of BS (inumber_of_dronesex 0)
# for i in range(info.number_of_drones):
#     if len(self.drone_dict[i]) == self.time_slots: # If this is the longest discrete tour drone
#         self.path_matrix[i+1] = self.drone_dict[i]
#     else : # If this is NOT the longest discrete tour drone
#         len_diff = self.time_slots - len(self.drone_dict[i])
#         filler = np.array([-1]*len_diff)
#         self.path_matrix[i+1] = np.hstack( (self.drone_dict[i] , filler)  )

# self.real_time_path_matrix = self.path_matrix

# # Set Mission Time
# drone_path_matrix = self.real_time_path_matrix[1:,:].T
# max_distances_at_steps = []
# while(len(max_distances_at_steps) < drone_path_matrix.shape[0] - 1):
#     step_prev = drone_path_matrix[0]
#     step = drone_path_matrix[1]
#     # print(step_prev, step)
#     max_distances_at_steps.append( max([info.D[step_prev[i], step[i]] for i in range(info.number_of_drones)]) )
#     drone_path_matrix = np.delete(arr=drone_path_matrix, obj=0, axis=0)
# self.mission_time = sum(max_distances_at_steps) / info.max_drone_speed

"""Add TBV attributes to moo solutions"""
# # solution_filenames = [x for x in os.listdir("Results/Solutions") if "time_conn_disconn" in x or "time_conn_disconn_tbv" in x]
# solution_filenames = [x for x in os.listdir("Results/Solutions") if "NSGA2" in x and "time_conn_disconn_tbv" in x ] # and "minv_1" not in x and "Best-Mission_Time" in x

# for filename in solution_filenames:
#     # Load the solution
#     file = load_pickle(f"Results/Solutions/{filename}")
#     # Add the TBV attribute
#     if isinstance(file, np.ndarray):
#         new_file = np.empty(file.shape, dtype=PathSolution)
#         for i, sol in enumerate(file):
#             get_visit_times(sol[0])
#             calculate_tbv(sol[0])
#             calculate_mean_tbv(sol[0])
#             new_file[i][0] = sol[0]
#             # print(new_file[i][0].max_mean_tbv)
#             # print(sol[0].max_mean_tbv)
#     else:
#         # print(filename, file)
#         get_visit_times(file)
#         calculate_tbv(file)
#         calculate_mean_tbv(file)
#         new_file = file
#         # print(new_file.max_mean_tbv)

#     save_as_pickle(f"Results/Solutions/{filename}", new_file)

#     # Load the file again and see if max_mean_tbv attribute got saved
#     file = load_pickle(f"Results/Solutions/{filename}")
#     if isinstance(file, np.ndarray):
#         for i, sol in enumerate(file):
#             print(file[i][0].max_mean_tbv)
#     else:
#         print(file.mission_time, file.max_mean_tbv)
    


"""Change 2*sqrt(2)s with sqrt(8)"""
# old_str = "2*sqrt(2)"
# new_str = "sqrt(8)"
# # List all files in the directory
# directories = ["Results/Animations", "Results/Res", "Results/Objectives", "Results/Paths", "Results/Solutions", "Results/Runtimes"]
# for directory in directories:
#     for filename in os.listdir(directory):
#         # Check if the old string is in the filename
#         if old_str in filename:
#             # Create the new filename by replacing the old string with the new string
#             new_filename = filename.replace(old_str, new_str)
#             # Get the full paths for the old and new filenames
#             old_filepath = os.path.join(directory, filename)
#             new_filepath = os.path.join(directory, new_filename)
#             # Rename the file
#             os.rename(old_filepath, new_filepath)
#             # print(f'Renamed: {old_filepath} -> {new_filepath}')