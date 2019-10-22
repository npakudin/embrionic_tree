from src.compare_trees.compare_trees import get_distances_by_files
from src.compare_trees.global_params import GlobalParams
from src.ultra_metric.ultra_metric import UltraMetricParams, get_ultra_metric, average_error

ultra_metric_params = UltraMetricParams(level_count=6)

global_params = GlobalParams(a=0.5, b=0.5, g=1, param_g_weight=0.1, chain_length_weight=0.1, is_swap_left_right=True,
                             max_levels=11)
[trees, distance_matrix] = get_distances_by_files("../../input/xtg/*.xtg", global_params)

ultra_matrix = get_ultra_metric(distance_matrix, ultra_metric_params)

# print distance matrix to console
for tree in trees:
    print(f", {tree.name.replace(' ', '_')}", end='')
print("")
for row in ultra_matrix:
    for item in row:
        print("%0.2f " % item, end='')
    print()

[avg_err, avg_err_percent] = average_error(distance_matrix, ultra_matrix)
print(f"avg error {avg_err} - {avg_err_percent}")

