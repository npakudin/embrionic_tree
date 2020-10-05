import copy

from src.single_tree.development_tree import Axis, TreeNode, NONE_NODE


# Returns the number with the highest bit only
# 0 -> 0
# 1 -> 1
# 2 -> 2
# 3 -> 2
# ...
# 255 -> 128
# 256 -> 256
# ...
def hi_bit(n):
    n |= (n >> 1)
    n |= (n >> 2)
    n |= (n >> 4)
    n |= (n >> 8)
    n |= (n >> 16)
    n |= (n >> 32)
    return n - (n >> 1)


# Iterates over all chains of the full binary tree of the height 'max_level'
def get_address(number):
    if number == 0:
        return ""
    res = "Z"
    cur_mask = hi_bit(number) >> 1
    while cur_mask > 0:
        res += (".L" if cur_mask & number == 0 else ".R")
        cur_mask >>= 1
    return res


# Returns a chain in the infinite full binary tree by number
# Each chain the infinite full binary tree has a unique number
# (There is a bijection between numbers 0..inf and chains)
def get_chain(number):
    if number == 0:
        return NONE_NODE
    root = TreeNode(address="Z", axis=Axis.X)
    root.left = NONE_NODE
    root.right = NONE_NODE

    # iterate over bits from the highest to the 0th
    cur_node = root
    cur_mask = hi_bit(number) >> 1
    while cur_mask > 0:
        if cur_mask & number == 0:
            cur_node.left = TreeNode(address=cur_node.address + ".L", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
            cur_node = cur_node.left
        else:
            cur_node.right = TreeNode(address=cur_node.address + ".R", axis=Axis.X, left=NONE_NODE, right=NONE_NODE)
            cur_node = cur_node.right
        cur_mask >>= 1
    return root


# Iterates over all subtrees of the binary tree 'node'
def get_subtrees(node):
    yield NONE_NODE  # no node
    if not node.is_none():
        left_nodes = [x for x in get_subtrees(node.left)]
        right_nodes = [x for x in get_subtrees(node.right)]
        for left_node in left_nodes:
            for right_node in right_nodes:
                copy_node = copy.copy(node)
                copy_node.left = left_node
                copy_node.right = right_node
                if copy_node.left.is_none() and copy_node.right.is_none():
                    copy_node.axis = Axis.NONE
                yield copy_node


# Generates a full bin tree of height 'max_level'
def generate_bin_tree(max_level, address="Z", reduced_level=0):
    if max_level == 0:
        return NONE_NODE

    node = TreeNode(axis=Axis.X, address=address, reduced_address=address, reduced_level=reduced_level, left=NONE_NODE, right=NONE_NODE)
    node.left = generate_bin_tree(max_level - 1, address + ".L", reduced_level + 1)
    node.right = generate_bin_tree(max_level - 1, address + ".R", reduced_level + 1)
    return node


def get_deepest_node(node):
    if node.is_none():
        return node

    if not node.left.is_none():
        return get_deepest_node(node.left)

    if not node.right.is_none():
        return get_deepest_node(node.right)

    return node


def iterate_nodes(node1, node2):
    if not (node1.left.is_none() and node2.left.is_none()):
        for x in iterate_nodes(node1.left, node2.left):
            yield x
    yield [node1, node2]
    if not (node1.right.is_none() and node2.right.is_none()):
        for x in iterate_nodes(node1.right, node2.right):
            yield x


# Returns number of the node at the level
# left to right direction
#
# root - the root of the tree
# address - address of the node
# is_reduced - True to use reduced tree attributes, False to use "raw" tree attributes
def number_by_address(root1, root2, address, is_reducing):
    level = int(len(address) / 2)

    nodes_at_level = [x for x in filter(lambda x: (x[0].reduced_level == level and not x[0].is_none()) or (x[1].reduced_level == level and not x[1].is_none()),
                                        iterate_nodes(root1, root2))]

    for i, [item1, item2] in enumerate(nodes_at_level):
        if (item1.reduced_address == address and not item1.is_none()) or (item2.reduced_address == address and not item2.is_none()):
            return i + 1
    return None  # not found

# for i in range(16):
#     subtree = get_chain(i)
#     print(f"{i} - {get_address(i)} - {'()' if subtree is None else get_deepest_node(subtree)}")


# for level in range(6):
#     root = generate_bin_tree(level)
#     #print(f"root: {'()' if root is None else root.full_tree_str()}")
#     count = 0
#     for subtree in get_subtrees(root):
#         #print(f"{'()' if subtree is None else subtree.full_tree_str()}")
#         count += 1
#
#     print(f"level: {level}, count: {count}")
