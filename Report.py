from matplotlib import pyplot as plt
from FilePaths import *
from FileManagement import load_pickle
from PathSolution import *
from PathInfo import *
# from TimeBetweenVisits import calculate_mean_tbv

from collections import defaultdict

import os

def get_visit_times(sol:PathSolution):
    info = sol.info
    drone_path_matrix = sol.real_time_path_matrix[1:,:]
    visit_times = [[] for _ in range(info.number_of_cells)]
    # print(f"Path Matrix:\n{drone_path_matrix}")
    for cell in range(info.number_of_cells):
        # print(f"cell {cell} visit steps: {np.where(sol.real_time_path_matrix==cell)[1].tolist()}")
        visit_times[cell] = np.sort(np.where(drone_path_matrix==cell)[1])[:info.min_visits] # Last bit is to exclude hovering steps
    return visit_times

def calculate_tbv(visit_times):
    # print(visit_times)
    tbv = [np.diff(x) for x in visit_times]
    return tbv

def calculate_mean_tbv(tbv):
    return list(map(lambda x: np.mean(x), tbv))

def calculate_var_of_mean_tbv(sol:PathSolution):
    mean_tbv = get_visit_times(sol)



def model_comparison_heatmap_for_best_objs(models:list, r, numbers_of_drones:list, numbers_of_visits:list, show=True, save=False):
    """Plot a heatmap for comparison of the best objective values of the models for different numbers of drones and visits"""
    # TODO: Iterate through the scenario parameters - IP
    for n in numbers_of_drones:
        for v in numbers_of_visits:
            pass
            
    # TODO: Load the best objective values for the models - IP
    # TODO: Create a heatmap for each objective - IP
    # TODO: Save the heatmap - IP
    return -1


def plot_best_objs_for_nvisits(model, r, numbers_of_drones:list, numbers_of_visits:list, show=False, save=True):

    # directions = ["Best", "Mid", "Worst"]
    info_dict=PathInfo()
    info_dict.model = model
    info_dict.comm_cell_range = r

    y_values_list = [ dict() for _ in range(len(numbers_of_visits))]

    for i,v in enumerate(numbers_of_visits):
        info_dict.min_visits = v
        for n in numbers_of_drones:
            info_dict.number_of_drones = n
            scenario = str(info_dict)
            v_visits_n_drones_all_objective_values = pd.read_pickle(f"{objective_values_filepath}{scenario}-ObjectiveValues.pkl")
            objective_names = v_visits_n_drones_all_objective_values.columns
            for objective in objective_names:
                # print(y_values_list[v])
                if objective not in list(y_values_list[i].keys()):
                    y_values_list[i][objective] = []
                # print(y_values_list[v])
                # y_values_list[v][objective]
                # fig, ax = plt.subplots()
                # ax.set_xticks(numbers_of_drones)
                # ax.grid()
                v_visits_n_drones_objective_values = v_visits_n_drones_all_objective_values[objective]
                best_objective_value = min(v_visits_n_drones_objective_values) if objective != "Percentage Connectivity" else max(v_visits_n_drones_objective_values)
                y_values_list[i][objective].append(best_objective_value)


    # PLOT

    if r == 2*sqrt(2):
        r = sp.sqrt(round(r**2))

    # print("-->", r)

    x = numbers_of_drones
    for objective in objective_names:
        objective_with_underscore = objective.replace(" ", "_")
        # Create a figure and axis
        fig, ax = plt.subplots()
        ax.set_xticks(numbers_of_drones)
        ax.grid()
        # Add axis labels and a title
        ax.set_xlabel('Number of Drones')
        ax.set_ylabel(objective)
        ax.set_title(f'{objective} for Different Number of Visits and {r} Cell(s) Communication Range', fontsize="small")
        for i,v in enumerate(numbers_of_visits):
            y = y_values_list[i][objective]
            ax.scatter(x, y, label=f'{v} Visit(s)')
            # Annotate Scatter Plot
            for j in range(len(x)):
                ax.annotate(f'{round(y[j], 2)}', (x[j], y[j]), textcoords="offset points", xytext=(0,5), ha='center')
            ax.plot(x, y)
        # Add a legend to the plot
        ax.legend()
        # Save plot
        if save:
            plt.savefig(f"Figures/Objective Values/r_{r}_n_{numbers_of_drones}_v_{numbers_of_visits}_{objective_with_underscore}.png")
    
    if show:
        plt.show()


