from PIL import Image, ImageDraw
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

from src.compare_trees.distances import development_tree_distance, node_dist
from src.compare_trees.global_params import GlobalParams, const_weight, threshold_weight, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix
import scipy.spatial.distance as ssd


systematic_tree = "morph"

globalMatrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_levels=11)

res_matrices = []
res_corrcoef = []

# iterate over max_levels
for max_level in range(2, 12):

    global_params = GlobalParams(g_weight=0.5, calc_weight=exponent_reduced_weight(0.50), max_levels=max_level,
                                 level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                                 )

    matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                          max_levels=max_level)

    experiment_matrix = matrDiff.make_experiment_matrix(global_params)
    corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
    #print(f"max_dist: {max_dist}, corrcoef: {corrcoef}")

    res_matrices.append(experiment_matrix)
    res_corrcoef.append(corrcoef)


trees = globalMatrDiff.vertices
for i in range(len(res_matrices[0])):
    for j in range(len(res_matrices[0][i])):
        print(f"{trees[i].name} {trees[j].name}", end='')
        for max_level in range(len(res_matrices)):
            print(f" {res_matrices[max_level][i][j]:0.3f}", end='')
        print("")
