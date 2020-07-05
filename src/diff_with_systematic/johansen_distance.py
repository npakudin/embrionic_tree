from scipy.cluster import hierarchy

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams, exponent_reduced_weight
from src.diff_with_systematic.clustering import draw_plot
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, to_full_matrix
import scipy.spatial.distance as ssd


def first_vowel(str, from_index=1):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    for i in range(from_index, len(str)):
        if str[i] in vowels:
            return i
    return len(str)


# 'Arabidopsis_thaliana' => 'Arab. t.'
def short_sp_name(name):
    genus_index = first_vowel(name, from_index=3)
    underscore_index = name.find('_')
    personal_name = name[underscore_index + 1:]
    personal_index = first_vowel(personal_name)
    return f"{name[:genus_index]}. {personal_name[:personal_index]}"


systematic_tree = "morph"
max_level = 4

global_params = GlobalParams(g_weight=0.5, calc_weight=exponent_reduced_weight(0.50), max_level=max_level,
                             level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                             )

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level, filter_by_taxon=False)
johansenMatrDiff = MatrixDiff("../../input/xtg_johansen/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg", ["Angiosperms"],
                      max_level=max_level, filter_by_taxon=False)


johansen_experiment_matrix = johansenMatrDiff.make_experiment_matrix(global_params)
print_matrix(johansen_experiment_matrix, "johansen_experiment_matrix", johansenMatrDiff.names)

plot_matrix = to_full_matrix(johansen_experiment_matrix)
# convert the redundant n*n square matrix form into a condensed nC2 array
# dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
dist_array = ssd.squareform(plot_matrix)

#clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
clustered_trees = hierarchy.linkage(dist_array, 'average')

name = "johansen_experiment_matrix"
draw_plot(clustered_trees, matrDiff.names, name, f"../../output/johansen/{name}.png")

trees = matrDiff.vertices
johansenTrees = johansenMatrDiff.vertices

print(f"name ", end='')
for j in range(len(johansenTrees)):
    print(f"{johansenMatrDiff.names[j]} ", end='')
print(f"nearest_johansen_dist nearest_johansen")

johansen_matr = []
for i in range(len(trees)):
    #print(f"{matrDiff.names[i]} - {short_sp_name(matrDiff.names[i])}")
    print(f"{matrDiff.names[i]} ", end='')
    johansen_matr.append([])
    min_dist = (-1, 1.0E+100)
    for j in range(len(johansenTrees)):
        dist = development_tree_distance(trees[i], johansenTrees[j], global_params)
        johansen_matr[i].append(dist)
        if dist < min_dist[1]:
            min_dist = (j, dist)
        print(f"{dist:0.4f} ", end='')
    print(f"{min_dist[1]} {johansenMatrDiff.names[min_dist[0]]}")
