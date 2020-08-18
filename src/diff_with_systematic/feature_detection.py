import numpy as np

from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.iterate_trees import generate_bin_tree, get_subtrees
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, corrcoef

# Build matrices and corr coef only

systematic_tree = "morph"
max_level = 11

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                      ["Angiosperms"], max_level=max_level)

global_params = GlobalParams(max_level=max_level, param_a=0.5, g_weight=0, chain_length_weight=0)

trees = matrDiff.vertices


name2index = {}
for i in range(len(matrDiff.names)):
    name2index[matrDiff.names[i]] = i

# ползучее корневище
creeping_rhizome = {"Ottelia_alismoides", "Polemonium_caeruleum", "Potamogeton_lucens", "Sagina_procumbens",
                    "Sedum_acre", "Sedum_sieboldii", "Sparganium_simplex", "Stratiotes_aloides"}

# мочковатая корн. система
fibrous_root_system = {"Triticum_aestivum"}


# Arabidopsis_thaliana Capsella_bursa-pastoris Cephalaria_gigantea Chenopodium_bonus-henricus
# Cyclamen_persicum Cynomorium_coccineum Datura_stramonium Drosera_burmanni Drosera_rotundifolia
# Fumaria_officinalis Geum_urbanum Lathraea_squamaria Linum_catharticum
# Senecio_vulgaris Solanum_nigrum Solanum_tuberosum
# Streptocarpus_rexii Striga_hermonthica  Urtica_pilulifera Urtica_urens


feature_matrix = []
for i in range(len(matrDiff.taxon_matrix)):
    feature_matrix.append([])
    for j in range(i):

        # # eudicots / monocots
        # dist = 0 if matrDiff.taxon_matrix[i][j] < 5 else 1

        # creeping_rhizome root
        dist = 1
        if (matrDiff.names[i] in creeping_rhizome) == (matrDiff.names[j] in creeping_rhizome):
            dist = 0

        feature_matrix[i].append(dist)

print_matrix(feature_matrix, "feature_matrix", matrDiff.names, 0, with_headers=True)


# iterate over chains
# for i in range(1, pow(2, 7)):
#     pattern = get_chain(i)
#     experiment_matrix = matrDiff.make_experiment_matrix(global_params, pattern=pattern)
#     corr = corrcoef(feature_matrix, experiment_matrix)
#     res.append([corr, get_deepest_node(pattern).address])


for param_a in np.linspace(0.5, 1.6, 12):
    global_params = GlobalParams(max_level=max_level, param_a=param_a, g_weight=0, chain_length_weight=0)
    res = []

    # iterate over subtrees
    for level in range(5):
        root = generate_bin_tree(level)
        for pattern in get_subtrees(root):
            if pattern is None:
                continue

            # node = TreeNode()
            # node.right = pattern
            # pattern = node

            experiment_matrix = matrDiff.make_experiment_matrix(global_params, pattern=pattern)
            corr = corrcoef(feature_matrix, experiment_matrix)
            #print_matrix(feature_matrix, "feature_matrix", matrDiff.names, corr, with_headers=True)
            res.append([corr, pattern.full_tree_str()])

    # for i in range(1, pow(2, 7)):
    #     pattern = get_chain(i)
    #     experiment_matrix = matrDiff.make_experiment_matrix(global_params, pattern=pattern)
    #     corr = corrcoef(feature_matrix, experiment_matrix)
    #     res.append([corr, get_deepest_node(pattern).address])

    print(f"\nparam_a: {param_a:0.2f}")
    res = sorted(res, key=lambda item: -item[0])
    for item in res[:2]:
        print(f"{item[0]:0.3f} - {item[1]}")
