from unittest import TestCase

from src.multiple_trees.iterate_trees import generate_bin_tree
from src.single_tree.development_tree_reader import read_all_trees
from src.single_tree.development_tree_utils import calculate_number_on_level_2_trees


class TestDistance(TestCase):
    def test_calculate_number_on_level_2_trees_full_bin_trees(self):
        max_level = 3
        node1 = generate_bin_tree(max_level)
        node2 = generate_bin_tree(max_level)

        start_numbers = [1] * max_level
        calculate_number_on_level_2_trees(node1, node2, start_numbers)

        self.assertEqual(1, node1.number_on_level)
        self.assertEqual(1, node2.number_on_level)

        self.assertEqual(1, node1.left.number_on_level)
        self.assertEqual(1, node2.left.number_on_level)
        self.assertEqual(2, node1.right.number_on_level)
        self.assertEqual(2, node2.right.number_on_level)

        self.assertEqual(1, node1.left.left.number_on_level)
        self.assertEqual(1, node2.left.left.number_on_level)
        self.assertEqual(2, node1.left.right.number_on_level)
        self.assertEqual(2, node2.left.right.number_on_level)
        self.assertEqual(3, node1.right.left.number_on_level)
        self.assertEqual(3, node2.right.left.number_on_level)
        self.assertEqual(4, node1.right.right.number_on_level)
        self.assertEqual(4, node2.right.right.number_on_level)

    def test_calculate_number_on_level_2_trees_common_trees(self):
        is_reducing = False
        trees = read_all_trees(pattern="../../test/test_input/development_tree_utils/*.xtg")

        # prepare to calculate distances
        for tree in trees:
            if is_reducing:
                tree.reduce()
            tree.prepare()

        node1 = trees[0].root
        node2 = trees[1].root

        start_numbers = [1] * 3
        calculate_number_on_level_2_trees(node1, node2, start_numbers)

        self.assertEqual(1, node1.number_on_level)
        self.assertEqual(1, node2.number_on_level)

        self.assertEqual(1, node1.left.number_on_level)
        self.assertEqual(1, node2.left.number_on_level)
        self.assertEqual(2, node1.right.number_on_level)
        self.assertEqual(2, node2.right.number_on_level)

        self.assertEqual(1, node1.left.left.number_on_level)
        self.assertEqual(1, node2.left.left.number_on_level)
        self.assertTrue(node1.left.right.is_none())
        self.assertEqual(2, node2.left.right.number_on_level)
        self.assertEqual(3, node1.right.left.number_on_level)
        self.assertEqual(3, node2.right.left.number_on_level)
        self.assertTrue(node1.right.right.is_none())
        self.assertTrue(node2.right.right.is_none())
