import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.iterate_trees import get_chain, get_deepest_node, generate_bin_tree, get_subtrees
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, corrcoef

# Build matrices and corr coef only

systematic_tree = "morph"
max_level = 11

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                      ["Angiosperms"], max_level=max_level)

global_params = GlobalParams(max_level=max_level, param_a=0.5, g_weight=0,
                             chain_length_weight=0, subtree_threshold=1000,
                             subtree_multiplier=1, level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

trees = matrDiff.vertices



feature_matrix = []
for i in range(len(matrDiff.taxon_matrix)):
    feature_matrix.append([])
    for j in range(i):
        dist = 0 if matrDiff.taxon_matrix[i][j] < 5 else 1
        #dist = matrDiff.taxon_matrix[i][j]
        feature_matrix[i].append(dist)

res = []

# iterate over chains
# for i in range(1, pow(2, 7)):
#     pattern = get_chain(i)
#     experiment_matrix = matrDiff.make_experiment_matrix(global_params, pattern=pattern)
#     corr = corrcoef(feature_matrix, experiment_matrix)
#     res.append([corr, get_deepest_node(pattern).address])

# iterate over subtrees
for level in range(5):
    root = generate_bin_tree(level)
    for pattern in get_subtrees(root):
        if pattern is None:
            continue

        experiment_matrix = matrDiff.make_experiment_matrix(global_params, pattern=pattern)
        corr = corrcoef(feature_matrix, experiment_matrix)
        #print_matrix(feature_matrix, "feature_matrix", matrDiff.names, corr, with_headers=True)
        res.append([corr, pattern.full_tree_str()])

res = sorted(res, key=lambda item: -item[0])
for item in res:
    print(f"{item[0]:0.3f} - {item[1]}")
