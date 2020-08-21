import copy

from src.compare_trees.development_tree import Axis, TreeNode


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
        return None
    root = TreeNode(address="Z")

    # iterate over bits from the highest to the 0th
    cur_node = root
    cur_mask = hi_bit(number) >> 1
    while cur_mask > 0:
        if cur_mask & number == 0:
            cur_node.left = TreeNode(address=cur_node.address + ".L")
            cur_node = cur_node.left
        else:
            cur_node.right = TreeNode(address=cur_node.address + ".R")
            cur_node = cur_node.right
        cur_mask >>= 1
    return root


# Iterates over all subtrees of the binary tree 'node'
def get_subtrees(node):
    yield None  # no node
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


# Generates a full bin tree of height 'max_level'
def generate_bin_tree(max_level, address="Z", reduced_level=0):
    if max_level == 0:
        return None

    node = TreeNode(address=address, reduced_address=address, reduced_level=reduced_level)
    node.left = generate_bin_tree(max_level - 1, address + ".L", reduced_level + 1)
    node.right = generate_bin_tree(max_level - 1, address + ".R", reduced_level + 1)
    return node


def get_deepest_node(node):
    if node is None:
        return node

    if node.left is not None:
        return get_deepest_node(node.left)

    if node.right is not None:
        return get_deepest_node(node.right)

    return node


def iterate_nodes(node):
    if node.left is not None:
        for x in iterate_nodes(node.left):
            yield x
    yield node
    if node.right is not None:
        for x in iterate_nodes(node.right):
            yield x


# Returns number of the node at the level
# left to right direction
#
# root - the root of the tree
# address - address of the node
# is_reduced - True to use reduced tree attributes, False to use "raw" tree attributes
def number_by_address(root, address, is_reducing):
    level = int(len(address) / 2)

    nodes_at_level = [x for x in filter(lambda x: x.reduced_level == level if is_reducing else x.src_level == level,
                                        iterate_nodes(root))]
    for i, item in enumerate(nodes_at_level):
        if is_reducing:
            if item.reduced_address == address:
                return i + 1
        else:
            if item.address == address:
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
