import copy

from src.single_tree.development_tree import Axis, NONE_NODE


class SuperimposedNode:
    def __init__(self, n1, n2, is_first_none=False):
        self.n1 = n1
        self.n2 = n2

        if not (n1.is_none() and n2.is_none()):
            self.left = SuperimposedNode(n1.left, n2.left)
            self.right = SuperimposedNode(n1.right, n2.right)
        else:
            if not is_first_none:
                self.left = NONE_SUPERIMPOSED_NODE
                self.right = NONE_SUPERIMPOSED_NODE

        self.leaves_number = None

    def __str__(self):
        return f"{self.n1} - {self.n2}"

    def get_reduced_level(self):
        return self.n2.reduced_level if (self.n1.is_none()) else self.n1.reduced_level

    # Calculates distance between nodes n1 and n2
    def node_dist(self, global_params):
        raw_distance = global_params.fertility_weight * self.dist_fertility() + \
                       global_params.axis_weight * self.dist_axis() + \
                       global_params.g_weight * self.dist_gr() + \
                       global_params.chain_length_weight * self.dist_chain_length()

        # get weight from level
        reduced_level = self.get_reduced_level()
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
    def dist_fertility(self):
        if self.n1.is_none() or self.n2.is_none():
            return 1
        return 0

    # distance is 0 if one of nodes is None, it's calculated in fertility_dist()
    # calculate difference in axis only
    def dist_axis(self):
        if self.n1.is_none() or self.n2.is_none():
            return 0

        axis1 = self.n1.axis
        axis2 = self.n2.axis

        (axis1, axis2) = sorted((axis1, axis2))
        # x < d < у < z < L < N < growth

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

    def dist_gr(self):
        g1 = 0 if (self.n1.is_none()) or (self.n1.growth is None) else self.n1.growth - 1
        g2 = 0 if (self.n2.is_none()) or (self.n2.growth is None) else self.n2.growth - 1

        return abs(g1 - g2)

    def dist_chain_length(self):
        chain_length1 = 1 if (self.n1.is_none()) else self.n1.chain_length
        chain_length2 = 1 if (self.n2.is_none()) else self.n2.chain_length

        return abs(chain_length1 - chain_length2)

    def dist_leaves_number(self):
        if self.n1 is None:
            print("n1 is None")

        leaves1 = self.n1.get_leaves_number()
        leaves2 = self.n2.get_leaves_number()
        return abs(leaves2 - leaves1)

    def calculate_leaves_number(self):
        if self.is_none():
            self.leaves_number = 0
        else:
            [n1, n2] = self.ordered_nodes()

            if n1 == Axis.LEAVE or n2 == Axis.LEAVE:
                self.leaves_number = 1
            else:
                leaves_left = self.left.calculate_leaves_number()
                leaves_right = self.right.calculate_leaves_number()
                self.leaves_number = leaves_left + leaves_right
        return self.leaves_number

    def ordered_nodes(self):
        n1 = self.n1
        n2 = self.n2

        # swap to guarantee that n1 is always not none
        if n1.is_none():
            tmp = n1
            n1 = n2
            n2 = tmp

        return [n1, n2]

    def is_none(self):
        return self.n1.is_none() and self.n2.is_none()


NONE_SUPERIMPOSED_NODE = SuperimposedNode(NONE_NODE, NONE_NODE, is_first_none=True)
NONE_SUPERIMPOSED_NODE.left = NONE_SUPERIMPOSED_NODE
NONE_SUPERIMPOSED_NODE.right = NONE_SUPERIMPOSED_NODE
# NONE_SUPERIMPOSED_NODE.reduced_depth = 0
# NONE_SUPERIMPOSED_NODE.leaves_number = 0
