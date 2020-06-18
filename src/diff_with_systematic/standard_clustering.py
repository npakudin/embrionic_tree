import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix
import scipy.spatial.distance as ssd


def draw_plot(clustered_trees, names, plot_name, filename):
    plt.rcParams["figure.figsize"] = (12.5, 8)
    plt.rcParams["figure.dpi"] = 80
    fig = plt.figure()

    ax1 = fig.add_axes((0.13, 0.1, 0.84, 0.85))
    ax1.set_title(plot_name)
    ax1.set_xlabel("distance, Minarskys")

    hierarchy.dendrogram(clustered_trees,
                         labels=np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in names], np.str),
                         orientation='right', count_sort='ascending', distance_sort='ascending')
    fig.savefig(filename)
    #plt.show()


systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_levels = 11

#calc_weights = [const_weight(1.0), exponent_reduced_weight(0.5), threshold_weight(5, 1.0, 0.75)]
#calc_weights = [exponent_reduced_weight(0.45), exponent_reduced_weight(0.50), exponent_reduced_weight(0.55)]
calc_weights = [exponent_reduced_weight(0.50)]
systematic_trees = ["morph"]
cluster_algorithms = ['complete', 'average']

for calc_weight in calc_weights:
    for systematic_tree in systematic_trees:
        for cluster_algorithm in cluster_algorithms:
            global_params = GlobalParams(g_weight=0.1, chain_length_weight=0.0, is_swap_left_right=is_swap_left_right,
                                         calc_weight=calc_weight,  max_levels=max_levels,
                                         subtree_threshold=100, subtree_multiplier=1,
                                         #level_weight_multiplier=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
                                         level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                                         )

            matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"], max_levels=max_levels)

            experiment_matrix = matrDiff.make_experiment_matrix(global_params)

            corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
            name = f"{calc_weight.name}_corr_{corrcoef:0.2f}_{systematic_tree}_{cluster_algorithm}_swap={is_swap_left_right}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
            print_matrix(experiment_matrix, name, matrDiff.names, corrcoef, with_headers=True)
            experiment_array = make_experiment_array(experiment_matrix)

            plot_matrix = to_full_matrix(experiment_matrix)
            # convert the redundant n*n square matrix form into a condensed nC2 array
            # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
            dist_array = ssd.squareform(plot_matrix)
            Z = hierarchy.linkage(dist_array, 'complete')

            clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
            draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")


# calc_weights = [const_weight(1.0), exponent_reduced_weight(0.5), threshold_weight(5, 1.0, 0.75)]
# systematic_trees = ["apg4", "morph"]
# cluster_algorithms = ['average', 'centroid', 'complete', 'median', 'weighted']
#
# for calc_weight in calc_weights:
#     for systematic_tree in systematic_trees:
#         for cluster_algorithm in cluster_algorithms:
#
#             name = f"{calc_weight.name}_{systematic_tree}_{cluster_algorithm}"
#
#             global_params = GlobalParams(g_weight=0.1, chain_length_weight=0.1, is_swap_left_right=True, calc_weight=calc_weight)
#
#             matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"], max_levels=11)
#
#             experiment_matrix = matrDiff.make_experiment_matrix(global_params)
#
#             corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
#             print_matrix(experiment_matrix, name, matrDiff.names, corrcoef, with_headers=True)
#             experiment_array = make_experiment_array(experiment_matrix)
#
#             clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
#             draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")
