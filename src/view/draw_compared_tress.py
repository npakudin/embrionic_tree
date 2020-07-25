from PIL import Image, ImageDraw
from src.compare_trees.distances import node_dist

ITEM_SIZE = 20
ITEM_SPACE = 20
COLOR_LEFT  = 0xff0050ff
COLOR_RIGHT = 0xff00d0ff
COLOR_EQ    = 'black'
COLOR_INEQ  = 0xffe00000


def draw_node(draw, node1, node2, global_params, border_left, border_top, border_right, border_bottom, level, min_reduced_depth, parent=None):

    color = COLOR_EQ
    if node1 is None:
        color = COLOR_LEFT
    elif node2 is None:
        color = COLOR_RIGHT
    elif node1.axis != node2.axis:
        color = COLOR_INEQ

    cur_node_distance = node_dist(node1, node2, "", "", global_params)

    center_x = (border_right + border_left) / 2
    item_left = center_x - ITEM_SIZE / 2
    item_top = border_bottom - ITEM_SIZE - ITEM_SPACE
    center_y = item_top + ITEM_SIZE / 2

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    total_max_distance = cur_node_distance
    total_min_distance = cur_node_distance
    if left1 is not None or left2 is not None:
        [add_max_dist, add_min_dist] = draw_node(draw, left1, left2, global_params, border_left, border_top, center_x, item_top, level+1, min_reduced_depth, parent=(center_x, center_y))
        total_max_distance += add_max_dist
        total_min_distance += add_min_dist
    if right1 is not None or right2 is not None:
        [add_max_dist, add_min_dist] = draw_node(draw, right1, right2, global_params, center_x, border_top, border_right, item_top, level+1, min_reduced_depth, parent=(center_x, center_y))
        total_max_distance += add_max_dist
        total_min_distance += add_min_dist

    draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
    draw.text((item_left, item_top+ITEM_SIZE), f"{cur_node_distance:0.4f}", fill='purple')
    if parent is not None:
        draw.line([parent, (center_x, center_y)], width=1, fill=color)

    return [total_max_distance, total_min_distance if level < min_reduced_depth else 0]


def draw_legend(draw, item_left, item_top, color, text):
    draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
    draw.text((item_left + ITEM_SIZE + ITEM_SPACE, item_top), text, fill=color)


def draw_tree(tree1, tree2, global_params, dist, taxon_dist, folder):

    im = Image.new('RGBA', [1000, 400], (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)

    min_reduced_depth = min(tree1.root.reduced_depth, tree2.root.reduced_depth)
    [raw_max_dist, raw_min_dist] = draw_node(draw, tree1.root, tree2.root, global_params, 0, 0, im.size[0] - ITEM_SIZE - ITEM_SPACE, im.size[1], 0, min_reduced_depth)

    # legend
    draw_legend(draw, 500, 10, COLOR_LEFT, 'Node exists in the left tree only')
    draw_legend(draw, 500, 30, COLOR_RIGHT, 'Node exists in the right tree only')
    draw_legend(draw, 500, 50, COLOR_EQ, 'Node exists in both trees and axis are equal, e.g. X and X')
    draw_legend(draw, 500, 70, COLOR_INEQ, 'Node exists in both trees and axis are NOT equal, e.g. X and Y')

    # distances
    correction_coef = sum([pow(2 * global_params.param_a, i) for i in range(min_reduced_depth)])
    draw.text((200, 10), f"{tree1.name[:15]} reduced_depth: {tree1.root.reduced_depth}", fill=COLOR_LEFT)
    draw.text((200, 30), f"{tree2.name[:15]} reduced_depth: {tree2.root.reduced_depth}", fill=COLOR_RIGHT)
    draw.text((10, 10), f"taxon_dist   = {taxon_dist:0.4f}", fill='black')
    draw.text((10, 30), f"raw_max_dist = {raw_max_dist:0.4f}", fill='black')
    draw.text((10, 50), f"raw_min_dist = {raw_min_dist:0.4f}", fill='black')
    draw.text((10, 70), f"corr_min_dist= {dist:0.4f}", fill='black')
    draw.text((10, 90), f"corr_coef    = {correction_coef:0.4f}", fill='black')

    for i in range(0, 9):
        draw.text((im.size[0] - 20, im.size[1] - (i + 1)*(ITEM_SIZE + ITEM_SPACE)), f"{i}", fill='black')

    del draw

    im.save(f"../../output/{folder}/{tree1.name}-{tree2.name}.png")
