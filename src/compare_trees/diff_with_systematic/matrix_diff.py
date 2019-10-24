import copy
import glob
import math

import numpy

from src.compare_trees.development_tree_reader import read_all_trees
from src.compare_trees.diff_with_systematic.build_morph_graph import taxon_from_xml
#from src.compare_trees.distances import *
from src.compare_trees.distances import dist_branch_direction
from src.compare_trees.global_params import GlobalParams


def apply_each(matr, fun):
    res = []
    for i, row in enumerate(matr):
        res.append([])
        for j, col in enumerate(row):
            res[i].append(fun(matr[i][j]))
    return res


def apply_reduce(matr, fun, init_value):
    res = init_value
    for i, row in enumerate(matr):
        for j, col in enumerate(row):
            res = fun(res, matr[i][j])
    return res


def normalize(matr):
    summ = apply_reduce(matr, lambda accumulator, val: accumulator + abs(val), 0.0)
    res = apply_each(matr, lambda val: val / summ)
    return res


def print_matrix(matr, name):
    print(f"")
    print(f"matrix {name}")
    summ = 0
    for row in matr:
        for item in row:
            print("%0.2f " % (item), end='')
            summ += item
        print()
    avg = summ / (len(matr) ** 2)
    print(f"avg: {avg}")


def diff_matrices(experiment_morph_coeff, experiment_matrix, morph_matrix):
    res = 0
    for i, experiment_row in enumerate(experiment_matrix):
        for j, experiment_col in enumerate(experiment_row):
            if j > i:
                experiment = experiment_morph_coeff * experiment_matrix[i][j]
                morph = morph_matrix[i][j]

                res += abs(experiment - morph) / (min(experiment, morph) + 1.0E-100)
    return res


