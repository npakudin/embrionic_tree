import copy
from unittest import TestCase

from src.multiple_trees.compare_trees import get_distances_by_files
from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.global_params import GlobalParams

global_params = GlobalParams(max_level=11, param_a=0.6, g_weight=0.1, chain_length_weight=0.1)


class TestDistance(TestCase):
    # def test_chain_length_exist(self):
    #     is_reducing = True
    #     global_params_copy = copy.deepcopy(global_params)
    #     [_trees, matr] = get_distances_by_files("test/test_input/test_chain_level_only_*.xtg", global_params_copy, is_reducing)
    #     # `a` at level 1  +  2*a^2 at level 2
    #     expected_distance = global_params_copy.chain_length_weight *\
    #                         (math.pow(global_params_copy.param_a, 1) + math.pow(global_params_copy.param_a, 2) * 2)
    #     self.assertAlmostEqual(expected_distance, matr[0][1])
    #
    # def test_chain_length_0_weight(self):
    #     is_reducing = True
    #     global_params_copy = copy.deepcopy(global_params)
    #     global_params_copy.chain_length_weight = 0
    #     [_trees, matr] = get_distances_by_files("test/test_input/test_chain_level_only_*.xtg", global_params_copy, is_reducing)
    #     expected_distance = 0
    #     self.assertAlmostEqual(expected_distance, matr[0][1])
    #
    # def test_reduce(self):
    #     is_reducing = True
    #     [_trees, matr] = get_distances_by_files("test/test_input/test_reduce*.xtg", GlobalParams(max_level=11), is_reducing)
    #     expected_distance = 0
    #     self.assertAlmostEqual(expected_distance, matr[0][1])

    # expected_matr = top-right matr (diagonal is excluded)
    def compare(self, path, is_reducing, expected_matr, g_weight=0.0):
        [_trees, matr] = get_distances_by_files(f"test/test_input/{path}",
                                                GlobalParams(max_level=11, is_test_nodes=True, g_weight=g_weight),
                                                is_reducing=is_reducing,
                                                is_test_nodes=True)
        for (i, expected_row) in enumerate(expected_matr):
            for (j, expected_value) in enumerate(expected_row):
                actual_value = matr[i][j + i + 1]
                self.assertAlmostEqual(expected_value, actual_value)

    def test_chain(self):
        # if reduce - all trees are the same
        # distance between chain_13 and chain_13_with_division_at_12 = 0
        distance_13_13_with_div_at_12 = 0
        self.compare("chains/test_chain_*.xtg", True,  [[0, 0, 0],
                                                           [0, 0],
                                                              [distance_13_13_with_div_at_12]])

        # if NO reduce
        dist_level_10 = pow(0.5, 9)  # d(Leave, Growth)
        dist_level_11 = pow(0.5, 10) # d(Leave, Null)
        dist_chain_10_chain_11 = dist_level_10 +  dist_level_11
        dist_chain_10_chain_13 = dist_chain_10_chain_11 # equal because of cut at level 11
        dist_chain_11_chain_13 = 0 # equal because of cut at level 11
        self.compare("chains/test_chain_*.xtg", False, [[dist_chain_10_chain_11, dist_chain_10_chain_13, dist_chain_10_chain_13],
                                                                                [dist_chain_11_chain_13, dist_chain_11_chain_13],
                                                                                                         [0]])

    def test_growth_chain(self):
        # if growth > 0, then distance[0][1] > 0
        # then distance[1][2] tests producing growths in the chain
        d_growth_and_no_growth = pow(0.5, 1) * (256 - 1)
        self.compare("chains/test_*chain_10.xtg", True,  [[d_growth_and_no_growth, d_growth_and_no_growth],
                                                                                   [0]],
                     g_weight=1.0)

        # if growth = 0, then distance[0][1] = 0
        self.compare("chains/test_*chain_10.xtg", True,  [[0, 0],
                                                             [0]],
                     g_weight=0.0)


    def test_m2(self):
        self.compare("paper_m/M2_*.xtg", True,  [[0, 0],
                                                    [0]])
        # self.compare("paper_m/M2_*.xtg", False, [[1.25, 3.00],
        #                                                [1.00]])
        self.compare("paper_m/M2_*.xtg", False, [[0, 0],
                                                    [0]])

    def test_m3(self):
        self.compare("paper_m/M3_*.xtg", True,  [[0, 0],
                                                    [0]])
        # self.compare("paper_m/M3_*.xtg", False, [[1, 2],
        #                                             [1]])
        self.compare("paper_m/M3_*.xtg", False, [[0, 0],
                                                    [0]])

    def test_m4(self):
        self.compare("paper_m/M4_*.xtg", True,  [[0.5, 2.0],
                                                      [2.0]])
        self.compare("paper_m/M4_*.xtg", False, [[0.5, 2.0],
                                                      [2.0]])

    def test_m5(self):
        self.compare("paper_m/M5_*.xtg", False, [[0.00, 0.50, 2.00],
                                                       [0.50, 2.00],
                                                             [2.00]])

    def test_m6(self):
        self.compare("paper_m/M6_*.xtg", True,  [[1.25]])
        self.compare("paper_m/M6_*.xtg", False, [[1.25]])

    def test_patt(self):
        self.compare("patt_*.xtg", True,  [[0.75]])
        self.compare("patt_*.xtg", False, [[1.00]])

    def test_to_standard_form_growth(self):
        # read trees from *.xtg files in xtg folder
        src_trees = read_all_trees(pattern="test/test_input/test_standard_form_growth_*.xtg", is_test_nodes=True)

        # create a copy of trees to modify
        trees = [copy.deepcopy(src_tree) for src_tree in src_trees]

        self.assertEqual("XGN X XGN".replace(" ", ""), trees[0].to_string(3))
        self.assertEqual("XGN X XGN".replace(" ", ""), trees[1].to_string(3))

        trees[0].to_standard_form(3)
        trees[1].to_standard_form(3)

        self.assertEqual(trees[1].root.to_array(3), trees[0].root.to_array(3))  # equal after standartization
        self.assertNotEqual(src_trees[1].root.to_array(3), trees[1].root.to_array(3))  # changed

        self.assertEqual(src_trees[0].root.to_array(3), trees[0].root.to_array(3))  # not changed during standartization

    def test_to_standard_form_completion(self):
        # read trees from *.xtg files in xtg folder
        src_trees = read_all_trees(pattern="test/test_input/test_standard_form_compl_*.xtg", is_test_nodes=True)

        # create a copy of trees to modify
        trees = [copy.deepcopy(src_tree) for src_tree in src_trees]

        self.assertEqual("ZDG X NAN".replace(" ", ""), trees[0].to_string(3))
        self.assertEqual("NAN X GDZ".replace(" ", ""), trees[1].to_string(3))

        trees[0].to_standard_form(3)
        trees[1].to_standard_form(3)

        self.assertEqual("ZDG X NAN".replace(" ", ""), trees[0].to_string(3))

        self.assertEqual(trees[1].root.to_array(3), trees[0].root.to_array(3))  # equal after standartization
        self.assertNotEqual(src_trees[1].root.to_array(3), trees[1].root.to_array(3))  # changed

        self.assertEqual(src_trees[0].root.to_array(3), trees[0].root.to_array(3))  # not changed during standartization

