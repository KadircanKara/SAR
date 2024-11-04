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
# import sympy as sp


scenario = {
                        'grid_size': 8,
                        'cell_side_length': 50,
                        'number_of_drones': 20, # n=12, r=2*sqrt(2), n_visits=1
                        'max_drone_speed': 2.5, # m/s
                        'comm_cell_range': 2*sqrt(2),  # 4 cells
                        'min_visits': 3,  # Minimum number of cell visits
                        'max_visits':5, # Maximum number of cell visits
                        'number_of_targets': 1,
                        'target_positions':12,
                        'true_detection_probability': 0.99,
                        'false_detection_probability': 0.01,
                        'detection_threshold': 0.9,
                        'max_isolated_time': 0,
                        }

number_of_drones_values = [4,8,12,16]
min_visits_values = [1,2,3]

scenarios = []
for n in number_of_drones_values:
    for v in min_visits_values:
        scenarios.append(
            {'grid_size': 8,
                'cell_side_length': 50,
                'number_of_drones': n,
                'max_drone_speed': 2.5, # m/s
                'comm_cell_range': 2,  # 4 cells
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
                    "random_one_sp_mutation": (0.95, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
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

        test = PathUnitTest(scenario)
        test(save_results=True, animation=False, copy_to_drive=False)

    # for scenario in scenarios:
    #     test = PathUnitTest(scenario)
    #     test(save_results=True, animation=False, copy_to_drive=False)