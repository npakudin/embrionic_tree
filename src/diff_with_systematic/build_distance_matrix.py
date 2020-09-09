import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.johansen_distance import short_sp_name
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, corrcoef

# Build matrices and corr coef only

systematic_tree = "morph"
max_level = 10

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                      ["Angiosperms"], max_level=max_level)

trees = matrDiff.vertices

# param_a = 0.5
# g_weight = 0.5
# chain_length_weight = 0.1

min_corr = 1000

for param_a in np.linspace(0.4, 0.6, 3):
    for g_weight in np.linspace(0.0, 0.3, 4):
        for chain_length_weight in np.linspace(0.0, 0.3, 4):
            global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=g_weight,
                                         chain_length_weight=chain_length_weight, is_swap_left_right=False)
            experiment_matrix = matrDiff.make_experiment_matrix(global_params)

            swap_global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=g_weight,
                                         chain_length_weight=chain_length_weight, is_swap_left_right=True)
            swap_experiment_matrix = matrDiff.make_experiment_matrix(swap_global_params)

            corr = corrcoef(swap_experiment_matrix, experiment_matrix)
            print(f"{param_a:0.2f} {g_weight:0.2f} {chain_length_weight:0.2f} {corr:0.3f}")
            if corr < min_corr:
                min_corr = corr
print(f"mincorr: {min_corr}")

#corr = matrDiff.corrcoef(experiment_matrix)
#name = f"param_a = {param_a}, g_weight = {g_weight}, chain_length_weight = {chain_length_weight}"

#tree_names = [short_sp_name(item) for item in matrDiff.names]

#print_matrix(experiment_matrix, name, tree_names, corr, with_headers=True)
