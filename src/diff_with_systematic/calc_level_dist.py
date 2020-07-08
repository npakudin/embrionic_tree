from PIL import Image, ImageDraw
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from src.compare_trees.distances import development_tree_distance, node_dist
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix
import scipy.spatial.distance as ssd

ITEM_SIZE = 20
ITEM_SPACE = 20
COLOR_LEFT  = 0xff0050ff
COLOR_RIGHT = 0xff00d0ff
COLOR_EQ    = 'black'
COLOR_INEQ  = 0xffe00000

ALL = 0
LEFT = 1
RIGHT = 2
EQ = 3
INEQ = 4
total = []
for i in range(11):
    total.append([0,0,0,0,0])


def proceed_node(node1, node2, level):

    color = COLOR_EQ
    total[level][ALL] += 1
    if node1 is None:
        color = COLOR_LEFT
        total[level][LEFT] += 1
    elif node2 is None:
        color = COLOR_RIGHT
        total[level][RIGHT] += 1
    elif node1.axis != node2.axis:
        color = COLOR_INEQ
        total[level][INEQ] += 1
    else:
        total[level][EQ] += 1

    node_distance = node_dist(node1, node2, "", "", global_params, level)

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
max_level = 11

global_params = GlobalParams(g_weight=0.5, calc_weight=exponent_reduced_weight(0.50), max_level=max_level,
                             level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                             )

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level)
trees = matrDiff.vertices

tree_number = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        proceed_node(trees[i].node, trees[j].node, 0)
        tree_number += 1

print(f"level total one_only eq ineq both_existing_part existing_part")
for i, item in enumerate(total):
    print(f"{i} {item[0]} {item[1] + item[2]} {item[3]} {item[4]} {'nan' if item[0] == 0 else (item[3] + item[4]) / item[0]} {item[0] / (tree_number * pow(2, i))}")
