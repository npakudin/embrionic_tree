from unittest import TestCase

from scipy.cluster import hierarchy
from src.cluster_trees.find_similar_branches import find_similar_branches
import scipy.spatial.distance as ssd

from src.multiple_trees.trees_matrix import to_full_matrix


def tree_to_matr(t):
    return []


def tree_to_clustering(t):
    experiment_matrix = tree_to_matr(t)
    plot_matrix = to_full_matrix(experiment_matrix)
    # convert the redundant n*n square matrix form into a condensed nC2 array
    # dist_array[{n choose 2}-{n-i choose 2} + (j-i-1)] is the distance between points i and j
    dist_array = ssd.squareform(plot_matrix)

    cluster_algorithm = "average"
    clustered_items = hierarchy.linkage(dist_array, cluster_algorithm)

    return clustered_items


def trees_to_clustering(trees):
    return [tree_to_clustering(i) for i in trees]


class TestClustering(TestCase):
    def setUp(self):
        self.t1 = ((0, 1), (2, 3))
        self.t2 = (((0, 1), 2), 3)
        self.t3 = (((0, 2), 1), 3)

    def test_corr_clustered_trees_1(self):
        clusterings = trees_to_clustering([self.t1, self.t2])

        actual_branches = find_similar_branches(clusterings)

        # (branch, similarity)
        expected_branches = [
            ([0,1], 1.0), # [0,1] are in both
            ([0,1,2,3], 1.0), # full list is always presented
            ([2,3], 0.5), # 0.5 - intersection / union
            # other aren't presented, because ((0,1),2) intersect (0,1) formally gives ([0,1], 0.6667)
            # but they will be absorbed by ([0,1], 1.0) of (0,1) intersect (0,1)
            # equal intersection [0,1], but similarity is greater 1.0 > 0.6667
            ]

        self.assertEqual(expected_branches, actual_branches)

    def test_corr_clustered_trees_2(self):
        clusterings = trees_to_clustering([self.t2, self.t3])

        actual_branches = find_similar_branches(clusterings)

        # (branch, similarity)
        expected_branches = [
            ([0,1,2], 1.0), # are always in the same tree
            ([0,1,2,3], 1.0), # full list is always presented
            # no other intersections
            ]

        self.assertEqual(expected_branches, actual_branches)

    def test_corr_clustered_trees_3(self):
        clusterings = trees_to_clustering([self.t1, self.t2, self.t3])

        actual_branches = find_similar_branches(clusterings)

        # (branch, similarity)
        expected_branches = [
            ([0,1,2,3], 1.0), # full list is always presented
            ([0,1,2], 0.75), # similar(t2,t2) = 1.0, but similar(t1, (t2,t2)) = similar(t2,t3) * intersect / union = 1.0 * 3 / 4
            # no other intersections
            ]

        self.assertEqual(expected_branches, actual_branches)
