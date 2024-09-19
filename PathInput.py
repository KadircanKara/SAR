from copy import deepcopy

from PathOptimizationModel import *

from PathSampling import *
from PathMutation import *
from PathCrossover import *
from PathRepair import *
from pymoo.core.duplicate import NoDuplicateElimination


# CHANGE INPUTS FROM HERE !!!

# One single scenario for testing
scenario = {
'grid_size': 8,
'cell_side_length': 50,
'number_of_drones': 16,
'max_drone_speed': 2.5, # m/s
'comm_cell_range': 2,  # 2 cells
'min_visits': 3,  # Minimum number of cell visits
'max_visits':5, # Maximum number of cell visits
'number_of_targets': 1,
'target_positions':12,
'true_detection_probability': 0.99,
'false_detection_probability': 0.01,
'detection_threshold': 0.9,
'max_isolated_time': 0,
}

# MODEL
model = moo_model_with_disconn

# Gen, Pop
pop_size = 200
gen_size = 3000

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



# OPERATORS
# path_sampling = PathSampling()
# path_mutation = PathMutation()
# path_crossover = PathCrossover()
# path_eliminate_duplicates = NoDuplicateElimination()
# path_repair = PathRepair()


# algorithm = model['Alg']

# if model == distance_soo_model:
#     algorithm = 'GA'
# elif model == moo_model_with_disconn:
#     algorithm = ['NSGA2','NSGA3']

# algorithm = 'NSGA2' if model==moo_model else 'GA'



single_visit_setup_scenarios = [

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 4,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 2,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 4,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 4,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 8,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 2,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 8,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 4,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 12,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 2,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 12,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 4,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},


    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 16,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 2,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
},

    {
    'grid_size': 8,
    'cell_side_length': 50,
    'number_of_drones': 16,
    'max_drone_speed': 2.5, # m/s
    'comm_cell_range': 4,  # 2 cells
    'min_visits': 1,  # Minimum number of cell visits
    'max_visits':5, # Maximum number of cell visits
    'number_of_targets': 1,
    'target_positions':12,
    'true_detection_probability': 0.99,
    'false_detection_probability': 0.01,
    'detection_threshold': 0.9,
    'max_isolated_time': 0,
}

]

two_visits_setup_scenarios = deepcopy(single_visit_setup_scenarios)
three_visits_setup_scenarios = deepcopy(single_visit_setup_scenarios)
four_visits_setup_scenarios = deepcopy(single_visit_setup_scenarios)
five_visits_setup_scenarios = deepcopy(single_visit_setup_scenarios)

for i in range(len(two_visits_setup_scenarios)):
    two_visits_setup_scenarios[i]["min_visits"] = 2
    three_visits_setup_scenarios[i]["min_visits"] = 3
    four_visits_setup_scenarios[i]["min_visits"] = 4
    five_visits_setup_scenarios[i]["min_visits"] = 5