import copy


# order should be: x < d < у < z < L < N
# to provide it, use lexicographic order of: x < xd < у < z < zLeave < zzGrowth
class Axis:
    X = 'x'
    Y = 'y'
    DIAGONAL = 'yd'
    LEAVE = 'yyLeave'
    Z = 'z'
    GROWTH = 'zGrowth'
    APOPTOSIS = 'zzApoptosis'
    NONE = 'zzNone'  # for really not existing node


def dist_div(axis1, axis2):
    if axis1 == axis2:
        return 0

    (axis1, axis2) = sorted((axis1, axis2))
    # X < Y < Diagonal < Leave < Z < Growth < Apoptosis < None

    if axis2 in [Axis.Z, Axis.GROWTH, Axis.APOPTOSIS, Axis.NONE]:
        return 1
    if axis2 in [Axis.DIAGONAL, Axis.LEAVE]:
        return 0.5
    if axis2 == Axis.Y and axis1 == Axis.X:
        return 1

    assert False, f"Unhandled axes pair: {axis1}, {axis2}"


def get_axis(node):
    if node is None:
        return Axis.NONE
    return node.axis


class TreeNode:
    def __init__(self, address="unknown", axis=Axis.NONE, left=None, right=None, src_level=0, reduced_level=0,
                 reduced_address=None):
        self.address = address
        self.axis = axis
        self.left = left
        self.right = right
        self.growth = 1.0
        self.depth = 0
        self.src_level = src_level
        self.reduced_level = reduced_level
        self.reduced_depth = None
        self.reduced_address = reduced_address
        self.chain_length = 1
        self.fertility = None
        self.number_on_level = None
        self.leaves_number = None
        self.tree = None

    def __str__(self):
        return self.get_full_addr()

    def get_full_addr(self):
        return f"{self.address}"

    def full_tree_str(self):
        left_str = "" if self.left.is_none() else self.left.full_tree_str()
        right_str = "" if self.right.is_none() else self.right.full_tree_str()
        return f"({left_str}, {right_str})"

    # cut tree to max_level if more levels exist in the source tree
    def cut(self, max_level):
        self.internal_cut(0, max_level)

    def internal_cut(self, src_level, max_level):
        if self.is_none():
            return

        self.depth = src_level
        if src_level >= max_level:
            self.left = NONE_NODE
            self.right = NONE_NODE
            self.axis = Axis.LEAVE
            self.growth = 1.0
            self.chain_length = 1.0
        self.left.internal_cut(src_level + 1, max_level)
        self.right.internal_cut(src_level + 1, max_level)

        self.depth = max(self.right.depth, self.left.depth)

    def order_left_right(self):
        left_axis = get_axis(self.left)
        right_axis = get_axis(self.right)

        if left_axis > right_axis:
            tmp = self.left
            self.left = self.right
            self.right = tmp

    # merge chains (nodes in line without division) into single edge
    def reduce(self):
        self.internal_reduce(parent_growth=1, chain_length=1)

    def internal_reduce(self, parent_growth, chain_length):
        if self.is_none():
            return self

        self.chain_length = chain_length

        # multiply growth of cells on each edge in the chain
        self.growth = self.growth * parent_growth

        # HACK to remove axis Z
        if self.axis == Axis.Z:
            self.axis = Axis.GROWTH
            self.right = NONE_NODE

        if self.left.is_none() and self.right.is_none():
            self.axis = Axis.LEAVE  # this is a leave
            return self
        if self.right.is_none():
            # if continue chain - add 1 to its' length
            return self.left.internal_reduce(parent_growth=self.growth, chain_length=chain_length + 1)
        # assert self.left is not None

        # if there is a division - set length to 1
        self.left = self.left.internal_reduce(parent_growth=1, chain_length=1)
        self.right = self.right.internal_reduce(parent_growth=1, chain_length=1)

        return self

    def internal_prepare(self, reduced_level, reduced_address="Z"):
        if self.is_none():
            return

        # assert (self.left is None) == (self.right is None)

        self.reduced_level = reduced_level
        self.reduced_address = reduced_address

        self.left.internal_prepare(reduced_level + 1, reduced_address + ".L")
        self.right.internal_prepare(reduced_level + 1, reduced_address + ".R")

        self.reduced_depth = 1 + max(self.left.reduced_depth, self.right.reduced_depth)

    def flip(self):
        if self.is_none():
            return

        if self.axis == Axis.Y or self.axis == Axis.DIAGONAL:
            tmp = self.left
            self.left = self.right
            self.right = tmp

        self.left.flip()
        self.right.flip()

    def calculate_fertility(self, param_a):
        if self.is_none():
            return 0

        self.fertility = 1 * pow(param_a, self.reduced_level)
        self.fertility += self.left.calculate_fertility(param_a)
        self.fertility += self.right.calculate_fertility(param_a)
        return self.fertility

    # leaves number in the single tree
    def calculate_leaves_number(self):
        if self.is_none():
            return

        # assert (self.left.is_none() and self.right.is_none) == (self.axis == Axis.LEAVE),
        #   f"{self.axis}, {self.left.is_none()}, {self.right.is_none()}"

        if self.axis == Axis.LEAVE:
            self.leaves_number = 1
        else:
            self.left.calculate_leaves_number()
            self.right.calculate_leaves_number()
            self.leaves_number = self.left.leaves_number + self.right.leaves_number

    # def recursive(self, params, handler, params_getter):
    #     if self.is_none():
    #         return 0
    #
    #     left_params = params_getter(self, params)
    #     left_res = self.recursive(left_params, handler, params_getter)
    #     right_params = params_getter(self, params)
    #     right_res = self.recursive(right_params, handler, params_getter)
    #
    #     cur_res = handler(self, params)
    #     return cur_res

    def is_none(self):
        return self.axis == Axis.NONE

    def is_exist(self):
        return self.axis != Axis.NONE


