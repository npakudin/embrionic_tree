import copy
from src.compare_trees.development_tree_reader import read_all_trees
from src.compare_trees.distances import development_tree_distance


def get_distances_by_files(pattern, global_params):

    # read trees from *.xtg files in xtg folder
    src_trees = read_all_trees(pattern=pattern, max_levels = global_params.max_levels)

    # create a copy of trees to modify
    trees = [copy.deepcopy(src_tree) for src_tree in src_trees]

    # prepare to calculate distances
    for tree in trees:
        tree.root.reduce(global_params)
        tree.root.prepare(global_params)

    # calculate distances matrix
    distance_matrix = [[development_tree_distance(v1.root, v2.root, global_params) for v2 in trees] for v1 in trees]

    return [src_trees, distance_matrix]