class MatrixDiff:
    def __init__(self, experiment_pattern, morph_file, leave_list):
        # files = glob.glob(experiment_pattern)
        # files.sort()
        # vertices = [prepared_tree_from_yml(x) for x in files]
        vertices = read_all_trees(pattern=experiment_pattern, max_levels=11)

        # morph matrix
        taxon = taxon_from_xml(morph_file)
        taxon.leave_only_names(leave_list)
        taxon.leave_only_names([v.name for v in vertices])
        taxon_names = list(map(lambda x: x.name, taxon.get_leaves()))

        # filter experiment vertices
        self.vertices = list(filter(lambda x: x.name in taxon_names, vertices))
        self.names = [v.name for v in self.vertices]

        print(f"count of names: {len(self.names)}")
        print(f"count of vertices: {len(self.vertices)}")

        self.taxon_matrix = taxon.calculate()

    def make_experiment_matrix(self, global_params):

        # create a copy of trees to modify
        trees = [copy.deepcopy(src_tree) for src_tree in self.vertices]

        # prepare to calculate distances
        for tree in trees:
            tree.root.reduce(global_params)
            tree.root.prepare(global_params)

        experiment_matrix = []
        for i in range(len(trees)):
            experiment_matrix.append([])
            #for j in range(len(trees)):
            for j in range(i):
                dist = dist_branch_direction(trees[i].root, trees[j].root, global_params)
                experiment_matrix[i].append(dist)

        #experiment_matrix = [[dist_branch_direction(v1.root, v2.root, global_params) for v2 in trees] for v1 in trees]

        return experiment_matrix

        # cur_vertices = []
        #
        # for v in self.vertices:
        #     v.prepare(global_params)
        #
        # experiment_matrix = [[dist_branch_direction(v1, v2, global_params) for v2 in self.vertices] for v1 in self.vertices]
        # return normalize(experiment_matrix)

        # print(f"count of matr: {len(experiment_matrix)}")
        # print(f"count of vertices: {len(self.vertices)}")

        return experiment_matrix

    def make_linear_morph_matrix(self):
        def dist(val):
            return val

        morph_matrix = apply_each(self.taxon_matrix, dist)
        return morph_matrix

    def make_morph_matrix(self, global_params):
        def exp_dist(val):
            return val
            #return global_params.morph_exp * val
            #return param_morph * val + param_morph_offset
            # return math.pow(param_morph, val + 5) + param_morph_offset
            # if val == 0:
            #     return 0
            # return math.pow(global_params.morph_exp, val)
            # if val == 0:
            #     return 0
            # if val == 1:
            #     return 1
            # return math.pow(param_morph_exp, val - 1)

        morph_matrix = []
        for i in range(len(self.taxon_matrix)):
            morph_matrix.append([])
            #for j in range(len(self.taxon_matrix)):
            for j in range(i):
                dist = self.taxon_matrix[i][j]
                morph_matrix[i].append(dist)

        #morph_matrix = apply_each(self.taxon_matrix, exp_dist)
        return morph_matrix

    def matr_diff(self, x):
        # param_a = x[0]
        # param_morph_exp = x[1]
        # param_g_weight = x[2]
        # param_morph_offset = x[3]

        global_params = GlobalParams(a=x[0], g_weight=x[1], chain_length_weight=x[2], is_swap_left_right=False,
                                     max_levels=11)

        experiment_matrix = self.make_experiment_matrix(global_params)
        morph_matrix = self.make_morph_matrix(global_params)

        print_matrix(experiment_matrix, "experiment_matrix")
        #print_matrix(morph_matrix, "morph_matrix")

        experiment_array = []
        morph_array = []
        for i, experiment_row in enumerate(experiment_matrix):
            for j, experiment_col in enumerate(experiment_row):
                experiment_array.append(experiment_matrix[i][j])
                morph_array.append(morph_matrix[i][j])

        corrcoef_matrix = numpy.corrcoef([experiment_array, morph_array])
        # print(f"corrcoef_matrix:")
        # print(f"{corrcoef_matrix}")
        return -corrcoef_matrix[0][1]

        # print_matrix(experiment_matrix, "experiment_matrix")
        # print_matrix(morph_matrix, "morph_matrix")

        # sum_exp = apply_reduce(experiment_matrix, lambda accumulator, val: accumulator + val, 0.0)
        # sum_morph = apply_reduce(morph_matrix, lambda accumulator, val: accumulator + val, 0.0)
        #
        # print(f"{sum_exp} - {sum_morph}")
        #
        # res = []
        # for i, experiment_row in enumerate(experiment_matrix):
        #     res.append([])
        #     for j, experiment_col in enumerate(experiment_row):
        #         experiment = experiment_matrix[i][j]
        #         morph = morph_matrix[i][j] * sum_exp / sum_morph
        #         res[i].append(abs(experiment - morph) / (morph + 1.0E-100))
        #         #res[i].append(abs(experiment - morph) / (min(experiment, morph) + 1.0E-100))
        #         #res[i].append(abs(experiment - morph))
        # return res

    def matr_diff_sum(self, x):
        #matr = self.matr_diff(x)
        # res = normalize(matr)
        #res = apply_reduce(matr, lambda accumulator, val: accumulator + abs(val), 0.0)
        res = self.matr_diff(x)

        a = x[0]
        g_weight = x[1]
        chain_length_weight = x[2]
        #morph_exp = x[3]
        print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res:0.14f}")
        return res


#
#
# # 0.6569679 , 1.05135879, 0.08006142
#
# a = 0.45432
# morph_exp = 1.25910
# g_weight = 0.04658
# experiment_morph_coeff = 1
#
#
# # init_values = [a, morph_exp, g_weight, experiment_morph_coeff]
# # result = optimize.minimize(matr_diff, np.array(init_values), bounds=((0.01, 2.5), (1.01, 3.0), (0, 5), (0.01, 100))) # try Newton-CG
#
# init_values = [a, morph_exp, g_weight]
# result = optimize.minimize(matr_diff, np.array(init_values), bounds=((0.01, 2.5), (1.01, 3.0), (0, 5))) # try Newton-CG
#
#
# print(result.success)
# print(result.x)
# print(result)
# print(f"len: {len(names)}")
# #exit()
#
#
# param_a = result.x[0]
# param_morph_exp = result.x[1]
# param_g_weight = result.x[2]

# param_a = 0.45128
# param_morph_exp = 1.23710
# param_g_weight = 0.05721
#
# experiment_matrix = make_experiment_matrix(param_a, param_g_weight)
# morph_matrix = make_morph_matrix(param_morph_exp)
#
# print_matrix(experiment_matrix, "experiment_matrix")
# print_matrix(morph_matrix, "morph_matrix")
# print(f"res: {diff_matrices(1.0, experiment_matrix, morph_matrix)}")
#
