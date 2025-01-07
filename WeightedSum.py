from PathSolution import PathSolution

def mission_time_and_percentage_connectivity_ws(sol:PathSolution):
    return sol.mission_time/2 - sol.percentage_connectivity/2

def mission_time_and_percentage_connectivity_and_max_disconnected_time_and_mean_disconnected_time_ws(sol:PathSolution):
    return sol.mission_time/4 - sol.percentage_connectivity/4 + sol.max_disconnected_time/4 + sol.mean_disconnected_time/4

def mission_time_and_percentage_connectivity_and_max_mean_tbv_ws(sol:PathSolution):
    return sol.mission_time/3 - sol.percentage_connectivity/3 + sol.max_mean_tbv/3

def mission_time_and_percentage_connectivity_and_max_disconnected_time_and_mean_disconnected_time_and_max_mean_tbv_ws(sol:PathSolution):
    # Normalize Required Objectives
    normalized_mission_time = float(f"0.{str(round(sol.mission_time))}")
    normalized_max_disconnected_time = float(f"0.{str(round(sol.max_disconnected_time))}")
    normalized_max_mean_tbv = float(f"0.{str(round(sol.max_mean_tbv))}")
    # Sum Objectives (Normalized and otherwise)
    normalized_objective_value = normalized_mission_time - sol.percentage_connectivity + normalized_max_disconnected_time + sol.mean_disconnected_time + normalized_max_mean_tbv
    # print(f"Normalized Objective Value: {normalized_objective_value}")
    return normalized_objective_value
    # return sol.mission_time/5 - sol.percentage_connectivity/5 + sol.max_disconnected_time/5 + sol.mean_disconnected_time/5 + sol.max_mean_tbv/5