def plot_time_between_visits_vs_number_of_drones(model:dict, r_values:list, numbers_of_drones:list, numbers_of_visits:list, show=True, save=False):
    """Take the best objective solutions for the required scenarios and plot tbv vs number of drones"""

    filepath = "Figures/Time Between Visits/Mean Mean TBV vs Number of Drones/"

    assert (1 not in numbers_of_visits), "1 Should not be in numbers of visits"

    x = numbers_of_drones

    # objective_names = []

    # y_values_list = [ np.zeros(len(numbers_of_drones)) for _ in range(len(numbers_of_visits))]

    model_parameters_str = f"{model['Type']}_{model['Alg']}_{model['Exp']}"
    model_solutions_filenames = [x for x in os.listdir("Results/Solutions") if model_parameters_str in x]
    best_solutions_filenames = [x for x in model_solutions_filenames if "Best" in x]
    # best_solutions_filenames = [x for x in os.listdir("Results/Solutions") if "SolutionObjects" not in x and "Best" in x]
    objective_names = model["F"] # list(set([x.split("-")[2].replace("_", " ") for x in best_solutions_filenames]))
    best_solutions = [load_pickle(f"{solutions_filepath}{x}") for x in best_solutions_filenames]
    infos_of_best_solutions = [x.info for x in best_solutions]

    # n_12_filenames = [x for x in best_solutions_filenames if "n_12" in x and "r_2" in x and "r_2*sqrt(2)" not in x and "Mission_Time" in x]
    # print(np.array(n_12_filenames))

    # fmts = ['o', 's', '^', 'x', 'D', 'P', 'H', 'v', '<', '>', 'd', 'p', '*', 'X', '+', '|', '_', '.', ',']

    for r_comm in r_values:
        for obj in objective_names:
            objective_with_underscore = obj.replace(" ", "_")
            fig, ax = plt.subplots(figsize=(7,5))
            ax.set_xticks(numbers_of_drones)
            ax.grid()
            for n_visits in numbers_of_visits:
                # fmt = fmts[numbers_of_visits.index(n_visits)]
                y = []
                max_values = []
                for n_drones in numbers_of_drones:
                    print(obj, n_drones, r_comm, n_visits)
                    n_drones_r_comm_n_visits_best_obj_solution = [
                                                                    best_solutions[i] for i in range(len(best_solutions)) if infos_of_best_solutions[i].model["F"]==model["F"] # Filter model parameters
                                                                    and infos_of_best_solutions[i].model["Type"]==model["Type"] 
                                                                    and infos_of_best_solutions[i].model["Exp"]==model["Exp"] 
                                                                    and infos_of_best_solutions[i].model["Alg"]==model["Alg"] # Filter model parameters
                                                                    and infos_of_best_solutions[i].min_visits==n_visits 
                                                                    and infos_of_best_solutions[i].number_of_drones==n_drones 
                                                                    and infos_of_best_solutions[i].comm_cell_range==r_comm # Filter scenario parameters
                                                                    and obj.replace(" ","_") in best_solutions_filenames[i] # Filter objective
                                                                ][0]
                    n_drones_r_comm_n_visits_best_obj_info = n_drones_r_comm_n_visits_best_obj_solution.info
                    scenario = str(n_drones_r_comm_n_visits_best_obj_info)
                    # Get cumulative mean
                    # vt = get_visit_times(n_drones_r_comm_n_visits_best_obj_solution)
                    # tbv = calculate_tbv(vt)
                    # mean_tbv = [np.mean(x) for x in tbv]
                    mean_tbv = n_drones_r_comm_n_visits_best_obj_solution.mean_tbv
                    cum_mean_tbv = np.mean(mean_tbv)
                    # Append cumulative mean tbv to y
                    y.append(cum_mean_tbv)
                # Scatter Plot
                ax.scatter(x, y)
                ax.plot(x, y, label=f"{n_visits} visit(s)")
                # Add Error Bars
                variance = np.var(y)
                std_dev = np.sqrt(variance)
                # ax.errorbar(x, y, yerr=std_dev, fmt="x", capsize=5, label=f'{n_visits} visit(s) error bar')
                # Add shaded variance area
                ax.fill_between(x, y - variance, y + variance, alpha=0.2, label=f"{n_visits} visit(s) variance")
                max_values.append(max(y))

            
            max_value = max(max_values)
            # ax.set_ylim([0, max_value+1])
            ax.set_title(f"Best {obj} Solution Cumulative Mean TBV vs Number of Drones with Variance", fontsize="small")
            ax.legend(loc='upper right', ncol=2, fontsize="small")

            # plt.tight_layout()

            if show:
                plt.show()

            if save:
                fig.savefig(f"{filepath}{scenario}-Best-{objective_with_underscore}-mean_tbv_vs_number_of_drones_with_variance.png")

