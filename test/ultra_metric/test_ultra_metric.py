from unittest import TestCase
from src.ultra_metric.ultra_metric import get_ultra_metric, UltraMetricParams


class TestUltraMetric(TestCase):
    def test_ultrametrize_already_ultrametric(self):
        # Ultrametrize and set to 2 levels already ultrametric from tree below
        # 0  1     2  3
        #  \/ d=1   \/ d=3
        #  01       23
        #     \    / d=8
        #      0123
        src_matr = [
            [0, 1, 8, 8],
            [1, 0, 8, 8],
            [8, 8, 0, 3],
            [8, 8, 3, 0],
        ]
        expected_matr = [
            [0, 1, 2, 2],
            [1, 0, 2, 2],
            [2, 2, 0, 1],
            [2, 2, 1, 0],
        ]
        res = get_ultra_metric(src_matr, UltraMetricParams(max_level=2))
        self.assertEqual(expected_matr, res)

    def test_ultrametrize_to_top_level(self):
        # Ultrametrize and set to 2 levels already ultrametric from tree below
        # 0  1     2  3
        #  \/ d=1   \/ d=4.6 (here the difference, d=4.6, it will be 2nd level)
        #  01       23
        #     \    / d=8
        #      0123
        src_matr = [
            [0, 1, 8, 8],
            [1, 0, 8, 8],
            [8, 8, 0, 4.6],  # here the difference - 4.6
            [8, 8, 4.6, 0],  # here the difference - 4.6
        ]
        expected_matr = [
            [0, 1, 2, 2],
            [1, 0, 2, 2],
            [2, 2, 0, 2],
            [2, 2, 2, 0],
        ]
        res = get_ultra_metric(src_matr, UltraMetricParams(max_level=2))
        self.assertEqual(expected_matr, res)

    def test_ultrametrize_non_ultrametric(self):
        # get matrix from sample 1 (test_ultrametrize_already_ultrametric)
        # but some distances aren't ultrametric
        src_matr = [
            [0, 1, 7, 8],  # here the difference: 7
            [1, 0, 8, 8],
            [7, 8, 0, 3],  # here the difference: 7
            [8, 8, 3, 0],
        ]
        expected_matr = [
            [0, 1, 2, 2],
            [1, 0, 2, 2],
            [2, 2, 0, 1],
            [2, 2, 1, 0],
        ]
        res = get_ultra_metric(src_matr, UltraMetricParams(max_level=2))
        self.assertEqual(expected_matr, res)

    def test_ultrametrize_with_empty_levels(self):
        # Ultrametrize and set to 2 levels already ultrametric from tree below
        # 0  1     2  3
        #  \/ d=1   \/ d=3
        #  01       23
        #     \    / d=8
        #      0123
        src_matr = [
            [0, 1, 8, 8],
            [1, 0, 8, 8],
            [8, 8, 0, 3],
            [8, 8, 3, 0],
        ]
        expected_matr = src_matr
        res = get_ultra_metric(src_matr, UltraMetricParams(max_level=8))
        self.assertEqual(expected_matr, res)

