from pathlib import Path

from PIL import Image, ImageDraw
from PIL.ImageFont import truetype

from src.multiple_trees.trees_matrix import TreesMatrix
from src.single_tree.development_tree import Axis
from src.single_tree.superimposed_tree import SuperimposedNode

ITEM_SIZE = 32
ITEM_SPACE = 20
FONT_SIZE = 19
LEGEND_FONT_SIZE = 30
#FONT_PATH = "/Library/Fonts/Arial.ttf"
#FONT_PATH = "input/fonts/OpenSans-Light.ttf"
FONT_PATH = "input/fonts/OpenSans-Regular.ttf"


def load_font(font_path=FONT_PATH, font_size=FONT_SIZE):
    try:
        arial_font = truetype(font_path, font_size)
    except OSError:
        print(f"Cannot load font {font_path}")
        arial_font = None
    return arial_font


def single_axis_node_caption(node):
    if node.axis == Axis.X or node.axis == Axis.Y or node.axis == Axis.Z:
        return f"{node.axis.upper()}"
    elif node.axis == Axis.DIAGONAL:
        return "D"
    elif node.axis == Axis.APOPTOSIS:
        return "A"
    elif node.axis == Axis.NONE:
        return "N"
    elif node.axis == Axis.LEAVE:
        return "L"
    return ""


def single_node_caption_1(node):
    res = single_axis_node_caption(node)

    if node.growth is not None and node.growth != 1.0:
        res = f"{node.growth:.1f},{res}".strip(",")

    return res.strip()


def not_empty_single_node_caption_1(node):
    res = single_node_caption_1(node)
    if not res:
        res = "1.0"
    return res


def double_node_caption_1(n1, n2):
    a1 = not_empty_single_node_caption_1(n1)
    a2 = not_empty_single_node_caption_1(n2)

    return f"{a1}/{a2}"


def unreduced_node_caption_1(n1, n2):
    res = single_axis_node_caption(n1)

    return res.strip()


def reduced_node_caption_1(n1, n2):
    return single_axis_node_caption(n1)


def reduced_node_caption_2(superimposed_node, global_params):
    n1 = superimposed_node.n1
    n2 = superimposed_node.n2
    if n1.growth is not None and n1.growth != 1.0:
        res = f"{n1.growth:.1f}; "
    else:
        res = f"-; "

    if n1.chain_length is not None and n1.chain_length != 1:
        res += f"{n1.chain_length}"
    else:
        res += "-"

    return res
    #return f"{n1.growth:.1f}; {n1.chain_length}"


def node_dist_caption_2(superimposed_node, global_params):
    return f"{superimposed_node.node_dist(global_params)}"


class TreeDrawSettings:
    def __init__(self, color_left=0, color_right=0, color_eq=0, color_ineq=0,
                 get_node_caption_1=None, get_node_caption_2=None,
                 font=load_font(), legend_font=load_font(FONT_PATH, LEGEND_FONT_SIZE),
                 is_full_legend=True, width=1500, height=700):
        self.color_left = color_left
        self.color_right = color_right
        self.color_eq = color_eq
        self.color_ineq = color_ineq
        self.get_node_caption_1 = get_node_caption_1
        self.get_node_caption_2 = get_node_caption_2
        self.font = font
        self.legend_font = legend_font
        self.is_full_legend = is_full_legend
        self.width = width
        self.height = height

    def node_caption_1(self, n1, n2):
        if self.get_node_caption_1 is None:
            return ""
        return self.get_node_caption_1(n1, n2)

    def node_caption_2(self, superimposed_node, global_params):
        if self.get_node_caption_2 is None:
            return ""
        return self.get_node_caption_2(superimposed_node, global_params)

    @staticmethod
    def fertility_unreduced():
        return TreeDrawSettings(color_left=0xFF285EDD, color_right=0xFFFC7074,
                                color_eq=0xFFE8E4DE, color_ineq=0xFFE8E4DE,
                                width=2000, height=720)

    @staticmethod
    def fertility_reduced():
        return TreeDrawSettings(color_left=0xFF285EDD, color_right=0xFFFC7074,
                                color_eq=0xFFE8E4DE, color_ineq=0xFFE8E4DE,
                                width=2000, height=570)

    @staticmethod
    def single_tree_unreduced():
        return TreeDrawSettings(color_eq=0xFFE8E4DE, get_node_caption_1=unreduced_node_caption_1,
                                is_full_legend=False, width=1500, height=590)

    @staticmethod
    def single_tree_reduced():
        return TreeDrawSettings(color_eq=0xFFE8E4DE, get_node_caption_1=reduced_node_caption_1,
                                get_node_caption_2=reduced_node_caption_2,
                                is_full_legend=False, width=1500, height=470)

    @staticmethod
    def johansen():
        return TreeDrawSettings(color_eq=0xFFE8E4DE, get_node_caption_1=unreduced_node_caption_1,
                                is_full_legend=False, width=800, height=390)


