import numpy as np
import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy

from src.cluster_trees.clustering import corr_clustered_trees, draw_plot
from src.multiple_trees.trees_matrix import to_full_matrix
from src.single_tree.global_params import GlobalParams
from src.multiple_trees.matrix_diff import MatrixDiff
from src.ultra_metric.ultra_metric import get_ultra_metric, UltraMetricParams

systematic_tree = "morph"
max_level = 11

systematic_trees = ["morph"]
#cluster_algorithms = ['complete', 'average', 'weighted', 'centroid', 'median', 'ultrametric']
cluster_algorithms = ['average']

alg_to_corr = {}



# for tree in matrDiff.vertices:
#     print(f"{tree.name} : {tree.node.depth}")

for param_a in np.linspace(0.2, 0.8, 7):
    for systematic_tree in systematic_trees:
        for cluster_algorithm in cluster_algorithms:
            #for increasing_level in [-1, 3 - 1, 7 - 1]: #range(-1, 8):
            #for increasing_level in [-1]: #range(-1, 8):
            for use_flipping in [False, True]:
                matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                                      ["Angiosperms"],
                                      max_level=max_level, is_reducing=True, use_flipping=use_flipping)

                increasing_level = -1
                level_weight_multiplier = [1] * 11
                if increasing_level >= 0:
                    level_weight_multiplier[increasing_level] *= 5

                global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=0.0,
                                             chain_length_weight=0.0, level_weight_multiplier=level_weight_multiplier,
                                             use_flipping=use_flipping)

                experiment_matrix = matrDiff.make_experiment_matrix(global_params)

                # corr = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
                # name = f"param_a={param_a}_corr_{corr:0.2f}_{systematic_tree}_{cluster_algorithm}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
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
                print(f"{global_params.g_weight:0.2f} {param_a:0.2f} {increasing_level:2} {cluster_algorithm} {corr:0.8f}")

                if cluster_algorithm not in alg_to_corr.keys():
                    alg_to_corr[cluster_algorithm] = []
                alg_to_corr[cluster_algorithm].append(corr)

                name = f"param_a={param_a}_{systematic_tree}_{cluster_algorithm}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}_corr_{corr:0.2f}"
                draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")


# for k in alg_to_corr.keys():
#     mean = np.mean(alg_to_corr[k])
#     stddev = np.std(alg_to_corr[k], ddof=1)
#     print(f"{k} {mean:0.3f} {stddev:0.3f}")


# param_as = [1.0, 0.5, threshold_weight(5, 1.0, 0.75)]
# systematic_trees = ["apg4", "morph"]
# cluster_algorithms = ['average', 'centroid', 'complete', 'median', 'weighted']
#
# for param_a in param_as:
#     for systematic_tree in systematic_trees:
#         for cluster_algorithm in cluster_algorithms:
#
#             name = f"param_a={param_a}_{systematic_tree}_{cluster_algorithm}"
#
#             global_params = GlobalParams(g_weight=0.1, chain_length_weight=0.1, param_a=param_a)
#
#             matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"], max_level=10)
#
#             experiment_matrix = matrDiff.make_experiment_matrix(global_params)
#
#             corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
#             print_matrix(experiment_matrix, name, matrDiff.names, corrcoef, with_headers=True)
#             experiment_array = make_experiment_array(experiment_matrix)
#
#             clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
#             draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")
