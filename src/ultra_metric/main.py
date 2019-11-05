from scipy.cluster import hierarchy
import numpy as np
from src.compare_trees.compare_trees import get_distances_by_files
from src.compare_trees.global_params import GlobalParams, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, make_experiment_array, print_matrix
from src.diff_with_systematic.standard_clustering import draw_plot
from src.ultra_metric.ultra_metric import UltraMetricParams, get_ultra_metric, average_error

matrDiff = MatrixDiff("../../input/xtg/*.xtg", "../../input/systematic_tree_morph.xtg", ["Angiosperms"], max_levels=11)

init_values = [0.15, 0.2, 0.1]
x = init_values
global_params = GlobalParams(g_weight=x[1], chain_length_weight=x[2], is_swap_left_right=True,
                             calc_weight=exponent_reduced_weight(a=x[0]))


experiment_matrix = matrDiff.make_full_experiment_matrix(global_params)
print(experiment_matrix)

for level_count in range(27):
    name = f"minarsky_um_{level_count + 1}"
    ultra_matrix = get_ultra_metric(experiment_matrix, UltraMetricParams(level_count=level_count + 1))

    experiment_array = make_experiment_array(ultra_matrix)
    clustered_trees = hierarchy.linkage(np.asarray(experiment_array), 'average')
    corrcoef = matrDiff.corrcoef(ultra_matrix)

    print_matrix(ultra_matrix, name, matrDiff.names, corrcoef, with_headers=True)
    draw_plot(clustered_trees, matrDiff.names, name, f"../../output/ultra_metric/{name}.png")
