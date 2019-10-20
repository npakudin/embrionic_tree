def dist_branch_direction(node1, node2, global_params):
    def dist(n1, n2):
        assert not (n1 is None and n2 is None)
        return global_params.param_g_weight * dist_gr(n1, n2) + dist_br_dir(n1, n2)

    def dist_br_dir(n1, n2):
        none = 'zNone'

        axis1 = none if (n1 is None) else n1.axis
        axis2 = none if (n2 is None) else n2.axis

        (axis1, axis2) = sorted((axis1, axis2))
        # L < d < x < y < z < zNone

        weight = n2.weight if (n1 is None) else n1.weight

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
                if axis2 == 'd':
                    return 0.6 * weight
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

        weight = n2.weight if (n1 is None) else n1.weight

        return abs(g1 - g2) * weight

    # TODO: n1.timer_length - count of items in the chain
    def dist_timer(n1, n2):
        timer_length1 = 0 if (n1 is None) or (n1.timer_length is None) else n1.timer_length - 1
        timer_length2 = 0 if (n2 is None) or (n2.timer_length is None) else n2.timer_length - 1

        weight = n2.weight if (n1 is None) else n1.weight

        return abs(timer_length1 - timer_length2) * weight

    return visit_virtual(dist, node1, node2, global_params)


def visit_virtual(fun, node1, node2, global_params):
    res = fun(node1, node2)
    left1 = None if (node1 is None) else node1.left
    right1 = None if (node1 is None) else node1.right
    left2 = None if (node2 is None) else node2.left
    right2 = None if (node2 is None) else node2.right

    # swap left2 and right2 if they fit better than direct order
    if global_params.change_left_right:
        if all(x is not None for x in [left1, left2, right1, right2]):
            direct_order_fertility = min(left1.fertility, left2.fertility) + min(right1.fertility, right2.fertility)
            reverse_order_fertility = min(left1.fertility, right2.fertility) + min(right1.fertility, left2.fertility)
            if reverse_order_fertility > direct_order_fertility:
                tmp = left2
                left2 = right2
                right2 = tmp


    if (left1 is not None) or (left2 is not None):
        res += visit_virtual(fun, left1, left2)
    if (right1 is not None) or (right2 is not None):
        res += visit_virtual(fun, right1, right2)
    return res
