class GlobalParams:
    def __init__(self, a, b, g, param_g_weight, chain_length_weight, change_left_right):
        self.a = a
        self.b = b
        self.g = g
        self.param_g_weight = param_g_weight
        self.chain_length_weight = chain_length_weight
        self.change_left_right = change_left_right

        self.swaps = 0
        self.total = 0
