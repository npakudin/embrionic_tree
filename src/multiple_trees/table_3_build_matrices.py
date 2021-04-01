from src.multiple_trees.compare_trees import get_distances_by_files
from src.multiple_trees.trees_matrix import print_matrix
from src.single_tree.development_tree_utils import not_standard_short_sp_name
from src.single_tree.global_params import GlobalParams


global_params = GlobalParams(max_level=10, param_a=0.50, g_weight=0.0, chain_length_weight=0.0)

[trees, distance_matrix] = get_distances_by_files("../../input/xtg/*.xtg", global_params, is_reducing=True)

# print distance matrix to console
#print(f"_", end='')
for tree in trees:
    print(f" {not_standard_short_sp_name(tree.name)}")
# print("")
# for i, row in enumerate(distance_matrix):
#     print(f"{trees[i].name.replace(' ', '_')} ", end='')
#     for item in row:
#         print("%0.2f " % item, end='')
#     print()


#print_matrix(distance_matrix, "", trees)
