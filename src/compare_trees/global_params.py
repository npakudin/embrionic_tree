class GlobalParams:
    def __init__(self, max_level, param_a=0.5,
                 axis_weight=1.0, fertility_weight=1.0, g_weight=0.0, chain_length_weight=0.0,
                 subtree_threshold=1.0E+100, subtree_multiplier=1.0,
                 level_weight_multiplier=None,
                 use_min_common_depth=False
                 ):
        self.axis_weight = axis_weight
        self.fertility_weight = fertility_weight
        self.max_level = max_level
        self.g_weight = g_weight
        self.chain_length_weight = chain_length_weight
        self.param_a = param_a
        self.subtree_threshold = subtree_threshold
        self.subtree_multiplier = subtree_multiplier
        if level_weight_multiplier is None:
            level_weight_multiplier = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.level_weight_multiplier = level_weight_multiplier
        self.use_min_common_depth = use_min_common_depth
