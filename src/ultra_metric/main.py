import numpy as np
from scipy.cluster import hierarchy

from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff, make_experiment_array, print_matrix
from src.diff_with_systematic.standard_clustering import draw_plot
from src.ultra_metric.ultra_metric import UltraMetricParams, get_ultra_metric


def common_corrcoef(systematic_matrix, experiment_matrix):
    systematic_array = []
    experiment_array = []
    for i, systematic_row in enumerate(systematic_matrix):
        for j, systematic_col in enumerate(systematic_row):
            systematic_array.append(systematic_matrix[i][j])
            experiment_array.append(experiment_matrix[i][j])

    corrcoef_matrix = np.corrcoef([systematic_array, experiment_array])

    return corrcoef_matrix[0][1]


matrDiff = MatrixDiff("../../input/xtg/*.xtg", "../../input/systematic_tree_morph.xtg", ["Angiosperms"], max_level=11)

init_values = [0.5, 0.1, 0.0]
x = init_values
global_params = GlobalParams(max_level=11, param_a=x[0], g_weight=x[1], chain_length_weight=x[2])


experiment_matrix = matrDiff.make_full_experiment_matrix(global_params)
print(experiment_matrix)

for level_count in range(30):
    name = f"ultrametric_{x[0]}_{x[1]}_{x[2]}_{level_count + 1}"
    ultra_matrix = get_ultra_metric(experiment_matrix, UltraMetricParams(max_level=level_count + 1))

    ultra_array = make_experiment_array(ultra_matrix)
    clustered_trees = hierarchy.linkage(np.asarray(ultra_array), 'average')
    corrcoef = matrDiff.corrcoef(ultra_matrix)
    corrcoef2 = common_corrcoef(experiment_matrix, ultra_matrix)

    print_matrix(ultra_matrix, name, matrDiff.names, corrcoef, with_headers=True)
    draw_plot(clustered_trees, matrDiff.names, name, f"../../output/ultra_metric/{name}.png")
