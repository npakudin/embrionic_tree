from src.multiple_trees.trees_matrix import TreesMatrix, full_distance
from src.single_tree.global_params import GlobalParams
from src.single_tree.superimposed_tree import SuperimposedNode


def do_it():
    max_level = 10
    use_min_common_depth = True
    use_flipping = False

    # [param_a, is_reducing]
    params = [[0.5, True], [1.0, False]]

    for [param_a, is_reducing] in params:
        trees_matrix = TreesMatrix("../../input/xtg/*.xtg", max_level=max_level, is_reducing=is_reducing,
                                   use_min_common_depth=use_min_common_depth, use_flipping=use_flipping)

        johansen_trees_matrix = TreesMatrix("../../input/xtg_johansen/*.xtg", max_level=max_level,
                                            is_reducing=is_reducing, use_min_common_depth=use_min_common_depth,
                                            use_flipping=use_flipping)

        trees = trees_matrix.vertices
        johansen_trees = johansen_trees_matrix.vertices

        global_params = GlobalParams(max_level=max_level, param_a=param_a, use_min_common_depth=True,
                                     use_flipping=use_flipping)

        matches_number = 0
        print(f"Johansen-Batygina types to species distance, is_reducing: True, param_a: 0.5, division_weight: 1.0, "
              f"g_weight: 0.0, chain_length_weight: 0.0")
        print(f"Specie Reference_type 1st_type 1st_type_distance 2nd_type 2nd_type_distance")
        for i in range(len(trees)):
            print(f"{trees_matrix.names[i]} {short_embryo_name(trees[i].embryo_type)} ", end='')
            res = []
            # min_dist = (-1, 1.0E+100)
            for j in range(len(johansen_trees)):
                min_reduced_depth = min(trees[i].root.reduced_depth, johansen_trees[j].root.reduced_depth)

                flipped_root = None
                if use_flipping:
                    flipped_root = johansen_trees[j].flipped_roots[min_reduced_depth]

                dist = full_distance(global_params,
                                     trees[i].roots[min_reduced_depth],
                                     johansen_trees[j].roots[min_reduced_depth],
                                     flipped_root)

                res.append((dist, johansen_trees_matrix.names[j]))
                # draw_tree(trees[i], johansen_trees[j], global_params, dist, 0, "johansen")

            res = sorted(res, key=lambda dist_name: dist_name[0])
            for (dist, name) in res[:2]:
                print(f"{short_embryo_name(name)} {dist:0.2f} ", end='')
            print(f"")

            if trees[i].embryo_type == res[0][1]:
                matches_number += 1
        print(f"matches_number: {matches_number}\n")


do_it()

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
#
#
# trees = matrDiff.vertices
# johansenTrees = johansenMatrDiff.vertices
#
# print(f"joh_tree depth")
# for j in range(len(johansenTrees)):
#     print(f"{johansenTrees[j].name} {johansenTrees[j].root.depth}")
#
#
# print()
# print(f"name reference_value 1st_embryo_type 1st_embryo_type_dist 2nd_embryo_type 2nd_embryo_type_dist" \
#       f"3rd_embryo_type 3rd_embryo_type_dist")
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
