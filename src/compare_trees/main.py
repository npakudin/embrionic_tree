import copy
from src.compare_trees.development_tree_reader import read_all_trees
from src.compare_trees.distances import dist_branch_direction
from src.compare_trees.global_params import GlobalParams


src_trees = read_all_trees()


# create a copy to modify
trees = [copy.deepcopy(src_tree) for src_tree in src_trees]
global_params = GlobalParams(a=0.8, b=0.8, g=1, param_g_weight=0.1, change_left_right=True)

# prepare to calculate distances
for tree in trees:
    tree.root.reduce(global_params.g)
    tree.root.prepare(global_params)

# calculate distances matrix
distance_matrix = [[dist_branch_direction(v1.root, v2.root, global_params) for v2 in trees] for v1 in trees]

# print distance matrix to console
for tree in trees:
    print(f", {tree.name.replace(' ', '_')}", end='')
print("")
for row in distance_matrix:
    for item in row:
        print("%0.2f " % item, end='')
    print()
