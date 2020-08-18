import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy

from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, to_full_matrix

systematic_tree = "morph"
cluster_algorithm = "complete"
max_level = 11
param_a = 0.5
g_weight = 0.1
chain_length_weight = 0.0

global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=g_weight,
                             chain_length_weight=chain_length_weight)
name = f"param_a={param_a}_{systematic_tree}_{cluster_algorithm}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level)

experiment_matrix = matrDiff.make_experiment_matrix(global_params)
plot_matrix = to_full_matrix(experiment_matrix)

corrcoef = matrDiff.corrcoef(experiment_matrix)
print_matrix(plot_matrix, "experiment_matrix", matrDiff.names, corrcoef=corrcoef, with_headers=True)

# convert the redundant n*n square matrix form into a condensed nC2 array
# distArray[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
distArray = ssd.squareform(plot_matrix)
Z = hierarchy.linkage(distArray, 'complete')
# Z = hierarchy.linkage(distArray, 'average')
# print(Z)

plt.figure()
dn = hierarchy.dendrogram(Z,
                          labels=np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in matrDiff.names], np.str)
                          , orientation='right', count_sort='ascending', distance_sort='ascending')
plt.show()
exit()
