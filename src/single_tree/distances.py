import copy

from src.single_tree.development_tree import get_axis, Axis, TreeNode


def addr(node, reduced_addr):
    if node.is_none():
        return f"reduced_addr {reduced_addr}"
    return node.get_full_addr()


# Calculates distance between nodes n1 and n2
def node_dist(n1, n2, global_params):
    assert not (n1.is_none() and n2.is_none())

    raw_distance = global_params.fertility_weight * dist_fertility(n1, n2) + \
                   global_params.division_weight * dist_division(n1, n2) + \
                   global_params.g_weight * dist_gr(n1, n2) + \
                   global_params.chain_length_weight * dist_chain_length(n1, n2)

    # get weight from level
    reduced_level = n2.reduced_level if (n1.is_none()) else n1.reduced_level
    weight = pow(global_params.param_a, reduced_level)

    # increase subtree weight
    if raw_distance > global_params.subtree_threshold:
        # print(f"subtree_raw_distance: {'%0.2f' % raw_distance} n1: {addr(n1, 'full_addr_1')} n2: {addr(n2, 'full_addr_2')}")
        weight *= global_params.subtree_multiplier

    # increase some levels weight
    weight *= global_params.level_weight_multiplier[reduced_level]

    return raw_distance * weight


# distance is 1 if one of nodes exists and the 2nd does not
# don't care about axis
def dist_fertility(n1, n2):
    if n1.is_none() or n2.is_none():
        return 1
    return 0


# distance is 0 if one of nodes is None, it's calculated in fertility_dist()
# calculate difference in axis only
def dist_division(n1, n2):
    if n1.is_none() or n2.is_none():
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
        if axis2 == Axis.GROWTH:
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
    g1 = 0 if (n1.is_none()) or (n1.growth is None) else n1.growth - 1
    g2 = 0 if (n2.is_none()) or (n2.growth is None) else n2.growth - 1

    return abs(g1 - g2)


def dist_chain_length(n1, n2):
    chain_length1 = 1 if (n1.is_none()) else n1.chain_length
    chain_length2 = 1 if (n2.is_none()) else n2.chain_length

    return abs(chain_length1 - chain_length2)


def dist_leaves_number(n1, n2):
    if n1 is None:
        print("n1 is None")

    leaves1 = n1.leaves_number
    leaves2 = n2.leaves_number
    return abs(leaves2 - leaves1)


def pattern_tree_infinite():
    root = TreeNode(axis=Axis.X)
    root.left = root
    root.right = root
    return root
