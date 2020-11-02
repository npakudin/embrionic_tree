import copy

from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.superimposed_tree import SuperimposedNode


def get_distances_by_files(pattern, global_params, is_reducing=True):
    # read trees from *.xtg files in xtg folder
    src_trees = read_all_trees(pattern=pattern)

    # create a copy of trees to modify
    trees = [copy.deepcopy(src_tree) for src_tree in src_trees]

    # prepare to calculate distances
    for tree in trees:
        if is_reducing:
            tree.reduce()
        tree.prepare()

    # calculate distances matrix
    distance_matrix = [[SuperimposedNode(v1.root, v2.root).full_distance(global_params) for v2 in trees] for v1 in trees]

    return [src_trees, distance_matrix]
