from src.multiple_trees.matrix_diff import MatrixDiff
from src.single_tree.global_params import GlobalParams
from src.view.draw_compared_trees import TreeDrawer, TreeDrawSettings, get_prepared_trees


def draw_trees(folder, draw_settings, is_reducing, max_level=10, param_a=0.5):
    global_params = GlobalParams(max_level=max_level, param_a=param_a)

    systematic_tree = "morph"
    max_level = 10
    matr_diff = MatrixDiff("../../input/xtg_johansen/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                           ["Angiosperms"], max_level=max_level, filter_by_taxon=False, is_reducing=is_reducing)

    trees = matr_diff.vertices

    tree_drawer = TreeDrawer(draw_settings, global_params)
    for i in range(0, len(trees)):
        tree_drawer.draw_tree(trees[i], trees[i], folder)


draw_trees("johansen_only", TreeDrawSettings.johansen(), is_reducing=False)
