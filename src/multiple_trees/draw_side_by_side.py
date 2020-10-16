from src.single_tree.global_params import GlobalParams
from src.view.draw_compared_trees import TreeDrawer, TreeDrawSettings, get_prepared_trees


def draw_trees(folder, draw_settings, is_reducing, max_level=10, param_a=0.5):
    global_params = GlobalParams(max_level=max_level, param_a=param_a)

    trees = get_prepared_trees(is_reducing, max_level)

    tree_drawer = TreeDrawer(draw_settings, global_params)
    for i in range(0, len(trees)):
        for j in range(0, len(trees)):
            tree_drawer.draw_tree(trees[i], trees[j], folder)


draw_trees("side_by_side_unreduced", TreeDrawSettings.fertility_unreduced(), is_reducing=False)
draw_trees("side_by_side_reduced", TreeDrawSettings.fertility_reduced(), is_reducing=True)
