import numpy

from src.multiple_trees.trees_matrix import TreesMatrix
from src.single_tree.global_params import GlobalParams
from src.view.build_morph_graph import taxon_from_xml


def diff_matrices(experiment_morph_coef, experiment_matrix, systematic_matrix):
    res = 0
    for i, experiment_row in enumerate(experiment_matrix):
        for j, experiment_col in enumerate(experiment_row):
            if j > i:
                experiment = experiment_morph_coef * experiment_matrix[i][j]
                morph = systematic_matrix[i][j]

                res += abs(experiment - morph) / (min(experiment, morph) + 1.0E-100)
    return res


def corrcoef(matr1, matr2):
    array1 = []
    array2 = []
    for i, row1 in enumerate(matr1):
        for j, col1 in enumerate(row1):
            array1.append(matr1[i][j])
            array2.append(matr2[i][j])

    corrcoef_matrix = numpy.corrcoef([array1, array2])

    return corrcoef_matrix[0][1]


class MatrixDiff(TreesMatrix):
    def __init__(self, experiment_pattern, morph_file, leave_list, max_level=10, filter_by_taxon=True,
                 is_reducing=True, use_min_common_depth=False):
        super().__init__(experiment_pattern, max_level, is_reducing, use_min_common_depth)

        # morph matrix
        taxon = taxon_from_xml(morph_file)
        taxon.leave_only_names(leave_list)
        taxon.leave_only_names([v.name for v in self.vertices])
        self.taxon_matrix = taxon.calculate()

        taxon_names = list(map(lambda x: x.name, taxon.get_leaves()))
        # print("taxon_names")
        # print(taxon_names)

        # filter experiment vertices
        self.vertices = filter(lambda x: x.name in taxon_names, self.vertices) if filter_by_taxon else self.vertices
        self.vertices = sorted(list(self.vertices), key=lambda x: x.name)
        self.names = [v.name for v in self.vertices]

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
        increasing_level = x[3]
        level_weight_multiplier = [1] * 11
        if increasing_level >= 0:
            level_weight_multiplier[int(increasing_level)] *= 5

        global_params = GlobalParams(max_level=10, param_a=x[0], g_weight=x[1], chain_length_weight=x[2],
                                     level_weight_multiplier=level_weight_multiplier)

        experiment_matrix = self.make_experiment_matrix(global_params)
        return self.corrcoef(experiment_matrix)

    def matr_diff_sum(self, x):
        res = self.matr_diff(x)

        a = x[0]
        g_weight = x[1]
        chain_length_weight = x[2]
        increasing_level = x[3]
        print(f"{a:0.5f}, {g_weight:0.8f}, {chain_length_weight:0.8f}, {int(increasing_level):2} : {res:0.14f}")
        return res
