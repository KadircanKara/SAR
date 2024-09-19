from PathDuplicateElimination import PathDuplicateElimination
from pymoo.core.duplicate import NoDuplicateElimination

from PathSampling import PathSampling
from PathMutation import PathMutation
from PathCrossover import PathCrossover
from PathRepair import PathRepair
from PathUnitTest import *

import os

pop_size = 100
gen_size = 3000

scenario = {
                        'grid_size': 8,
                        'cell_side_length': 50,
                        'number_of_drones': 4,
                        'max_drone_speed': 2.5, # m/s
                        'comm_cell_range': 2,  # 4 cells
                        'min_visits': 3,  # Minimum number of cell visits
                        'max_visits':5, # Maximum number of cell visits
                        'number_of_targets': 1,
                        'target_positions':12,
                        'true_detection_probability': 0.99,
                        'false_detection_probability': 0.01,
                        'detection_threshold': 0.9,
                        'max_isolated_time': 0,
                        }

# SAMPLING
path_sampling = PathSampling()

# MUTATION
sp_mut_probs = {4 : 0.9, 8 : 0.9, 12 : 1.0, 16 : 0.9, 20 : 0.9}    # {4 : 1.0, 8 : 0.95, 12 : 0.7, 16 : 0.5, 20 : 0.2}

# if scenario["number_of_drones"] == 4:
#     sp_mut_prob = 1.0
# elif scenario["number_of_drones"] == 8:
#     sp_mut_prob = 0.95
# elif scenario["number_of_drones"] == 12:
#     sp_mut_prob = 0.7
# elif scenario["number_of_drones"] == 16:
#     sp_mut_prob = 0.5
# elif scenario["number_of_drones"] == 20:
#     sp_mut_prob = 0.2

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
                    "sp_mutation": (sp_mut_probs[scenario["number_of_drones"]], 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
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

    dir = os.listdir("Results/Objectives")
    minv_2_files = np.array([x for x in dir if ("minv_2" in x) and ("time_conn_disconn" in x)])
    # print(minv_2_files)

    print(f"sp mut prob: {path_mutation.mutation_info['sp_mutation']}, crossover prob: {path_crossover.prob}, ox prob: {path_crossover.ox_prob}" )

    # run_n_visit_scenarios(2)
    test = PathUnitTest(scenario)
    test(save_results=True, animation=False, copy_to_drive=False)
