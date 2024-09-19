from pymoo.core.duplicate import DuplicateElimination, ElementwiseDuplicateElimination

class PathDuplicateElimination(DuplicateElimination):

    def __init__(self, func=None) -> None:
        super().__init__(func)

    def is_equal(self, a, b):
        # Check if two solutions are equal based on their path attributes
        path_a = a.get("path")
        path_b = b.get("path")

    def _do(self, pop, other, is_duplicate):
        pass

    

"""from pymoo.core.duplicate import DuplicateElimination, ElementwiseDuplicateElimination
import numpy as np

class PathDuplicateElimination(DuplicateElimination):

    def __init__(self, func=None) -> None:
        super().__init__(func)
    
    def is_equal(self, a, b):
        # Check if two solutions are equal based on their path attributes
        path_a = a.get("path")
        path_b = b.get("path")

    def _do(self, pop, other, is_duplicate):
        unique = []
        for i in range(len(pop)-1):
            for j in range(i+1, len(pop)):
                a = pop[i][0].path
                b = pop[j][0].path
                if np.all(a==b):
                    unique.append()

        # return super()._do(pop, other, is_duplicate)
        
        # Assuming the 'path' is a list or any iterable that can be compared
        return np.all(path_a==path_b)
"""