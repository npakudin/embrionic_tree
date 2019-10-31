import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

# clean levels_11 dir
from src.diff_with_systematic import MatrixDiff, print_matrix


# def experiment_matr(matrDiff, a, g_weight, chain_length_weight):
#     global_params = GlobalParams(a=a, g_weight=g_weight, chain_length_weight=chain_length_weight, is_swap_left_right=True, max_levels=11)
#     plot_matr = matrDiff.make_full_experiment_matrix(global_params)
#
#     matrDiff.matr_diff_sum(init_values)
#
#     return plot_matr



#matrDiff = MatrixDiff("../../../input/xtg/*.xtg", "../../../input/phylo_tree_morph_src.xtg", ["Angiosperms"])
#matrDiff = MatrixDiff("../../../input/xtg/*.xtg", "../../../input/phylo_tree_molecular_genetic.xtg", ["Angiosperms"])
#matrDiff = MatrixDiff("../../../input/xtg/*.xtg", "../../../input/phylo_tree_morph.xtg", ["Angiosperms"])
from src.compare_trees.global_params import GlobalParams

matrDiff = MatrixDiff("../../../input/xtg/*.xtg", "../../../input/phylo_tree_morph.xtg", ["Angiosperms"])

#init_values = [0.39706, 0.33998504, 0.27387935] # 0.43221117679823 - phylo_tree_molecular_genetic, Angiosperms
#init_values = [0.40015, 0.22183295, 0.06671602] # 0.4242109756144572 - phylo_tree_morph, Angiosperms

init_values = [0.50000, 0.10000000, 0.10000000]

#clusterize
#ytdist = np.matrix(morph_matrix)
global_params = GlobalParams(a=init_values[0], g_weight=init_values[1], chain_length_weight=init_values[2], is_swap_left_right=True, max_levels=11)

plot_matr = matrDiff.make_full_experiment_matrix(global_params)

for name in matrDiff.names:
    print(f"{name.replace(' ', '_')} ", end='')
print("")

print_matrix(plot_matr, "experiment_matrix")
res = matrDiff.matr_diff_sum(init_values)
print(f"res: {res}")


Z = hierarchy.linkage(np.matrix(plot_matr), 'average')
#print(Z)
plt.figure()
dn = hierarchy.dendrogram(Z, labels = np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in matrDiff.names], np.str)
                          , orientation='right',count_sort = 'ascending', distance_sort='ascending')
plt.show()
exit





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
