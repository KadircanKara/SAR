# from PathSolution import *
# from Distance import *
# from Connectivity import *
# from Time import *

moo_model_without_disconn = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity'], # 'Max Long Jumps per Drone'
    'G': ['Min Percentage Connectivity'], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations'] # 'No Long Jumps' 'Hovering Drones Full Connectivity'
}

moo_model_with_disconn = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': ['Path Speed Violations as Constraint', 'Min Percentage Connectivity','Max Mission Time'], # 'Min Percentage Connectivity','Max Mission Time'
    'H': [] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}

moo_model_mtsp = {
    'Type': 'MOO',
    'Exp': 'dist_subtour',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Longest Subtour'],
    'G': [],
    'H': ['No Speed Violations']  # 'No Long Jumps', 'No Extra Revisits'
}

distance_soo_model = {
    'Type': 'SOO',
    'Exp': 'dist',
    'Alg': "GA",
    'F': ['Mission Time'],
    'G': ['Path Speed Violations as Constraint'],
    'H': []  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}