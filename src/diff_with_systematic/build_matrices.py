import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, corrcoef

# Build matrices and corr coef only

systematic_tree = "morph"
cluster_algorithm = "average"
max_level = 10

johansenMatrDiff = MatrixDiff("../../input/xtg_johansen/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                              ["Angiosperms"], max_level=max_level, filter_by_taxon=False)

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                      ["Angiosperms"], max_level=max_level)

trees = matrDiff.vertices
johansenTrees = johansenMatrDiff.vertices

# for g_weight in np.linspace(0.0, 1.00, 11):
#     for param_a in np.linspace(0.1, 1.0, 10):
#         global_params = GlobalParams(g_weight=g_weight, chain_length_weight=0,
#                                      param_a=param_a, max_level=max_level,
#                                      subtree_threshold=1000, subtree_multiplier=1,
#                                      # level_weight_multiplier=[512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 0]
#                                      # level_weight_multiplier=[4, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
#                                      level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#                                      )
#         name = f"param_a={param_a}_{systematic_tree}_{cluster_algorithm}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
#         experiment_matrix = matrDiff.make_experiment_matrix(global_params)
#
#         # dictionary - nearest joh tree to specie tree
#         specie_to_joh = []
#         for i in range(len(trees)):
#             specie_distances = []
#             for j in range(len(johansenTrees)):
#                 dist = development_tree_distance(trees[i], johansenTrees[j], global_params)
#                 specie_distances.append((j, dist, johansenMatrDiff.names[j]))
#
#             specie_distances = sorted(specie_distances, key=lambda dist_name: dist_name[1])
#             specie_to_joh.append(specie_distances[0][0])
#             # for (j, dist, name) in specie_distances:
#             #     print(f"{name} {dist:0.4f} ", end='')
#             # print(f"")
#
#         # for (i, joh_i) in enumerate(specie_to_joh):
#         #     print(f"{trees[i].name} {johansenTrees[joh_i].name} ", end='\n')
#         # print(f"")
#
#         # distance between joh trees
#         joh_matrix = []
#         for i in range(len(johansenTrees)):
#             joh_matrix.append([])
#             for j in range(len(johansenTrees)):
#                 dist = development_tree_distance(johansenTrees[i], johansenTrees[j], global_params)
#                 joh_matrix[i].append(dist)
#
#         # matrix of species, where all distances replaced with joh trees
#         specie_joh_matrix = []
#         for i in range(len(trees)):
#             specie_joh_matrix.append([])
#             for j in range(i):
#                 dist = joh_matrix[ specie_to_joh[i] ][ specie_to_joh[j] ]
#                 specie_joh_matrix[i].append(dist)
#
#         corr = corrcoef(specie_joh_matrix, experiment_matrix)
#
#         #corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
#         print(f"{param_a:0.4f} {g_weight:0.4f} {corr:0.4f}")
#         #print_matrix(experiment_matrix, name, matrDiff.names, corr, with_headers=True)


def get_corrcoef(param_a, g_weight, chain_length_weight):
    global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=g_weight,
                                 chain_length_weight=chain_length_weight)
    name = f"a={param_a}_{systematic_tree}_{cluster_algorithm}_subtree_(thr,mult)=({global_params.subtree_threshold},{global_params.subtree_multiplier})_lev_mult={global_params.level_weight_multiplier}"
    experiment_matrix = matrDiff.make_experiment_matrix(global_params)

    # dictionary - nearest joh tree to specie tree
    specie_to_joh = []
    for i in range(len(trees)):
        specie_distances = []
        for j in range(len(johansenTrees)):
            dist = development_tree_distance(trees[i], johansenTrees[j], global_params)
            specie_distances.append((j, dist, johansenMatrDiff.names[j]))

        specie_distances = sorted(specie_distances, key=lambda dist_name: dist_name[1])
        specie_to_joh.append(specie_distances[0][0])
        # for (j, dist, name) in specie_distances:
        #     print(f"{name} {dist:0.4f} ", end='')
        # print(f"")

    # for (i, joh_i) in enumerate(specie_to_joh):
    #     print(f"{trees[i].name} {johansenTrees[joh_i].name} ", end='\n')
    # print(f"")

    # distance between joh trees
    joh_matrix = []
    for i in range(len(johansenTrees)):
        joh_matrix.append([])
        for j in range(len(johansenTrees)):
            dist = development_tree_distance(johansenTrees[i], johansenTrees[j], global_params)
            joh_matrix[i].append(dist)

    # matrix of species, where all distances replaced with joh trees
    specie_joh_matrix = []
    for i in range(len(trees)):
        specie_joh_matrix.append([])
        for j in range(i):
            dist = joh_matrix[specie_to_joh[i]][specie_to_joh[j]]
            specie_joh_matrix[i].append(dist)

    corr = corrcoef(specie_joh_matrix, experiment_matrix)

    # print_matrix(experiment_matrix, name, matrDiff.names, corr, with_headers=True)

    return corr


def create_fun(chain_length_weight):
    def fun(a, g_weight):
        return get_corrcoef(a, g_weight, chain_length_weight)
    return fun


if True:
    a = np.linspace(0.001, 1.0, 11)
    g_weight = np.linspace(-0.1, 1.0, 12)
    chain_length = 0.0

    X, Y = np.meshgrid(a, g_weight)
    Z = np.vectorize(create_fun(chain_length))(X, Y)

    fig = plt.figure()

    ax = Axes3D(fig)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel('param_a')
    ax.set_ylabel('g_weight')
    ax.set_zlabel('coefcorr')
    ax.set_title(f"chain_length_weight={chain_length}")

    plt.show()


