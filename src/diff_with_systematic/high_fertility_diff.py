from src.compare_trees.development_tree_reader import read_all_trees
from src.compare_trees.development_tree_utils import prepare_trees, short_sp_name
from src.compare_trees.distances import high_fertility_diff_development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.iterate_trees import number_by_address

# Build matrices and corr coef only

max_level = 10
is_reducing = True

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

            is_left_0_descendants = (node1.left is None) and (node1.right is None)
            is_right_0_descendants = (node2.left is None) and (node2.right is None)
            l_or_r = "-"
            if is_left_0_descendants:
                l_or_r = trees[i].name
            elif is_right_0_descendants:
                l_or_r = trees[j].name

            res = [trees[i].name, trees[j].name, normalized_dist, reduced_level + 1, left_right_number,
                   is_left_0_descendants or is_right_0_descendants,
                   l_or_r, addr, node1.address, node2.address]
            sp_fert_dist.append(res)

# print in alphabet sort
print(
    f"Fertility_distance Level_of_the_difference Number_of_the_node_from_left_to_right_on_the_level "
    f"Is_zero_fertility_in_the_one_of_trees Specie_with_zero_fertility Specie Compare_with_the_tree_of")
prev_tree1 = None
prev_tree2 = None
for item in sorted(sp_fert_dist, key=lambda x: (x[0], x[1], -x[2], -x[3])):
    [tree1_name, tree2_name, normalized_dist, level, left_right_number, is_0_descendants, which_0_descendants,
     reduced_addr, node1_addr, node2_addr] = item
    if prev_tree1 == tree1_name:
        tree1_name = '-"-'
    else:
        prev_tree1 = tree1_name

    if prev_tree2 == tree2_name:
        tree2_name = '-"-'
    else:
        prev_tree2 = tree2_name

    # print(
    #     f"{normalized_dist:0.1f} {level} {left_right_number} {is_0_descendants} {short_sp_name(which_0_descendants)} {short_sp_name(tree1_name)} {short_sp_name(tree2_name)}")

# print top 10
for item in sorted(sp_fert_dist, key=lambda x: (-x[2], -x[3], x[0], x[1])):
    [tree1_name, tree2_name, normalized_dist, level, left_right_number, is_0_descendants, which_0_descendants,
     reduced_addr, node1_addr, node2_addr] = item

    print(
        f"{normalized_dist:0.1f} {level} {left_right_number} {is_0_descendants} {short_sp_name(which_0_descendants)} {short_sp_name(tree1_name)} {short_sp_name(tree2_name)}")

# print(f"{level2count}")