class TreeDrawer:
    def __init__(self, draw_settings, global_params):
        self.draw_settings = draw_settings
        self.draw = None
        self.min_reduced_depth = 0
        self.max_reduced_depth = 0
        self.global_params = global_params

    def draw_caption(self, node_caption, center_x, top):
        text_width = self.draw_settings.font.getsize(node_caption)[0]
        text_height = self.draw_settings.font.getsize(node_caption)[1]
        if len(node_caption) >= 6:
            node_caption = node_caption.replace("/", "/\n")
            text_width = self.draw_settings.font.getsize(node_caption.split("\n")[0])[0]
            text_height = self.draw_settings.font.getsize(node_caption.split("\n")[0])[1] * 2
        self.draw.text((center_x + (ITEM_SIZE - text_width) / 2, top + (ITEM_SIZE - text_height) / 2 - 2), node_caption, fill=0xff000000, font=self.draw_settings.font)

    def draw_superimposed_node(self, superimposed_node, border_left, border_top, border_right, border_bottom, level,
                               parent=None, is_equal_history=True):
        if superimposed_node.is_none():
            return [0, 0]

        color = self.draw_settings.color_eq
        if superimposed_node.n2.is_none():
            color = self.draw_settings.color_left
        elif superimposed_node.n1.is_none():
            color = self.draw_settings.color_right
        elif superimposed_node.n1.axis != superimposed_node.n2.axis:
            color = self.draw_settings.color_ineq

        cur_node_distance = superimposed_node.node_dist(self.global_params)
        cur_node_dist_division = superimposed_node.dist_division()
        is_equal_history = is_equal_history and cur_node_dist_division == 0

        center_x = (border_right + border_left) / 2

        item_left = center_x - ITEM_SIZE / 2
        item_top = border_bottom - ITEM_SIZE - ITEM_SPACE
        center_y = item_top + ITEM_SIZE / 2

        total_max_distance = cur_node_distance
        total_min_distance = cur_node_distance
        new_border = border_left + (border_right - border_left) * superimposed_node.left.leaves_number / superimposed_node.leaves_number
        if not superimposed_node.left.is_none():
            # is_right_exists = not superimposed_node.right.is_none()
            # right = center_x if is_right_exists else border_right
            right = new_border

            [add_max_dist, add_min_dist] = self.draw_superimposed_node(superimposed_node.left,
                                                                       border_left, border_top, right, item_top,
                                                                       level + 1, parent=(center_x, center_y),
                                                                       is_equal_history=is_equal_history)
            total_max_distance += add_max_dist
            total_min_distance += add_min_dist
        if not superimposed_node.right.is_none():
            # is_left_exists = not superimposed_node.left.is_none()
            # left = center_x if is_left_exists else border_left
            left = new_border

            [add_max_dist, add_min_dist] = self.draw_superimposed_node(superimposed_node.right,
                                                                       left, border_top, border_right, item_top,
                                                                       level + 1, parent=(center_x, center_y),
                                                                       is_equal_history=is_equal_history)
            total_max_distance += add_max_dist
            total_min_distance += add_min_dist

        if parent is not None:
            self.draw.line([parent, (center_x, center_y)], width=1, fill=0xff000000)

        self.draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color,
                          outline='black')

        node_caption_1 = self.draw_settings.node_caption_1(superimposed_node.n1, superimposed_node.n2)
        self.draw_caption(node_caption_1, item_left, item_top)

        node_caption_2 = self.draw_settings.node_caption_2(superimposed_node, self.global_params)
        self.draw_caption(node_caption_2, item_left, item_top + 25)

        # leaves1 = superimposed_node.n1.leaves_number
        # leaves2 = superimposed_node.n2.leaves_number
        # leaves_diff = abs(leaves1 - leaves2)
        # if is_equal_history and ((level == 3 and leaves_diff >= 10) or (level > 3 and leaves_diff >= 5)):
        #     selection_color = 0xFF52A710
        #     self.draw.rounded_rectangle(((border_left, border_top), (border_right, border_bottom - ITEM_SPACE)), 1,
        #       selection_color, selection_color)
        #     self.draw.text((border_left + 00, border_top - 20), f"leaves #:", fill=selection_color)
        #     self.draw.text((border_left + 55, border_top - 20), f"{leaves1}", fill=self.draw_settings.color_right)
        #     self.draw.text((border_left + 70, border_top - 20), f"{leaves2}", fill=self.draw_settings.color_left)

        return [total_max_distance, total_min_distance if level < self.min_reduced_depth else 0]

    def draw_legend(self, item_left, item_top, color, text):
        self.draw.ellipse((item_left, item_top, item_left + ITEM_SIZE, item_top + ITEM_SIZE), fill=color,
                          outline='black')
        self.draw.text((item_left + ITEM_SIZE + ITEM_SPACE, item_top), text, fill='black',
                       font=self.draw_settings.legend_font)

    def draw_tree(self, tree1, tree2, folder):

        self.min_reduced_depth = min(tree1.root.reduced_depth, tree2.root.reduced_depth)
        self.max_reduced_depth = max(tree1.root.reduced_depth, tree2.root.reduced_depth)

        superimposed_node = SuperimposedNode(tree1.root, tree2.root)
        superimposed_node.calculate_leaves_number([0] * self.max_reduced_depth)

        image_height = (ITEM_SIZE + ITEM_SPACE) * (self.max_reduced_depth + 0)
        image_width = (ITEM_SIZE + 7) * (superimposed_node.leaves_number + 0) + 60
        if self.draw_settings.is_full_legend:
            image_height += 140
        else:
            image_height += 60

        image_width = max(image_width, 400)

        im = Image.new('RGBA', [image_width, image_height], (255, 255, 255, 255))
        self.draw = ImageDraw.Draw(im)

        [raw_max_dist, raw_min_dist] = self.draw_superimposed_node(superimposed_node,
                                                                   10, im.size[1] - (ITEM_SIZE + ITEM_SPACE) * (self.max_reduced_depth + 0),
                                                                   im.size[0] - ITEM_SIZE - ITEM_SPACE, im.size[1],
                                                                   0, is_equal_history=True)

        # legend
        if self.draw_settings.is_full_legend:
            self.draw_legend(600, 10, self.draw_settings.color_left, 'Node exists in the 1st tree only')
            self.draw_legend(600, 48, self.draw_settings.color_right, 'Node exists in the 2nd tree only')
            self.draw_legend(600, 86, self.draw_settings.color_eq, 'Node exists in both trees')

            self.draw.text((10, 10), f"1st tree: {tree1.name.replace('_', ' ')}",
                           fill=self.draw_settings.color_left, font=self.draw_settings.legend_font)
            self.draw.text((10, 48), f"2nd tree: {tree2.name.replace('_', ' ')}",
                           fill=self.draw_settings.color_right, font=self.draw_settings.legend_font)
        else:
            name = tree1.name.replace('_', ' ') # for 'Chenopodium_bonus-henricus' to 'Chenopodium bonus-henricus'
            if 'a' <= name[0] <= 'z':
                name = name.capitalize().replace('-', ' ') # for 'asterad-1' to 'Asterad 1'
            self.draw.text((10, 10), f"{name}", fill='black', font=self.draw_settings.legend_font)

        for i in range(0, self.max_reduced_depth):
            self.draw.text((im.size[0] - 40, im.size[1] - (i + 1) * (ITEM_SIZE + ITEM_SPACE)), f"{i + 1}", fill='black',
                           font=self.draw_settings.legend_font)

        del self.draw

        if folder:
            path = f"output/{folder}"
            Path(path).mkdir(parents=True, exist_ok=True)
            name = tree1.name if tree1.name == tree2.name else f"{tree1.name}-{tree2.name}"
            im.save(f"{path}/{name}.png")

        return im


def get_prepared_trees(is_reducing, max_level, use_min_common_depth=False, use_flipping=False):
    trees_matrix = TreesMatrix("../../input/xtg/*.xtg", max_level=max_level, is_reducing=is_reducing,
                               use_min_common_depth=use_min_common_depth, use_flipping=use_flipping)

    trees = trees_matrix.vertices
    for tree in trees:
        tree.prepare(use_min_common_depth, use_flipping)

    return trees
