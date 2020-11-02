# Reduces trees and then calculates reduced_level etc
def prepare_trees(trees, max_level, is_reducing, use_min_common_depth):
    for tree in trees:
        # print(f"prepare {tree.name}")

        # cut all to 11 (10, because it's 0-based) levels to ignore overlevels if we have 12 or 13 for some species
        # notice: zygote has level=0
        tree.cut(max_level=10)

        if is_reducing:
            tree.reduce()
        tree.prepare(use_min_common_depth)
        tree.cut(max_level=max_level)


# 'Arabidopsis_thaliana' => 'A. thaliana'
def short_sp_name(name):
    underscore_index = name.find('_')

    personal_name = name[underscore_index + 1:]
    return f"{name[0]}._{personal_name}"


# Set number_on_level for each node on each level trees with roots n1 and n2
# If node exists at 1 of trees only - this number is used on the 2nd "virtually"
#
# L3.1 L3.2  L3.3   R3.1       R3.3
#  \   /      \       \         \
#   L2.1     L2.2     R2.1     R2.2
#      \    /            \    /
#       L1.1              R1.1
#
# note, that R3.2 doesn't exist, but number is taken
def calculate_number_on_level_2_trees(node1, node2, start_numbers):
    if node1.is_none() and node2.is_none():
        return

    reduced_level = node2.reduced_level if node1.is_none() else node1.reduced_level

    node1.number_on_level = start_numbers[reduced_level]
    node2.number_on_level = start_numbers[reduced_level]

    start_numbers[reduced_level] += 1

    calculate_number_on_level_2_trees(node1.left, node2.left, start_numbers)
    calculate_number_on_level_2_trees(node1.right, node2.right, start_numbers)

    # left1 = None if (node1 is None) else node1.left
    # right1 = None if (node1 is None) else node1.right
    # left2 = None if (node2 is None) else node2.left
    # right2 = None if (node2 is None) else node2.right
    #
    # existing_nodes = 1
    # if left1 is not None or left2 is not None:
    #     existing_nodes += calculate_number_on_level_2_trees(left1, left2, 1)
    #
    # if right1 is not None or right2 is not None:
    #     existing_nodes += calculate_number_on_level_2_trees(right1, right2, existing_nodes)
    #
    # return existing_nodes


def calculate_number_of_leaves(node1, node2):
    if node1.is_none() and node2.is_none():
        return

    calculate_number_of_leaves(node1.left, node2.left)
    calculate_number_of_leaves(node1.right, node2.right)

    left_leaves = max(node1.left.number_of_leaves, node2.left.number_of_leaves)
    right_leaves = max(node1.right.number_of_leaves, node2.right.number_of_leaves)
    number_of_leaves = max(1, left_leaves + right_leaves)

    node1.number_of_leaves = number_of_leaves
    node2.number_of_leaves = number_of_leaves

