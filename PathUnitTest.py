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

from PathOptimizationModel import moo_model_with_disconn, distance_soo_model
from PathInput import *
from FilePaths import objective_values_filepath, solutions_filepath, runtimes_filepath
from FileManagement import save_as_pickle, load_pickle


class PathUnitTest(object):

    def __init__(self, scenario) -> None:

        self.model = model
        self.algorithm = self.model["Alg"] # From PathInput

        self.info = [PathInfo(scenario)] if not isinstance(scenario, list) else list(map(lambda x: PathInfo(x), scenario))

    def __call__(self, save_results=True, animation=True, *args: Any, **kwds: Any) -> Any:

        for info in self.info:
            F,X,R = self.run_optimization(info)
            if save_results:
                save_as_pickle(f"{solutions_filepath}{str(info)}-SolutionObjects.pkl", X)
                F.to_pickle(f"{objective_values_filepath}{str(info)}-ObjectiveValues.pkl")
                save_as_pickle(f"{runtimes_filepath}{str(info)}-Runtime.pkl", R)
                save_paths_and_anims_from_scenario(str(info))
            if animation:
                animate_extreme_point_paths(info)

            
    def run_optimization(self, info):

        t = time.time()
        t_start = time.time()
        res = minimize(problem=PathProblem(info),
                        algorithm=PathAlgorithm(self.algorithm)(),
                        termination=('n_gen',n_gen),
                        save_history=True,
                        seed=1,
                        output=PathOutput(PathProblem(info)),
                        verbose=True,
                        )
        t_end = time.time()
        t_elapsed_seconds = t_end - t_start
        t_elapsed_minutes = t_elapsed_seconds / 60
        X = res.X
        F= pd.DataFrame(abs(res.F), columns=model['F'])
        R = t_elapsed_seconds
        return F,X,R
        # print(f"Scenario: {str(info)}\nRuntime: {R} seconds\n") # Print the results



    # def Optimize(self, save_results, show_anim):

    #     t = time.time()

    #     for info in self.info:

    #         print(f"Scenario: {str(info)}")

    #         t_start = time.time()
    #         res = minimize(problem=PathProblem(info),
    #                         algorithm=PathAlgorithm(self.algorithm)(),
    #                         termination=('n_gen',n_gen),
    #                         save_history=True,
    #                         seed=1,
    #                         output=PathOutput(PathProblem(info)),
    #                         verbose=True,
    #                         )
    #         t_end = time.time()
    #         t_elapsed_seconds = t_end - t_start
    #         t_elapsed_minutes = t_elapsed_seconds / 60

    #         X = res.X

    #         F= pd.DataFrame(abs(res.F), columns=model['F'])

    #         R = t_elapsed_seconds
            
    #         print(f"Scenario: {str(info)}\nRuntime: {R} seconds\n") # Print the results

    #         if save_results:

    #             save_as_pickle(f"{solutions_filepath}{str(info)}-SolutionObjects.pkl", X)
    #             F.to_pickle(f"{objective_values_filepath}{str(info)}-ObjectiveValues.pkl")
    #             save_as_pickle(f"{runtimes_filepath}{str(info)}-Runtime.pkl", R)
    #             save_paths_and_anims_from_scenario(str(info))

    #             if show_anim:

    #                 if self.model == distance_soo_model:
    #                     test_anim = load_pickle(f"Results/Animations/{str(info)}-Best-Total_Distance-Animation.pkl")
    #                 else:
    #                     test_anim = load_pickle(f"Results/Animations/{str(info)}-Mid-Percentage_Connectivity-Animation.pkl")

    #                 show_anim = test_anim()

    #                 plt.show()


test = PathUnitTest(scenario=test_setup_scenario)
test(save_results=True, animation=False)
