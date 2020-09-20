# Find difference of fertility at high levels
# Get all tree pairs
#   - on each pair get nodes with the same history - path from nodes to zygote has the same axis
#   - for each node pair calculate fertility_distance - difference of children nodes,
#       node existence only don't care about difference of axis if both nodes exist
#   - multiply fertility_distance * 2^level to get nodes at the highest level
#       with the biggest difference

from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.development_tree_utils import prepare_trees, short_sp_name
from src.single_tree.distances import high_fertility_diff_development_tree_distance
from src.single_tree.global_params import GlobalParams
from src.multiple_trees.iterate_trees import number_by_address


def specie_fertility_distance(max_level=10, is_reducing=True):
    trees = read_all_trees(pattern="../../input/xtg/*.xtg")
    prepare_trees(trees, max_level, is_reducing)

    global_params = GlobalParams(max_level=max_level, param_a=0.5, g_weight=0.0, chain_length_weight=0.0)

    level2count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}

    sp_fert_dist = []
    for i in range(len(trees)):
        for j in range(i + 1, len(trees)):  # skip repeating pairs

            # get array of tuples (node1, node2, distance, ...)
            distances = high_fertility_diff_development_tree_distance(trees[i], trees[j], global_params)
            for [addr, dist, reduced_level, node1, node2] in distances:

                # ignore cases when at the last level history is completely equal
                if dist == 0:
                    continue

                level2count[reduced_level + 1] += 1

                # ignore zygote and the next level
                if reduced_level < 5:
                    continue

                weight = pow(2.0 / global_params.param_a, reduced_level)
                normalized_dist = dist * weight

                left_right_number = number_by_address(trees[i].root, addr, is_reducing=is_reducing)

                is_left_0_descendants = (node1.left.is_none()) and (node1.right.is_none())
                is_right_0_descendants = (node2.left.is_none()) and (node2.right.is_none())
                l_or_r = "-"
                if is_left_0_descendants:
                    l_or_r = trees[i].name
                elif is_right_0_descendants:
                    l_or_r = trees[j].name

                res = [trees[i].name, trees[j].name, normalized_dist, reduced_level + 1, left_right_number,
                       is_left_0_descendants or is_right_0_descendants,
                       l_or_r, addr, node1.address, node2.address]
                sp_fert_dist.append(res)

    return sp_fert_dist
