import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

import math
import os
import glob

from scipy import optimize
from scipy import stats
import statistics as st

# clean levels_11 dir
from src.compare_trees.diff_with_systematic.matrix_diff import MatrixDiff


matrDiff = MatrixDiff("../../../input/xtg/*.xtg", "../../../input/phylo_morph_tree.xtg", ["Angiosperms"])

# a = x[0]
# g_weight = x[1]
# chain_length_weight = x[2]
# morph_exp = x[3]

init_values = [0.9, 0.1, 0.1, 1]
#init_values = [0.58436, 0.27789530, 0.32182174, 1.00000028] #: -0.6507422696501239
#init_values = [0.58436, 0.27789530, 0.32182174, 1.00000028] #: -0.6507422696501239
#init_values = [0.58436, 0.27789530, 0.32182174, 1.50000000] #: -0.6507422696501239
init_values = [0.58438, 0.27789559, 0.32181927] #: -0.62653454803831 - swap
init_values = [0.58436, 0.27789479, 0.32182123] #: -0.6507422696505727 - no swap
#init_values = [0.99, 1.0, 1.0]

res = optimize.minimize(matrDiff.matr_diff_sum, np.array(init_values), bounds=((0.001, 1000.0), (0.001, 1000.0), (0.001, 1000.0))) # try Newton-CG

a = res.x[0]
g_weight = res.x[1]
chain_length_weight = res.x[2]
#morph_exp = res.x[3]
print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res.fun}")

# for filename in glob.glob("../trees/levels_11/*"):
#     os.unlink(filename)
#
#
#
# # cut to 11 levels
# files = glob.glob("../trees/*.xtg")
#
# # to compare matrices we need files always in the same order
# files.sort()
#
# # leave files with size = 0
# files = list(filter(lambda f: os.path.getsize(f) > 0, files))
#
# max_levels = 11
#
# for file in files:
#     # read, cut and prepare
#     node = src.distances.tree_from_xml(file)
#     node.cut(max_levels)
#     node.prepare()
#
#     # print
#     print(file + " " + str(node.depth))
#     if node.depth >= max_levels - 1:
#     #if True:
#         with open(f"../trees/levels_11/{node.name}.yml", "w") as text_file:
#             print(f"{node}", file=text_file)
#
#
# matrDiff = MatrixDiff("../../input/xtg/*.xtg", "../../../input/phylo_morph_tree.xtg", ["Angiosperms"])


# param_g_weight = 0.1
#
# count = 16
# for param_a in np.linspace(0.2, 1, count + 1):
#     experiment_matrix = matrDiff.make_experiment_matrix(param_a, param_g_weight)
#     morph_matrix = matrDiff.make_linear_morph_matrix()
#
#     x = []
#     y = []
#     res = {}
#     for i, experiment_row in enumerate(experiment_matrix):
#         for j, experiment_col in enumerate(experiment_row):
#             if j > i:
#                 experiment = experiment_matrix[i][j]
#                 morph = morph_matrix[i][j]
#                 x.append(morph)
#                 y.append(experiment)
#
#                 experiment = experiment_matrix[i][j]
#                 morph = morph_matrix[i][j]
#                 morph_set = []
#                 if morph in res:
#                     morph_set = res[morph]
#                 else:
#                     res[morph] = morph_set
#                 #morph_set.append((experiment, matrDiff.names[i], matrDiff.names[j]))
#                 morph_set.append(experiment)
#
#     k, b, r_value, p_value, std_err = stats.linregress(x, y)
#     #means = [st.mean(res[key]) for key in sorted(res.keys())]
#     stdevs = [st.stdev(res[key]) for key in sorted(res.keys())]
#     knbs = [(k * key + b, st.mean(res[key]), st.stdev(res[key]), st.stdev(res[key], 1000 + k * key + b)) for key in sorted(res.keys())]
#
#     print(f"a: {param_a:0.2f}, k: {k:0.5f}, b: {b:0.5f}, knbs: {knbs}, stdevs: {stdevs}")
#     print(res)
#     #print(f"a: {param_a:0.2f}, k: {k:0.5f}, b: {b:0.5f}, mean: {means}, knbs: {knbs}, stdevs: {stdevs}")
#     #if a == 0.5:
#     # if abs(param_a - 0.55) < 0.16: # 1.0E-14:
#     #     for n, (knb, mean, mean_stdev, regres_stdev) in enumerate(knbs):
#     #         print(f"n: {n}, res: {res}")
#     #         print(f"n: {n + 2}, count: {len(res[n])}, k*n+b: {knb:0.5f}, mean: {mean:0.5f}, rel_mean_diff:{(abs(knb-mean)/min(knb, mean)):0.5f}, mean_stdev: {mean_stdev:0.5f}, rel_stdev: {(mean_stdev / mean):0.5f}, rg = {(k*4 / b):0.5f}, regres_stdev: {regres_stdev:0.5f}")
#
#
#
#
#     # print("res")
#     # for key, val in sorted(res.items()):
#     #     print("%s, %s" % (key, val))

