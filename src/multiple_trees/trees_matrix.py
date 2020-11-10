from src.single_tree.development_tree import INFINITE_PATTERN
from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.development_tree_utils import prepare_trees
from src.single_tree.superimposed_tree import SuperimposedNode


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


def print_matrix(matr, name, tree_names, corr_coef=None, with_headers=False):
    print(f"")
    print(f"{name}")
    if with_headers:
        print(f"Sp. ", end='')
    for tree_name in tree_names:
        print(f"{tree_name.replace(' ', '_')} ", end='')
    print(f"")

    plot_matr = [[(0 if i == j else (matr[i][j] if i > j else matr[j][i])) for j in
                  range(len(matr))] for i in range(len(matr))]

    summ = 0
    maxx = 0
    for i, row in enumerate(plot_matr):
        if with_headers:
            print(f"{tree_names[i].replace(' ', '_')} ", end='')
        for index, item in enumerate(row):
            if index == i:
                print("- ", end='')
            else:
                print("%0.2f " % item, end='')
            summ += item
            if item > maxx:
                maxx = item
        print()
    avg = summ / (len(plot_matr) * (len(plot_matr) - 1))
    print(f"avg: {avg}; max: {maxx}")
    if corr_coef is not None:
        print(f"corrcoef: {corr_coef}")


def to_full_matrix(left_bottom_matrix):
    plot_matr = [[(0 if i == j else (left_bottom_matrix[i][j] if i > j else left_bottom_matrix[j][i])) for j in
                  range(len(left_bottom_matrix))] for i in range(len(left_bottom_matrix))]
    return plot_matr


class TreesMatrix:
    def __init__(self, experiment_pattern, max_level=10, is_reducing=True, use_min_common_depth=False,
                 use_flipping=False):
        vertices = read_all_trees(pattern=experiment_pattern)

        self.vertices = sorted(list(vertices), key=lambda x: x.name)
        self.names = [v.name for v in self.vertices]

        prepare_trees(self.vertices, max_level, is_reducing, use_min_common_depth, use_flipping)

    def make_full_experiment_matrix(self, global_params):
        left_bottom_matrix = self.make_experiment_matrix(global_params)
        return to_full_matrix(left_bottom_matrix)

    def make_experiment_matrix(self, global_params, pattern=INFINITE_PATTERN):
        trees = self.vertices

        experiment_matrix = []
        for i in range(len(trees)):
            experiment_matrix.append([])
            for j in range(i):
                dist = full_distance(global_params, trees[i].root, trees[j].root, trees[j].flipped_root, pattern=pattern)

                experiment_matrix[i].append(dist)

        return experiment_matrix


def full_distance(global_params, root1, root2, flipped_root2, pattern=INFINITE_PATTERN):
    dist1 = SuperimposedNode(root1, root2).full_distance(global_params, pattern=pattern)
    dist2 = dist1
    if global_params.use_flipping:
        dist2 = SuperimposedNode(root1, flipped_root2).full_distance(global_params, pattern=pattern)
    return min(dist1, dist2)

