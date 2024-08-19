import numpy as np
from pymoo.core.mutation import Mutation
from pymoo.operators.crossover.ox import random_sequence
from pymoo.operators.mutation.inversion import inversion_mutation
from scipy.spatial import distance
from typing import List, Dict
import random
from copy import copy, deepcopy

from PathSolution import *
from PathInfo import *
from PathProblem import *

# class PathMutation(Mutation):
#     def __init__(self, prob=0.1, mutation_info=None):
#         super().__init__()
#         self.prob = prob
#         if mutation_info is None:
#             mutation_info = {
#                 "swap_last_point": (0, 3),
#                 "swap": (0.3, 1),
#                 "inversion": (0.4, 1),
#                 "scramble": (0.3, 1),
#                 "insertion": (0, 1),
#                 "displacement": (0, 1),
#                 "block inversion": (0, 1),
#             }
#         self.mutation_info = mutation_info

#     def _do(self, problem: PathProblem, X, **kwargs):
#         Y = X.copy()

#         for i, y in enumerate(X):
#             # if np.random.random() < self.prob:
#             sol: PathSolution = y[0]
#             path = np.copy(sol.path)
#             mut_path = path

#             # Batch mutation checks
#             mutations_to_apply = {
#                 "swap": np.random.random() <= self.mutation_info["swap"][0],
#                 "inversion": np.random.random() <= self.mutation_info["inversion"][0],
#                 "scramble": np.random.random() <= self.mutation_info["scramble"][0],
#                 "insertion": np.random.random() <= self.mutation_info["insertion"][0],
#                 "displacement": np.random.random() <= self.mutation_info["displacement"][0],
#                 "block inversion": np.random.random() <= self.mutation_info["block inversion"][0]
#             }

#             # Apply mutations efficiently using numpy
#             if mutations_to_apply["swap"]:
#                 for _ in range(self.mutation_info["swap"][1]):
#                     seq = random_sequence(len(path))
#                     mut_path[seq[0]], mut_path[seq[1]] = mut_path[seq[1]], mut_path[seq[0]]

#             if mutations_to_apply["inversion"]:
#                 for _ in range(self.mutation_info["inversion"][1]):
#                     seq = random_sequence(len(path))
#                     mut_path[seq[0]:seq[1]] = mut_path[seq[0]:seq[1]][::-1]

#             if mutations_to_apply["scramble"]:
#                 for _ in range(self.mutation_info["scramble"][1]):
#                     seq = random_sequence(len(path))
#                     np.random.shuffle(mut_path[seq[0]:seq[1]])

#             if mutations_to_apply["insertion"]:
#                 for _ in range(self.mutation_info["insertion"][1]):
#                     cell = np.random.choice(mut_path)
#                     cell_ind = np.where(mut_path == cell)[0][0]
#                     mut_path = np.delete(mut_path, cell_ind)
#                     new_position = np.random.choice(np.arange(len(mut_path) + 1))
#                     mut_path = np.insert(mut_path, new_position, cell)

#             if mutations_to_apply["displacement"]:
#                 for _ in range(self.mutation_info["displacement"][1]):
#                     start, end = random_sequence(len(path))
#                     seq = mut_path[start:end]
#                     mut_path = np.delete(mut_path, np.arange(start, end))
#                     new_position = np.random.choice(np.arange(len(mut_path) + 1))
#                     mut_path = np.insert(mut_path, new_position, seq)

#             if mutations_to_apply["block inversion"]:
#                 for _ in range(self.mutation_info["block inversion"][1]):
#                     start, end = random_sequence(len(path))
#                     seq = np.flip(mut_path[start:end])
#                     mut_path = np.delete(mut_path, np.arange(start, end))
#                     new_position = np.random.choice(np.arange(len(mut_path) + 1))
#                     mut_path = np.insert(mut_path, new_position, seq)

#             Y[i][0] = PathSolution(mut_path, sol.start_points, problem.info)

#         return Y


