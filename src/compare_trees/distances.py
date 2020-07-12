from src.compare_trees.development_tree import get_axis, Axis


def node_dist(n1, n2, full_addr_1, full_addr_2, global_params, level):
    assert not (n1 is None and n2 is None)

    raw_distance = 1 * dist_br_dir(n1, n2) + \
                   global_params.g_weight * dist_gr(n1, n2) + \
                   global_params.chain_length_weight * dist_chain_length(n1, n2)

    # get weight from level
    reduced_level = n2.reduced_level if (n1 is None) else n1.reduced_level
    src_level = n2.src_level if (n1 is None) else n1.src_level
    weight = global_params.calc_weight.fun(src_level, level)

    # increase subtree weight
    if raw_distance > global_params.subtree_threshold:
        print(
            f"subtree_raw_distance: {'%0.2f' % raw_distance} n1: {full_addr_1 if n1 is None else n1.get_full_addr()} n2: {full_addr_2 if n2 is None else n2.get_full_addr()}")
        weight *= global_params.subtree_multiplier

    # increase some levels weight
    weight *= global_params.level_weight_multiplier[reduced_level]

    return raw_distance * weight


def dist_br_dir(n1, n2):
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
    # if any(x is None for x in [n1, n2]):
    #     pass

    chain_length1 = 1 if (n1 is None) or (n1.chain_length is None) else n1.chain_length
    chain_length2 = 1 if (n2 is None) or (n2.chain_length is None) else n2.chain_length

    # if chain_length1 != chain_length2:
    #     print(f"chain_length: {chain_length1} {chain_length2}")
    #     if n1 is not None and n2 is not None:
    #         print(f"    {n1.name} {n2.name}")

    return abs(chain_length1 - chain_length2)


def development_tree_distance(tree1, tree2, global_params):

    # get trees cut to the same level - min of both reduced trees
    min_reduced_depth = min(tree1.node.reduced_depth, tree2.node.reduced_depth)
    node1 = tree1.nodes[min_reduced_depth]
    node2 = tree2.nodes[min_reduced_depth]

    # for exp_reduced_weight = sum([ (2*a) ^ i for i in ... ])
    correction_coef = sum([pow(2, i) * global_params.calc_weight.fun(i, i) for i in range(min_reduced_depth)])

    raw_res = visit_virtual(node_dist, node1, node2, node1.get_full_addr(), node2.get_full_addr(), global_params, 0)
    res = raw_res / correction_coef

    return res


def visit_virtual(fun, node1, node2, full_addr_1, full_addr_2, global_params, level):
    res = fun(node1, node2, full_addr_1, full_addr_2, global_params, level)

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right
    reduced_level = node1.reduced_level if (node2 is None) else node2.reduced_level

    # swap left2 and right2 if reverse order fit better than direct order
    if global_params.is_swap_left_right:
        raise "Not supported"
        # if all(x is not None for x in [left1, left2, right1, right2]):
        #     direct_order_fertility = min(left1.fertility, left2.fertility) + min(right1.fertility, right2.fertility)
        #     reverse_order_fertility = min(left1.fertility, right2.fertility) + min(right1.fertility, left2.fertility)
        #     global_params.total += 1
        #     if reverse_order_fertility > direct_order_fertility:
        #         # swap
        #         tmp = left2
        #         left2 = right2
        #         right2 = tmp
        #         global_params.swaps += 1
        #         #print(f"swap {direct_order_fertility} {reverse_order_fertility} {node1.level} {node2.level} {node1.name} {node2.name} {node1.address} {node2.address} {node1.axis} {node2.axis}")

    if (left1 is not None) or (left2 is not None):
        res += visit_virtual(fun, left1, left2, full_addr_1 + ".vL" if node1 is None else node1.get_full_addr(), full_addr_2 + ".vL" if node2 is None else node2.get_full_addr(), global_params, level + 1)
    if (right1 is not None) or (right2 is not None):
        #mult = 0.8 if reduced_level < 4 else 1.0
        mult = 1.0
        res += mult * visit_virtual(fun, right1, right2, full_addr_1 + ".vR" if node1 is None else node1.get_full_addr(), full_addr_2 + ".vR" if node2 is None else node2.get_full_addr(), global_params, level + 1)
    return res
