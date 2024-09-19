from PathSolution import *
from Distance import calculate_path_speed_violations

from math import atan2, radians, degrees, sqrt
import numpy as np


def speed_violation_smoothness_as_constraint(sol:PathSolution):

    penalty = 0
    angles = [0.0, 45.0, 90.0, 135.0, 180.0, -135.0, -90.0, -45.0]

    if not sol.path_speed_violations:
        calculate_path_speed_violations(sol)

    path = [x % sol.info.number_of_cells for x in sol.path]
    
    if sol.path_speed_violations > 0:
        for i in range(len(sol.path)-1):
            prev_cell, next_cell = path[i], path[i+1]
            is_speed_violation = bool(sol.info.D[prev_cell, next_cell] > sol.info.cell_side_length * sqrt(2))
            if is_speed_violation:
                prev_coords = sol.get_coords(prev_cell)
                next_coords = sol.get_coords(next_cell)
                x, y = next_coords - prev_coords
                theta = degrees(atan2(y, x))
                print(f"Prev Cell: {prev_cell}, Next Cell: {next_cell}, Theta: {theta}")
                if theta not in angles:
                    penalty += 1
    
    return penalty

def calculate_path_smoothness_penalties(sol:PathSolution) -> dict:
    drone_path_smoothness_penalties = dict() # Dİct that involves all the penalties
    drone_path_smoothness_penalties["Traceback"] = []
    drone_path_smoothness_penalties["Ugly Step"] = []
    drone_path_smoothness_penalties["Triangle"] = []

    subpaths = sol.drone_dict.values()
    path_matrix = [np.array([sol.get_coords(cell) for cell in drone_path]) for drone_path in subpaths]
    allowed_abs_angles = [45.0, 135.0, 0.0, 180.0, 90.0]

    for drone_path in path_matrix:
        # Initialize all relevant penalties
        drone_traceback_penalty = 0
        drone_ugly_step_penalty = 0
        drone_triangle_penalty = 0
        # Calculate differences between consecutive cells
        deltas = np.diff(drone_path, axis=0)
        # Calculate angles between consecutive segments
        angles = np.degrees(np.arctan2(deltas[:, 1], deltas[:, 0]))
        # Check for tracebacks (specific patterns of angle changes)            
        for i in range(len(angles)):
            if i < len(angles) - 1:
                cons_degrees = [angles[i], angles[i+1]]
                # Specific conditions to detect tracebacks (adjust as needed)
                if (
                    (90.0 in cons_degrees and -90.0 in cons_degrees) or
                    (0.0 in cons_degrees and 180.0 in cons_degrees) or
                    (45.0 in cons_degrees and -135.0 in cons_degrees) or
                    (135.0 in cons_degrees and -45.0 in cons_degrees)
                    # (angles[i] == 90.0 and angles[i + 1] == -90.0) or (angles[i] == -90.0 and angles[i + 1] == 90.0) or
                    # (angles[i] == 0.0 and angles[i + 1] == 180.0) or (angles[i] == 180.0 and angles[i + 1] == 0.0) or
                    # (angles[i] == 45.0 and angles[i + 1] == -135.0) or (angles[i] == -135.0 and angles[i + 1] == 45.0) or
                    # (angles[i] == 135.0 and angles[i + 1] == -45.0) or (angles[i] == -45.0 and angles[i + 1] == 135.0)
                ):
                    drone_traceback_penalty += 1
            # Check for Ugly Step Penalties
            drone_ugly_step_penalty += int(bool(angles[i] not in allowed_abs_angles))

            # Check for triangle penalties
            drone_triangle_penalty += int(bool( (i < len(angles)-2) and (sol.get_city(drone_path[i]) == sol.get_city(drone_path[i+2])) ))
        
        drone_path_smoothness_penalties["Traceback"].append(drone_traceback_penalty)
        drone_path_smoothness_penalties["Ugly Step"].append(drone_ugly_step_penalty)
        drone_path_smoothness_penalties["Triangle"].append(drone_triangle_penalty)

        sol.drone_path_smoothness_penalties = drone_path_smoothness_penalties

    return drone_path_smoothness_penalties


