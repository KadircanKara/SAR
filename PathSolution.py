
import numpy as np
from numpy.lib.function_base import average
from pymoo.core.problem import ElementwiseProblem
from scipy.spatial import distance
from typing import List, Dict
import itertools
from math import sin, cos, atan2, ceil
from scipy import io
# from scipy.stats import itemfreq
import subprocess
import time
import copy
import matplotlib.pyplot as plt # 1.20.3
from collections import deque
import multiprocessing as mp
from multiprocessing import Pool, cpu_count

from PathInfo import *
from PathOptimizationModel import moo_model_with_disconn, distance_soo_model
from PathInput import model

# from PathRepair import *

# from distance import *
# from Conumber_of_nodesectivity import *
# from Time import *

# from PathAnimation import PathAnimation

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0  # Returns 0 if x is exactly 0

def split_list(lst, val):
    return [list(group) for k,
    group in
            itertools.groupby(lst, lambda x: x == val) if not k]


# if __name__ == '__main__' :

class PathSolution():

    def __str__(self):
        info = self.info
        return f"Scenario: number_of_cells_{info.number_of_cells}_A_{info.cell_side_length}_number_of_drones_{info.number_of_drones}_V_{info.max_drone_speed}_rc_{info.comm_cell_range}_maxVisits_{info.min_visits}\n" \
            f"Objective Values: totaldistance_{self.total_distance}_longestSubtour_{self.longest_subtour}_percentageConumber_of_nodesectivity_{self.percentage_connectivity}\n" \
            f"Chromosome: pathSequenumber_of_cellse_{self.path}_startPoints_{self.start_points}"

    def __init__(self, path, start_points, info:PathInfo, calculate_pathplan=True, calculate_connectivity=True, calculate_disconnectivity=True):

        # self.hovering = info.hovering
        # self.realtime_conumber_of_nodesectivity = info.realtime_conumber_of_nodesectivity

        # Inputs
        self.path = path
        self.start_points = start_points
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

        # Connectivity
        self.connectivity_matrix = None
        self.disconnected_time_steps = None
        self.percentage_connectivity = None

        if calculate_pathplan:
            self.get_drone_dict()
            self.get_pathplan() # Calculates drone dict and path matrix (not interpolated, directly from the path sequenumber_of_cellse and start points)
        
        if calculate_connectivity:
            if model != distance_soo_model:
                self.do_connectivity_calculations()
        if calculate_disconnectivity:
            if model == moo_model_with_disconn:
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

        subtour_lengths = dict()

        for i in range(info.number_of_drones):
            drone_path = self.real_time_path_matrix[i+1]
            drone_dist = 0
            for j in range(time_steps-1):
                drone_dist += info.D[drone_path[j],drone_path[j+1]]
            subtour_lengths[i] = drone_dist

        self.total_distance = sum(subtour_lengths.values())
        self.longest_subtour = max(subtour_lengths.values())

        # APPLY HOVERING TO DRONES WITH SHORTER PATHS (ONLY IF MOO)

        if info.model != distance_soo_model:

            # drone_dict = {k:v for k,v in self.drone_dict.items() if k!=-1}
            # print(f"Dict Values Object: {list(drone_dict.items())}")
            path_lens = [len(path) for path in list(self.drone_dict.values())]
            # hovering_drone_ids = [path_lens.index(i) for i in path_lens if i != max(path_lens)]
            # hovering_drone_ids = [i for i in range(info.number_of_drones) if i != path_lens.index(max(path_lens))]
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
            # print(f"Path Lens: {path_lens}")
            # print(f"Hovering Drone IDs: {hovering_drone_ids}")
            for drone in hovering_drone_ids:
                # print("----------------------------------------------------------")
                # print(f"Drone {drone}:")
                # print("----------------------------------------------------------")
                # APPLY HOVERING
                path_without_hovering = self.real_time_path_matrix[drone+1].copy()
                # Find last cell
                hovering_cell_idx = np.where(path_without_hovering==-1)[0][1] - 1
                hovering_cell = path_without_hovering[hovering_cell_idx]
                # print(f"Hovering Cell Idx: {hovering_cell_idx}, Hovering Cell: {hovering_cell}")
                hovering_component = np.array([hovering_cell] * (len(path_without_hovering) - hovering_cell_idx - 1))
                # print(f"Hovering Component: {hovering_component}")
                path_with_hovering = path_without_hovering.copy()
                # path_with_hovering = np.insert(path_with_hovering, )
                path_with_hovering[hovering_cell_idx:len(path_without_hovering)-1] = hovering_component
                self.real_time_path_matrix[drone+1] = path_with_hovering
            # INTERPOLATE PATH BACK TO BS AFTER HOVERING
            # print("Iniitial Path Matrix:\n", self.real_time_path_matrix)
            drone_interpolated_last_step_list = []
            for drone in range(info.number_of_drones):
                drone_interpolated_last_step = interpolate_between_cities(self, self.real_time_path_matrix[drone+1][-2], 0)
                if self.real_time_path_matrix[drone+1][-2] != 0:
                    drone_interpolated_last_step = drone_interpolated_last_step[1:]
                # print("-->", drone_interpolated_last_step)
                drone_interpolated_last_step_list.append(drone_interpolated_last_step)
            max_interpolated_last_step_len = max([len(x) for x in drone_interpolated_last_step_list])

            # print(drone_interpolated_last_step_list)

            for drone in range(info.number_of_drones):
                if len(drone_interpolated_last_step_list[drone]) < max_interpolated_last_step_len:
                    # print("Old Last Step:", drone_interpolated_last_step_list[drone])
                    drone_interpolated_last_step_list[drone].extend([drone_interpolated_last_step_list[drone][-1]] * (max_interpolated_last_step_len - len(drone_interpolated_last_step_list[drone])))
                    # print("New Last Step:", drone_interpolated_last_step_list[drone])
                    # print(drone_interpolated_last_step_list[i])
                # self.real_time_path_matrix[drone+1] = np.insert(self.real_time_path_matrix, -1, drone_interpolated_last_step_list[i])
            # print("Final Last Steps:", drone_interpolated_last_step_list)
            drone_interpolated_path_array = np.insert(np.array(drone_interpolated_last_step_list), 0, np.full((1,max_interpolated_last_step_len), -1, dtype=int), axis=0)
            # print(drone_interpolated_path_array)
            # print(np.array(drone_interpolated_last_step_list))
            # print(np.array(drone_interpolated_last_step_list).shape, self.real_time_path_matrix.shape)
            # print(self.real_time_path_matrix.shape, drone_interpolated_path_array.shape)
            self.real_time_path_matrix = np.hstack((self.real_time_path_matrix[:,:-1], drone_interpolated_path_array, np.full((info.number_of_nodes,1), -1, dtype=int)))
            # self.real_time_path_matrix = np.insert(self.real_time_path_matrix, -1, drone_interpolated_path_array, axis=1)

        # print("Final Path Matrix:\n", self.real_time_path_matrix)


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

        for time in range(self.time_slots):

            adj_mat = self.connectivity_matrix[time]

            # Find disconnected nodes
            disconnected_rows = np.all(adj_mat == 0, axis=1)
            # Get the indices of disconnected nodes
            num_disconnected_nodes = len(np.where(disconnected_rows)[0])
            # Update disconnected node array
            num_disconnected_nodes_array[time] = num_disconnected_nodes

        self.mean_disconnected_time = np.mean(num_disconnected_nodes_array)
        self.max_disconnected_time = np.max(num_disconnected_nodes_array)
        self.total_disconnected_time = np.sum(num_disconnected_nodes_array)
        self.percentage_disconnectivity = np.sum(num_disconnected_nodes_array) / (self.time_slots * self.info.number_of_nodes)

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
