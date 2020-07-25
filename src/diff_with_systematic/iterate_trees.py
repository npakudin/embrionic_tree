import copy

from src.compare_trees.development_tree import Axis, TreeNode


def get_subtrees(node):
    yield None # no node
    if node is not None:
        left_nodes = [x for x in get_subtrees(node.left)]
        right_nodes = [x for x in get_subtrees(node.right)]
        for left_node in left_nodes:
            for right_node in right_nodes:
                copy_node = copy.copy(node)
                copy_node.left = left_node
                copy_node.right = right_node
                if copy_node.left is None and copy_node.right is None:
                    copy_node.axis = Axis.NONE
                yield copy_node


def generate_bin_tree(max_level):
    if max_level == 0:
        return None

    node = TreeNode()
    node.left = generate_bin_tree(max_level - 1)
    node.right = generate_bin_tree(max_level - 1)
    return node


for level in range(6):
    root = generate_bin_tree(level)
    #print(f"root: {'()' if root is None else root.full_tree_str()}")
    count = 0
    for subtree in get_subtrees(root):
        #print(f"{'()' if subtree is None else subtree.full_tree_str()}")
        count += 1

    print(f"level: {level}, count: {count}")


#
#
# systematic_tree = "morph"
# cluster_algorithm = "average"
# max_level = 11
#
# matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
#                       ["Angiosperms"], max_level=max_level)
#