def limit_total_traceback_penalty(sol:PathSolution):

    if sol.info.min_visits == 1:
        return 0
    else:
        if not sol.drone_path_smoothness_penalties:
            calculate_path_smoothness_penalties(sol)
        return np.sum(sol.drone_path_smoothness_penalties["Traceback"]) - (sol.info.min_visits - 1) * 6
    
def limit_max_traceback_penalty(sol:PathSolution):

    if sol.info.min_visits == 1:
        return 0
    else:
        if not sol.drone_path_smoothness_penalties:
            calculate_path_smoothness_penalties(sol)
        return np.max(sol.drone_path_smoothness_penalties["Traceback"]) - (sol.info.min_visits - 1) * 2


def eliminate_path_smoothness_penalties(sol:PathSolution):

    if not sol.drone_path_smoothness_penalties:
        calculate_path_smoothness_penalties(sol)

    return np.sum(np.array(list(sol.drone_path_smoothness_penalties.values())))
        
    


        






def calculate_drone_tracebacks(sol:PathSolution):

    drone_tracebacks = []

    # Convert the path to coordinates upfront to avoid repeated get_coords() calls

    # Get drone dict without hovering section (enforcing higher connectivity is more important than eliminating all tracebacks)
    # subpaths = [sol.drone_dict[i][:-2] if "Percentage Connectivity" in sol.info.model["F"] else sol.drone_dict[i] for i in range(sol.info.number_of_drones)]  
    subpaths = sol.drone_dict.values()

    path_matrix = [
        np.array([sol.get_coords(cell) for cell in drone_path]) for drone_path in subpaths
    ]

    # print(f"path matrix:\n{path_matrix}")

    for drone_path in path_matrix:
        drone_traceback_penalty = 0
        # Calculate differences between consecutive cells
        deltas = np.diff(drone_path, axis=0)

        # Calculate angles between consecutive segments
        angles = np.degrees(np.arctan2(deltas[:, 1], deltas[:, 0]))

        # Check for tracebacks (specific patterns of angle changes)            
        for i in range(len(angles) - 1):
            cons_degrees = [angles[i], angles[i+1]]
            # Specific conditions to detect tracebacks (adjust as needed)
            if (
                (90.0 in cons_degrees and -90.0 in cons_degrees) or
                (0.0 in cons_degrees and 180.0 in cons_degrees) or
                (45.0 in cons_degrees and -135.0 in cons_degrees) or
                (135.0 in cons_degrees and -45.0 in cons_degrees)
                # (angles[i] == 90.0 and angles[i + 1] == -90.0) or (angles[i] == -90.0 and angles[i + 1] == 90.0) or
                # (angles[i] == 0.0 and angles[i + 1] == 180.0) or (angles[i] == 180.0 and angles[i + 1] == 0.0) or
                # (angles[i] == 45.0 and angles[i + 1] == -135.0) or (angles[i] == -135.0 and angles[i + 1] == 45.0) or
                # (angles[i] == 135.0 and angles[i + 1] == -45.0) or (angles[i] == -45.0 and angles[i + 1] == 135.0)
            ):
                drone_traceback_penalty += 1

        # print(f"drone path: {drone_path}\nangles: {angles}\ntracebacks: {drone_traceback_penalty}")
        
        drone_tracebacks.append(drone_traceback_penalty)
    
    sol.drone_tracebacks = drone_tracebacks

    return drone_tracebacks

def path_smoothness_as_objective(sol:PathSolution):
    if sol.info.min_visits==1:
        return 0
    else:
        if not sol.drone_tracebacks:
            calculate_path_smoothness_penalties(sol)
        return np.sum(np.array(list(sol.drone_path_smoothness_penalties.values())))

def limit_max_traceback_per_drone(sol:PathSolution):
    if not sol.drone_tracebacks:
        drone_tracebacks = calculate_drone_tracebacks(sol)
    return max(drone_tracebacks) - (sol.info.min_visits-1) * 1

def limit_total_traceback(sol:PathSolution):
    if not sol.drone_tracebacks:
        drone_tracebacks = calculate_drone_tracebacks(sol)
    # print(f"drone tracebacks: {sol.drone_tracebacks}")
    return sum(drone_tracebacks) - (sol.info.min_visits-1) * 2

