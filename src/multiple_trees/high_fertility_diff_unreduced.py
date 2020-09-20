# Find difference of fertility at high levels
from src.multiple_trees.high_fertility_diff import specie_fertility_distance
from src.single_tree.development_tree_utils import short_sp_name

sp_fert_dist = specie_fertility_distance(max_level=10, is_reducing=False)

# print in alphabet sort
print(
    f"Fertility_distance Level_of_the_difference Number_of_the_node_from_left_to_right_on_the_level "
    f"Specie Compare_with_the_tree_of")
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
        f"{normalized_dist:0.1f} {level} {left_right_number} {short_sp_name(tree1_name)} {short_sp_name(tree2_name)}")

# print(f"{level2count}")
