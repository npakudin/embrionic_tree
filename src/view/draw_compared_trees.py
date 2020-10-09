from pathlib import Path
from PIL import Image, ImageDraw
from src.view.rounded_rect import rounded_rectangle

from src.single_tree.development_tree_utils import calculate_number_on_level_2_trees
from src.single_tree.distances import node_dist
from src.single_tree.superimposed_tree import SuperimposedNode

ITEM_SIZE = 20
ITEM_SPACE = 20
COLOR_LEFT  = 0xff0050ff
COLOR_RIGHT = 0xff00c0ff
COLOR_EQ    = 'black'
COLOR_INEQ  = 0xffe00000


class TreeDrawSettings:
    def __init__(self, color_left=0, color_right=0, color_eq=0, color_ineq=0, get_node_caption=None):
        self.color_left = color_left
        self.color_right = color_right
        self.color_eq = color_eq
        self.color_ineq = color_ineq
        self.get_node_caption = get_node_caption

    def node_caption(self, n1, n2):
        if self.get_node_caption is None:
            return ""
        return self.get_node_caption()


FERTILITY_DRAW_SETTINGS = TreeDrawSettings(color_left=0xFF285EDD, color_right=0xFFFC7074,
                                           color_eq=0xFFE8E4DE, color_ineq=0xFFE8E4DE)

DEBUG_DRAW_SETTINGS = TreeDrawSettings(color_left=0xFF285EDD, color_right=0xFFFC7074,
                                     color_eq=0xFFE8E4DE, color_ineq=0xff808080)


