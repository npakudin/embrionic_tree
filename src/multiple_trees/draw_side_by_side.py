from src.single_tree.distances import development_tree_distance
from src.single_tree.global_params import GlobalParams
from src.multiple_trees.matrix_diff import MatrixDiff
from src.view.draw_compared_tress import draw_tree


def draw_trees(param_a, is_reducing, folder):
    systematic_tree = "morph"
    max_level = 10

    global_params = GlobalParams(max_level=max_level, param_a=param_a)

    matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                          max_level=max_level, is_reducing=is_reducing)
    trees = matrDiff.vertices
    for tree in trees:
        tree.prepare()

    for i in range(0, len(trees)):
        for j in range(i+1, len(trees)):
        #for j in range(len(trees)):
            # if i == j:
            #     continue
            dist = development_tree_distance(trees[i], trees[j], global_params)
            draw_tree(trees[i], trees[j], global_params, dist, param_a, folder)


#draw_trees(param_a=0.5, is_reducing=True, folder="side_by_side_reduced")
draw_trees(param_a=0.5, is_reducing=False, folder="side_by_side_unreduced")
