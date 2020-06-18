from PIL import Image, ImageDraw
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix
import scipy.spatial.distance as ssd

ITEM_SIZE = 20
ITEM_SPACE = 20
COLOR_LEFT  = 0xff0050ff
COLOR_RIGHT = 0xff00d0ff
COLOR_EQ    = 'black'
COLOR_INEQ  = 0xffe00000


def draw_node(draw, node1, node2, border_left, border_top, border_right, border_bottom, parent=None):

    color = COLOR_EQ
    if node1 is None:
        color = COLOR_LEFT
    elif node2 is None:
        color = COLOR_RIGHT
    elif node1.axis != node2.axis:
        color = COLOR_INEQ

    center_x = (border_right + border_left) / 2
    item_left = center_x - ITEM_SIZE / 2
    item_top = border_bottom - ITEM_SIZE - ITEM_SPACE
    center_y = item_top + ITEM_SIZE / 2

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    if left1 is not None or left2 is not None:
        draw_node(draw, left1, left2, border_left, border_top, center_x, item_top, parent=(center_x, center_y))
    if right1 is not None or right2 is not None:
        draw_node(draw, right1, right2, center_x, border_top, border_right, item_top, parent=(center_x, center_y))

    draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
    if parent is not None:
        draw.line([parent, (center_x, center_y)], width=1, fill=color)


def draw_tree(tree1, tree2, dist, taxon_dist):
    im = Image.new('RGBA', [1000, 400], (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    draw_node(draw, tree1, tree2, 0, 0, im.size[0] - ITEM_SIZE - ITEM_SPACE, im.size[1])


    draw.text((10, 10), tree1.name, fill=COLOR_LEFT)
    draw.text((10, 30), tree2.name, fill=COLOR_RIGHT)
    draw.text((10, 50), f"ndist = {dist:0.3f}", fill='black')
    draw.text((10, 70), f"taxon_dist = {taxon_dist:0.3f}", fill='black')

    for i in range(0, 9):
        draw.text((im.size[0] - 20, im.size[1] - i*(ITEM_SIZE + ITEM_SPACE)), f"{i}", fill='black')


    del draw

    im.save(f"../../output/side_by_side/{taxon_dist}-{tree1.name}-{tree2.name}-{dist:0.2f}.png")


systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_levels = 11

global_params = GlobalParams(g_weight=0.1, calc_weight=exponent_reduced_weight(0.50), max_levels=max_levels,
                             level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                             )

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_levels=max_levels)
trees = matrDiff.vertices
for tree in trees:
    tree.prepare(global_params)


MORPH_MAX_DIST = 6
max_dist = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        dist = development_tree_distance(trees[i], trees[j], global_params)
        max_dist = max(max_dist, dist)

for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        dist = development_tree_distance(trees[i], trees[j], global_params)
        taxon_dist = matrDiff.taxon_matrix[i][j]
        draw_tree(trees[i], trees[j], dist / max_dist * MORPH_MAX_DIST, taxon_dist)
