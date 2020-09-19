import copy
from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.distances import development_tree_distance


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
    distance_matrix = [[development_tree_distance(v1, v2, global_params) for v2 in trees] for v1 in trees]

    return [src_trees, distance_matrix]
