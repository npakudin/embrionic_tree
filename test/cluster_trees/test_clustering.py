from unittest import TestCase

import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy

from src.cluster_trees.clustering import corr_clustered_trees
from src.multiple_trees.matrix_diff import MatrixDiff
from src.multiple_trees.trees_matrix import to_full_matrix
from src.single_tree.global_params import GlobalParams


class TestClustering(TestCase):
    def test_corr_clustered_trees(self):

        systematic_tree = "morph"
        max_level = 11
        cluster_algorithm = 'average'
        matr_diff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                              ["Angiosperms"], max_level=max_level, is_reducing=True)

        params = [(0.5, -1, 0.29536767921530455), (1.0, -1, 0.04947724771267295),
                  (0.5, 3-1, 0.29337382536794604), (1.0, 3-1, 0.12199025619653726)]
        for (param_a, increasing_level, expected_corr) in params:
            level_weight_multiplier = [1] * 11
            if increasing_level >= 0:
                level_weight_multiplier[increasing_level] *= 5

            global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=0.0,
                                         chain_length_weight=0.0, level_weight_multiplier=level_weight_multiplier)

            experiment_matrix = matr_diff.make_experiment_matrix(global_params)

            plot_matrix = to_full_matrix(experiment_matrix)
            # convert the redundant n*n square matrix form into a condensed nC2 array
            # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
            dist_array = ssd.squareform(plot_matrix)

            # clustered_trees = hierarchy.linkage(np.asarray(experiment_array), cluster_algorithm)
            clustered_trees = hierarchy.linkage(dist_array, cluster_algorithm)

            actual_corr = corr_clustered_trees(clustered_trees, matr_diff.names, matr_diff.make_systematic_matrix())

            # compare floats as == to control changes in results on refactoring
            self.assertEqual(expected_corr, actual_corr)
