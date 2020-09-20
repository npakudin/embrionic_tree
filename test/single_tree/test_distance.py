import copy
import math
from unittest import TestCase
from src.single_tree.compare_trees import get_distances_by_files
from src.single_tree.global_params import GlobalParams

global_params = GlobalParams(max_level=11, param_a=0.6, g_weight=0.1, chain_length_weight=0.1)


class TestDistance(TestCase):
    def test_chain_length_exist(self):
        global_params_copy = copy.deepcopy(global_params)
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_chain_level_only_*.xtg", global_params_copy)
        # `a` at level 1  +  2*a^2 at level 2
        expected_distance = global_params_copy.chain_length_weight *\
                            (math.pow(global_params_copy.param_a, 1) + math.pow(global_params_copy.param_a, 2) * 2)
        self.assertAlmostEqual(expected_distance, distance_matrix[0][1])

    def test_chain_length_0_weight(self):
        global_params_copy = copy.deepcopy(global_params)
        global_params_copy.chain_length_weight = 0
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_chain_level_only_*.xtg", global_params_copy)
        expected_distance = 0
        self.assertAlmostEqual(expected_distance, distance_matrix[0][1])

    def test_reduce(self):
        [_trees, distance_matrix] = get_distances_by_files("../../test/test_input/test_reduce*.xtg", GlobalParams(max_level=11))
        expected_distance = 0
        self.assertAlmostEqual(expected_distance, distance_matrix[0][1])
