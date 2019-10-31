def development_tree_distance(node1, node2, global_params):
    def dist(n1, n2):
        assert not (n1 is None and n2 is None)

        # dcl = dist_chain_length(n1, n2)
        # global_params.total_dist += 1
        # if dcl > 0:
        #     global_params.dcl_more_zero += 1

        return 1 * dist_br_dir(n1, n2) +\
            global_params.g_weight * dist_gr(n1, n2) + \
            global_params.chain_length_weight * dist_chain_length(n1, n2)

    def dist_br_dir(n1, n2):
        none = 'zNone'

        axis1 = none if (n1 is None) else n1.axis
        axis2 = none if (n2 is None) else n2.axis

        (axis1, axis2) = sorted((axis1, axis2))
        # L < d < x < y < z < zNone

        weight = n2.personal_weight if (n1 is None) else n1.personal_weight

        if axis1 == axis2:
            return 0 * weight
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
            if axis2 == none:
                return 1 * weight
            if axis1 == 'L':
                if axis2 == 'z':
                    return 1 * weight
                return 0.5 * weight
            if axis1 == 'd':
                if axis2 == 'z':
                    return 1 * weight
                return 0.5 * weight
            return 1 * weight

    def dist_gr(n1, n2):
        g1 = 0 if (n1 is None) or (n1.growth is None) else n1.growth - 1
        g2 = 0 if (n2 is None) or (n2.growth is None) else n2.growth - 1

        weight = n2.personal_weight if (n1 is None) else n1.personal_weight

        return abs(g1 - g2) * weight

    def dist_chain_length(n1, n2):
        # if any(x is None for x in [n1, n2]):
        #     pass

        chain_length1 = 1 if (n1 is None) or (n1.chain_length is None) else n1.chain_length
        chain_length2 = 1 if (n2 is None) or (n2.chain_length is None) else n2.chain_length

        # if chain_length1 != chain_length2:
        #     print(f"chain_length: {chain_length1} {chain_length2}")
        #     if n1 is not None and n2 is not None:
        #         print(f"    {n1.name} {n2.name}")

        weight = n2.personal_weight if (n1 is None) else n1.personal_weight

        return abs(chain_length1 - chain_length2) * weight

    return visit_virtual(dist, node1, node2, global_params)


def visit_virtual(fun, node1, node2, global_params):
    res = fun(node1, node2)

    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    # swap left2 and right2 if reverse order fit better than direct order
    if global_params.is_swap_left_right:
        if all(x is not None for x in [left1, left2, right1, right2]):
            direct_order_fertility = min(left1.fertility, left2.fertility) + min(right1.fertility, right2.fertility)
            reverse_order_fertility = min(left1.fertility, right2.fertility) + min(right1.fertility, left2.fertility)
            global_params.total += 1
            if reverse_order_fertility > direct_order_fertility:
                # swap
                tmp = left2
                left2 = right2
                right2 = tmp
                global_params.swaps += 1
                #print(f"swap {direct_order_fertility} {reverse_order_fertility} {node1.level} {node2.level} {node1.name} {node2.name} {node1.address} {node2.address} {node1.axis} {node2.axis}")

    if (left1 is not None) or (left2 is not None):
        res += visit_virtual(fun, left1, left2, global_params)
    if (right1 is not None) or (right2 is not None):
        res += visit_virtual(fun, right1, right2, global_params)
    return res