def eliminate_total_traceback(sol:PathSolution):
    if not sol.drone_path_smoothness_penalties:
        calculate_path_smoothness_penalties(sol)
    # print(f"drone tracebacks: {sol.drone_tracebacks}")
    return np.sum(sol.drone_path_smoothness_penalties["Traceback"])

def eliminate_longest_path_traceback(sol:PathSolution):
    if not sol.drone_tracebacks:
        drone_tracebacks = calculate_drone_tracebacks(sol)
    drone_paths = list(sol.drone_dict.values())
    drone_path_lens = [len(x) for x in drone_paths]
    max_len_drone_id = drone_path_lens.index(max(drone_path_lens))
    return drone_tracebacks[max_len_drone_id]

def no_path_traceback(sol: PathSolution):
    traceback_penalty = 0

    # Convert the path to coordinates upfront to avoid repeated get_coords() calls

    # Get drone dict without hovering section (enforcing higher connectivity is more important than eliminating all tracebacks)
    subpaths = [sol.drone_dict[i][:-2] if "Percentage Connectivity" in sol.info.model["F"] else sol.drone_dict[i] for i in range(sol.info.number_of_drones)]  

    path_matrix = [
        np.array([sol.get_coords(cell) for cell in drone_path]) for drone_path in subpaths
    ]

    # print(f"path matrix:\n{path_matrix}")

    for drone_path in path_matrix:
        # Calculate differences between consecutive cells
        deltas = -np.diff(drone_path, axis=0)

        # Calculate angles between consecutive segments
        angles = np.degrees(np.arctan2(deltas[:, 0], deltas[:, 1]))

        # Check for tracebacks (specific patterns of angle changes)            
        for i in range(len(angles) - 1):
            cons_degrees = [angles[i], angles[i+1]]
            # Specific conditions to detect tracebacks (adjust as needed)
            if (
                (90.0 in cons_degrees and -90.0 in cons_degrees) or
                (0.0 in cons_degrees and 180.0 in cons_degrees) or
                (45.0 in cons_degrees and -135.0 in cons_degrees) or
                (135.0 in cons_degrees and -45.0 in cons_degrees)
                # (angles[i] == 90.0 and angles[i + 1] == -90.0) or (angles[i] == -90.0 and angles[i + 1] == 90.0) or
                # (angles[i] == 0.0 and angles[i + 1] == 180.0) or (angles[i] == 180.0 and angles[i + 1] == 0.0) or
                # (angles[i] == 45.0 and angles[i + 1] == -135.0) or (angles[i] == -135.0 and angles[i + 1] == 45.0) or
                # (angles[i] == 135.0 and angles[i + 1] == -45.0) or (angles[i] == -45.0 and angles[i + 1] == 135.0)
            ):
                traceback_penalty += 1

    return traceback_penalty

    # traceback_penalty = 0

    # path_matrix = sol.real_time_path_matrix.copy()

    # for drone_path in path_matrix:
    #     for i in range(len(drone_path)-2):
    #         prev_cell_coords = sol.get_coords(drone_path[i])
    #         mid_cell_coords = sol.get_coords(drone_path[i+1])
    #         next_cell_coords = sol.get_coords(drone_path[i+2])
    #         prev_to_mid_delta_x, prev_to_mid_delta_y = mid_cell_coords - prev_cell_coords
    #         mid_to_next_delta_x, mid_to_next_delta_y = next_cell_coords - mid_cell_coords
    #         delta_x, delta_y = next_cell_coords - prev_cell_coords
    #         prev_to_mid_theta = degrees(atan2(prev_to_mid_delta_x, prev_to_mid_delta_y))
    #         mid_to_next_theta = degrees(atan2(mid_to_next_delta_x, mid_to_next_delta_y))
    #         # print(f"{drone_path[i]}->{drone_path[i+1]}: {theta}")
    #         traceback_penalty += int(bool(  (prev_to_mid_theta == 90.0 and mid_to_next_theta == 180.0) or (prev_to_mid_theta == 180.0 and mid_to_next_theta == 90.0)  ))
    # return traceback_penalty

