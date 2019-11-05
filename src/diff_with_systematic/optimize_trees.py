import numpy as np
from scipy import optimize
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams, exponent_reduced_weight
from src.diff_with_systematic.matrix_diff import MatrixDiff

matrDiff = MatrixDiff("../../input/xtg/*.xtg", "../../input/systematic_tree_morph.xtg", ["Angiosperms"], max_levels=11)

# for a in np.linspace(0.05, 0.5, 10):
#     for g_weight in np.linspace(0.1, 0.7, 7):
#         for chain_length_weight in np.linspace(0.1, 0.7, 7):
#             res = matrDiff.matr_diff_sum([a, g_weight, chain_length_weight])
#             #res = matrDiff.matr_diff_sum([a, 0, 0])
#             #print(f"res: {res}")
# exit()


# 0.04000, 0.50000000, 0.50000000 : -0.45027154234063 - reduced
# 0.18000, 0.30000000, 0.10000000 : -0.45251470564757 - reduced

# 0.13222, 0.24444444, 0.10962963 : -0.4595687612421574 - reduced, global min for 11 levels
# 0.16020, 0.44018060, 0.03917439 : -0.4409801682956000 - reduced, global min for 7 levels
# 0.14000, 0.30992188, 0.09010417 : -0.3840999803542500 - reduced, global min for 6 levels
# 0.04264, 5.19455396, -0.21404590 : -0.3313438151254414 - reduced, global min for 3 levels
# 0.00100, 217.86693536, 0.10000000 : -0.28623655068061654 - reduced, global min for 2 levels


# 0.30050, 0.27631854, 0.05856897 : -0.44255210249159 - local min
# 0.22550, 0.27540941, 0.05000028 : -0.45025639992644
init_values = [0.15, 0.2, 0.1]

res = optimize.minimize(matrDiff.matr_diff_sum, np.array(init_values), bounds=((0.001, 0.7), (0.0, 0.9), (0.0, 0.9)),
                        method='SLSQP')

a = res.x[0]
g_weight = res.x[1]
chain_length_weight = res.x[2]
print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res.fun}")
print(f"{matrDiff.min_params} : {matrDiff.min_value}")













# #init_values = [0.39706, 0.33998504, 0.27387935] # 0.43221117679823 - phylo_tree_molecular_genetic, Angiosperms
# #init_values = [0.40015, 0.22183295, 0.06671602] # 0.4242109756144572 - phylo_tree_morph, Angiosperms
#
# init_values = [0.50000, 0.10000000, 0.10000000]
#
# #clusterize
# #ytdist = np.matrix(morph_matrix)
# global_params = GlobalParams(g_weight=init_values[1], chain_length_weight=init_values[2], is_swap_left_right=True)
#
# plot_matr = matrDiff.make_full_experiment_matrix(global_params)
#
# for name in matrDiff.names:
#     print(f"{name.replace(' ', '_')} ", end='')
# print("")
#
# print_matrix(plot_matr, "experiment_matrix")
# res = matrDiff.matr_diff_sum(init_values)
# print(f"res: {res}")
#
#
# Z = hierarchy.linkage(np.matrix(plot_matr), 'average')
# #print(Z)
# plt.figure()
# dn = hierarchy.dendrogram(Z, labels = np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in matrDiff.names], np.str)
#                           , orientation='right',count_sort = 'ascending', distance_sort='ascending')
# plt.show()
# exit
#
#
#
#
#
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












