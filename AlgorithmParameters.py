from PathSampling import *
from PathMutation import *
from PathCrossover import *
from PathRepair import *
from pymoo.core.duplicate import NoDuplicateElimination

pop_size = 100
gen_size = 3000

# MUTATION
# sp_mut_probs = {4 : 0.9, 8 : 0.9, 12 : 1.0, 16 : 0.9, 20 : 0.9}    # {4 : 1.0, 8 : 0.95, 12 : 0.7, 16 : 0.5, 20 : 0.2}

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
                    # "sp_mutation": (sp_mut_probs[scenario["number_of_drones"]], 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "sp_mutation": (0.9, 1), # 1.0 for 4 drones |  0.95 for 8 drones | 0.7 for 12 drones | 0.5 for 16 drones
                    "longest_path_swap": (0.3,1),
                    "longest_path_inversion": (0.4,1),
                    "longest_path_scramble": (0.3,1),
                })


# SAMPLING
path_sampling = PathSampling()

# CROSSOVER
path_crossover = PathCrossover(prob=0.9, ox_prob=1.0)

# REPAIR
path_repair = PathRepair()

# DUPLICATES
path_eliminate_duplicates = NoDuplicateElimination()