from PathUnitTest import *

def run_n_visit_scenarios(n:int, save_results=True, animation=False):
    n_dict = {  
                0: test_setup_scenario,
                1: single_visit_setup_scenarios,
                2: two_visits_setup_scenarios,
                3: three_visits_setup_scenarios,
                4: four_visits_setup_scenarios,
                5: five_visits_setup_scenarios
    }
    scenario = n_dict[n]
    test = PathUnitTest(scenario)
    test(save_results, animation)