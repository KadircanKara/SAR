# from PathSolution import *
# from Distance import *
# from Connectivity import *
# from Time import *

moo_model_without_disconn = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity'], # 'Max Long Jumps per Drone'
    'G': [], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations'] # 'No Long Jumps' 'Hovering Drones Full Connectivity'
}

moo_model_with_disconn = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Percentage Disconnectivity'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity'
    'G': [], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations', 'Hovering Drones Full Connectivity'] # 'No Long Jumps' 'Enforce Hovering Connectivity' 'Search Drone Path Smoothness'
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
    'F': ['Total Distance'],
    'G': ['Limit Long Jumps'],
    'H': []  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}