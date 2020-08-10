from src.compare_trees.development_tree import get_axis, Axis, TreeNode


def addr(node, reduced_addr):
    if node is None:
        return f"reduced_addr {reduced_addr}"
    return node.get_full_addr()


def node_dist(n1, n2, full_addr_1, full_addr_2, global_params):
    assert not (n1 is None and n2 is None)

    raw_distance = global_params.fertility_weight * fertility_dist(n1, n2) + \
                   global_params.axis_weight * dist_axis(n1, n2) + \
                   global_params.g_weight * dist_gr(n1, n2) + \
                   global_params.chain_length_weight * dist_chain_length(n1, n2)

    # get weight from level
    reduced_level = n2.reduced_level if (n1 is None) else n1.reduced_level
    weight = pow(2 * global_params.param_a, reduced_level)

    # increase subtree weight
    if raw_distance > global_params.subtree_threshold:
        print(f"subtree_raw_distance: {'%0.2f' % raw_distance} n1: {addr(n1, full_addr_1)} n2: {addr(n2, full_addr_2)}")
        weight *= global_params.subtree_multiplier

    # increase some levels weight
    weight *= global_params.level_weight_multiplier[reduced_level]

    return raw_distance * weight


# distance is 1 if one of nodes exists and the 2nd does not
# don't care about axis
def fertility_dist(n1, n2):
    if n1 is None or n2 is None:
        return 1
    return 0


# distance is 0 if one of nodes is None, it's calculated in fertility_dist()
# calculate difference in axis only
def dist_axis(n1, n2):
    if n1 is None or n2 is None:
        return 0

    axis1 = get_axis(n1)
    axis2 = get_axis(n2)

    (axis1, axis2) = sorted((axis1, axis2))
    # x < d < у < z < L < N

    if axis1 == axis2:
        return 0
    else:
        # d1, d2    => 1
        # d1, None  => 1
        # d1, L     => 0.5
        # L, None   => 1
        # if (a1 == 'L' and a2 is not None) or (a2 == 'L' and a1 is not None):
        #     return 0.5 * weight  # d1, L     => 0.5
        # if (a1 == 'd' and a2 is not None) or (a2 == 'd' and a1 is not None):
        #     return 0.60 * weight  # d1, diag  => 0.60
        # return 1 * weight

        # different for leave, D, Z etc
        if axis2 == Axis.NONE:
            return 1
        if axis1 == 'L':
            if axis2 == 'z':
                return 1
            return 0.5
        if axis1 == 'd':
            if axis2 == 'z':
                return 1
            return 0.5
        return 1


def dist_gr(n1, n2):
    g1 = 0 if (n1 is None) or (n1.growth is None) else n1.growth - 1
    g2 = 0 if (n2 is None) or (n2.growth is None) else n2.growth - 1

    return abs(g1 - g2)


def dist_chain_length(n1, n2):
    chain_length1 = 1 if (n1 is None) else n1.chain_length
    chain_length2 = 1 if (n2 is None) else n2.chain_length

    return abs(chain_length1 - chain_length2)


def pattern_tree_infinite():
    root = TreeNode()
    root.left = root
    root.right = root
    return root


def iterate_pattern_tree(max_level, cur_level=0):
    yield TreeNode()


def development_tree_distance(tree1, tree2, global_params, pattern_tree=pattern_tree_infinite()):

    node1 = tree1.root
    node2 = tree2.root
    correction_coef = 1

    if global_params.use_min_common_depth:
        # get trees cut to the same level - min of both reduced trees
        min_reduced_depth = min(tree1.root.reduced_depth, tree2.root.reduced_depth)
        node1 = tree1.roots[min_reduced_depth]
        node2 = tree2.roots[min_reduced_depth]

        # sum([ (2*a) ^ i for i in ... ])
        correction_coef = sum([pow(2 * global_params.param_a, i) for i in range(min_reduced_depth)])

    raw_res = visit_virtual(node1, node2, node1.get_full_addr(), node2.get_full_addr(), global_params, pattern_tree)
    res = raw_res / correction_coef

    return res


def visit_virtual(node1, node2, full_addr_1, full_addr_2, global_params, pattern_node):
    res = node_dist(node1, node2, full_addr_1, full_addr_2, global_params)

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right
    pattern_left = None if (pattern_node is None) else pattern_node.left
    pattern_right = None if (pattern_node is None) else pattern_node.right

    if ((left1 is not None) or (left2 is not None)) and (pattern_left is not None):
        res += visit_virtual(left1, left2, full_addr_1 + ".vL" if node1 is None else node1.get_full_addr(), full_addr_2 + ".vL" if node2 is None else node2.get_full_addr(), global_params, pattern_left)
    if ((right1 is not None) or (right2 is not None)) and (pattern_right is not None):
        res += visit_virtual(right1, right2, full_addr_1 + ".vR" if node1 is None else node1.get_full_addr(), full_addr_2 + ".vR" if node2 is None else node2.get_full_addr(), global_params, pattern_right)
    return res