def plot_time_between_visits_vs_dist_to_bs(info:PathInfo, show=False, save=True):

    mean_tbv_vs_dist_to_bs_dist_folder = "Figures/Time Between Visits/Distance to BS vs Mean TBV/Distribution/"
    mean_tbv_vs_dist_to_bs_hist_folder = "Figures/Time Between Visits/Distance to BS vs Mean TBV/Histogram/"
    cum_mean_tbv_vs_number_of_drones_folder = "Figures/Time Between Visits/Cumulative Mean TBV vs Number of Drones/"

    scenario = str(info)
    brief_scenario = f"n_{info.number_of_drones}_r_{info.comm_cell_range}_v_{info.min_visits}" if info.comm_cell_range != 2*sqrt(2) else f"n_{info.number_of_drones}_r_{sp.sqrt(round(info.comm_cell_range**2))}_v_{info.min_visits}"
    save_as = f"{info.model['Type']}_{info.model['Alg']}_{info.model['Exp']}_n_{info.number_of_drones}_r_{info.comm_cell_range}_v_{info.min_visits}" if info.comm_cell_range != 2*sqrt(2) else f"{info.model['Type']}_{info.model['Alg']}_{info.model['Exp']}_n_{info.number_of_drones}_r_{sp.sqrt(round(info.comm_cell_range**2))}_v_{info.min_visits}"
    # print(scenario)

    scenario_all_objective_values = pd.read_pickle(f"{objective_values_filepath}{scenario}-ObjectiveValues.pkl")
    objective_names = scenario_all_objective_values.columns

    dist_to_bs = info.D[-1][:-1]
    # print(f"Dist to BS: {dist_to_bs}, Len: {len(dist_to_bs)}")

    directions = ["Best"]

    for objective in objective_names:

        # Create a figure and axis
        mean_tbv_vs_dist_to_bs_dist_fig, mean_tbv_vs_dist_to_bs_dist_ax = plt.subplots()
        mean_tbv_vs_dist_to_bs_hist_fig, mean_tbv_vs_dist_to_bs_hist_ax = plt.subplots()
        # ax.set_xticks(dist_to_bs)
        mean_tbv_vs_dist_to_bs_dist_ax.grid(axis='y')
        # Add axis labels and a title
        mean_tbv_vs_dist_to_bs_dist_ax.set_xlabel('Distance to BS')
        mean_tbv_vs_dist_to_bs_dist_ax.set_ylabel("Mean Time Between Visits")

        mean_tbv_vs_dist_to_bs_hist_ax.set_xlabel('Mean Time Between Visits')
        mean_tbv_vs_dist_to_bs_hist_ax.set_ylabel("Frequency")

        objective_with_underscore = objective.replace(" ","_")
        # objective_values = scenario_all_objective_values[objective]
        # best_objective_value_ind = objective_values.idxmin() if objective != "Percentage Connectivity" else objective_values.idxmax()
        for dir in directions:
            sol = load_pickle(f"{solutions_filepath}{scenario}-{dir}-{objective_with_underscore}-Solution.pkl")
            vt = get_visit_times(sol)
            tbv = calculate_tbv(vt)
            mean_tbv = [np.mean(x) for x in tbv]
            cum_mean_tbv = np.mean(mean_tbv)
            # sum_tbv = [np.sum(x) for x in tbv]
            mean_tbv_vs_dist_to_bs_dist_ax.set_title(f'{save_as} {dir} {objective} Solution Mean TBV', fontsize="small")
            mean_tbv_vs_dist_to_bs_dist_ax.scatter(dist_to_bs, mean_tbv, label="Mean TBV")
            mean_tbv_vs_dist_to_bs_dist_ax.plot(np.arange(ceil(max(dist_to_bs))+1), [cum_mean_tbv]*(ceil(max(dist_to_bs))+1), label = "Cumulative Mean TBV", color="blue")
            mean_tbv_vs_dist_to_bs_dist_ax.set_xlim([0,round(max(dist_to_bs))+1])
            mean_tbv_vs_dist_to_bs_dist_ax.set_xticks([min(dist_to_bs), np.mean(dist_to_bs), max(dist_to_bs)])
            mean_tbv_vs_dist_to_bs_dist_ax.legend()
            bin_width = 1.0
            bins = np.arange(min(mean_tbv), max(mean_tbv) + bin_width, bin_width)
            # hist_ax.set_title(f'{scenario} {dir} {objective} Solution Mean TBV Histogram', fontsize="small")
            mean_tbv_vs_dist_to_bs_hist_ax.set_title(f'{save_as} {dir} {objective} Solution Mean TBV', fontsize="small")
            mean_tbv_vs_dist_to_bs_hist_ax.hist(mean_tbv, bins=bins, edgecolor='black')
            # ax.scatter(dist_to_bs, sum_tbv, label="Sum TBV")
            # Save Plot
            if save:
                mean_tbv_vs_dist_to_bs_dist_fig.savefig(f"{mean_tbv_vs_dist_to_bs_dist_folder}{save_as}-{dir}-{objective_with_underscore}-mean_tbv_dist.png")
                mean_tbv_vs_dist_to_bs_hist_fig.savefig(f"{mean_tbv_vs_dist_to_bs_hist_folder}{save_as}-{dir}-{objective_with_underscore}-mean_tbv_hist.png")
            if show:
                plt.show()


