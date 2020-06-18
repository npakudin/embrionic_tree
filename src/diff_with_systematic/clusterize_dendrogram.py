import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, to_full_matrix
import matplotlib
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
import scipy.spatial.distance as ssd



systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_levels = 11
param_a = 0.5
g_weight=0.1
chain_length_weight=0.0

calc_weight = exponent_reduced_weight(param_a)
global_params = GlobalParams(g_weight=g_weight, chain_length_weight=chain_length_weight, is_swap_left_right=is_swap_left_right,
                             calc_weight=calc_weight, max_levels=max_levels,
                             subtree_threshold=1000, subtree_multiplier=1,
                             #level_weight_multiplier=[512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 0]
                             #level_weight_multiplier=[4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
                             level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                             )
name = f"{calc_weight.name}_{systematic_tree}_{cluster_algorithm}_swap={is_swap_left_right}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"], max_levels=max_levels)

experiment_matrix = matrDiff.make_experiment_matrix(global_params)
plot_matrix = to_full_matrix(experiment_matrix)


corrcoef = matrDiff.corrcoef(experiment_matrix)
print_matrix(plot_matrix, "experiment_matrix", matrDiff.names, corrcoef=corrcoef, with_headers=True)

# convert the redundant n*n square matrix form into a condensed nC2 array
# distArray[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
distArray = ssd.squareform(plot_matrix)
Z = hierarchy.linkage(distArray, 'complete')
#Z = hierarchy.linkage(distArray, 'average')
#print(Z)

plt.figure()
dn = hierarchy.dendrogram(Z, labels = np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in matrDiff.names], np.str)
                          , orientation='right',count_sort = 'ascending', distance_sort='ascending')
plt.show()
exit()
