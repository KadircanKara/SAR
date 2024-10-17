from matplotlib import pyplot as plt
from FilePaths import *
from FileManagement import load_pickle
from PathSolution import *
from PathInfo import *
from TimeBetweenVisits import calculate_mean_tbv

from collections import defaultdict

import os
import shutil

'''def zip_folders(folder1, folder2, )
# Paths of folders to compress
folder1 = '/path/to/folder1'
folder2 = '/path/to/folder2'

# Temporary directory to copy folders for compression
temp_dir = '/path/to/temp_dir'

# Copy both folders to a temporary directory
shutil.copytree(folder1, os.path.join(temp_dir, 'folder1'))
shutil.copytree(folder2, os.path.join(temp_dir, 'folder2'))

# Create the archive (choose zip or tar)
shutil.make_archive('combined_archive', 'zip', temp_dir)

# Cleanup: Optionally, remove the temporary folder after compression
shutil.rmtree(temp_dir)
'''

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

def calculate_mean_tbv(sol:PathSolution):
    info = sol.info
    drone_path_matrix = sol.real_time_path_matrix[1:,:]
    visit_times = [[] for _ in range(info.number_of_cells)]
    tbv = visit_times.copy()
    # print(f"Path Matrix:\n{drone_path_matrix}")
    for cell in range(info.number_of_cells):
        # print(f"cell {cell} visit steps: {np.where(sol.real_time_path_matrix==cell)[1].tolist()}")
        visit_times[cell] = np.sort(np.where(drone_path_matrix==cell)[1])[:info.min_visits] # Last bit is to exclude hovering steps
        tbv[cell] = np.diff(visit_times[cell])
    return visit_times, list(map(lambda x: np.mean(x), tbv))



def plot_best_objs_for_nvisits(r, numbers_of_drones:list, numbers_of_visits:list, show=False, save=True):

    # directions = ["Best", "Mid", "Worst"]
    info_dict=PathInfo()
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
            for i in range(len(x)):
                ax.annotate(f'{round(y[i], 2)}', (x[i], y[i]), textcoords="offset points", xytext=(0,5), ha='center')
            ax.plot(x, y)
        # Add a legend to the plot
        ax.legend()
        # Save plot
        if save:
            plt.savefig(f"Figures/Objective Values/r_{r}_n_{numbers_of_drones}_v_{numbers_of_visits}_{objective_with_underscore}.png")
    
    if show:
        plt.show()


def plot_time_between_visits_vs_number_of_drones(model:dict, r_values:list, numbers_of_drones:list, numbers_of_visits:list, shaded_area=True, errorbar=True, show=True, save=False):
    """Take the best objective solutions for the required scenarios and plot tbv vs number of drones"""

    assert (1 not in numbers_of_visits), "1 Should not be in numbers of visits"

    folder = "Figures/Time Between Visits/Mean Mean TBV vs Number of Drones/"

    x = numbers_of_drones

    # objective_names = []

    # y_values_list = [ np.zeros(len(numbers_of_drones)) for _ in range(len(numbers_of_visits))]

    best_solutions_filenames = [x for x in os.listdir("Results/Solutions") if "SolutionObjects" not in x and "Best" in x]
    objective_names = model["F"] # list(set([x.split("-")[2].replace("_", " ") for x in best_solutions_filenames]))
    best_solutions = [load_pickle(f"{solutions_filepath}{x}") for x in best_solutions_filenames]
    infos_of_best_solutions = [x.info for x in best_solutions]

    # n_12_filenames = [x for x in best_solutions_filenames if "n_12" in x and "r_2" in x and "r_2*sqrt(2)" not in x and "Mission_Time" in x]
    # print(np.array(n_12_filenames))

    fmt_colors = ['kx', 'cx']
    fill_colors = ['k','c']

    for r_comm in r_values:
        for obj in objective_names:
            fig, ax = plt.subplots()
            max_value = 0
            ax.set_xticks(numbers_of_drones)
            ax.grid()
            for k, n_visits in enumerate(numbers_of_visits):
                fmt = fmt_colors[k]
                fill = fill_colors[k]
                y = []
                for n_drones in numbers_of_drones:
                    
                    # print(obj, n_drones, r_comm, n_visits)
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
                    # Get cumulative mean
                    vt = get_visit_times(n_drones_r_comm_n_visits_best_obj_solution)
                    tbv = calculate_tbv(vt)
                    mean_tbv = [np.mean(x) for x in tbv]
                    mean_mean_tbv = np.mean(mean_tbv)
                    var_mean_tbv = np.var(mean_tbv)
                    std_mean_tbv = np.sqrt(var_mean_tbv)
                    # Append cumulative mean tbv to y
                    y.append(mean_mean_tbv)
                # Scatter Plot
                ax.scatter(x, y)
                ax.plot(x, y, label=f"{n_visits} visit(s)")
                # Add variance with errorbar or shaded area or both
                if errorbar:
                    ax.errorbar(x, y, yerr=std_mean_tbv, fmt=fmt, label=f'{n_visits} visit(s) error bars', capsize=5)
                if shaded_area:
                    ax.fill_between(x, y - std_mean_tbv, y + std_mean_tbv, color=fill, alpha=0.2, label=f'{n_visits} visit(s) variance')

                if max(y)+std_mean_tbv > max_value:
                    max_value = max(y)+std_mean_tbv

            # Set y-lim, title and legend    
            ax.set_ylim([0, max_value+3])
            ax.set_title(f"r_{sp.sqrt(round(r_comm**2))}_Best_{obj}_Solution_Mean_Mean_TBV_with_Errorbars", fontsize="medium")
            ax.legend(fontsize='small', ncol=3)

            if save:
                fig.savefig(f"{folder}{ax.get_title()}.png")
    if show:
        plt.show()


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


# if __name__ == "__main":

# plot_time_between_visits_vs_number_of_drones(model=time_conn_disconn_nsga2_model, r_values=[2, 2*sqrt(2), 4], numbers_of_drones=[4,8,12,16], numbers_of_visits=[2,3], shaded_area=True, errorbar=True, show=False, save=True)

comm_cell_range_values = [2, 2*sqrt(2)]
for r in comm_cell_range_values:
    plot_best_objs_for_nvisits(r, numbers_of_drones=[4,8,12,16], numbers_of_visits=[1], show=True, save=False)


    # info = PathInfo()
    # numbers_of_drones_values = [4,8,12,16]
    # comm_cell_range_values = [2, 2*sqrt(2), 4]
    # min_visits_values = [2,3]
    # for n in numbers_of_drones_values:
    #     info.number_of_drones = n
    #     for r in comm_cell_range_values:
    #         info.comm_cell_range = r
    #         for v in min_visits_values:
    #             info.min_visits = v
    #             plot_time_between_visits_vs_dist_to_bs(info=info, show=False, save=True)