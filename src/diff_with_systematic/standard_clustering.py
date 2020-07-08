import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.clustering import corr_clustered_trees, draw_plot
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix, \
    corrcoef
import scipy.spatial.distance as ssd

from src.ultra_metric.ultra_metric import get_ultra_metric, UltraMetricParams


systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_level = 11

#calc_weights = [const_weight(1.0), exponent_reduced_weight(0.5), threshold_weight(5, 1.0, 0.75)]
calc_weights = [exponent_reduced_weight(0.45), exponent_reduced_weight(0.50), exponent_reduced_weight(0.55)]
#calc_weights = [exponent_reduced_weight(0.50)]
systematic_trees = ["morph"]
#cluster_algorithms = ['complete', 'average', 'weighted', 'centroid', 'median', 'ultrametric']
cluster_algorithms = ['average']

alg_to_corr = {}


matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level)

#for calc_weight in calc_weights:
for param_a in np.linspace(0.2, 0.6, 5):
#for param_a in np.linspace(0.1, 1.0, 10):
    calc_weight = exponent_reduced_weight(param_a)
    for systematic_tree in systematic_trees:
        for cluster_algorithm in cluster_algorithms:
            global_params = GlobalParams(g_weight=0.5, chain_length_weight=0.0, is_swap_left_right=is_swap_left_right,
                                         calc_weight=calc_weight, max_level=max_level,
                                         subtree_threshold=100, subtree_multiplier=1,
                                         # level_weight_multiplier=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
                                         level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                                         )

            experiment_matrix = matrDiff.make_experiment_matrix(global_params)

            # corr = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
            # name = f"{calc_weight.name}_corr_{corr:0.2f}_{systematic_tree}_{cluster_algorithm}_swap={is_swap_left_right}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
            #print_matrix(experiment_matrix, name, matrDiff.names, corr, with_headers=True)
            #experiment_array = make_experiment_array(experiment_matrix)

            effective_cluster_algorithm = cluster_algorithm
            if cluster_algorithm == 'ultrametric':
                ultra_matrix = get_ultra_metric(to_full_matrix(experiment_matrix), UltraMetricParams(max_level=len(experiment_matrix)))
                experiment_matrix = ultra_matrix
                effective_cluster_algorithm = 'average'

            plot_matrix = to_full_matrix(experiment_matrix)
            # convert the redundant n*n square matrix form into a condensed nC2 array
            # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
            dist_array = ssd.squareform(plot_matrix)

            #clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
            clustered_trees = hierarchy.linkage(dist_array, effective_cluster_algorithm)

            corr = corr_clustered_trees(clustered_trees, matrDiff.names, matrDiff.make_systematic_matrix())
            print(f"{global_params.g_weight:0.2f} {param_a:0.2f} {cluster_algorithm} {corr:0.2f}")

            if cluster_algorithm not in alg_to_corr.keys():
                alg_to_corr[cluster_algorithm] = []
            alg_to_corr[cluster_algorithm].append(corr)

            name = f"{calc_weight.name}_corr_{corr:0.2f}_{systematic_tree}_{cluster_algorithm}_swap={is_swap_left_right}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
            draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")


for k in alg_to_corr.keys():
    mean = np.mean(alg_to_corr[k])
    stddev = np.std(alg_to_corr[k], ddof=1)
    print(f"{k} {mean:0.3f} {stddev:0.3f}")


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
#             matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"], max_level=11)
#
#             experiment_matrix = matrDiff.make_experiment_matrix(global_params)
#
#             corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
#             print_matrix(experiment_matrix, name, matrDiff.names, corrcoef, with_headers=True)
#             experiment_array = make_experiment_array(experiment_matrix)
#
#             clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
#             draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")
