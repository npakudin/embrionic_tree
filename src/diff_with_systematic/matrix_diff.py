import copy

import numpy

from src.compare_trees.development_tree_reader import read_all_trees
from src.diff_with_systematic.build_morph_graph import taxon_from_xml
from src.compare_trees.distances import development_tree_distance
from src.compare_trees.global_params import GlobalParams, exponent_reduced_weight, exponent_src_weight, const_weight


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


def make_experiment_array(experiment_matrix):
    experiment_array = []
    for j in range(len(experiment_matrix)):  # column
        for i in range(len(experiment_matrix) - j - 1):  # row
            experiment_array.append(experiment_matrix[i + j + 1][j])
    return experiment_array


def print_matrix(matr, name, tree_names, corrcoef=None, with_headers=False):
    print(f"")
    print(f"{name}")
    if with_headers:
        print(f"names ", end='')
    for tree_name in tree_names:
        print(f"{tree_name.replace(' ', '_')} ", end='')
    print(f"")

    plot_matr = [[(0 if i == j else (matr[i][j] if i > j else matr[j][i])) for j in
                  range(len(matr))] for i in range(len(matr))]

    summ = 0
    maxx = 0
    for i, row in enumerate(plot_matr):
        if with_headers:
            print(f"{tree_names[i]} ", end='')
        for index, item in enumerate(row):
            if index == i:
                print("- ", end='')
            else:
                print("%0.2f " % (item), end='')
            summ += item
            if item > maxx:
                maxx = item
        print()
    avg = summ / (len(plot_matr) * (len(plot_matr) - 1))
    print(f"avg: {avg}; max: {maxx}")
    if corrcoef is not None:
        print(f"corrcoef: {corrcoef}")


def diff_matrices(experiment_morph_coeff, experiment_matrix, systematic_matrix):
    res = 0
    for i, experiment_row in enumerate(experiment_matrix):
        for j, experiment_col in enumerate(experiment_row):
            if j > i:
                experiment = experiment_morph_coeff * experiment_matrix[i][j]
                morph = systematic_matrix[i][j]

                res += abs(experiment - morph) / (min(experiment, morph) + 1.0E-100)
    return res


def to_full_matrix(left_bottom_matrix):
    plot_matr = [[(0 if i == j else (left_bottom_matrix[i][j] if i > j else left_bottom_matrix[j][i])) for j in
                  range(len(left_bottom_matrix))] for i in range(len(left_bottom_matrix))]
    return plot_matr


def corrcoef(matr1, matr2):
    array1 = []
    array2 = []
    for i, row1 in enumerate(matr1):
        for j, col1 in enumerate(row1):
            array1.append(matr1[i][j])
            array2.append(matr2[i][j])

    corrcoef_matrix = numpy.corrcoef([array1, array2])

    return corrcoef_matrix[0][1]



class MatrixDiff:
    def __init__(self, experiment_pattern, morph_file, leave_list, max_levels=11):
        vertices = read_all_trees(pattern=experiment_pattern, max_levels=max_levels)

        # morph matrix
        taxon = taxon_from_xml(morph_file)
        taxon.leave_only_names(leave_list)

        taxon.leave_only_names([v.name for v in vertices])

        # sort by name, but also possible to sort both names and taxon_names by order_index
        # for it in this file and in get_leaves
        # replace "key=lambda x: x.name" to "key=lambda x: x.order_index"
        leaves = taxon.get_leaves()
        for index, leave in enumerate(leaves):
            leave.order_index = index

        taxon_names = list(map(lambda x: x.name, taxon.get_leaves()))
        # print("taxon_names")
        # print(taxon_names)

        # O(n^2), but n~26, so for now it's OK
        for vertex in vertices:
            for index, leave in enumerate(leaves):
                if leave.name == vertex.name:
                    vertex.order_index = index

        # filter experiment vertices
        self.vertices = sorted(list(filter(lambda x: x.name in taxon_names, vertices)), key=lambda x: x.name)
        self.names = [v.name for v in self.vertices]

        for tree in self.vertices:
            tree.prepare()

        # print("names")
        # print(self.names)

        self.taxon_matrix = taxon.calculate()

        self.min_value = float("inf")
        self.min_params = [0, 0, 0]

    def make_full_experiment_matrix(self, global_params):
        left_bottom_matrix = self.make_experiment_matrix(global_params)
        return to_full_matrix(left_bottom_matrix)

    def make_experiment_matrix(self, global_params):
        # create a copy of trees to modify
        # trees = [copy.deepcopy(src_tree) for src_tree in self.vertices]
        #
        # # prepare to calculate distances
        # for tree in trees:
        #     tree.prepare(global_params)

        #trees = [tree.left for tree in trees]
        trees = self.vertices

        depths = [v.reduced_depth for v in trees]
        # print("depths")
        # print(depths)

        experiment_matrix = []
        for i in range(len(trees)):
            experiment_matrix.append([])
            for j in range(i):
                dist = development_tree_distance(trees[i], trees[j], global_params)
                experiment_matrix[i].append(dist)

        return experiment_matrix

    def make_systematic_matrix(self):
        def systematic_dist(val):
            return val

        systematic_matrix = []
        for i in range(len(self.taxon_matrix)):
            systematic_matrix.append([])
            for j in range(i):
                dist = systematic_dist(self.taxon_matrix[i][j])
                systematic_matrix[i].append(dist)

        return systematic_matrix

    def corrcoef(self, experiment_matrix):
        systematic_matrix = self.make_systematic_matrix()
        return corrcoef(systematic_matrix, experiment_matrix)

    def matr_diff(self, x):
        global_params = GlobalParams(max_levels=11, g_weight=x[1], chain_length_weight=x[2], is_swap_left_right=False,
                                     calc_weight=exponent_reduced_weight(a=x[0]))
                                     #calc_weight=exponent_src_weight(a=x[0]))
                                     #calc_weight=const_weight(weight=x[0]))

        experiment_matrix = self.make_experiment_matrix(global_params)
        return self.corrcoef(experiment_matrix)

    def matr_diff_sum(self, x):
        res = self.matr_diff(x)

        a = x[0]
        g_weight = x[1]
        chain_length_weight = x[2]
        print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f} : {res:0.14f}")
        return res


