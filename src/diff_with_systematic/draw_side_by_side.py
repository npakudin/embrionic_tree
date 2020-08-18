import numpy as np

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff
from src.view.draw_compared_tress import draw_tree

systematic_tree = "morph"
max_level = 11

global_params = GlobalParams(max_level=max_level, param_a=0.50, g_weight=0.5)

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level)
trees = matrDiff.vertices
for tree in trees:
    tree.prepare()


MORPH_MAX_DIST = 6
max_dist = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
        dist = development_tree_distance(trees[i], trees[j], global_params)
        max_dist = max(max_dist, dist)


experiment_matrix = matrDiff.make_experiment_matrix(global_params)
corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
print(f"max_dist: {max_dist}, corrcoef: {corrcoef}")

distrib = {}
step = 0
for i in range(0, len(trees)):
    for j in range(i+1, len(trees)):
    #for j in range(0, len(trees)):
        # if i == j:
        #     continue
        step += 1
        dist = development_tree_distance(trees[i], trees[j], global_params)
        taxon_dist = matrDiff.taxon_matrix[i][j]
        ndist = dist / max_dist * MORPH_MAX_DIST
        diff_ndist = (taxon_dist - ndist) / max(taxon_dist, ndist)
        draw_tree(trees[i], trees[j], global_params, dist, taxon_dist, "side_by_side")
        print(f"{step} {trees[i].name} {trees[j].name} {taxon_dist} {ndist} {taxon_dist - ndist} {diff_ndist}")

        if trees[i].name not in distrib.keys():
            distrib[trees[i].name] = []
        distrib[trees[i].name].append(diff_ndist)

        if trees[j].name not in distrib.keys():
            distrib[trees[j].name] = []
        distrib[trees[j].name].append(diff_ndist)

for k in distrib.keys():
    mean = np.mean(distrib[k])
    stddev = np.std(distrib[k], ddof=1)
    print(f"{k} {mean} {stddev} {mean - stddev} {mean + stddev}")
