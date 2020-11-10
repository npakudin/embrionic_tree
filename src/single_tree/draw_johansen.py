from src.multiple_trees.trees_matrix import TreesMatrix
from src.single_tree.global_params import GlobalParams
from src.view.draw_compared_trees import TreeDrawer, TreeDrawSettings


def draw_trees(folder, draw_settings, is_reducing, use_flipping, max_level=10, param_a=0.5):
    global_params = GlobalParams(max_level=max_level, param_a=param_a)

    trees_matrix = TreesMatrix("../../input/xtg_johansen/*.xtg", max_level=max_level, is_reducing=is_reducing,
                               use_flipping=use_flipping)

    trees = trees_matrix.vertices

    tree_drawer = TreeDrawer(draw_settings, global_params)
    for i in range(0, len(trees)):
        tree_drawer.draw_tree(trees[i], trees[i], folder)


draw_trees("johansen_only", TreeDrawSettings.johansen(), is_reducing=False, use_flipping=False)
