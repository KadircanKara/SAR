from typing import Any
import time

from PathAlgorithm import *
from PathOutput import *
from pymoo.optimize import minimize
from PathResults import save_paths_and_anims_from_scenario, animate_extreme_point_paths
# from PathTermination import PathTermination
# from Time import *
import os
import shutil
# from google.colab import drive
# drive.mount('/content/drive')

from PathInput import *
from FilePaths import *
from FileManagement import save_as_pickle


class PathUnitTest(object):

    def __init__(self, scenario) -> None:

        self.model = model
        self.algorithm = self.model["Alg"] # From PathInput

        self.info = [PathInfo(scenario=scenario, pop_size=pop_size, gen_size=gen_size, model=model)] if not isinstance(scenario, list) else list(map(lambda x: PathInfo(scenario=x, pop_size=pop_size, gen_size=gen_size, model=model), scenario))

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
                    save_paths_and_anims_from_scenario(info)
                    if copy_to_drive:
                        source_dir = '/content/Results'
                        target_dir = '/content/drive/My Drive/SAR/Results'
                        shutil.copy(source_dir, target_dir)

                if animation:
                    animate_extreme_point_paths(info)
            else:
                print(f"Scenario: {str(info)} NO SOLUTION FOUND !!!")

            
    def run_optimization(self, info):

        res, F, X, R = None, None, None, None,

        t = time.time()
        t_start = time.time()

        res = minimize(problem=PathProblem(info),
                        algorithm=PathAlgorithm(self.algorithm)(),
                        termination=('n_gen',gen_size),
                        save_history=True,
                        seed=1,
                        output=PathOutput(PathProblem(info)),
                        verbose=True,
                        )
        
        t_end = time.time()
        t_elapsed_seconds = t_end - t_start

        if res.X is not None:
            print(res.X)
            X = res.X
            F= pd.DataFrame(abs(res.F), columns=model['F'])
            R = t_elapsed_seconds

        return res, F,X,R
    
if __name__ == "__main__":

    dir = os.listdir("Results/Objectives")
    minv_2_files = np.array([x for x in dir if ("minv_2" in x) and ("time_conn_disconn" in x)])
    # print(minv_2_files)

    print(f"sp mut prob: {path_mutation.mutation_info['sp_mutation']}, crossover prob: {path_crossover.prob}, ox prob: {path_crossover.ox_prob}" )

    # run_n_visit_scenarios(2)
    test = PathUnitTest(scenario)
    test(save_results=True, animation=False, copy_to_drive=False)

    os.system('afplay /System/Library/Sounds/Glass.aiff')
