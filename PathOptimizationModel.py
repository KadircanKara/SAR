"""Mission Time, Percentage Connectivity, Max and Mean Disconnected Time, TBV MOO Models"""
time_conn_disconn_tbv_nsga2_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn_tbv',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Max Mean TBV as Objective', 'Path Speed Violations as Objective'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': ['Max Mission Time', 'Min Percentage Connectivity', 'Max Mean TBV as Constraint'], # 'Min Percentage Connectivity','Max Mission Time', 'Max Mission Time','Max Mean TBV as Constraint'
    'H': [] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}
time_conn_disconn_tbv_nsga3_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn_tbv',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time','Max Mean TBV as Objective'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': ['Min Percentage Connectivity','Max Mission Time','Max Mean TBV as Constraint'], # 'Min Percentage Connectivity','Max Mission Time'
    'H': ['Path Speed Violations as Constraint'] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}
time_conn_disconn_tbv_moead_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn_tbv',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Path Speed Violations as Objective', 'Max Mean TBV as Objective'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': [], # 'Min Percentage Connectivity','Max Mission Time'
    'H': [] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}


"""Mission Time, Percentage Connectivity, Max and Mean Disconnected Time MOO Models"""
time_conn_disconn_nsga2_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': ['Path Speed Violations as Constraint', 'Max Mission Time', 'Min Percentage Connectivity'], # 'Min Percentage Connectivity','Max Mission Time'
    'H': [] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}
time_conn_disconn_nsga3_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': ['Min Percentage Connectivity','Max Mission Time'], # 'Min Percentage Connectivity','Max Mission Time'
    'H': ['Path Speed Violations as Constraint'] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}
time_conn_disconn_moead_model = {
    'Type': 'MOO',
    'Exp':'time_conn_disconn',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time', 'Path Speed Violations as Objective'], # 'Mean Disconnected Time','Max Disconnected Time','Percentage Disconnectivity' 'Total Drone Speed Violations as Objective'
    'G': [], # 'Min Percentage Connectivity','Max Mission Time'
    'H': [] # 'No Long Jumps' 'Hovering Drones Full Connectivity' 'Search Drone Path Smoothness' 'Speed Violation Smoothness'
}



"""Mission Time, Percentage Connectivity MOO Models"""
time_conn_nsga2_model = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "NSGA2",
    'F': ['Mission Time', 'Percentage Connectivity'], # 'Max Long Jumps per Drone'
    'G': ['Min Percentage Connectivity', 'Max Mission Time'], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations'] # 'No Long Jumps' 'Hovering Drones Full Connectivity'
}
time_conn_nsga3_model = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "NSGA3",
    'F': ['Mission Time', 'Percentage Connectivity'], # 'Max Long Jumps per Drone'
    'G': ['Min Percentage Connectivity', 'Max Mission Time'], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations'] # 'No Long Jumps' 'Hovering Drones Full Connectivity'
}
time_conn_moead_model = {
    'Type': 'MOO',
    'Exp':'time_conn',
    'Alg': "MOEAD",
    'F': ['Mission Time', 'Percentage Connectivity'], # 'Max Long Jumps per Drone'
    'G': ['Min Percentage Connectivity', 'Max Mission Time'], # 'Limit Subtour Range' 'Limit Long Jumps'
    'H': ['Speed Violations'] # 'No Long Jumps' 'Hovering Drones Full Connectivity'
}



"""Percentage Connectivity, Max and Mean Disconnected Time MOO Models"""
conn_disconn_nsga2_model = {
    'Type': 'MOO',
    'Exp': 'conn_disconn',
    'Alg': "NSGA2",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Total Drone Speed Violations as Constraint']  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}
conn_disconn_nsga3_model = {
    'Type': 'MOO',
    'Exp': 'conn_disconn',
    'Alg': "NSGA3",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Total Drone Speed Violations as Constraint']  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}
conn_disconn_moead_model = {
    'Type': 'MOO',
    'Exp': 'conn_disconn',
    'Alg': "MOEAD",
    'F': ['Percentage Connectivity', 'Mean Disconnected Time','Max Disconnected Time'],
    'G': [],
    'H': ['Total Drone Speed Violations as Constraint']  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}


"""GA Models"""
time_ga_model = {
    'Type': 'SOO',
    'Exp': 'time',
    'Alg': "GA",
    'F': ['Mission Time'],
    'G': [],
    'H': ['Path Speed Violations as Constraint']  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}
conn_ga_model = {
    'Type': 'SOO',
    'Exp': 'conn',
    'Alg': "GA",
    'F': ['Percentage Connectivity'],
    'G': [],
    'H': ['Total Drone Speed Violations as Constraint']  # 'No Long Jumps', 'No Extra Revisits', 'Number of Visits Hard Constraint'
}