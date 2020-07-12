import copy
from enum import Enum
import math


# order should be: x < d < у < z < L < N
# to provide it, use lexicographic order of: x < xd < у < z < zLeave < zNone
class Axis():
    X = 'x'
    DIAGONAL = 'xd'
    Y = 'y'
    Z = 'z'
    NONE = 'zNone'
    LEAVE = 'zLeave'


def get_axis(node):
    if node is None:
        return Axis.NONE
    return node.axis


class TreeNode:
    def __init__(self, address="unknown", axis=Axis.NONE, left=None, right=None, src_level=0, reduced_level=0):
        self.address = address
        self.axis = axis
        self.left = left
        self.right = right
        self.growth = 1.0
        self.depth = 0
        self.src_level = src_level
        self.reduced_level = reduced_level
        self.reduced_depth = None
        self.chain_length = 1
        # self.personal_weight = 0
        # self.total_weight = 0
        # self.fertility = 0
        self.order_index = None

    def __str__(self):
        return self.get_full_addr()

    def get_full_addr(self):
        return f"{self.address}"

    # cut tree to max_level if more levels exist in the source tree
    def cut(self, max_level):
        self.internal_cut(0, max_level)

    def internal_cut(self, src_level, max_level):
        self.depth = src_level
        if src_level >= max_level:
            self.left = None
            self.right = None
            self.axis = Axis.NONE
        if self.left is not None:
            self.left.internal_cut(src_level + 1, max_level)
            self.depth = self.left.depth
        if self.right is not None:
            self.right.internal_cut(src_level + 1, max_level)
            #assert self.depth == self.right.depth, f"self.depth: {self.depth} self.right.depth: {self.right.depth}, right.address: {self.right.address}"
            self.depth = max(self.right.depth, self.depth)

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

        self.chain_length = chain_length

        # multiply growth of cells on each edge in the chain
        self.growth = self.growth * parent_growth

        # HACK to remove axis Z
        if self.axis == Axis.Z:
            self.axis = Axis.NONE
            self.right = None

        if self.left is None and self.right is None:
            self.axis = Axis.LEAVE # this is a leave
            return self
        if self.right is None:
            # if continue chain - add 1 to its' length
            return self.left.internal_reduce(parent_growth=self.growth, chain_length=chain_length + 1)
        assert self.left is not None

        # if there is a division - set length to 1
        self.left = self.left.internal_reduce(parent_growth=1, chain_length=1)
        self.right = self.right.internal_reduce(parent_growth=1, chain_length=1)

        return self

    def prepare(self):
        self.reduce()
        #self.order_left_right()
        self.internal_prepare(0)

    def internal_prepare(self, reduced_level):
        #assert (self.left is None) == (self.right is None)

        self.reduced_level = reduced_level
        # self.personal_weight = global_params.calc_weight.fun(self.src_level, self.reduced_level) #math.pow(global_params.a, reduced_level)
        # self.total_weight = self.personal_weight
        # self.fertility = 0

        self.reduced_depth = 0

        if self.left is not None:
            self.left.internal_prepare(reduced_level + 1)
            # self.total_weight += self.left.total_weight
            self.reduced_depth = max(self.reduced_depth, 1 + self.left.reduced_depth)

        if self.right is not None:
            #if self.reduced_level > 0: # skip Z.R and all it's ancestors
            self.right.internal_prepare(reduced_level + 1)
            # self.total_weight += self.right.total_weight
            self.reduced_depth = max(self.reduced_depth, 1 + self.right.reduced_depth)

            assert self.left is not None
            assert self.left.depth == self.right.depth
        # self.fertility = (self.total_weight - self.personal_weight) / self.personal_weight
        #
        # assert self.fertility >= 0, f"src_level: {self.src_level}, reduced_level: {self.reduced_level}, personal_weight: {self.personal_weight}"


class Tree:
    def __init__(self, node, name="unknown", embryo_type="unknown"):
        self.name = name
        self.embryo_type = embryo_type
        self.node = node
        self.nodes = []

    def __str__(self):
        return self.get_full_addr()

    def get_full_addr(self):
        return f"{self.name} {self.node.get_full_addr()}"

    # cut tree to max_level if more levels exist in the source tree
    def cut(self, max_level):
        self.node.internal_cut(0, max_level)

    def reduce(self):
        self.node.internal_reduce(parent_growth=1, chain_length=1)

    def prepare(self):
        #self.node.reduce()
        #self.order_left_right()
        self.node.internal_prepare(0)

        for i in range(self.node.reduced_depth + 1):
            cur_node = copy.deepcopy(self.node)
            cur_node.internal_cut(0, i)
            self.nodes.append(cur_node)

