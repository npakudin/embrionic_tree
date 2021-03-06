from src.single_tree.global_params import GlobalParams
from src.multiple_trees.matrix_diff import MatrixDiff

# calculates distance between species if cut all trees at level 2, 3, 4, ..., 11

systematic_tree = "morph"

globalMatrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                            ["Angiosperms"], max_level=10)

res_matrices = []
res_corrcoef = []

# iterate over max_level
for cur_max_level in range(2, 12):

    global_params = GlobalParams(max_level=cur_max_level, param_a=0.50, g_weight=0.5)

    matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                          ["Angiosperms"], max_level=cur_max_level)

    experiment_matrix = matrDiff.make_experiment_matrix(global_params)
    corrcoef = matrDiff.corrcoef(experiment_matrix=experiment_matrix)
    # print(f"max_dist: {max_dist}, corrcoef: {corrcoef}")

    res_matrices.append(experiment_matrix)
    res_corrcoef.append(corrcoef)


print(f"specie_1 specie_2", end='')
for cur_max_level in range(len(res_matrices)):
    print(f" dist_if_cut_at_level_{cur_max_level + 2}", end='')
print("")

trees = globalMatrDiff.vertices
for i in range(len(res_matrices[0])):
    for j in range(len(res_matrices[0][i])):
        print(f"{trees[i].name} {trees[j].name}", end='')
        for cur_max_level in range(len(res_matrices)):
            print(f" {res_matrices[cur_max_level][i][j]:0.3f}", end='')
        print("")