class PathMutation(Mutation):

    def __init__(self,
                mutation_info={
                    "swap_last_point":(0, 1),
                    "swap": (0.3, 1), # 0.5
                    "inversion": (0.4, 1), # 1
                    "scramble": (0.3, 1), # 0.6
                    "insertion": (0, 1),
                    "displacement": (0, 1),
                    # "reverse sequence": (0.3, 1),
                    "block inversion": (0, 1),
                    # "shift": (0.3, 1),
                }
    ) -> None:

        super().__init__()

        self.mutation_info = mutation_info

    def _do(self, problem : PathProblem, X, **kwargs):

        Y = X.copy()

        for i, y in enumerate(X):
            # print("-->", y)
            sol : PathSolution = y[0]

            start_points = sol.start_points
            path = np.copy(sol.path)
            mut_path = path

            # print("Original Start Points:",start_points)
            #
            # PATH MUTATIONS
            if np.random.random() <= self.mutation_info["swap_last_point"][0] and "Percentage Connectivity" in sol.info.model["F"]:
                    hovering_cells = [sol.drone_dict[i][-2] for i in range(sol.info.number_of_drones)]
                    # hovering_cell_indexes =[np.where(sol.path==cell) for cell in hovering_cells]
                    for _ in range(self.mutation_info["swap_last_point"][1]):
                        random_hovering_cell = random.choice(hovering_cells)
                        random_hovering_cell_ind = np.where(sol.path==random_hovering_cell)[0][0]
                        # print("-->",list(np.arange(len(sol.path))))
                        all_cell_indices = list(np.arange(len(sol.path)))
                        all_cell_indices.pop(random_hovering_cell_ind)
                        swap_ind = random.choice(all_cell_indices)
                        seq = (random_hovering_cell_ind, swap_ind)
                        mut_path = np.hstack((
                        mut_path[:seq[0]], np.array([mut_path[seq[1]]]), mut_path[seq[0]+1:seq[1]], np.array([mut_path[seq[0]]]), mut_path[seq[1]+1:]
                    ))


            if np.random.random() <= self.mutation_info["swap"][0]:
                for _ in range(self.mutation_info["swap"][1]):
                    seq = random_sequence(len(path))
                    # print(f"swapped cells: {mut_path[seq[0]]} and {mut_path[seq[1]]}")
                    # print(f"pre-swap path: {mut_path}")
                    mut_path = np.hstack((
                        mut_path[:seq[0]], np.array([mut_path[seq[1]]]), mut_path[seq[0]+1:seq[1]], np.array([mut_path[seq[0]]]), mut_path[seq[1]+1:]
                    ))
                    # print(f"post-swap path: {mut_path}")


            if np.random.random() <= self.mutation_info["inversion"][0]:
                for _ in range(self.mutation_info["inversion"][1]):
                    seq = random_sequence(len(path))
                    mut_path = inversion_mutation(mut_path, seq, inplace=True)


            if np.random.random() <= self.mutation_info["scramble"][0]:
                for _ in range(self.mutation_info["scramble"][1]):
                    seq = random_sequence(len(path))
                    random.shuffle(mut_path[seq[0]:seq[1]])


            if np.random.random() <= self.mutation_info["insertion"][0]:
                for _ in range(self.mutation_info["insertion"][1]):
                    cell = np.random.choice(mut_path)
                    cell_ind = np.where(mut_path == cell)[0][0]
                    mut_path = np.delete(mut_path, cell_ind)
                    new_position = np.random.choice(np.array([i for i in range(len(mut_path) + 1) if i != cell_ind]))
                    mut_path = np.insert(mut_path, new_position, cell)


            if np.random.random() <= self.mutation_info["displacement"][0]:
                for _ in range(self.mutation_info["displacement"][1]):
                    start, end = random_sequence(len(path))
                    seq = mut_path[start:end]
                    indices = np.arange(start, end)
                    mut_path = np.delete(mut_path, indices)
                    new_position = np.random.choice(np.array([i for i in range(len(mut_path) + 1) if i < start or i > start]))
                    mut_path = np.insert(mut_path, new_position, seq)


            if np.random.random() <= self.mutation_info["block inversion"][0]:
                for _ in range(self.mutation_info["block inversion"][1]):
                    start, end = random_sequence(len(path))
                    seq = np.flip(mut_path[start:end])
                    indices = np.arange(start, end)
                    mut_path = np.delete(mut_path, indices)
                    new_position = np.random.choice(np.array([i for i in range(len(mut_path) + 1) if i < start or i > start]))
                    mut_path = np.insert(mut_path, new_position, seq)



            # START POINTS MUTATIONS

                    # cell = np.random.choice(mut_path)
                    # print("cell: ", cell)
                    # cell_ind = np.where(mut_path==cell)[0][0]
                    # print("pre-insertion: ", mut_path)
                    # mut_path = np.delete(arr=mut_path, obj=cell, axis=0)
                    # mut_path = np.insert(mut_path, np.random.choice(np.array([i for i in range(len(mut_path)+1) if i != cell_ind])), cell)
                    # print("post-insertion: ", mut_path)

            mut_start_points = np.copy(start_points)

            Y[i][0] = PathSolution(mut_path, mut_start_points, problem.info)

        return Y