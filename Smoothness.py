from PathSolution import *
from math import atan2, radians, degrees

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
            # Specific conditions to detect tracebacks (adjust as needed)
            if (
                (angles[i] == 90.0 and angles[i + 1] == 180.0) or
                (angles[i] == 180.0 and angles[i + 1] == 90.0)
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
    x_penalty = 0

    subpaths = [sol.drone_dict[i][:-2] if "Percentage Connectivity" in sol.info.model["F"] else sol.drone_dict[i] for i in range(sol.info.number_of_drones)]  
    # subpaths = list(sol.drone_dict.values())

    path_matrix = [
        np.array([sol.get_coords(cell) for cell in drone_path]) for drone_path in subpaths
    ]

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
        for i in range(len(angles) - 1):
            # Specific conditions to detect tracebacks (adjust as needed)

            angle_diff = angles[i+1] - angles[i]
            if abs(angle_diff) == 180.0:
                traceback_penalty += 1

    return traceback_penalty + triangle_penalty

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