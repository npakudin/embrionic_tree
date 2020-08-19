from unittest import TestCase

from src.compare_trees.development_tree import TreeNode
from src.diff_with_systematic.iterate_trees import generate_bin_tree, get_chain, get_deepest_node, get_address
from src.diff_with_systematic.iterate_trees import number_by_address


class TestUtils(TestCase):
    def test_get_chain(self):
        self.assertEqual(None, get_deepest_node(get_chain(0)))
        self.assertEqual("Z", get_deepest_node(get_chain(1)).address)

        self.assertEqual("Z.L", get_deepest_node(get_chain(2)).address)
        self.assertEqual("Z.R", get_deepest_node(get_chain(3)).address)

        self.assertEqual("Z.L.L", get_deepest_node(get_chain(4)).address)
        self.assertEqual("Z.L.R", get_deepest_node(get_chain(5)).address)
        self.assertEqual("Z.R.L", get_deepest_node(get_chain(6)).address)
        self.assertEqual("Z.R.R", get_deepest_node(get_chain(7)).address)

        for i in range(1, 16):
            expected_address = get_address(i)
            actual_chain = get_chain(i)
            actual_address = get_deepest_node(actual_chain).address
            self.assertEqual(expected_address, actual_address)

    def test_number_of_node_full_bin_tree(self):
        max_level = 4
        node = generate_bin_tree(max_level)
        self.assertEqual([1, 1], number_by_address(node, "Z"))

        self.assertEqual([2, 1], number_by_address(node, "Z.L"))
        self.assertEqual([2, 2], number_by_address(node, "Z.R"))

        self.assertEqual([3, 1], number_by_address(node, "Z.L.L"))
        self.assertEqual([3, 2], number_by_address(node, "Z.L.R"))
        self.assertEqual([3, 3], number_by_address(node, "Z.R.L"))
        self.assertEqual([3, 4], number_by_address(node, "Z.R.R"))

        self.assertEqual([4, 1], number_by_address(node, "Z.L.L.L"))
        self.assertEqual([4, 2], number_by_address(node, "Z.L.L.R"))
        self.assertEqual([4, 3], number_by_address(node, "Z.L.R.L"))
        self.assertEqual([4, 4], number_by_address(node, "Z.L.R.R"))
        self.assertEqual([4, 5], number_by_address(node, "Z.R.L.L"))
        self.assertEqual([4, 6], number_by_address(node, "Z.R.L.R"))
        self.assertEqual([4, 7], number_by_address(node, "Z.R.R.L"))
        self.assertEqual([4, 8], number_by_address(node, "Z.R.R.R"))

    def test_number_of_node_full_random_tree(self):
        node = TreeNode(reduced_level=0, address="Z")

        node.left = TreeNode(reduced_level=1, address="Z.L")
        node.left.left = TreeNode(reduced_level=2, address="Z.L.L")
        node.left.left.left = TreeNode(reduced_level=3, address="Z.L.L.L")
        node.left.left.right = TreeNode(reduced_level=3, address="Z.L.L.R")

        node.right = TreeNode(reduced_level=1, address="Z.R")
        node.right.left = TreeNode(reduced_level=2, address="Z.R.L")
        node.right.left.left = TreeNode(reduced_level=3, address="Z.R.L.L")
        node.right.left.right = TreeNode(reduced_level=3, address="Z.R.L.R")

        self.assertEqual([1, 1], number_by_address(node, "Z"))

        self.assertEqual([2, 1], number_by_address(node, "Z.L"))
        self.assertEqual([2, 2], number_by_address(node, "Z.R"))

        self.assertEqual([3, 1], number_by_address(node, "Z.L.L"))
        self.assertEqual([3, None], number_by_address(node, "Z.L.R"))
        self.assertEqual([3, 2], number_by_address(node, "Z.R.L"))
        self.assertEqual([3, None], number_by_address(node, "Z.R.R"))

        self.assertEqual([4, 1], number_by_address(node, "Z.L.L.L"))
        self.assertEqual([4, 2], number_by_address(node, "Z.L.L.R"))
        self.assertEqual([4, None], number_by_address(node, "Z.L.R.L"))
        self.assertEqual([4, None], number_by_address(node, "Z.L.R.R"))
        self.assertEqual([4, 3], number_by_address(node, "Z.R.L.L"))
        self.assertEqual([4, 4], number_by_address(node, "Z.R.L.R"))
        self.assertEqual([4, None], number_by_address(node, "Z.R.R.L"))
        self.assertEqual([4, None], number_by_address(node, "Z.R.R.R"))
