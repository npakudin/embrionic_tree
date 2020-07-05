from src.compare_trees.compare_trees import get_distances_by_files
from src.compare_trees.global_params import GlobalParams, exponent_reduced_weight

global_params = GlobalParams(calc_weight=exponent_reduced_weight(0.50), g_weight=0.05, chain_length_weight=0.4,
                             is_swap_left_right=True, max_level=11)

[trees, distance_matrix] = get_distances_by_files("../../input/xtg/*.xtg", global_params)

# print distance matrix to console
for tree in trees:
    print(f", {tree.name.replace(' ', '_')}", end='')
print("")
for row in distance_matrix:
    for item in row:
        print("%0.2f " % item, end='')
    print()

print(f"res {global_params.swaps} / {global_params.total}")
