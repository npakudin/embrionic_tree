import math


class WeightCalculator:
    def __init__(self, name, fun):
        self.name = name
        self.fun = fun


def exponent_src_weight(a=0.5):
    return WeightCalculator(f"exp_src(a={a:0.2f})",
                            lambda src_level, reduced_level: math.pow(a, src_level))


def exponent_reduced_weight(a=0.5):
    return WeightCalculator(f"exp_reduced(a={a:0.2f})",
                            lambda src_level, reduced_level: math.pow(a, reduced_level))


def const_weight(weight=1.0):
    return WeightCalculator(f"const({weight:0.2f})",
                            lambda src_level, reduced_level: weight)


def threshold_weight(threshold_level=5, weight_1=1.0, weight_2=0.75):
    return WeightCalculator(f"threshold(thr_lev={threshold_level:0.2f},weight_1={weight_1:0.2f},weight_2={weight_2:0.2f})",
                            lambda src_level, reduced_level: weight_1 if src_level < threshold_level else weight_2)


class GlobalParams:
    def __init__(self, calc_weight, max_levels, g_weight, chain_length_weight=0.0, is_swap_left_right=False,
                 subtree_threshold=1.0E+100, subtree_multiplier=1.0,
                 level_weight_multiplier=None
                 ):
        self.max_levels = max_levels
        self.g_weight = g_weight
        self.chain_length_weight = chain_length_weight
        self.is_swap_left_right = is_swap_left_right
        self.calc_weight = calc_weight
        self.subtree_threshold = subtree_threshold
        self.subtree_multiplier = subtree_multiplier
        if level_weight_multiplier is None:
            level_weight_multiplier = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.level_weight_multiplier = level_weight_multiplier

        self.swaps = 0
        self.total = 0

        self.total_dist = 0
        self.dcl_more_zero = 0
