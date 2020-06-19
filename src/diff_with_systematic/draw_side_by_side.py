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


def draw_node(draw, node1, node2, border_left, border_top, border_right, border_bottom, level, parent=None):

    color = COLOR_EQ
    if node1 is None:
        color = COLOR_LEFT
    elif node2 is None:
        color = COLOR_RIGHT
    elif node1.axis != node2.axis:
        color = COLOR_INEQ

    node_distance = node_dist(node1, node2, "", "", global_params, level)

    center_x = (border_right + border_left) / 2
    item_left = center_x - ITEM_SIZE / 2
    item_top = border_bottom - ITEM_SIZE - ITEM_SPACE
    center_y = item_top + ITEM_SIZE / 2

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    total_distance = node_distance
    if left1 is not None or left2 is not None:
        total_distance += draw_node(draw, left1, left2, border_left, border_top, center_x, item_top, level+1, parent=(center_x, center_y))
    if right1 is not None or right2 is not None:
        total_distance += draw_node(draw, right1, right2, center_x, border_top, border_right, item_top, level+1, parent=(center_x, center_y))

    draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
    draw.text((item_left, item_top+ITEM_SIZE), f"{int(node_distance * 10000)}", fill='purple')
    if parent is not None:
        draw.line([parent, (center_x, center_y)], width=1, fill=color)

    return total_distance

def draw_legend(draw, item_left, item_top, color, text):
    draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
    draw.text((item_left + ITEM_SIZE + ITEM_SPACE, item_top), text, fill=color)


def draw_tree(tree1, tree2, dist, ndist, taxon_dist):
    dist_diff = taxon_dist - ndist
    dist_diff_str = f"{dist_diff:0.2f}" if dist_diff >= 0 else f"-{(6+dist_diff):0.2f}"
    if abs(dist_diff) < 3.85:
        return

    # if tree1.right.reduced_depth <= 1 and tree2.right.reduced_depth <= 1:
    #     tree1 = tree1.left
    #     tree2 = tree2.left

    im = Image.new('RGBA', [1000, 400], (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    total_distance = draw_node(draw, tree1, tree2, 0, 0, im.size[0] - ITEM_SIZE - ITEM_SPACE, im.size[1], 0)

    # legend
    draw_legend(draw, 300, 10, COLOR_LEFT, 'Node exists in the left tree only')
    draw_legend(draw, 300, 30, COLOR_RIGHT, 'Node exists in the right tree only')
    draw_legend(draw, 300, 50, COLOR_EQ, 'Node exists in both trees and axis are equal, e.g. X and X')
    draw_legend(draw, 300, 70, COLOR_INEQ, 'Node exists in both trees and axis are NOT equal, e.g. X and Y')


    draw.text((10, 10), tree1.name, fill=COLOR_LEFT)
    draw.text((10, 30), tree2.name, fill=COLOR_RIGHT)
    draw.text((10, 50), f"taxon_dist = {taxon_dist:0.3f}", fill='black')
    draw.text((10, 60), f"ndist      = {ndist:0.3f}", fill='black')
    draw.text((10, 70), f"ndist diff = {(taxon_dist - ndist):0.3f}", fill='black')
    draw.text((10, 80), f"dist       = {dist:0.3f}", fill='black')
    draw.text((10, 90), f"total_dist = {total_distance:0.3f}", fill='black')

    for i in range(0, 9):
        draw.text((im.size[0] - 20, im.size[1] - i*(ITEM_SIZE + ITEM_SPACE)), f"{i}", fill='black')

    del draw

    #im.save(f"../../output/side_by_side/{dist_diff:0.2f}-{tree1.name}-{tree2.name}.png")
    im.save(f"../../output/side_by_side_text/{dist_diff_str}-{tree1.name}-{tree2.name}.png")


systematic_tree = "morph"
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

print(f"max_dist: {max_dist}")

q = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        q += 1
        dist = development_tree_distance(trees[i], trees[j], global_params)
        taxon_dist = matrDiff.taxon_matrix[i][j]
        draw_tree(trees[i], trees[j], dist, dist / max_dist * MORPH_MAX_DIST, taxon_dist)
        print(f"{q} {i} {j} {trees[i].name} {trees[j].name} {dist / max_dist * MORPH_MAX_DIST} {taxon_dist}")