# corr_max = 0
# for param_a in np.linspace(0.1, 0.95, 18):
#     #for param_g_weight in np.linspace(0.05, 0.5, 10):
#
#         param_morph_exp = 1.0
#         param_g_weight = 0.15
#
#
#         #experiment_matrix = matrDiff.make_experiment_matrix(param_a, 0)
#         experiment_matrix = matrDiff.make_experiment_matrix(param_a, param_g_weight)
#         morph_matrix = matrDiff.make_morph_matrix(param_morph_exp, 0)
#
#
#         # # clusterize
#         # #ytdist = np.matrix(morph_matrix)
#         # Z = hierarchy.linkage(np.matrix(experiment_matrix), 'complete')
#         # #print(Z)
#         # plt.figure()
#         # dn = hierarchy.dendrogram(Z, labels = np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in matrDiff.names], np.str)
#         #                           , orientation='right',count_sort = 'ascending', distance_sort='ascending')
#         # plt.show()
#
#
#
#         # for name in matrDiff.names:
#         #     print(f", {name.replace(' ', '_')}", end='')
#         # print("")
#         #
#         # print_matrix(experiment_matrix, "experiment_matrix")
#         # print_matrix(morph_matrix, "morph_matrix")
#
#
#         avg_morph = 0.0
#         avg_experiment = 0.0
#         items = 0
#         distances = []
#
#         res = {}
#         for i, experiment_row in enumerate(experiment_matrix):
#             for j, experiment_col in enumerate(experiment_row):
#                 if j > i:
#                     experiment = experiment_matrix[i][j]
#                     morph = morph_matrix[i][j]
#                     morph_set = []
#                     if morph in res:
#                         morph_set = res[morph]
#                     else:
#                         res[morph] = morph_set
#                     #morph_set.append((experiment, matrDiff.names[i], matrDiff.names[j]))
#                     morph_set.append(experiment)
#
#                     avg_morph += morph
#                     avg_experiment += experiment
#                     items += 1
#                     distances.append(experiment)
#
#         # print("distances")
#         # print(sorted(distances))
#
#         res_avg = {}
#         for k,v in res.items():
#             avg = np.average(v)
#             stddev = np.std(v)
#             res_avg[k] = [avg, stddev, avg - stddev, avg + stddev]
#
#
#         avg_morph /= items
#         avg_experiment /= items
#
#         cov_exp_morph = 0
#         disp_morph = 0
#         disp_experiment = 0
#
#         for i, experiment_row in enumerate(experiment_matrix):
#             for j, experiment_col in enumerate(experiment_row):
#                 if j > i:
#                     experiment = experiment_matrix[i][j]
#                     morph = morph_matrix[i][j]
#                     cov_exp_morph += (experiment - avg_experiment) * (morph - avg_morph)
#                     disp_morph += (morph - avg_morph) * (morph - avg_morph)
#                     disp_experiment += (experiment - avg_experiment) * (experiment - avg_experiment)
#
#         corr = cov_exp_morph / (math.sqrt(disp_morph) * math.sqrt(disp_experiment))
#
#         print(f"param_a: {param_a}, param_g_weight: {param_g_weight}, corr: {corr}")
#
#         if corr > corr_max:
#             corr_max = corr
#
#         # print("res")
#         # for key, val in sorted(res.items()):
#         #     print("%s, %s" % (key, val))
#         #
#         # print("res_avg")
#         # for key, val in sorted(res_avg.items()):
#         #     print("%s, %s" % (key, val))
#
# print(f"corr_max: {corr_max}")
# exit()

# gr = 0, dist_dir = 1; avg: 2.1548202760083903
# gr = 1, dist_dir = 0; avg: 2.4373013948464073
# gr = 1, dist_dir = 1; avg: 4.592121670854795




# 0.62248, 1.10513907, 0.25874813, 1.08080493 : 98.81245484324980 , for pow(morph, val-3) + morph_offset
# 0.62261, 1.09702663, 0.25845481, 1.08124007 : 98.81529981772437 , for pow(morph, val-1) + morph_offset
# 0.62270, 1.09090768, 0.25821851, 1.08150308 : 98.81747403992031 , for pow(morph, val+1) + morph_offset
# 0.62278, 1.08224147, 0.25783362, 1.08166328 : 98.82068293183832 , for pow(morph, val+5) + morph_offset
# 0.62461, 0.22533131, 0.25284749, 3.20159324 : 98.85357913946267 , for morph * val + morph_offset
# 0.61371, 0.14720072, 0.18996398, 3.22037342 : 99.21467219410209 , for morph * val + morph_offset (updated distance formula)

#
#
# print(result.success)
# print(result.x)
# print(result)
# print(f"len: {len(matrDiff.names)}")
#
#
#
# param_a = result.x[0]
# param_morph_exp = result.x[1]
# param_g_weight = result.x[2]
# param_morph_offset = result.x[3]
#
# experiment_matrix = matrDiff.make_experiment_matrix(param_a, param_g_weight)
# morph_matrix = matrDiff.make_morph_matrix(param_morph_exp, param_morph_offset)
#
# print_matrix(experiment_matrix, "experiment_matrix")
# print_matrix(morph_matrix, "morph_matrix")
# print_matrix(matrDiff.matr_diff(result.x), "diff_matrix")
# #print(f"res: {matrDiff.matr_diff_sum(result.x)}")
#
# #
# # for name in names:
# #     print(f", {name.replace(' ', '_')}", end='')
# # print("")
# #
# #
# # print_matrix(experiment_matrix, "experiment_matrix")
# # print_matrix(morph_matrix, "morph_matrix")
# # print_matrix(res_matrix, "res_matrix")
