from unittest import TestCase

from src.single_tree.development_tree import TreeNode, NONE_NODE, Axis
from src.multiple_trees.iterate_trees import generate_bin_tree, get_chain, get_deepest_node, get_address
from src.multiple_trees.iterate_trees import number_by_address


class TestUtils(TestCase):
    def test_get_chain(self):
        self.assertEqual("unknown", get_deepest_node(get_chain(0)).address)
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
        self.assertEqual(1, number_by_address(node, node, "Z", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.L.R", is_reducing=True))
        self.assertEqual(3, number_by_address(node, node, "Z.R.L", is_reducing=True))
        self.assertEqual(4, number_by_address(node, node, "Z.R.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L.L.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.L.L.R", is_reducing=True))
        self.assertEqual(3, number_by_address(node, node, "Z.L.R.L", is_reducing=True))
        self.assertEqual(4, number_by_address(node, node, "Z.L.R.R", is_reducing=True))
        self.assertEqual(5, number_by_address(node, node, "Z.R.L.L", is_reducing=True))
        self.assertEqual(6, number_by_address(node, node, "Z.R.L.R", is_reducing=True))
        self.assertEqual(7, number_by_address(node, node, "Z.R.R.L", is_reducing=True))
        self.assertEqual(8, number_by_address(node, node, "Z.R.R.R", is_reducing=True))

    def test_number_of_node_full_random_tree(self):
        node = TreeNode(reduced_level=0, address="Z", reduced_address="Z", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node.left = TreeNode(reduced_level=1, address="Z.L", reduced_address="Z.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.left.left = TreeNode(reduced_level=2, address="Z.L.L", reduced_address="Z.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.left.left.left = TreeNode(reduced_level=3, address="Z.L.L.L", reduced_address="Z.L.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.left.left.right = TreeNode(reduced_level=3, address="Z.L.L.R", reduced_address="Z.L.L.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node.right = TreeNode(reduced_level=1, address="Z.R", reduced_address="Z.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.right.left = TreeNode(reduced_level=2, address="Z.R.L", reduced_address="Z.R.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.right.left.left = TreeNode(reduced_level=3, address="Z.R.L.L", reduced_address="Z.R.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node.right.left.right = TreeNode(reduced_level=3, address="Z.R.L.R", reduced_address="Z.R.L.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        self.assertEqual(1, number_by_address(node, node, "Z", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.L.R", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.R.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.R.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node, node, "Z.L.L.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node, node, "Z.L.L.R", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.L.R.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.L.R.R", is_reducing=True))
        self.assertEqual(3, number_by_address(node, node, "Z.R.L.L", is_reducing=True))
        self.assertEqual(4, number_by_address(node, node, "Z.R.L.R", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.R.R.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node, node, "Z.R.R.R", is_reducing=True))

    def test_number_of_node_two_trees(self):
        # node1
        node1 = TreeNode(reduced_level=0, address="Z", reduced_address="Z", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node1.left = TreeNode(reduced_level=1, address="Z.L", reduced_address="Z.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.left.left = TreeNode(reduced_level=2, address="Z.L.L", reduced_address="Z.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.left.left.left = TreeNode(reduced_level=3, address="Z.L.L.L", reduced_address="Z.L.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.left.left.right = TreeNode(reduced_level=3, address="Z.L.L.R", reduced_address="Z.L.L.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node1.right = TreeNode(reduced_level=1, address="Z.R", reduced_address="Z.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.right.left = TreeNode(reduced_level=2, address="Z.R.L", reduced_address="Z.R.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.right.left.left = TreeNode(reduced_level=3, address="Z.R.L.L", reduced_address="Z.R.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node1.right.left.right = TreeNode(reduced_level=3, address="Z.R.L.R", reduced_address="Z.R.L.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        # node2
        node2 = TreeNode(reduced_level=0, address="Z", reduced_address="Z", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node2.left = TreeNode(reduced_level=1, address="Z.L", reduced_address="Z.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node2.left.left = TreeNode(reduced_level=2, address="Z.L.L", reduced_address="Z.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node2.left.left.left = TreeNode(reduced_level=3, address="Z.L.L.L", reduced_address="Z.L.L.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        node2.right = TreeNode(reduced_level=1, address="Z.R", reduced_address="Z.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node2.right.right = TreeNode(reduced_level=2, address="Z.R.R", reduced_address="Z.R.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node2.right.right.left = TreeNode(reduced_level=3, address="Z.R.R.L", reduced_address="Z.R.R.L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
        node2.right.right.right = TreeNode(reduced_level=3, address="Z.R.R.R", reduced_address="Z.R.R.R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)

        # assert
        self.assertEqual(1, number_by_address(node1, node2, "Z", is_reducing=True))

        self.assertEqual(1, number_by_address(node1, node2, "Z.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node1, node2, "Z.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node1, node2, "Z.L.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node1, node2, "Z.L.R", is_reducing=True))
        self.assertEqual(2, number_by_address(node1, node2, "Z.R.L", is_reducing=True))
        self.assertEqual(3, number_by_address(node1, node2, "Z.R.R", is_reducing=True))

        self.assertEqual(1, number_by_address(node1, node2, "Z.L.L.L", is_reducing=True))
        self.assertEqual(2, number_by_address(node1, node2, "Z.L.L.R", is_reducing=True))
        self.assertEqual(None, number_by_address(node1, node2, "Z.L.R.L", is_reducing=True))
        self.assertEqual(None, number_by_address(node1, node2, "Z.L.R.R", is_reducing=True))
        self.assertEqual(3, number_by_address(node1, node2, "Z.R.L.L", is_reducing=True))
        self.assertEqual(4, number_by_address(node1, node2, "Z.R.L.R", is_reducing=True))
        self.assertEqual(5, number_by_address(node1, node2, "Z.R.R.L", is_reducing=True))
        self.assertEqual(6, number_by_address(node1, node2, "Z.R.R.R", is_reducing=True))
