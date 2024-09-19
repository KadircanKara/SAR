
import numpy as np
import itertools
from scipy.spatial.distance import cdist
from math import floor, ceil

# from PathInput import model, scenario

class PathInfo(object):

    def __init__(self, model, pop_size, gen_size, scenario) -> None:

        self.scenario = scenario

        self.model = model
        self.pop_size = pop_size
        self.gen_size = gen_size

        self.grid_size = self.scenario['grid_size']
        self.number_of_cells = self.grid_size ** 2
        self.cell_side_length = self.scenario['cell_side_length']
        self.number_of_drones = self.scenario['number_of_drones']
        self.number_of_nodes = self.number_of_drones + 1
        self.max_drone_speed = self.scenario['max_drone_speed']
        self.comm_cell_range = self.scenario['comm_cell_range']
        self.comm_dist = self.comm_cell_range * self.cell_side_length
        self.min_visits = self.scenario['min_visits']
        self.max_visits = self.scenario['max_visits']
        self.number_of_targets = self.scenario['number_of_targets']
        self.target_positions = self.scenario['target_positions']
        self.true_detection_probability = self.scenario['true_detection_probability']
        self.false_detection_probability = self.scenario['false_detection_probability']
        self.detection_threshold = self.scenario['detection_threshold']
        self.max_isolated_time = self.scenario['max_isolated_time']


        # self.grid_size = scenario_dict['grid_size'] if scenario_dict else scenario['grid_size']
        # self.number_of_cells = self.grid_size ** 2
        # self.cell_side_length = scenario_dict['cell_side_length'] if scenario_dict else scenario['cell_side_length']
        # self.number_of_drones = scenario_dict['number_of_drones'] if scenario_dict else scenario['number_of_drones']
        # self.number_of_nodes = self.number_of_drones + 1
        # self.max_drone_speed = scenario_dict['max_drone_speed'] if scenario_dict else scenario['max_drone_speed']
        # self.comm_cell_range = scenario_dict['comm_cell_range'] if scenario_dict else scenario['comm_cell_range']
        # self.comm_dist = self.comm_cell_range * self.cell_side_length
        # self.min_visits = scenario_dict['min_visits'] if scenario_dict else scenario['min_visits']
        # self.max_visits = scenario_dict['max_visits'] if scenario_dict else scenario['max_visits']
        # self.number_of_targets = scenario_dict['number_of_targets'] if scenario_dict else scenario['number_of_targets']
        # self.target_positions = scenario_dict['target_positions'] if scenario_dict else scenario['target_positions']
        # self.true_detection_probability = scenario_dict['true_detection_probability'] if scenario_dict else scenario['true_detection_probability']
        # self.false_detection_probability = scenario_dict['false_detection_probability'] if scenario_dict else scenario['false_detection_probability']
        # self.detection_threshold = scenario_dict['detection_threshold'] if scenario_dict else scenario['detection_threshold']
        # self.max_isolated_time = scenario_dict['max_isolated_time'] if scenario_dict else scenario['max_isolated_time']

        P = [[i, j] for i in range(self.grid_size) for j in range(self.grid_size)]
        P.append([-1, -1])
        self.D = cdist(P, P) * self.cell_side_length

        self.min_subtour_length_threshold = (self.number_of_cells * self.min_visits / self.number_of_drones)*self.cell_side_length
        self.max_subtour_length_threshold = (self.number_of_cells * self.min_visits / self.number_of_drones)*self.cell_side_length # self.min_subtour_length_threshold + 20

    def __str__(self) -> str:


        multi_line_scenario = f'''{self.model['Type']}_{self.model['Alg']}_{self.model['Exp']}_g_{self.grid_size}_a_{self.cell_side_length}_n_{self.number_of_drones}_
v_{self.max_drone_speed}_r_{self.comm_cell_range}_minv_{self.min_visits}_
maxv_{self.max_visits}_Nt_{self.number_of_targets}_tarPos_{self.target_positions}_
ptdet_{self.true_detection_probability}_pfdet_{self.false_detection_probability}_
detTh_{self.detection_threshold}_maxIso_{self.max_isolated_time}
'''


        lines = multi_line_scenario.splitlines()

        single_line_scenario = ''.join(lines)

        return single_line_scenario


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0  # Returns 0 if x is exactly 0

