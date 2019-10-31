import copy

import numpy

from src.compare_trees.development_tree_reader import read_all_trees
from src.compare_trees.diff_with_systematic.build_morph_graph import taxon_from_xml
from src.compare_trees.distances import development_tree_distance
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


def diff_matrices(experiment_morph_coeff, experiment_matrix, systematic_matrix):
    res = 0
    for i, experiment_row in enumerate(experiment_matrix):
        for j, experiment_col in enumerate(experiment_row):
            if j > i:
                experiment = experiment_morph_coeff * experiment_matrix[i][j]
                morph = systematic_matrix[i][j]

                res += abs(experiment - morph) / (min(experiment, morph) + 1.0E-100)
    return res


class MatrixDiff:
    def __init__(self, experiment_pattern, morph_file, leave_list):
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

    def make_full_experiment_matrix(self, global_params):
        left_bottom_matrix = self.make_experiment_matrix(global_params)
        plot_matr = [[(0 if i == j else (left_bottom_matrix[i][j] if i > j else left_bottom_matrix[j][i])) for j in
                      range(len(left_bottom_matrix))] for i in range(len(left_bottom_matrix))]
        return plot_matr

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
            for j in range(i):
                dist = development_tree_distance(trees[i].root, trees[j].root, global_params)
                experiment_matrix[i].append(dist)

        return experiment_matrix


    def make_systematic_matrix(self, global_params):
        def systematic_dist(val):
            return val

        systematic_matrix = []
        for i in range(len(self.taxon_matrix)):
            systematic_matrix.append([])
            for j in range(i):
                dist = systematic_dist(self.taxon_matrix[i][j])
                systematic_matrix[i].append(dist)

        return systematic_matrix

    def matr_diff(self, x):
        global_params = GlobalParams(a=x[0], g_weight=x[1], chain_length_weight=x[2], is_swap_left_right=True,
                                     max_levels=11)

        experiment_matrix = self.make_experiment_matrix(global_params)
        systematic_matrix = self.make_systematic_matrix(global_params)

        #print(f"global_params: {global_params.dcl_more_zero} / {global_params.total_dist}")

        #print_matrix(experiment_matrix, "experiment_matrix")
        #print_matrix(systematic_matrix, "systematic_matrix")

        experiment_array = []
        morph_array = []
        for i, experiment_row in enumerate(experiment_matrix):
            for j, experiment_col in enumerate(experiment_row):
                experiment_array.append(experiment_matrix[i][j])
                morph_array.append(systematic_matrix[i][j])

        corrcoef_matrix = numpy.corrcoef([experiment_array, morph_array])
        #print(f"corrcoef_matrix[0][1]: {corrcoef_matrix[0][1]}")

        # print_matrix(experiment_matrix, "experiment_matrix")
        # print_matrix(systematic_matrix, "systematic_matrix")

        return -corrcoef_matrix[0][1]

        #return sum_res

    def matr_diff_sum(self, x):
        res = self.matr_diff(x)

        a = x[0]
        g_weight = x[1]
        chain_length_weight = x[2]
        print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res:0.14f}")
        return res