# param_a: 0.35, corrcoef: 0.4430 - level_weight_multiplier=[1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
# param_a: 0.30, corrcoef: 0.4616 - level_weight_multiplier=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# param_a: 0.10, corrcoef: 0.4524 - level_weight_multiplier=[1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]


#
#
# matrDiff = MatrixDiff("../../input/xtg/*.xtg", "../../input/systematic_tree_morph.xtg", ["Angiosperms"], max_level=10)
# #
# # for chain_length_weight in np.linspace(0.1, 0.7, 7):
# #     for a in np.linspace(0.05, 1.0, 20):
# #         for g_weight in np.linspace(0.1, 1.0, 10):
# #             res = matrDiff.matr_diff_sum([a, g_weight, chain_length_weight])
# #             #res = matrDiff.matr_diff_sum([a, 0, 0])
# #             #print(f"res: {res}")
# #     print("")
# #
#
#
# def create_fun(chain_length_weight):
#     def fun(a, g_weight):
#         return matrDiff.matr_diff_sum([a, g_weight, chain_length_weight])
#     return fun
#
#
# # def my_fun(x, y):
# #     print(f"my_fun {x} {y}")
# #     return x + y
# # a = np.linspace(0.1, 1.0, 4)
# # g_weight = np.linspace(0.1, 1.0, 3)
# #
# # X, Y = np.meshgrid(a, g_weight)
# #
# # vfunc = np.vectorize(my_fun)
# # q = vfunc(X, Y)
# #
# # print(q)
# # exit()
#
#
# a = np.linspace(0.001, 1.0, 11) # 0.001 - 0.05
# g_weight = np.linspace(-0.1, 1.0, 12) # -0.1 - 1.0
# chain_length = 0.5
#
# X, Y = np.meshgrid(a, g_weight)
# Z = np.vectorize(create_fun(chain_length))(X, Y)
#
# fig = plt.figure()
#
# ax = Axes3D(fig)
# ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
# ax.set_xlabel('param_a')
# ax.set_ylabel('g_weight')
# ax.set_zlabel('coefcorr')
# ax.set_title(f"chain_length_weight={chain_length}")
#
# plt.show()
#
# # fig = plt.figure()
# #
# # ax = plt.axes(projection='3d')
# # ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
# #                 cmap='viridis', edgecolor='none')
# # ax.set_title('surface')
#
# exit()
#

# 0.04000, 0.50000000, 0.50000000 : -0.45027154234063 - reduced
# 0.18000, 0.30000000, 0.10000000 : -0.45251470564757 - reduced

# 0.13222, 0.24444444, 0.10962963 : -0.4595687612421574 - reduced, global min for 11 levels
# 0.16020, 0.44018060, 0.03917439 : -0.4409801682956000 - reduced, global min for 7 levels
# 0.14000, 0.30992188, 0.09010417 : -0.3840999803542500 - reduced, global min for 6 levels
# 0.04264, 5.19455396, -0.21404590 : -0.3313438151254414 - reduced, global min for 3 levels
# 0.00100, 217.86693536, 0.10000000 : -0.28623655068061654 - reduced, global min for 2 levels


# 0.30050, 0.27631854, 0.05856897 : -0.44255210249159 - local min
# 0.22550, 0.27540941, 0.05000028 : -0.45025639992644
# init_values = [0.15, 0.2, 0.1]
#
# res = optimize.minimize(matrDiff.matr_diff_sum, np.array(init_values), bounds=((0.001, 0.7), (0.0, 0.9), (0.0, 0.9)),
#                         method='SLSQP')
#
# a = res.x[0]
# g_weight = res.x[1]
# chain_length_weight = res.x[2]
# print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res.fun}")
# print(f"{matrDiff.min_params} : {matrDiff.min_value}")


# x_arrange = np.arange(0.1, 0.9, 0.1)
# y_arrange = np.arange(0.1, 0.9, 0.1)
# X, Y = np.meshgrid(x_arrange, y_arrange)
#
# Z = np.array([[experiment_matr(matrDiff, x, y, 0.1) for x in x_arrange] for y in y_arrange], np.float)


# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.contour3D(X, Y, Z, 50, cmap='binary')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z');


# fig = plt.figure()
#
# ax = Axes3D(fig)
# ax.set_xlabel('a')
# ax.set_ylabel('g_weight')
# ax.set_zlabel('res')
#
# # X, Y, Z = axes3d.get_test_data(0.05)
# # cset = ax.contour(X, Y, Z, 16, extend3d=True)
# # ax.clabel(cset, fontsize=9, inline=1)
# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# #ax.set_zlim(16.5, 17.5)
# #fig.colorbar(surf, shrink=0.5, aspect=10)
# plt.show()
#
# exit()


# 0.20000, 0.20000000, 0.00000000 : -0.45293492145738

# for a in np.linspace(0.05, 0.70, 14):
#     for g_weight in np.linspace(0.05, 0.5, 10):
#         res = matrDiff.matr_diff_sum([a, g_weight, 0.1])
#         #print(f"res: {res}")
# exit
#
#
# #init_values = [0.38312, 0.43016736, 0.11349846] # 0.44478748225533 - phylo_tree_morph, Angiosperms
# init_values = [0.5, 0.1, 0.1] # 0.44478748225533 - phylo_tree_morph, Angiosperms
#
# #res = optimize.minimize(matrDiff.matr_diff_sum, np.array(init_values), bounds=((0.1, 0.9), (0.0, 1.0), (0.0, 1.0)), method='Nelder-Mead') # try Newton-CG
#
# a = res.x[0]
# g_weight = res.x[1]
# chain_length_weight = res.x[2]
# print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res.fun}")
#
