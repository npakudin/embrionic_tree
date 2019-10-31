import math


class WeightCalculator:
    def __init__(self, name, fun):
        self.name = name
        self.fun = fun


def exponent_src_weight(a=0.5):
    return WeightCalculator(f"exponent_src_weight(a={a})",
                            lambda src_level, reduced_level: math.pow(a, src_level))


def exponent_reduced_weight(a=0.5):
    return WeightCalculator(f"exponent_reduced_weight(a={a})",
                            lambda src_level, reduced_level: math.pow(a, reduced_level))


def const_weight(weight=1.0):
    return WeightCalculator(f"const_weight({weight})",
                            lambda src_level, reduced_level: weight)


def threshold_weight(threshold_level=5, weight_1=1.0, weight_2=0.75):
    return WeightCalculator(f"threshold_weight(threshold_level={threshold_level},weight_1={weight_1},weight_2={weight_2})",
                            lambda src_level, reduced_level: weight_1 if src_level < threshold_level else weight_2)


class GlobalParams:
    def __init__(self, g_weight, chain_length_weight, is_swap_left_right, calc_weight):
        self.g_weight = g_weight
        self.chain_length_weight = chain_length_weight
        self.is_swap_left_right = is_swap_left_right
        self.calc_weight = calc_weight

        self.swaps = 0
        self.total = 0

        self.total_dist = 0
        self.dcl_more_zero = 0
