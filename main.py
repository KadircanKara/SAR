from PathDuplicateElimination import PathDuplicateElimination
from pymoo.core.duplicate import NoDuplicateElimination

from PathSampling import PathSampling
from PathMutation import PathMutation
from PathCrossover import PathCrossover
from PathRepair import PathRepair
from PathTermination import PathTermination, PathDefaultTermination, PathDefaultMultiObjectiveTermination
from PathUnitTest import *

import os
from math import sqrt
from PathInput import *
# from playsound import playsound

# Play sound file
# playsound('path_to_your_sound_file.mp3')
# import sympy as sp

"""Scenarios' SP Mutation Rates"""
# ------------------------------------------------------------------------------------------------------------------
# 0.95
# ------------------------------------------------------------------------------------------------------------------
# TCDT_MOO_NSGA2 : TCDT - 4 drones 1 visit all ranges, 8 drones 1 visit all ranges, 12 drones 2*sqrt(2) and 4 ranges, 
# 4 drones, 1 visit, all ranges
# 8 drones, 1 visit, all ranges
# 12 drones, 1 visit, 2*sqrt(2) and 4 ranges
# ------------------------------------------------------------------------------------------------------------------



# ------------------------------------------------------------------------------------------------------------------
# 0.75
# ------------------------------------------------------------------------------------------------------------------
# TCDT_MOO_NSGA2
# 12 drones, 1 visit, 2 range 
# ------------------------------------------------------------------------------------------------------------------


# time_conn_disconn
# n=4 r=2 v=2
# n=4 r=2 v=3
# n=4 r=sqrt(8) v=2
# n=4 r=sqrt(8) v=3
# n=4 r=4 v=1,2,3

# For the WS Method, we had to use 800 generation size for the scenario n=16, v=3 because terminal crashed at 1000 generation size

"""Run Again"""
# TODO: Time SOO - 8 drones 3 visits for each range - IP
# TODO: TCDT MOO - 16 drones 3 visits 2*sqr(2) range - DONE

"""Algoriithms To RUN"""
# TODO: Conn SOO -
# TODO: Time SOO -
# TODO: TCDT SOO - 
# TODO: TCDT MOO - IP (Only 3 visits on this machine)
# TODO: TCT MOO -
# TODO: TCT SOO -

"""NOTE: I used 0.85 sp_muatation rate instead of 0.75 for 8 drones, 2,2*sqrt(2),4 comm cell range and 3 visits for TCDT MOO Model !!!"""
# 8 drones 2,2*sqrt(2),4 ranges
# 12 drones 4 range
# 16 drones 2*sqrt(2),4 ranges
"""NOTE: I used 0.85 sp_muatation rate instead of 0.75 for 8 drones, 2,2*sqrt(2),4 comm cell range and 3 visits for TCT MOO Model !!!"""
# 8 drones, 4 range, 1 visit

"""DONT FORGET TO CHANGE POP SIZE AFTER YOU ARE DONE WITH n=16, v=3 WS Model !!!!!!!!!!!!!!!!!!"""

# 12, 2

scenario = {
                        'grid_size': 8,
                        'cell_side_length': 50,
                        'number_of_drones': 4, # n=12, r=2*sqrt(2), n_visits=1
                        'max_drone_speed': 2.5, # m/s
                        'comm_cell_range': 2,  # 4 cells
                        'min_visits': 1,  # Minimum number of cell visits
                        'max_visits':5, # Maximum number of cell visits
                        'number_of_targets': 1,
                        'target_positions':12,
                        'true_detection_probability': 0.99,
                        'false_detection_probability': 0.01,
                        'detection_threshold': 0.9,
                        'max_isolated_time': 0,
                        }

number_of_drones_values = [12]
comm_cell_range_values = [2]
min_visits_values = [1]

scenarios = []
for v in min_visits_values:
    for n in number_of_drones_values:
        for r in comm_cell_range_values:
            scenarios.append(
                {'grid_size': 8,
                    'cell_side_length': 50,
                    'number_of_drones': n,
                    'max_drone_speed': 2.5, # m/s
                    'comm_cell_range': r,  # 4 cells
                    'min_visits': v,  # Minimum number of cell visits
                    'max_visits':5, # Maximum number of cell visits
                    'number_of_targets': 1,
                    'target_positions':12,
                    'true_detection_probability': 0.99,
                    'false_detection_probability': 0.01,
                    'detection_threshold': 0.9,
                    'max_isolated_time': 0}
            )

# scenarios = [

#                 {'grid_size': 8,
#                 'cell_side_length': 50,
#                 'number_of_drones': 4,
#                 'max_drone_speed': 2.5, # m/s
#                 'comm_cell_range': 2,  # 4 cells
#                 'min_visits': 1,  # Minimum number of cell visits
#                 'max_visits':5, # Maximum number of cell visits
#                 'number_of_targets': 1,
#                 'target_positions':12,
#                 'true_detection_probability': 0.99,
#                 'false_detection_probability': 0.01,
#                 'detection_threshold': 0.9,
#                 'max_isolated_time': 0},

# ]

# SAMPLING
path_sampling = PathSampling()

# MUTATION
path_mutation = PathMutation({
                    "swap_last_point":(0, 1),
                    "swap": (0.3, 1), # 0.3 0.5
                    "inversion": (0.4, 1), # 0.4
                    "scramble": (0.3, 1), # 0.3 0.6
                    "insertion": (0, 1),
                    "displacement": (0, 1),
                    # "reverse sequence": (0.3, 1),
                    "block inversion": (0, 1),
                    # "shift": (0.3, 1),
                    "random_one_sp_mutation": (0.75, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "random_n_sp_mutation": (0.0, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "all_sp_mutation": (0.0, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "longest_path_sp_mutation": (0.0, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "randomly_selected_sp_mutation": (0.0, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                })

# CROSSOVER
path_crossover = PathCrossover(prob=0.9, ox_prob=1.0, n_offsprings=2)

# REPAIR
path_repair = PathRepair()

# DUPLICATES
path_eliminate_duplicates = NoDuplicateElimination()

# path_termination = PathTermination()
# path_default_termination = PathDefaultTermination()
# path_termination = PathDefaultMultiObjectiveTermination()
# path_termination = ("n_gen",n_gen)

# def run_n_visit_scenarios(n:int, save_results=True, animation=False, copy_to_drive=False):
#     n_dict = {  
#                 0: test_setup_scenario,
#                 1: single_visit_setup_scenarios,
#                 2: two_visits_setup_scenarios,
#                 3: three_visits_setup_scenarios,
#                 4: four_visits_setup_scenarios,
#                 5: five_visits_setup_scenarios
#     }
#     scenario = n_dict[n]
#     test = PathUnitTest(scenario)
#     test(save_results, animation, copy_to_drive)

if __name__ == "__main__":
        
        # test = PathUnitTest(scenario)
        # test(save_results=True, animation=False, copy_to_drive=False)

        old_filecount = len(os.listdir(objective_values_filepath))

        for scenario in scenarios:
            test = PathUnitTest(scenario)
            test(save_results=True, animation=False, copy_to_drive=False)

        new_filecount = len(os.listdir(objective_values_filepath))

        filecount_diff = new_filecount - old_filecount

        if filecount_diff == len(scenarios):
            print(f"ALL SCENARIOS RAN SUCCESSFULLY !!!")
        else:
            print(f"ERROR: {len(scenarios)-filecount_diff} SCENARIOS DIDN'T CONVERGE !!!")