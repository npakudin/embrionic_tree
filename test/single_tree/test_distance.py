import copy
import math
from unittest import TestCase
from src.multiple_trees.compare_trees import get_distances_by_files
from src.multiple_trees.trees_matrix import print_matrix, TreesMatrix
from src.single_tree.global_params import GlobalParams
from src.view.draw_compared_trees import TreeDrawer, TreeDrawSettings

global_params = GlobalParams(max_level=11, param_a=0.6, g_weight=0.1, chain_length_weight=0.1)


class TestDistance(TestCase):
    # def test_chain_length_exist(self):
    #     is_reducing = True
    #     global_params_copy = copy.deepcopy(global_params)
    #     [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_chain_level_only_*.xtg", global_params_copy, is_reducing)
    #     # `a` at level 1  +  2*a^2 at level 2
    #     expected_distance = global_params_copy.chain_length_weight *\
    #                         (math.pow(global_params_copy.param_a, 1) + math.pow(global_params_copy.param_a, 2) * 2)
    #     self.assertAlmostEqual(expected_distance, distance_matrix[0][1])
    #
    # def test_chain_length_0_weight(self):
    #     is_reducing = True
    #     global_params_copy = copy.deepcopy(global_params)
    #     global_params_copy.chain_length_weight = 0
    #     [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_chain_level_only_*.xtg", global_params_copy, is_reducing)
    #     expected_distance = 0
    #     self.assertAlmostEqual(expected_distance, distance_matrix[0][1])
    #
    # def test_reduce(self):
    #     is_reducing = True
    #     [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_reduce*.xtg", GlobalParams(max_level=11), is_reducing)
    #     expected_distance = 0
    #     self.assertAlmostEqual(expected_distance, distance_matrix[0][1])

    def test_m2(self):
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/paper_m/M2_*.xtg",
                                                           GlobalParams(max_level=11), is_reducing=False)

        self.assertAlmostEqual(0, distance_matrix[0][1])
        self.assertAlmostEqual(0, distance_matrix[0][2])
        self.assertAlmostEqual(0, distance_matrix[1][2])

    def test_m3(self):
        [trees, distance_matrix] = get_distances_by_files("../../test/test_input/paper_m/M3_*.xtg",
                                                           GlobalParams(max_level=11), is_reducing=False)

        # for tree in trees:
        #     tree.reduce()
        #     tree.prepare(False, False)
        #
        # tree_drawer = TreeDrawer(TreeDrawSettings.single_tree_unreduced(), global_params)
        # for i in range(0, len(trees)):
        #     tree_drawer.draw_tree(trees[i], trees[i], "../../test/test_output/m3")

        global_params = GlobalParams(max_level=11)

        trees_matrix = TreesMatrix("../../input/xtg_johansen/*.xtg", max_level=11)

        # trees = trees_matrix.vertices
        #
        # tree_drawer = TreeDrawer(TreeDrawSettings.single_tree_unreduced(), global_params)
        # for i in range(0, len(trees)):
        #     tree_drawer.draw_tree(trees[i], trees[i], "../../test/test_output/m3")

        self.assertAlmostEqual(2.5, distance_matrix[0][1])
        self.assertAlmostEqual(4.0, distance_matrix[0][2])
        self.assertAlmostEqual(2.0, distance_matrix[1][2])

    def test_m4(self):
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/paper_m/M4_*.xtg",
                                                           GlobalParams(max_level=11), is_reducing=False)

        self.assertAlmostEqual(0.5, distance_matrix[0][1])
        self.assertAlmostEqual(2.0, distance_matrix[0][2])
        self.assertAlmostEqual(2.0, distance_matrix[1][2])

    def test_m5(self):
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/paper_m/M5_*.xtg",
                                                           GlobalParams(max_level=11), is_reducing=False)

        self.assertAlmostEqual(1.75, distance_matrix[0][1])
        self.assertAlmostEqual(2.00, distance_matrix[0][2])
        self.assertAlmostEqual(2.00, distance_matrix[0][3])

        self.assertAlmostEqual(0.50, distance_matrix[1][2])
        self.assertAlmostEqual(1.50, distance_matrix[1][3])

        self.assertAlmostEqual(1.50, distance_matrix[2][3])
