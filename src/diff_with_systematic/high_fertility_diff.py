import statistics

from src.compare_trees.distances import high_fertility_diff_development_tree_distance
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff

# Build matrices and corr coef only

systematic_tree = "morph"
cluster_algorithm = "average"
max_level = 11

matrDiff = MatrixDiff("../../input/xtg/*.xtg", f"../../input/systematic_tree_{systematic_tree}.xtg",
                      ["Angiosperms"], max_level=max_level)

trees = matrDiff.vertices

global_params = GlobalParams(max_level=max_level, param_a=0.5, g_weight=0.0, chain_length_weight=0.0)

#experiment_matrix = []
for i in range(len(trees)):
    #experiment_matrix.append([])
    sp_node2dist = {}
    for j in range(len(trees)):
        #if i == j or trees[j].name != 'Chenopodium_bonus-henricus':
        if i == j:
            continue
        distances = high_fertility_diff_development_tree_distance(trees[i], trees[j], global_params)
        for [addr, dist, reduced_level] in distances:
            #print(f"INSERT INTO diff_nodes(tree1, tree2, addr, dist, reduced_level) VALUES('{trees[i].name}', '{trees[j].name}', '{addr}', {dist}, {reduced_level});")
            #key = f"{trees[i].name} - {addr}"
            key = f"{addr}"
            sp_node2dist.setdefault(key, [])

            weight = pow(2.0 / global_params.param_a, reduced_level)
            normalized_dist = dist * weight

            #sp_node2dist[key] += [[normalized_dist, trees[j].name, dist, reduced_level]]
            sp_node2dist[key] += [[normalized_dist, trees[j].name]]
            #sp_node2dist[key] += [normalized_dist]

    #print(f"{trees[i].name}")
    node_distances = []
    for key in sorted(sp_node2dist):
        normalized_distances = sorted(sp_node2dist[key], key=lambda tuple: tuple[0])
        median_dist = normalized_distances[int(len(normalized_distances) / 2)][0]
        median_dist_tree = normalized_distances[int(len(normalized_distances) / 2)][1]
        mean = statistics.mean([item[0] for item in normalized_distances])
        stdev = None if len(normalized_distances) < 2 else statistics.stdev([item[0] for item in normalized_distances])
        max_dist = normalized_distances[-1][0]
        max_dist_tree = normalized_distances[-1][1]
        #print(f"{key} {normalized_distances}")
        #node_distances += [[key, median_dist, median_tree, mean, stdev, max_dist, max_dist_tree]]
        #node_distances += [[key, max_dist, max_dist_tree]]
        #node_distances += [[key, median_dist, median_dist_tree]]
        node_distances += [[key, mean, stdev]]
    node_distances = sorted(node_distances, key=lambda tuple: -tuple[1])
    res_str = ""
    for item in node_distances[:3]:
        res_str += f" {item[0]} {item[1]} {item[2]}"
    #print(f"{trees[i].name}{res_str}")
    print(f"{trees[i].name} {node_distances[:10]}")




# CREATE DATABASE embrionic_tree;
# CREATE TABLE diff_nodes(id INTEGER PRIMARY KEY, tree1 varchar(255), tree2 varchar(255), addr varchar(255), dist FLOAT, reduced_level INTEGER);
# SELECT tree1, addr, COUNT(*) as cnt,  FROM diff_nodes GROUP BY tree1, addr

# 'Z', 0.578125
# 'Z.R', 0.6875
# 'Z.L', 0.46875


# 'Z', 0.734375, 'Chenopodium_bonus-henricus'
# 'Z.R', 0.5625, 'Chenopodium_bonus-henricus'