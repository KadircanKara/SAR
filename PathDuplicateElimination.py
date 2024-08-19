from pymoo.core.duplicate import ElementwiseDuplicateElimination
import numpy as np

class PathDuplicateElimination(ElementwiseDuplicateElimination):

    def is_equal(self, a, b):
        hash_a = hash(tuple(a.X[0].path))
        hash_b = hash(tuple(b.X[0].path))
        
        # Compare the hashes
        return hash_a == hash_b