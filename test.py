from PathInfo import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PathSolution import PathSolution
from FileManagement import load_pickle
from PathInput import test_setup_scenario
from PathAnimation import PathAnimation


# Initialize the PathInfo object
info = PathInfo(test_setup_scenario)

scenario = str(info)
directions = ["Best", "Mid", "Worst"]
objectives = [x.replace(" ", "_") for x in info.model["F"]]

# Iterate through each objective
for obj in objectives:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))  # Create subplots with 1 row and 3 columns
    fig.suptitle(f"Obj: {model['Exp']}, Alg: {model['Alg']}, n={info.number_of_drones}, r={info.comm_cell_range}, v:{info.min_visits}")
    # title = f"{direction} {obj.replace('_',' ')} Paths"
    animations = []  # Store all animations to prevent garbage collection

    for ax, direction in zip(axes, directions):
        ax.set_title(f"{direction} {obj.replace('_',' ')} Paths")
        sol = load_pickle(f"Results/Solutions/{scenario}-{direction}-{obj}-Solution.pkl")
        anim_object = PathAnimation(sol, fig, ax)
        anim = FuncAnimation(
            fig, anim_object.update, frames=anim_object.paths[0].shape[1],
            init_func=anim_object.initialize_figure, blit=False, interval=0
        )
        animations.append(anim)  # Store the animation object

    plt.tight_layout()
    plt.show()