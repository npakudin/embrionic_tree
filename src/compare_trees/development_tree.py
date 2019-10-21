import math
from enum import Enum


class NodeType(Enum):
    NONE = 0
    AXIS_X = 1
    AXIS_Y = 2
    GROWTH = 3
    LEAVE = 4


class Tree:
    def __init__(self, root, name):
        self.root = root
        self.name = name


class TreeNode:
    def __init__(self, left=None, right=None, time=None):
        self.name = "unknown"
        self.global_params = None
        self.type = None
        self.left = left
        self.right = right
        self.time = time
        self.growth = 1.0
        self.depth = 0
        self.level = 0
        self.chain_length = 1
        self.weight = 0
        self.total_weight = 0
        self.total_weight_b = 0
        self.fertility = 0

    # cut tree to max_level if more levels exist in the source tree
    def cut(self, max_level):
        self.internal_cut(0, max_level)

    def internal_cut(self, level, max_level):
        self.depth = level
        if level >= max_level:
            self.left = None
            self.right = None
        if self.left is not None:
            self.left.internal_cut(level + 1, max_level)
            self.depth = self.left.depth
        if self.right is not None:
            self.right.internal_cut(level + 1, max_level)
            assert self.depth == self.right.depth

    # merge chains (nodes in line without division) into single edge
    def reduce(self, g, chain_length):

        self.chain_length = chain_length

        # multiply growth of cells on each edge in the chain
        self.growth = self.growth * g

        if self.left is None and self.right is None:
            return self
        if self.right is None:
            # if continue chain - add 1 to its' length
            return self.left.reduce(self.growth, chain_length + 1)
        assert self.left is not None

        # if there is a division - set length to 1
        self.left = self.left.reduce(g, 1)
        self.right = self.right.reduce(g, 1)

        return self

    def prepare(self, global_params):
        self.internal_prepare(0, global_params)

    # calculate node.weight = a^level
    # calculate node.total_weight = node.weight + node.left.weight + node.right.weight
    def internal_prepare(self, level, global_params):

        self.level = level
        self.weight = math.pow(global_params.a, level)
        weight_b = math.pow(global_params.b, level)
        self.total_weight = self.weight
        self.total_weight_b = weight_b
        self.fertility = 0

        if self.left is not None:
            self.left.internal_prepare(level + 1, global_params)
            self.total_weight += self.left.total_weight
            self.total_weight_b += self.left.total_weight_b

        if self.right is not None:
            self.right.internal_prepare(level + 1, global_params)
            self.total_weight += self.right.total_weight
            self.total_weight_b += self.right.total_weight_b

            assert self.left.depth == self.right.depth

        # self.fertility = (self.total_weight_b - weight_b) / weight_b

        if weight_b == 0:
            print(f"weight_b: {weight_b}, level: {level}")

        self.fertility = (self.total_weight_b - 0.5 * weight_b) / weight_b
        assert self.fertility >= 0
