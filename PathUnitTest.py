from statistics import median, median_low, median_high
from typing import Any
import pickle
from PathAlgorithm import *
from PathOutput import *
from pymoo.operators.crossover.nox import NoCrossover
from pymoo.operators.mutation.nom import NoMutation
from pymoo.core.duplicate import NoDuplicateElimination
from pymoo.optimize import minimize
from PathResults import save_paths_and_anims_from_scenario, animate_extreme_point_paths
# from PathTermination import PathTermination
from PathAnimation import PathAnimation
from Time import *
import os
import shutil
# from google.colab import drive
# drive.mount('/content/drive')

from PathOptimizationModel import *
from PathInput import *
# from main import *
from FilePaths import *
from FileManagement import save_as_pickle, load_pickle

from pymoo.termination.default import DefaultTermination, DefaultMultiObjectiveTermination
from pymoo.core.termination import Termination
from PathTermination import PathDefaultMultiObjectiveTermination


class PathUnitTest(object):

    def __init__(self, scenario) -> None:

        self.model = model
        self.algorithm = self.model["Alg"] # From PathInput

        self.info = [PathInfo(scenario)] if not isinstance(scenario, list) else list(map(lambda x: PathInfo(x), scenario))

    def __call__(self, save_results=True, animation=True, copy_to_drive=False, *args: Any, **kwds: Any) -> Any:

        for info in self.info:
            print(f"Scenario: {str(info)}")
            res, F,X,R = self.run_optimization(info)
            if X is not None:
                if save_results:
                    save_as_pickle(f"{res_filepath}{str(info)}-Res.pkl", X)
                    save_as_pickle(f"{solutions_filepath}{str(info)}-SolutionObjects.pkl", X)
                    F.to_pickle(f"{objective_values_filepath}{str(info)}-ObjectiveValues.pkl")
                    save_as_pickle(f"{runtimes_filepath}{str(info)}-Runtime.pkl", R)
                    save_paths_and_anims_from_scenario(str(info))
                    if copy_to_drive:
                        source_dir = '/content/Results'
                        target_dir = '/content/drive/My Drive/SAR/Results'
                        shutil.copy(source_dir, target_dir)

                if animation:
                    animate_extreme_point_paths(info)

                print(f"Scenario: {str(info)} COMPLETED !!!")
            else:
                print(f"Scenario: {str(info)} NO SOLUTION FOUND !!!")

            
    def run_optimization(self, info):

        problem = PathProblem(info)
        algorithm = PathAlgorithm(self.algorithm)()
        # default_termination = DefaultTermination(algorithm.x, algorithm.cv, algorithm.f, n_max_gen=n_gen)
        # termination = DefaultMultiObjectiveTermination()
        termination = ('n_gen', n_gen)
        output = PathOutput(problem)

        res, F, X, R = None, None, None, None,

        t = time.time()
        t_start = time.time()

        res = minimize(problem=PathProblem(info),
                        algorithm=algorithm,
                        termination=termination,
                        save_history=True,
                        seed=1,
                        output=output,
                        verbose=True,
                        )
        
        t_end = time.time()
        t_elapsed_seconds = t_end - t_start

        if res.X is not None:
            # print(res.X)
            X = res.X
            F= pd.DataFrame(abs(res.F), columns=model['F'])
            R = t_elapsed_seconds
            # If certain attributes are missing from the solution objects, add them here
            sample_sol = X[0][0] if isinstance(X[0], np.ndarray) else X[0]
            # Add TBV and Disconnecivity attributes to the solution objects if they are not already calculated
            for row in X:
                if isinstance(row, np.ndarray):
                    sol = row[0]
                else:
                    sol = row
                if not sample_sol.calculate_tbv:
                    sol.get_visit_times()
                    sol.get_tbv()
                    sol.get_mean_tbv()
                if not sample_sol.calculate_disconnectivity:
                    sol.do_disconnectivity_calculations()


        return res, F,X,R