def plot_mean_mean_tbv_vs_number_of_drones_with_variance_for_extreme_points(model:dict, comm_cell_ranges, numbers_of_drones, numbers_of_visits, show=True, save=False):
    """Plot the mean mean tbv vs number of drones with variance"""
    # TODO: Convert comm_cell_ranges, numbers_of_drones, numbers_of_visits to lists if they are not - DONE
    if not isinstance(comm_cell_ranges, list):
        comm_cell_ranges = [comm_cell_ranges]
    if not isinstance(numbers_of_drones, list):
        numbers_of_drones = [numbers_of_drones]
    if not isinstance(numbers_of_visits, list):
        numbers_of_visits = [numbers_of_visits]

    # TODO: Filter the best solutions for the model - DONE
    model_parameters_str = f"{model['Type']}_{model['Alg']}_{model['Exp']}"
    model_solutions_filenames = [x for x in os.listdir("Results/Solutions") if model_parameters_str in x]
    best_solutions_filenames = [x for x in model_solutions_filenames if "Best" in x]
    objective_names = model["F"]
    best_solutions = [load_pickle(f"{solutions_filepath}{x}") for x in best_solutions_filenames]
    infos_of_best_solutions = [x.info for x in best_solutions]

    # TODO: Iterate through parameters - IP
    for r in comm_cell_ranges:
        for n in numbers_of_drones:
            for v in numbers_of_visits:
                pass

    
# if __name__ == "__main":

"""Plot TBV vs Number of Drones"""
plot_time_between_visits_vs_number_of_drones(model=time_conn_disconn_tbv_nsga2_model, r_values=[2, 2*sqrt(2), 4], numbers_of_drones=[4,8,12,16], numbers_of_visits=[2,3], show=False, save=True)


"""Plot Objs"""
# model = time_conn_disconn_tbv_nsga2_model
# comm_cell_range_values = [2]
# for r in comm_cell_range_values:
#     plot_best_objs_for_nvisits(model, r, numbers_of_drones=[4,8,12,16], numbers_of_visits=[1,2,3], show=True, save=False)


"""Plot TBV vs Dist to BS"""
# info = PathInfo()
# info.model = time_conn_disconn_tbv_nsga2_model
# numbers_of_drones_values = [4,8,12,16]
# comm_cell_range_values = [2, 2*sqrt(2), 4]
# min_visits_values = [2,3]
# for n in numbers_of_drones_values:
#     info.number_of_drones = n
#     for r in comm_cell_range_values:
#         info.comm_cell_range = r
#         for v in min_visits_values:
#             info.min_visits = v
#             plot_time_between_visits_vs_dist_to_bs(info=info, show=True, save=False)