def path_smoothness_penalty(sol:PathSolution):

    traceback_penalty = 0
    triangle_penalty = 0
    ugly_step_penalty = 0

    # subpaths = [sol.drone_dict[i][:-1] if "Percentage Connectivity" in sol.info.model["F"] else sol.drone_dict[i] for i in range(sol.info.number_of_drones)]  
    subpaths = list(sol.drone_dict.values())

    path_matrix = [
        np.array([sol.get_coords(cell) for cell in drone_path]) for drone_path in subpaths
    ]

    allowed_abs_angles = [45.0, 135.0, 0.0, 180.0, 90.0]

    for drone_path in path_matrix:

        deltas = np.diff(drone_path, axis=0)

        # print(deltas)

        # Calculate angles between consecutive segments
        angles = np.degrees(np.arctan2(deltas[:, 0], deltas[:, 1]))

        # Detect triangle-like subpaths
        for i in range(len(drone_path) - 2):
            if np.array_equal(drone_path[i], drone_path[i + 2]):
                triangle_penalty += 1

        # Check for tracebacks (specific patterns of angle changes)
        for i in range(len(angles)):
            if i < len(angles)-1:
                # Specific conditions to detect tracebacks (adjust as needed)
                angle_diff = angles[i+1] - angles[i]
                if abs(angle_diff) == 180.0:
                    traceback_penalty += 1
            
            if abs(angles[i]) not in allowed_abs_angles:
                ugly_step_penalty += 1

    return ugly_step_penalty

def longest_path_smoothness_penalty(sol:PathSolution):

    traceback_penalty = 0
    triangle_penalty = 0

    drone_paths = list(sol.drone_dict.values())
    path_lens = np.array([len(x) for x in drone_paths])
    longest_drone_path = drone_paths[path_lens.argmax()][:-2] if "Percentage Connectivity" in sol.info.model["F"] else sol.drone_dict[path_lens.argmax()]
    longest_drone_path_coords = [sol.get_coords(cell) for cell in longest_drone_path]

    deltas = np.diff(longest_drone_path_coords, axis=0)

    # print(deltas)

    # Calculate angles between consecutive segments
    angles = np.degrees(np.arctan2(deltas[:, 0], deltas[:, 1]))

    # Detect triangle-like subpaths
    for i in range(len(longest_drone_path_coords) - 2):
        if np.array_equal(longest_drone_path_coords[i], longest_drone_path_coords[i + 2]):
            triangle_penalty += 1

    # Check for tracebacks (specific patterns of angle changes)
    for i in range(len(angles) - 1):
        # Specific conditions to detect tracebacks (adjust as needed)

        # if (i < len(angles) - 2) and abs(angles[i] - angles[i+2]) == 180.0:
        #     zigzag_penalty += 1

        angle_diff = angles[i+1] - angles[i]
        if abs(angle_diff) == 180.0:
            traceback_penalty += 1

        # angle_set = [angles[i] , angles[i+1]]

        # if(
        #     (0.0 in angle_set and 180.0 in angle_set) or
        #     (90.0 in angle_set and -90.0 in angle_set) or
        #     (45.0 in angle_set and -135.0 in angle_set) or
        #     (135.0 in angle_set and -45.0 in angle_set)
        # ):
        #     traceback_penalty += 1

        # if (
        #     (angles[i] == 0.0 and angles[i + 1] == 180.0) or
        #     (angles[i] == 180.0 and angles[i + 1] == 0.0) or
        #     (angles[i] == 90.0 and angles[i + 1] == -90.0) or
        #     (angles[i] == -90.0 and angles[i + 1] == 90.0) or
        #     (angles[i] == 45.0 and angles[i + 1] == -135.0) or
        #     (angles[i] == -135.0 and angles[i + 1] == 45.0) or
        #     (angles[i] == 135.0 and angles[i + 1] == -45.0) or
        #     (angles[i] == -45.0 and angles[i + 1] == 135.0)
        # ):
        #     traceback_penalty += 1

    return traceback_penalty + triangle_penalty