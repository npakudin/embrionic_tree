from src.single_tree.distances import development_tree_distance
from src.single_tree.global_params import GlobalParams
from src.multiple_trees.matrix_diff import MatrixDiff
from src.multiple_trees.matrix_diff import print_matrix
from src.view.draw_compared_tress import draw_tree


def first_vowel(str, from_index=1):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    for i in range(from_index, len(str)):
        if str[i] in vowels:
            return i
    return len(str)


# # 'Arabidopsis_thaliana' => 'Arab. t.'
# def short_sp_name(name):
#     genus_index = first_vowel(name, from_index=3)
#     underscore_index = name.find('_')
#     dot = "." if genus_index < underscore_index else ""
#     genus_index = min(genus_index, underscore_index)
#
#     personal_name = name[underscore_index + 1:]
#     personal_index = first_vowel(personal_name)
#     return f"{name[:genus_index]}{dot} {personal_name[:personal_index]}."


def short_embryo_name(name):
    return name.replace("caryophyllad", "caryophyll.").replace("chenopodiad", "chenopod.")


# systematic_tree = "morph"
# max_level = 10
#
# # [param_a, is_reducing]
# params = [[0.5, True], [1.0, False]]
#
# for [param_a, is_reducing] in params:
#     matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
#                           ["Angiosperms"], max_level=max_level, filter_by_taxon=False, is_reducing=is_reducing)
#     johansenMatrDiff = MatrixDiff("../../input/xtg_johansen/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
#                                   ["Angiosperms"], max_level=max_level, filter_by_taxon=False, is_reducing=is_reducing)
#
#     trees = matrDiff.vertices
#     johansenTrees = johansenMatrDiff.vertices
#
#     global_params = GlobalParams(max_level=max_level, param_a=param_a)
#     gp = global_params
#
#     print(f"Johanson-Batygina types to species distance, is_reducing: True, param_a: 0.5, axis_weight: 1.0, fertility_weight: 1.0, g_weight: 0.0, chain_length_weight: 0.0")
#     print(f"Specie Reference_type 1st_type 1st_type_distance 2nd_type 2nd_type_distance")
#     for i in range(len(trees)):
#         print(f"{matrDiff.names[i]} {short_embryo_name(trees[i].embryo_type)} ", end='')
#         res = []
#         min_dist = (-1, 1.0E+100)
#         for j in range(len(johansenTrees)):
#             dist = development_tree_distance(trees[i], johansenTrees[j], global_params)
#             res.append((dist, johansenMatrDiff.names[j]))
#             # draw_tree(trees[i], johansenTrees[j], global_params, dist, 0, "johansen")
#
#         res = sorted(res, key=lambda dist_name: dist_name[0])
#         for (dist, name) in res[:2]:
#             print(f"{short_embryo_name(name)} {dist:0.2f} ", end='')
#         print(f"")

# johansen_experiment_matrix = johansenMatrDiff.make_experiment_matrix(global_params)
# print_matrix(johansen_experiment_matrix, "johansen_experiment_matrix", johansenMatrDiff.names)
#
#
# plot_matrix = to_full_matrix(johansen_experiment_matrix)
# dist_array = ssd.squareform(plot_matrix)
# clustered_trees = hierarchy.linkage(dist_array, 'average')
# plot_name = f"johansen_a={param_a:0.2f}_max_level={max_level}"
# draw_plot(clustered_trees, johansenMatrDiff.names, plot_name, f"../../output/johansen/{plot_name}.png")
#
#
# plot_matrix = to_full_matrix(johansen_experiment_matrix)
# # convert the redundant n*n square matrix form into a condensed nC2 array
# # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
# dist_array = ssd.squareform(plot_matrix)
#
# #clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
# clustered_trees = hierarchy.linkage(dist_array, 'average')
#
# matr_name = "johansen_experiment_matrix"
# draw_plot(clustered_trees, matrDiff.names, matr_name, f"../../output/johansen/{matr_name}.png")
#
# #exit()


# trees = matrDiff.vertices
# johansenTrees = johansenMatrDiff.vertices

# print(f"joh_tree depth")
# for j in range(len(johansenTrees)):
#     print(f"{johansenTrees[j].name} {johansenTrees[j].root.depth}")


# print()
# print(f"name reference_value 1st_embryo_type 1st_embryo_type_dist 2nd_embryo_type 2nd_embryo_type_dist 3rd_embryo_type 3rd_embryo_type_dist")
# # for j in range(len(johansenTrees)):
# #     print(f"{johansenMatrDiff.names[j]} ", end='')
# # print(f"nearest_johansen_dist nearest_johansen")
#
# param_a=0.5
# global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=0.0)
#
# for i in range(len(trees)):
#     #print(f"{matrDiff.names[i]} - {short_sp_name(matrDiff.names[i])}")
#     print(f"{matrDiff.names[i]} {trees[i].embryo_type} ", end='')
#     res = []
#     min_dist = (-1, 1.0E+100)
#     for j in range(len(johansenTrees)):
#         dist = development_tree_distance(trees[i], johansenTrees[j], global_params)
#         res.append((dist, johansenMatrDiff.names[j]))
#         #draw_tree(trees[i], johansenTrees[j], global_params, dist, 0, "johansen")
#
#     res = sorted(res, key=lambda dist_name: dist_name[0])
#     for (dist, name) in res:
#         print(f"{name} {dist:0.4f} ", end='')
#     print(f"")
#
#
# # # johansen types
# # johansen_experiment_matrix = johansenMatrDiff.make_experiment_matrix(global_params)
# # print_matrix(johansen_experiment_matrix, "johansen_experiment_matrix", johansenMatrDiff.names, with_headers=True)
# #
# # for i in range(len(johansenTrees)):
# #     for j in range(len(johansenTrees)):
# #         dist = development_tree_distance(johansenTrees[i], johansenTrees[j], global_params)
# #         draw_tree(johansenTrees[i], johansenTrees[j], global_params, dist, 0, "johansen")
