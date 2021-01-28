import copy

from src.multiple_trees.trees_matrix import full_distance
from src.single_tree.development_tree_reader import read_all_trees


def get_distances_by_files(pattern, global_params, is_reducing, use_flipping=False, use_min_common_depth=False, is_test_nodes=False):
    # read trees from *.xtg files in xtg folder
    src_trees = read_all_trees(pattern=pattern, is_test_nodes=is_test_nodes)

    # create a copy of trees to modify
    trees = [copy.deepcopy(src_tree) for src_tree in src_trees]

    # prepare to calculate distances
    for tree in trees:
        if is_reducing:
            tree.reduce(global_params.is_test_nodes)
        tree.prepare(use_min_common_depth, use_flipping)

    # calculate distances matrix
    distance_matrix = [[full_distance(global_params, v1.root, v2.root, v2.flipped_root) for v2 in trees] for v1 in trees]

    return [src_trees, distance_matrix]