class Tree:
    def __init__(self, root, name="unknown", embryo_type="unknown"):
        self.name = name
        self.embryo_type = embryo_type
        self.root = root
        self.roots = []  # trees, which were cut to levels 0, 1, 2, 3 etc
        self.flipped_root = None
        self.flipped_roots = []

    def __str__(self):
        return self.get_full_addr()

    def get_full_addr(self):
        return f"{self.name} {self.root.get_full_addr()}"

    # cut tree to max_level if more levels exist in the source tree
    # notice: zygote has level=0
    def cut(self, max_level):
        self.root.internal_cut(0, max_level)

    def reduce(self):
        self.root.internal_reduce(parent_growth=1, chain_length=1)

    def prepare(self, use_min_common_depth, use_flipping):
        self.root.internal_prepare(0)

        if use_flipping:
            self.flipped_root = copy.deepcopy(self.root)
            self.flipped_root.flip()

        # this if - performance optimization only
        if use_min_common_depth:
            # fill roots with cut trees to compare trees of different depth, e.g. with Johansen
            for i in range(self.root.reduced_depth + 1):
                cur_node = copy.deepcopy(self.root)
                cur_node.internal_cut(0, i)
                self.roots.append(cur_node)

                if use_flipping:
                    flipped_cur_node = copy.deepcopy(cur_node)
                    flipped_cur_node.flip()
                    self.flipped_roots.append(flipped_cur_node)

        self.root.calculate_leaves_number()


NONE_NODE = TreeNode()
NONE_NODE.left = NONE_NODE
NONE_NODE.right = NONE_NODE
NONE_NODE.reduced_depth = 0
NONE_NODE.leaves_number = 0


INFINITE_PATTERN = TreeNode(axis=Axis.X)
INFINITE_PATTERN.left = INFINITE_PATTERN
INFINITE_PATTERN.right = INFINITE_PATTERN
INFINITE_PATTERN.reduced_depth = 0
INFINITE_PATTERN.leaves_number = 0
