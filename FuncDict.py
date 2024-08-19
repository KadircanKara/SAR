from Distance import *
from Connectivity import *
from Time import *
from Smoothness import *

from PathSolution import *

model_metric_info = {
    # Objective Functions
    'Total Distance': get_total_distance,
    'Mission Time': get_mission_time,
    'Percentage Connectivity': calculate_percentage_connectivity,# bfs_connectivity
    'Percentage Disconnectivity': calculate_percentage_disconnectivity,
    'Path Smoothness': path_smoothness_penalty,
    'Total Disconnected Time': calculate_total_disconnected_time,
    'Max Disconnected Time': calculate_max_disconnected_time,
    'Mean Disconnected Time': calculate_mean_disconnected_time,
    # Inequality Constraints
    'Limit Mission Time': limit_mission_time,
    'Subtour Range':get_subtour_range,
    'Time Penalties': calculate_time_penalty,
    'Longest Subtour': get_longest_subtour,
    'Total Diagonal Steps':get_total_diagonal_steps,
    'Mean Turning Angle': get_mean_turning_angle,
    'Max Number of Visits':calculate_max_visits,
    # 'Total Long Jumps':calculate_number_of_long_jumps,
    'Max Long Jumps per Drone':calculate_max_long_jumps_per_drone,
    'Limit Long Jumps': long_jumps_ieq_constr,
    'Limit Cell per Drone': min_cells_per_drone_constr,
    'Limit Max Longest Subtour': max_longest_subtour_constr,
    'Limit Min Longest Subtour': min_longest_subtour_constr,
    'Limit Subtour Range': max_subtour_range_constr,
    # Equality Constraints
    'Speed Violations': calculate_speed_violations,
    'Hovering Drones Full Connectivity':enforce_hovering_connectivity,
    'Number of Visits Hard Constraint':nvisits_hard_constraint,
    'Traceback': no_path_traceback,
    'Search Drone Path Smoothness': longest_path_smoothness_penalty,
    'Path Smoothness': path_smoothness_penalty
}
