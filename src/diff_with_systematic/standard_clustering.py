import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix, \
    corrcoef
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
    plt.close(fig)
    #plt.show()


def corr_clustered_trees(clustered_trees, names, src_matr):
    n = len(names)
    matr = []
    for i in range(n):
        matr.append([])
        for j in range(i):
            matr[i].append(0)

    clusters = []
    for i in range(n):
        clusters.append([i])

    for i, item in enumerate(clustered_trees):
        cluster = clusters[int(item[0])] + clusters[int(item[1])]
        clusters.append(cluster)

    for item in clustered_trees:
        c1 = clusters[int(item[0])]
        c2 = clusters[int(item[1])]
        for i in c1:
            for j in c2:
                row = max(int(i), int(j))
                col = min(int(i), int(j))
                matr[row][col] = float(item[2])

    corr = corrcoef(matr, src_matr)
    #print_matrix(matr, f"clustered matr", names, corr, with_headers=True)
    return corr


systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_levels = 11

#calc_weights = [const_weight(1.0), exponent_reduced_weight(0.5), threshold_weight(5, 1.0, 0.75)]
calc_weights = [exponent_reduced_weight(0.45), exponent_reduced_weight(0.50), exponent_reduced_weight(0.55)]
#calc_weights = [exponent_reduced_weight(0.50)]
systematic_trees = ["morph"]
cluster_algorithms = ['complete', 'average', 'weighted', 'centroid', 'median']
#cluster_algorithms = ['complete']

alg_to_corr = {}


matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_levels=max_levels)

#for calc_weight in calc_weights:
for param_a in np.linspace(0.2, 0.6, 5):
    calc_weight = exponent_reduced_weight(param_a)
    for systematic_tree in systematic_trees:
        for cluster_algorithm in cluster_algorithms:
            global_params = GlobalParams(g_weight=0.5, chain_length_weight=0.0, is_swap_left_right=is_swap_left_right,
                                         calc_weight=calc_weight, max_levels=max_levels,
                                         subtree_threshold=100, subtree_multiplier=1,
                                         # level_weight_multiplier=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
                                         level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                                         )

            experiment_matrix = matrDiff.make_experiment_matrix(global_params)

            corr = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
            name = f"{calc_weight.name}_corr_{corr:0.2f}_{systematic_tree}_{cluster_algorithm}_swap={is_swap_left_right}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
            #print_matrix(experiment_matrix, name, matrDiff.names, corr, with_headers=True)
            experiment_array = make_experiment_array(experiment_matrix)

            plot_matrix = to_full_matrix(experiment_matrix)
            # convert the redundant n*n square matrix form into a condensed nC2 array
            # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
            dist_array = ssd.squareform(plot_matrix)

            #clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
            clustered_trees = hierarchy.linkage(dist_array, cluster_algorithm)
            #draw_plot(clustered_trees, matrDiff.names, name, f"../../output/diff_with_systematic/{name}.png")

            corr = corr_clustered_trees(clustered_trees, matrDiff.names, matrDiff.make_systematic_matrix())
            print(f"{global_params.g_weight:0.2f} {param_a:0.2f} {cluster_algorithm} {corr:0.2f}")

            if cluster_algorithm not in alg_to_corr.keys():
                alg_to_corr[cluster_algorithm] = []
            alg_to_corr[cluster_algorithm].append(corr)

for k in alg_to_corr.keys():
    mean = np.mean(alg_to_corr[k])
    stddev = np.std(alg_to_corr[k], ddof=1)
    print(f"{k} {mean} {stddev} {mean - stddev} {mean + stddev}")


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
