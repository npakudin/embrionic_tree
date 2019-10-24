class GlobalParams:
    def __init__(self, a, g_weight, chain_length_weight, is_swap_left_right, max_levels):
        self.a = a
        self.g_weight = g_weight
        self.chain_length_weight = chain_length_weight
        self.is_swap_left_right = is_swap_left_right
        self.max_levels = max_levels

        self.swaps = 0
        self.total = 0