class TreeDrawer:
    def __init__(self, draw_settings, global_params):
        self.draw_settings = draw_settings
        self.draw = None
        self.start_numbers = []
        self.min_reduced_depth = 0
        self.max_reduced_depth = 0
        self.global_params = global_params

    def draw_superimposed_node(self, superimposed_node, border_left, border_top, border_right, border_bottom, level,
                               parent=None, is_equal_history=True):
        if superimposed_node.is_none():
            return [0, 0]

        color = self.draw_settings.color_eq
        if superimposed_node.n1.is_none():
            color = self.draw_settings.color_left
        elif superimposed_node.n2.is_none():
            color = self.draw_settings.color_right
        elif superimposed_node.n1.axis != superimposed_node.n2.axis:
            color = self.draw_settings.color_ineq

        cur_node_distance = superimposed_node.node_dist(self.global_params)
        cur_node_dist_axis = superimposed_node.dist_axis()
        is_equal_history = is_equal_history and cur_node_dist_axis == 0

        # reduced_level = node2.reduced_level if node1.is_none() else node1.reduced_level
        # number_on_level = node2.number_on_level if node1.is_none() else node1.number_on_level
        # nodes_on_level = start_numbers[reduced_level]
        # center_x = ((border_right + border_left)) * (number_on_level + 0.5) / nodes_on_level
    
        center_x = (border_right + border_left) / 2
    
        item_left = center_x - ITEM_SIZE / 2
        item_top = border_bottom - ITEM_SIZE - ITEM_SPACE
        center_y = item_top + ITEM_SIZE / 2
    
        total_max_distance = cur_node_distance
        total_min_distance = cur_node_distance
        if not superimposed_node.left.is_none():
            is_right_exists = not superimposed_node.right.is_none()
            right = center_x if is_right_exists else border_right
            #right = border_right
    
            [add_max_dist, add_min_dist] = self.draw_superimposed_node(superimposed_node.left,
                border_left, border_top, right, item_top, level+1, parent=(center_x, center_y),
                is_equal_history=is_equal_history)
            total_max_distance += add_max_dist
            total_min_distance += add_min_dist
        if not superimposed_node.right.is_none():
            is_left_exists = not superimposed_node.left.is_none()
            left = center_x if is_left_exists else border_left
            #left = border_left
    
            [add_max_dist, add_min_dist] = self.draw_superimposed_node(superimposed_node.right,
                left, border_top, border_right, item_top, level+1, parent=(center_x, center_y),
                is_equal_history=is_equal_history)
            total_max_distance += add_max_dist
            total_min_distance += add_min_dist
    
        if parent is not None:
            self.draw.line([parent, (center_x, center_y)], width=1, fill=0xff000000)

        self.draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline='black')

        node_caption = self.draw_settings.node_caption(superimposed_node.n1, superimposed_node.n2)
        self.draw.text((item_left, item_top+ITEM_SIZE), node_caption, fill=0xff000000)

        leaves1 = superimposed_node.n1.get_leaves_number()
        leaves2 = superimposed_node.n2.get_leaves_number()
        leaves_diff = abs(leaves1 - leaves2)

        if is_equal_history and ((level == 3 and leaves_diff >= 10) or (level > 3 and leaves_diff >= 5)):
            selection_color = 0xFF52A710
            self.draw.rounded_rectangle(((border_left, border_top), (border_right, border_bottom - ITEM_SPACE)), 1, selection_color, selection_color)
            self.draw.text((border_left + 00, border_top - 20), f"leaves #:", fill=selection_color)
            self.draw.text((border_left + 55, border_top - 20), f"{leaves1}", fill=self.draw_settings.color_right)
            self.draw.text((border_left + 70, border_top - 20), f"{leaves2}", fill=self.draw_settings.color_left)


        return [total_max_distance, total_min_distance if level < self.min_reduced_depth else 0]

    def draw_legend(self, item_left, item_top, color, text):
        self.draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color, outline=color)
        self.draw.text((item_left + ITEM_SIZE + ITEM_SPACE, item_top), text, fill=color)

    def draw_tree(self, tree1, tree2, folder):
    
        im = Image.new('RGBA', [1500, 600], (255, 255, 255, 255))
        self.draw = ImageDraw.Draw(im)
    
        self.min_reduced_depth = min(tree1.root.reduced_depth, tree2.root.reduced_depth)
        self.max_reduced_depth = max(tree1.root.reduced_depth, tree2.root.reduced_depth)
    
        self.start_numbers = [0] * self.max_reduced_depth
        calculate_number_on_level_2_trees(tree1.root, tree2.root, self.start_numbers)
    
        superimposed_node = SuperimposedNode(tree1.root, tree2.root)
        superimposed_node.calculate_leaves_number()

        [raw_max_dist, raw_min_dist] = self.draw_superimposed_node(superimposed_node,
            0, im.size[1] - (ITEM_SIZE + ITEM_SPACE) * (self.max_reduced_depth + 0),
            im.size[0] - ITEM_SIZE - ITEM_SPACE, im.size[1], 0, is_equal_history=True)

        # legend
        self.draw_legend(300, 10, self.draw_settings.color_left, 'Node exists in the left tree only')
        self.draw_legend(300, 30, self.draw_settings.color_right, 'Node exists in the right tree only')
        self.draw_legend(300, 50, self.draw_settings.color_eq, 'Node exists in both trees and axis are equal, e.g. X and X')
        self.draw_legend(300, 70, self.draw_settings.color_ineq, 'Node exists in both trees and axis are NOT equal, e.g. X and Y')
    
        # distances
        #correction_coef = sum([pow(2 * global_params.param_a, i) for i in range(min_reduced_depth)])
        self.draw.text((0, 10), f"{tree1.name[:15]} reduced_depth: {tree1.root.reduced_depth}", fill=self.draw_settings.color_left)
        self.draw.text((0, 30), f"{tree2.name[:15]} reduced_depth: {tree2.root.reduced_depth}", fill=self.draw_settings.color_right)
        # draw.text((10, 10), f"param_a      = {param_a:0.2f}", fill='black')
        # draw.text((10, 30), f"raw_max_dist = {raw_max_dist:0.4f}", fill='black')
        # draw.text((10, 50), f"raw_min_dist = {raw_min_dist:0.4f}", fill='black')
        # draw.text((10, 70), f"corr_min_dist= {dist:0.4f}", fill='black')
        #draw.text((10, 90), f"corr_coef    = {correction_coef:0.4f}", fill='black')
    
        for i in range(0, 11):
            self.draw.text((im.size[0] - 20, im.size[1] - (i + 1)*(ITEM_SIZE + ITEM_SPACE)), f"{i + 1}", fill='black')
    
        del self.draw
    
        path = f"../../output/{folder}"
        Path(path).mkdir(parents=True, exist_ok=True)
        im.save(f"{path}/{tree1.name}-{tree2.name}.png")
