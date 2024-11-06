from PathInfo import *

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PathSolution import PathSolution
from FileManagement import load_pickle
# from PathInput import test_setup_scenario
from PathAnimation import PathAnimation

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

visits = [1, 2, 3]
drones = [4, 8, 12, 16]

data = {
    "Number of Drones": drones * len(visits) * 2,
    "Number of Visits": sum([[v] * len(drones) for v in visits] * 2, []),
    "Model": ["Model 1"] * (len(drones) * len(visits)) + ["Model 2"] * (len(drones) * len(visits)),
    "Performance": np.random.rand(len(drones) * len(visits) * 2)  # replace with actual values
}

df = pd.DataFrame(data)

# Plot line plot comparison
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="Number of Drones", y="Performance", hue="Model", style="Model", markers=True)
plt.title("Performance Comparison for Different Number of Visits")
plt.xlabel("Number of Drones")
plt.ylabel("Performance Metric")
plt.legend(title="Model")
plt.show()

"""F = load_pickle("Results/Objectives/MOO_NSGA2_time_conn_disconn_tbv_g_8_a_50_n_20_v_2.5_r_2*sqrt(2)_minv_3_maxv_5_Nt_1_tarPos_12_ptdet_0.99_pfdet_0.01_detTh_0.9_maxIso_0-ObjectiveValues.pkl")
shape = F.shape

print(shape)"""


"""# Initialize the PathInfo object
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
    plt.show()"""