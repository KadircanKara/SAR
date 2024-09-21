from PathDuplicateElimination import PathDuplicateElimination
from pymoo.core.duplicate import NoDuplicateElimination

from PathSampling import PathSampling
from PathMutation import PathMutation
from PathCrossover import PathCrossover
from PathRepair import PathRepair
from PathUnitTest import *

import os
from math import sqrt
# import sympy as sp

pop_size = 100
gen_size = 3000

scenario = {
                        'grid_size': 8,
                        'cell_side_length': 50,
                        'number_of_drones': 4,
                        'max_drone_speed': 2.5, # m/s
                        'comm_cell_range': sqrt(8),  # 4 cells
                        'min_visits': 2,  # Minimum number of cell visits
                        'max_visits':5, # Maximum number of cell visits
                        'number_of_targets': 1,
                        'target_positions':12,
                        'true_detection_probability': 0.99,
                        'false_detection_probability': 0.01,
                        'detection_threshold': 0.9,
                        'max_isolated_time': 0,
                        }

scenarios = [

                {'grid_size': 8,
                'cell_side_length': 50,
                'number_of_drones': 20,
                'max_drone_speed': 2.5, # m/s
                'comm_cell_range': 2,  # 4 cells
                'min_visits': 3,  # Minimum number of cell visits
                'max_visits':5, # Maximum number of cell visits
                'number_of_targets': 1,
                'target_positions':12,
                'true_detection_probability': 0.99,
                'false_detection_probability': 0.01,
                'detection_threshold': 0.9,
                'max_isolated_time': 0},

                # {'grid_size': 8,
                # 'cell_side_length': 50,
                # 'number_of_drones': 20,
                # 'max_drone_speed': 2.5, # m/s
                # 'comm_cell_range': 4,  # 4 cells
                # 'min_visits': 3,  # Minimum number of cell visits
                # 'max_visits':5, # Maximum number of cell visits
                # 'number_of_targets': 1,
                # 'target_positions':12,
                # 'true_detection_probability': 0.99,
                # 'false_detection_probability': 0.01,
                # 'detection_threshold': 0.9,
                # 'max_isolated_time': 0},

                # {'grid_size': 8,
                # 'cell_side_length': 50,
                # 'number_of_drones': 12,
                # 'max_drone_speed': 2.5, # m/s
                # 'comm_cell_range': sqrt(8),  # 4 cells
                # 'min_visits': 2,  # Minimum number of cell visits
                # 'max_visits':5, # Maximum number of cell visits
                # 'number_of_targets': 1,
                # 'target_positions':12,
                # 'true_detection_probability': 0.99,
                # 'false_detection_probability': 0.01,
                # 'detection_threshold': 0.9,
                # 'max_isolated_time': 0},

                # {'grid_size': 8,
                # 'cell_side_length': 50,
                # 'number_of_drones': 16,
                # 'max_drone_speed': 2.5, # m/s
                # 'comm_cell_range': sqrt(8),  # 4 cells
                # 'min_visits': 2,  # Minimum number of cell visits
                # 'max_visits':5, # Maximum number of cell visits
                # 'number_of_targets': 1,
                # 'target_positions':12,
                # 'true_detection_probability': 0.99,
                # 'false_detection_probability': 0.01,
                # 'detection_threshold': 0.9,
                # 'max_isolated_time': 0},

                # {'grid_size': 8,
                # 'cell_side_length': 50,
                # 'number_of_drones': 20,
                # 'max_drone_speed': 2.5, # m/s
                # 'comm_cell_range': sqrt(8),  # 4 cells
                # 'min_visits': 2,  # Minimum number of cell visits
                # 'max_visits':5, # Maximum number of cell visits
                # 'number_of_targets': 1,
                # 'target_positions':12,
                # 'true_detection_probability': 0.99,
                # 'false_detection_probability': 0.01,
                # 'detection_threshold': 0.9,
                # 'max_isolated_time': 0},

]

# SAMPLING
path_sampling = PathSampling()

# MUTATION
path_mutation = PathMutation({
                    "swap_last_point":(0, 1),
                    "swap": (0.3, 2), # 0.3 0.5
                    "inversion": (0.4, 1), # 0.4
                    "scramble": (0.3, 2), # 0.3 0.6
                    "insertion": (0, 1),
                    "displacement": (0, 1),
                    # "reverse sequence": (0.3, 1),
                    "block inversion": (0, 1),
                    # "shift": (0.3, 1),
                    "sp_mutation": (0.9, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "longest_path_swap": (0.3,1),
                    "longest_path_inversion": (0.4,1),
                    "longest_path_scramble": (0.3,1),
                })

# CROSSOVER
path_crossover = PathCrossover(prob=0.9, ox_prob=1.0)

# REPAIR
path_repair = PathRepair()

# DUPLICATES
path_eliminate_duplicates = NoDuplicateElimination()




def run_n_visit_scenarios(n:int, save_results=True, animation=False, copy_to_drive=False):
    n_dict = {  
                0: test_setup_scenario,
                1: single_visit_setup_scenarios,
                2: two_visits_setup_scenarios,
                3: three_visits_setup_scenarios,
                4: four_visits_setup_scenarios,
                5: five_visits_setup_scenarios
    }
    scenario = n_dict[n]
    test = PathUnitTest(scenario)
    test(save_results, animation, copy_to_drive)

if __name__ == "__main__":

    # dir = os.listdir("Results/Objectives")
    # for minv in range(1,4):
    #     minv_files = np.array([x for x in dir if (f"minv_{minv}" in x) and ("time_conn_disconn" in x)])
    #     print(f"{minv} visits:\n{minv_files}")

    print(f"sp mut prob: {path_mutation.mutation_info['sp_mutation']}, crossover prob: {path_crossover.prob}, ox prob: {path_crossover.ox_prob}" )

    # run_n_visit_scenarios(2)
    for scenario in scenarios:
        test = PathUnitTest(scenario)
        test(save_results=True, animation=False, copy_to_drive=False)

    # os.system('afplay /System/Library/Sounds/Glass.aiff')