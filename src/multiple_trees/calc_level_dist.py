from src.single_tree.distances import node_dist
from src.single_tree.global_params import GlobalParams
from src.multiple_trees.matrix_diff import MatrixDiff

# Calculates number of types of distances between nodes on each level
# Get all tree pairs, and for each pair impose one REDUCED tree to another
#   get all nodes - sometimes both, sometimes one node existing and the 2nd "virtual"
#   for each node pair increment variable in the table (level - type_of_node)

ALL = 0  # total number of nodes
LEFT = 1  # left only node exists
RIGHT = 2  # right only node exists
EQ = 3  # both nodes exist, axes are equal
INEQ = 4  # both nodes exist, axes are NOT equal
total = []
for i in range(11):
    total.append([0, 0, 0, 0, 0])


def proceed_node(node1, node2, level):

    total[level][ALL] += 1
    if node1 is None:
        total[level][LEFT] += 1
    elif node2 is None:
        total[level][RIGHT] += 1
    elif node1.axis != node2.axis:
        total[level][INEQ] += 1
    else:
        total[level][EQ] += 1

    node_distance = node_dist(node1, node2, global_params)

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    total_distance = node_distance
    if left1 is not None or left2 is not None:
        total_distance += proceed_node(left1, left2, level+1)
    if right1 is not None or right2 is not None:
        total_distance += proceed_node(right1, right2, level+1)

    return total_distance


systematic_tree = "morph"
max_level = 10

global_params = GlobalParams(max_level=max_level, param_a=0.50, g_weight=0.5)

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level)
trees = matrDiff.vertices

tree_number = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        proceed_node(trees[i].root, trees[j].root, 0)
        tree_number += 1

print(f"level total one_only eq ineq both_existing_part existing_part")
for i, item in enumerate(total):
    print(f"{i} {item[0]} {item[1] + item[2]} {item[3]} {item[4]} {'nan' if item[0] == 0 else (item[3] + item[4]) / item[0]} {item[0] / (tree_number * pow(2, i))}")
