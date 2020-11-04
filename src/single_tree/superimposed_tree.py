from src.single_tree.development_tree import Axis, NONE_NODE, dist_div, INFINITE_PATTERN


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

        self.number_on_level = None
        self.leaves_number = None
        self.leftest_leave_number = None

    def __str__(self):
        return f"{self.n1} - {self.n2}"

    def get_reduced_level(self):
        return self.n2.reduced_level if (self.n1.is_none()) else self.n1.reduced_level

    # Calculates distance between nodes n1 and n2
    def node_dist(self, global_params):
        raw_distance = global_params.division_weight * self.dist_division() + \
                       global_params.g_weight * self.dist_gr() + \
                       global_params.chain_length_weight * self.dist_chain_length()

        # get weight from level
        reduced_level = self.get_reduced_level()
        weight = pow(global_params.param_a, reduced_level)

        # increase subtree weight
        if raw_distance > global_params.subtree_threshold:
            # print(f"subtree_raw_distance: {'%0.2f' % raw_distance} n1: {addr(n1, 'full_addr_1')}
            #   n2: {addr(n2, 'full_addr_2')}")
            weight *= global_params.subtree_multiplier

        # increase some levels weight
        weight *= global_params.level_weight_multiplier[reduced_level]

        return raw_distance * weight

    def dist_division(self):
        return dist_div(self.n1.axis, self.n2.axis)

    def dist_gr(self):
        g1 = 1 if (self.n1.is_none()) or (self.n1.growth is None) else self.n1.growth
        g2 = 1 if (self.n2.is_none()) or (self.n2.growth is None) else self.n2.growth

        return abs(g1 - g2)

    def dist_chain_length(self):
        chain_length1 = 1 if (self.n1.is_none()) else self.n1.chain_length
        chain_length2 = 1 if (self.n2.is_none()) else self.n2.chain_length

        return abs(chain_length1 - chain_length2)

    def dist_leaves_number(self):
        if self.n1 is None:
            print("n1 is None")

        leaves1 = self.n1.leaves_number
        leaves2 = self.n2.leaves_number
        return abs(leaves2 - leaves1)

    def calculate_leaves_number(self, start_numbers):
        if self.is_none():
            self.leaves_number = 0  # it's already 0
            return

        # calculate for all descendants
        # important to start 1t left, and then right
        self.left.calculate_leaves_number(start_numbers)
        self.right.calculate_leaves_number(start_numbers)

        start_numbers[self.get_reduced_level()] += 1
        self.number_on_level = start_numbers[self.get_reduced_level()]

        [n1, n2] = self.ordered_nodes()
        if n1.axis == Axis.LEAVE and (n2.axis == Axis.LEAVE or n2.is_none()):
            self.leaves_number = 1
            self.leftest_leave_number = self.number_on_level
        else:
            self.leaves_number = self.left.leaves_number + self.right.leaves_number
            self.leftest_leave_number = self.left.leftest_leave_number

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

    def full_distance(self, global_params, pattern=INFINITE_PATTERN):
        if pattern.is_none():
            return 0

        if (self.n1.is_none()) and (self.n2.is_none()):
            return 0

        res = self.node_dist(global_params)

        # swap left2 and right2 if reverse order fit better than direct order
        if global_params.is_swap_left_right:
            left1 = self.n1.left
            right1 = self.n1.right
            left2 = self.n2.left
            right2 = self.n2.right

            if all(not x.is_none() for x in [left1, left2, right1, right2]):
                direct_order_fertility = min(left1.fertility, left2.fertility) + min(right1.fertility, right2.fertility)
                reverse_order_fertility = min(left1.fertility, right2.fertility) + min(right1.fertility,
                                                                                       left2.fertility)
                # DOESN'T WORK HERE
                if reverse_order_fertility > direct_order_fertility:
                    # # swap
                    # tmp = left2
                    # left2 = right2
                    # right2 = tmp
                    print(f"swap {direct_order_fertility} {reverse_order_fertility} {self.n1.reduced_level}"
                          f"{self.n2.reduced_level} {self.n1.address} {self.n2.address} {self.n1.axis} {self.n2.axis}")

        res += self.left.full_distance(global_params, pattern.left)
        res += self.right.full_distance(global_params, pattern.right)

        return res

    def high_fertility_distance(self, pattern=INFINITE_PATTERN):
        if pattern.is_none():
            return []

        if (self.n1.is_none()) or (self.n2.is_none()):  # note: OR here, not AND
            return []

        if (self.n1.axis != self.n2.axis) and (self.n1.axis != Axis.LEAVE) and (self.n2.axis != Axis.LEAVE):
            return []

        if not self.n1.is_none() and not self.n2.is_none():
            assert self.n1.reduced_address == self.n2.reduced_address,\
                f"{self.n1.reduced_address} - {self.n2.reduced_address}"
        reduced_level = self.get_reduced_level()
        reduced_address = self.n2.reduced_address if (self.n1.is_none()) else self.n1.reduced_address
        dist_fertility = self.dist_leaves_number()

        res = [[reduced_address, dist_fertility, reduced_level, self.n1, self.n2]]

        res += self.left.high_fertility_distance(pattern.left)
        res += self.right.high_fertility_distance(pattern.right)
        return res


NONE_SUPERIMPOSED_NODE = SuperimposedNode(NONE_NODE, NONE_NODE, is_first_none=True)
NONE_SUPERIMPOSED_NODE.left = NONE_SUPERIMPOSED_NODE
NONE_SUPERIMPOSED_NODE.right = NONE_SUPERIMPOSED_NODE
NONE_SUPERIMPOSED_NODE.leaves_number = 0
NONE_SUPERIMPOSED_NODE.leftest_leave_number = 0
