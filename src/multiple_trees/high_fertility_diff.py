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
from src.single_tree.superimposed_tree import SuperimposedNode


def specie_fertility_distance(max_level=10, is_reducing=True):
    trees = read_all_trees(pattern="../../input/xtg/*.xtg")
    prepare_trees(trees, max_level, is_reducing)

    global_params = GlobalParams(max_level=max_level, param_a=0.5, g_weight=0.0, chain_length_weight=0.0)

    level2count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}

    sp_fert_dist = []
    for i in range(len(trees)):
        for j in range(i + 1, len(trees)):  # skip repeating pairs

            # get array of tuples (node1, node2, distance, ...)
            superimposed_node = SuperimposedNode(trees[i].root, trees[j].root)
            distances = superimposed_node.high_fertility_distance()

            for [addr, dist, reduced_level, node1, node2] in distances:

                # ignore cases when at the last level history is completely equal
                if dist == 0:
                    continue

                level2count[reduced_level + 1] += 1

                # ignore zygote and the next level
                if reduced_level < 0:
                    continue

                leaves1 = node1.leaves_number
                leaves2 = node2.leaves_number

                tree1 = trees[i]
                tree2 = trees[j]

                # switch order
                if leaves1 < leaves2:
                    tree1 = trees[j]
                    tree2 = trees[i]

                    tmp_node = node1
                    node1 = node2
                    node2 = tmp_node

                    tmp_leaves = leaves1
                    leaves1 = leaves2
                    leaves2 = tmp_leaves

                left_right_number = number_by_address(tree1.root, tree2.root, addr, is_reducing=is_reducing)

                is_left_0_descendants = (node1.left.is_none()) and (node1.right.is_none())
                is_right_0_descendants = (node2.left.is_none()) and (node2.right.is_none())
                l_or_r = "-"
                if is_left_0_descendants:
                    l_or_r = trees[i].name
                elif is_right_0_descendants:
                    l_or_r = trees[j].name

                res = [tree1.name, tree2.name, dist, reduced_level + 1, left_right_number,
                       is_left_0_descendants or is_right_0_descendants,
                       l_or_r, addr, node1.address, node2.address, leaves1, leaves2]
                sp_fert_dist.append(res)

    return sp_fert_dist


if True:
    top_n = 6000

    unreduced_sp_fert_dist = specie_fertility_distance(max_level=10, is_reducing=False)
    print(f"NOT reduced")
    print(
        f"Fertility_distance Level_of_the_difference Number_of_the_node_from_left_to_right_on_the_level "
        f"Specie Compare_with_the_tree_of leaves_number_1st leaves_number_2nd")
    # print top_n
    for item in sorted(unreduced_sp_fert_dist, key=lambda x: (-x[3], -x[2], x[0], x[1]))[:top_n]:
        [tree1_name, tree2_name, normalized_dist, level, left_right_number, is_0_descendants, which_0_descendants,
         reduced_addr, node1_addr, node2_addr, leaves1, leaves2] = item

        print(
            f"{normalized_dist:0.1f} {level} {left_right_number} {short_sp_name(tree1_name)} {short_sp_name(tree2_name)} {leaves1} {leaves2}")

    print(f"")
    print(f"")

    reduced_sp_fert_dist = specie_fertility_distance(max_level=10, is_reducing=True)
    print(f"REDUCED")
    print(
        f"Fertility_distance Level_of_the_difference Number_of_the_node_from_left_to_right_on_the_level "
        f"Is_zero_fertility_in_the_one_of_trees Specie_with_zero_fertility Specie Compare_with_the_tree_of leaves_number_1st leaves_number_2nd")
    # print top_n
    for item in sorted(reduced_sp_fert_dist, key=lambda x: (-x[3], -x[2], x[0], x[1]))[:top_n]:
        [tree1_name, tree2_name, normalized_dist, level, left_right_number, is_0_descendants, which_0_descendants,
         reduced_addr, node1_addr, node2_addr, leaves1, leaves2] = item

        print(
            f"{normalized_dist:0.1f} {level} {left_right_number} {is_0_descendants} {short_sp_name(which_0_descendants)} {short_sp_name(tree1_name)} {short_sp_name(tree2_name)} {leaves1} {leaves2}")
