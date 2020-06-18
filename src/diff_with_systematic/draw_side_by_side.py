from PIL import Image, ImageDraw
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix
import scipy.spatial.distance as ssd

item_size = 20
item_space = 20


def draw_tree(draw, tree, left, top, right, bottom, parent=None):

    color = 'black'

    center_x = (right + left) / 2
    item_left = center_x - item_size / 2
    item_top = bottom - item_size - item_space
    center_y = item_top + item_size / 2
    draw.ellipse((item_left, item_top, item_left + item_size, item_top + item_size), fill=color, outline=color)

    if parent is not None:
        draw.line([parent, (center_x, center_y)], width=1, fill=color)

    if tree.left is not None:
        draw_tree(draw, tree.left, left, top, center_x, item_top, parent=(center_x, center_y))
    if tree.right is not None:
        draw_tree(draw, tree.right, center_x, top, right, item_top, parent=(center_x, center_y))


systematic_tree = "morph"
cluster_algorithm = "complete"
is_swap_left_right = False
max_levels = 11

global_params = GlobalParams(g_weight=0.1, calc_weight=exponent_reduced_weight(0.50), max_levels=max_levels,
                             level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                             )

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_levels=max_levels)

tree = matrDiff.vertices[0]
tree.prepare(global_params)

im = Image.new('RGBA', [1000, 400], (255, 255, 255, 255))
draw = ImageDraw.Draw(im)

draw_tree(draw, tree, 0, 0, im.size[0], im.size[1])



#draw.ellipse((20, 20, 180, 180), fill = 'blue', outline ='blue')
draw.text((10, 10), tree.name, fill=0xff000000)
del draw

# write to stdout
im.save("../../output/res.png")
