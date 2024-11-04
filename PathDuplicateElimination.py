from pymoo.core.duplicate import DuplicateElimination
import numpy as np

class PathDuplicateElimination(DuplicateElimination):
    def __init__(self, func=None) -> None:
        super().__init__(func)
    
    def is_equal(self, a, b):
        # Check if two solutions are equal based on their path and start_points attributes
        path_a = a.get("path")
        path_b = b.get("path")
        start_points_a = a.get("start_points")
        start_points_b = b.get("start_points")
        
        # Assuming the 'path' and 'start_points' are lists or any iterable that can be compared
        return np.array_equal(path_a, path_b) and np.array_equal(start_points_a, start_points_b)

    def _do(self, pop, other, is_duplicate):
        if other is None:
            return np.full(len(pop), False)
        
        # Only check the offspring solutions
        offspring = other
        is_duplicate_offspring = np.full(len(offspring), False)
        
        for i in range(len(offspring)):
            if is_duplicate_offspring[i]:
                continue
            for j in range(i + 1, len(offspring)):
                if self.is_equal(offspring[i], offspring[j]):
                    is_duplicate_offspring[j] = True
        
        return is_duplicate_offspring