def split_list(lst, val):
    return [list(group) for k,
    group in
            itertools.groupby(lst, lambda x: x == val) if not k]



class PathSolution():

    def __str__(self):
        info = self.info
        return f"Scenario: number_of_cells_{info.number_of_cells}_A_{info.cell_side_length}_number_of_drones_{info.number_of_drones}_V_{info.max_drone_speed}_rc_{info.comm_cell_range}_maxVisits_{info.min_visits}\n" \
            f"Objective Values: totaldistance_{self.total_distance}_longestSubtour_{self.longest_subtour}_percentageConumber_of_nodesectivity_{self.percentage_connectivity}\n" \
            f"Chromosome: pathSequenumber_of_cellse_{self.path}_startPoints_{self.start_points}"

    def __init__(self, path, start_points,  info:PathInfo, calculate_pathplan=True, calculate_connectivity=True, calculate_disconnectivity=True):

        # self.hovering = info.hovering
        # self.realtime_conumber_of_nodesectivity = info.realtime_conumber_of_nodesectivity

        # Inputs
        self.path = path
        self.start_points = start_points
        # self.relay_positions = relay_positions
        self.info: PathInfo = info

        # print(f'path: {self.path}')
        # print(f"start points: {self.start_points}")

        # cell - path
        # self.drone_dict = dict()

        # Time
        self.time_slots = None
        self.mission_time = 0
        # Distance
        self.subtour_lengths = None
        self.total_distance = None
        self.longest_subtour = None
        self.shortest_subtour = None
        self.subtour_range = None
        self.drone_speed_violations = None
        self.path_speed_violations = None
        self.speed_violations = None

        # Connectivity
        self.connectivity_matrix = None
        self.disconnected_time_steps = None
        self.percentage_connectivity = None

        # Smoothness
        self.drone_path_smoothness_penalties = None
        self.drone_tracebacks = None

        if calculate_pathplan:
            self.get_drone_dict()
            self.get_pathplan() # Calculates drone dict and path matrix (not interpolated, directly from the path sequenumber_of_cellse and start points)
        
        if calculate_connectivity:
                self.do_connectivity_calculations()
        if calculate_disconnectivity:
                self.do_disconnectivity_calculations()


    def get_drone_dict(self):

        self.drone_dict = dict()
        self.time_slots= 0
        info = self.info

        # GET CELL DICT
        for i in range(info.number_of_drones):
            if i < info.number_of_drones - 1:
                drone_path = (np.array(self.path) % info.number_of_cells)[self.start_points[i]:self.start_points[i + 1]]
            else:
                drone_path = (np.array(self.path) % info.number_of_cells)[self.start_points[i]:]
            # print(f"drone {i} path: {drone_path}")
            interpolated_first_step = interpolate_between_cities(self, -1, drone_path[0])[:-1]
            interpolated_last_step = interpolate_between_cities(self, drone_path[-1], 0)[1:]
            interpolated_last_step.append(-1)
            # self.drone_dict[i] = np.hstack(( np.array([-1,0]), self.path[self.start_points[i]:self.start_points[i + 1]], np.array([0,-1])))
            if "Percentage Connectivity" in info.model["F"]:
                self.drone_dict[i] = np.hstack((interpolated_first_step, drone_path, np.array([-1])))
            else:
                self.drone_dict[i] = np.hstack((interpolated_first_step, drone_path, interpolated_last_step))
            # print(f"city prev: {drone_path[-1]}, city: -1, interpolated last step: {interpolated_last_step}")

            # Set longest "discrete" subtour
            if len(self.drone_dict[i]) > self.time_slots : self.time_slots = len(self.drone_dict[i]) # Set max subtour length

            # Add BS as a node to drone_dict (key=1)
        # self.drone_dict[-1] = np.array([-1] * self.time_steps)


    def get_pathplan(self):

        info = self.info

        # GET CELL MATRIX
        self.path_matrix = np.zeros((info.number_of_drones+1, self.time_slots), dtype=int) - 1 # number_of_drones+1 bc. of BS (inumber_of_dronesex 0)
        for i in range(info.number_of_drones):
            if len(self.drone_dict[i]) == self.time_slots: # If this is the longest discrete tour drone
                self.path_matrix[i+1] = self.drone_dict[i]
            else : # If this is NOT the longest discrete tour drone
                len_diff = self.time_slots - len(self.drone_dict[i])
                filler = np.array([-1]*len_diff)
                self.path_matrix[i+1] = np.hstack( (self.drone_dict[i] , filler)  )

        self.real_time_path_matrix = self.path_matrix

        # Set Mission Time
        drone_path_matrix = self.real_time_path_matrix[1:,:].T
        max_distances_at_steps = []
        while(len(max_distances_at_steps) < drone_path_matrix.shape[0] - 1):
            step_prev = drone_path_matrix[0]
            step = drone_path_matrix[1]
            # print(step_prev, step)
            max_distances_at_steps.append( max([info.D[step_prev[i], step[i]] for i in range(info.number_of_drones)]) )
            drone_path_matrix = np.delete(arr=drone_path_matrix, obj=0, axis=0)
        self.mission_time = sum(max_distances_at_steps) / info.max_drone_speed


        # Set Total Distance and Longest Subtour
        Nd, time_steps = self.real_time_path_matrix.shape
        Nd -= 1 # Remove base station

        self.subtour_lengths = []

        for i in range(info.number_of_drones):
            drone_path = self.real_time_path_matrix[i+1]
            drone_dist = 0
            for j in range(time_steps-1):
                drone_dist += info.D[drone_path[j],drone_path[j+1]]
            self.subtour_lengths.append(drone_dist)

        self.total_distance = sum(self.subtour_lengths)
        self.longest_subtour = max(self.subtour_lengths)

        # APPLY HOVERING TO DRONES WITH SHORTER PATHS (ONLY IF MOO)

        # if info.model != distance_soo_model:

        path_lens = [len(path) for path in list(self.drone_dict.values())]
        # Get Hovering Drones
        hovering_drone_ids = []
        shift = 0
        path_lens_temp = path_lens.copy()
        while len(path_lens_temp) > 0:
            if path_lens_temp[0] != max(path_lens):
                hovering_drone_ids.append(shift)
            shift += 1
            path_lens_temp.pop(0)
        self.hovering_drones = hovering_drone_ids
        for drone in hovering_drone_ids:
            # APPLY HOVERING
            path_without_hovering = self.real_time_path_matrix[drone+1].copy()
            # Find last cell
            hovering_cell_idx = np.where(path_without_hovering==-1)[0][1] - 1
            hovering_cell = path_without_hovering[hovering_cell_idx]
            hovering_component = np.array([hovering_cell] * (len(path_without_hovering) - hovering_cell_idx - 1))
            path_with_hovering = path_without_hovering.copy()
            path_with_hovering[hovering_cell_idx:len(path_without_hovering)-1] = hovering_component
            self.real_time_path_matrix[drone+1] = path_with_hovering
        drone_interpolated_last_step_list = []
        for drone in range(info.number_of_drones):
            drone_interpolated_last_step = interpolate_between_cities(self, self.real_time_path_matrix[drone+1][-2], 0)
            if self.real_time_path_matrix[drone+1][-2] != 0:
                drone_interpolated_last_step = drone_interpolated_last_step[1:]
            drone_interpolated_last_step_list.append(drone_interpolated_last_step)
        max_interpolated_last_step_len = max([len(x) for x in drone_interpolated_last_step_list])

        for drone in range(info.number_of_drones):
            if len(drone_interpolated_last_step_list[drone]) < max_interpolated_last_step_len:
                drone_interpolated_last_step_list[drone].extend([drone_interpolated_last_step_list[drone][-1]] * (max_interpolated_last_step_len - len(drone_interpolated_last_step_list[drone])))
        drone_interpolated_path_array = np.insert(np.array(drone_interpolated_last_step_list), 0, np.full((1,max_interpolated_last_step_len), -1, dtype=int), axis=0)
        self.real_time_path_matrix = np.hstack((self.real_time_path_matrix[:,:-1], drone_interpolated_path_array, np.full((info.number_of_nodes,1), -1, dtype=int)))



        self.time_slots = self.real_time_path_matrix.shape[1]


    def do_connectivity_calculations(self):

        info = self.info
        comm_dist = info.comm_cell_range * info.cell_side_length
        real_time_path_matrix = self.real_time_path_matrix
        time_slots = real_time_path_matrix.shape[1]
        
        connectivity_matrix = np.zeros((time_slots, info.number_of_nodes, info.number_of_nodes))
        connectivity_to_base_matrix = np.zeros((time_slots, info.number_of_nodes))
        connectivity_to_base_percentage = np.zeros(time_slots)
        
        # Create a distance matrix for all drones at all times
        for time in range(time_slots):
            paths_at_time = real_time_path_matrix[:, time]
            for node_no in range(info.number_of_nodes):
                node_pos = paths_at_time[node_no]
                # Calculate distances from current node to all other nodes
                distances = info.D[node_pos, paths_at_time]
                # Create the connectivity matrix row for this node at this time
                connectivity_matrix[time, node_no, :] = distances <= comm_dist
                connectivity_matrix[time, node_no, node_no] = 0  # No self-connection

            adj_mat = connectivity_matrix[time]
            connectivity_to_base_matrix[time, BFS(adj_mat, self)] = 1
            connectivity_to_base_percentage[time] = np.mean(connectivity_to_base_matrix[time, 1:])
        
        self.connectivity_matrix = connectivity_matrix
        self.connectivity_to_base_matrix = connectivity_to_base_matrix
        self.percentage_connectivity = np.mean(connectivity_to_base_percentage)

        return self.percentage_connectivity


    def do_disconnectivity_calculations(self):

        num_disconnected_nodes_array = np.zeros(self.time_slots)
        drone_disconnected_times = np.zeros(self.info.number_of_nodes)

        for time in range(self.time_slots):

            adj_mat = self.connectivity_matrix[time] # nxn array (n = number of nodes)

            # Find disconnected nodes
            disconnected_rows = np.all(adj_mat == 0, axis=1)
            # Get the indices of disconnected nodes
            disconnected_drones = np.where(disconnected_rows)[0]
            for drone in disconnected_drones:
                drone_disconnected_times[drone] += 1
            num_disconnected_nodes = len(np.where(disconnected_rows)[0])
            # Update disconnected node array
            num_disconnected_nodes_array[time] = num_disconnected_nodes

            # if disconnected_drones.any():
            #     print(f"disconnected drones: {disconnected_drones}\nadj mat:\n{adj_mat}")

        self.mean_disconnected_time = np.mean(drone_disconnected_times)
        self.max_disconnected_time = np.max(drone_disconnected_times)
        self.total_disconnected_time = np.sum(drone_disconnected_times)
        self.percentage_disconnectivity = np.sum(num_disconnected_nodes_array) / (self.time_slots * self.info.number_of_nodes)


        # print(f"adj mat:\n{adj_mat}disconnected rows:\n{disconnected_rows}")

        return self.percentage_disconnectivity



        info = self.info
        path_matrix = self.real_time_path_matrix[1:,:].transpose()
        cell_visit_steps = dict()
        for i in range(info.number_of_cells):
            cell_visit_steps[i] = np.where(path_matrix==i)[0] # Steps at which the cell is visited

        self.cell_visit_steps = cell_visit_steps


    def get_coords(self, cell):

        if cell == -1:
            x = -self.info.cell_side_length / 2
            y = -self.info.cell_side_length / 2
        else:
            # x = ((cell % n) % self.info.grid_size + 0.5) * self.info.cell_len
            x = (cell % self.info.grid_size + 0.5) * self.info.cell_side_length
            # y = ((cell % n) // self.info.grid_size + 0.5) * self.info.cell_len
            y = (cell // self.info.grid_size + 0.5) * self.info.cell_side_length
        # return [x,y]
        return np.array([x, y])


    def get_city(self, coords):

        if coords[0] < 0 and coords[1] < 0:
            return -1
        else:
            x, y = coords
            return floor(y / self.info.cell_side_length) * self.info.grid_size + floor(x / self.info.cell_side_length)



def BFS(adj, sol:PathSolution):

    v = sol.info.number_of_nodes

    ctb = []
    start = 0
    # Visited vector to so that a
    # vertex is not visited more than
    # once Initializing the vector to
    # false as no vertex is visited at
    # the beginning
    visited = [False] * (sol.info.number_of_nodes)
    q = [start]

    # Set source as visited
    visited[start] = True

    while q:
        vis = q[0]

        # Print current node
        ctb.append(vis)

        q.pop(0)

        # For every adjacent vertex to
        # the current vertex
        for i in range(v):
            if (adj[vis][i] == 1 and
                (not visited[i])):

                # Push the adjacent node
                # in the queue
                q.append(i)

                # set
                visited[i] = True

    return ctb


def interpolate_between_cities(sol:PathSolution, city_prev, city):

    interpolated_path = [city_prev]

    info = sol.info
    coords_prev = sol.get_coords(city_prev)
    coords = sol.get_coords(city)
    coords_delta = coords - coords_prev
    axis_inc = np.array([sign(coords_delta[0]), sign(coords_delta[1])])

    num_mid_cities = int(max(abs(coords_delta))/info.cell_side_length)

    coords_temp = coords_prev.copy()

    for _ in range(num_mid_cities):
        if coords_temp[0] != coords[0]:
            coords_temp[0] += info.cell_side_length * axis_inc[0]
        if coords_temp[1] != coords[1]:
            coords_temp[1] += info.cell_side_length * axis_inc[1]
        mid_city = sol.get_city(coords_temp)
        # print(f"Iteration {_+1} coords: {coords_temp}, corresponding city: {mid_city}")
        interpolated_path.append(mid_city)

    # interpolated_path.pop(-1)

    # print(f"city prev: {city_prev}, city: {city}, mid cities: {interpolated_path}")
    
    return interpolated_path


'''
    def get_pathplan_new(self):

        info = self.info

        # Initialize path matrix
        self.path_matrix = np.full((info.number_of_drones + 1, self.time_steps), -1, dtype=int)
        
        for i in range(info.number_of_drones):
            drone_path = self.drone_dict[i]
            len_diff = self.time_steps - len(drone_path)
            self.path_matrix[i + 1] = np.pad(drone_path, (0, len_diff), constant_values=-1)

        self.real_time_path_matrix = self.path_matrix.copy()

        # Set Mission Time
        drone_path_matrix = self.real_time_path_matrix[1:, :].T
        max_distances_at_steps = [
            max(info.D[drone_path_matrix[i], drone_path_matrix[i + 1]])
            for i in range(drone_path_matrix.shape[0] - 1)
        ]
        self.mission_time = sum(max_distances_at_steps) / info.max_drone_speed

        # Set Total Distance and Longest Subtour
        subtour_lengths = {
            i: sum(info.D[self.real_time_path_matrix[i + 1, j], self.real_time_path_matrix[i + 1, j + 1]]
                for j in range(self.time_steps - 1))
            for i in range(info.number_of_drones)
        }

        self.total_distance = sum(subtour_lengths.values())
        self.longest_subtour = max(subtour_lengths.values())

        # Apply hovering if not single-objective model
        if info.model != distance_soo_model:
            path_lens = [len(path) for path in self.drone_dict.values()]
            max_len = max(path_lens)

            hovering_drone_ids = [i for i, length in enumerate(path_lens) if length != max_len]

            for drone in hovering_drone_ids:
                path = self.real_time_path_matrix[drone + 1].copy()
                hover_idx = np.where(path == -1)[0][1] - 1
                hover_cell = path[hover_idx]
                path[hover_idx:-1] = hover_cell
                self.real_time_path_matrix[drone + 1] = path

            # Interpolate path back to base station after hovering
            interpolated_steps = [
                interpolate_between_cities(self, self.real_time_path_matrix[drone + 1, -2], 0)[1:]
                if self.real_time_path_matrix[drone + 1, -2] != 0 else []
                for drone in range(info.number_of_drones)
            ]

            max_len_interpolated = max(len(step) for step in interpolated_steps)
            interpolated_steps = [
                step + [step[-1]] * (max_len_interpolated - len(step)) if step else [-1] * max_len_interpolated
                for step in interpolated_steps
            ]

            interpolated_array = np.vstack(
                [np.full((1, max_len_interpolated), -1, dtype=int)] + interpolated_steps
            )

            self.real_time_path_matrix = np.hstack(
                (self.real_time_path_matrix[:, :-1], interpolated_array, np.full((info.number_of_nodes, 1), -1, dtype=int))
            )

        self.time_slots = self.real_time_path_matrix.shape[1]


'''
