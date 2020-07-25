import copy
import math

from src.view.build_morph_graph import find_common_ancestor_level


class UltraMetricParams:
    def __init__(self, max_level):
        assert max_level >= 1
        self.max_level = max_level


class UltraMetricNode:
    def __init__(self, clusters, name=None):
        self.clusters = clusters
        self.name = name
        self.parent = None

    def __str__(self):
        return self.name

# Gets matrix NxN and returns matrix NxN
# The returned matrix is the ultra metric matrix
def get_ultra_metric(src_matrix, ultra_metric_params):
    matrix = copy.deepcopy(src_matrix)
    normalize_to_levels(matrix, ultra_metric_params.max_level)

    src_history_level = [UltraMetricNode(clusters=None, name=f"0.{i}") for i in range(len(matrix))]
    history_level = [item for item in src_history_level]
    target_value = 0
    while len(matrix) > 1:
        target_value += 1

        while True:
            set_to(matrix, target_value, target_value - 0.5, target_value)  # set to 1 for all items in [0.5; 1]
            _joined_count = join_triangles(matrix, target_value)
            [clusters, row_to_cluster] = get_cluster_mapping(matrix, target_value)

            merge_error_matrix = cluster_merge_error(matrix, clusters, target_value)

            [_, [error_max, error_max_i, error_max_j]] = find_min_max(merge_error_matrix)
            if error_max_i == -1 or error_max < 0:
                # everything is merged

                # save current cluster mapping to restore
                history_level = create_history_level(clusters, history_level, target_value)

                break
            else:
                # merge clusters i and j
                merge_two_clusters(matrix, clusters, target_value, error_max_i, error_max_j)

        # use cluster matrix for next steps
        cluster_matrix = cluster_distances(matrix, clusters)
        matrix = cluster_matrix

    # restore source matrix
    res = [[0 if i == j else find_common_ancestor_level(src_history_level[i], src_history_level[j]) for j in range(len(src_matrix))] for i in range(len(src_matrix))]
    # for target, clusters in enumerate(clustering_history):
    #     pass

    return res


def create_history_level(clusters, history_level, target_value):
    new_history_level = [UltraMetricNode(clusters=[history_level[cluster_row] for cluster_row in cluster],
                                         name=f"{target_value}.{cluster_index}") for cluster_index, cluster in
                         enumerate(clusters)]
    for cluster_index, cluster in enumerate(clusters):
        for cluster_row in cluster:
            history_level[cluster_row].parent = new_history_level[cluster_index]
    return new_history_level


def print_matrix(matrix, name):
    print("name")
    for row in matrix:
        for item in row:
            print("%0.2f " % item, end='')
        print()


def print_clusters(clusters, row_to_cluster):
    print("")
    print("clusters")
    for row in clusters:
        print(row)
    print()
    print("row_to_cluster")
    for key in sorted(row_to_cluster):
        print(f"{key}:{row_to_cluster[key]}")
    print()


# For both
#   min -> 0.5
#   max -> max_level + 0.5
#
# For 'log':
#   log(max, base) - log(min, base) = max_level
#   log(max/min, base) = max_level
#   max/min = base^max_level
#   base = math.pow(max/min, -max_level)
#
# So formula for item is:
#   item = log(item, base) - log(min, base) + 0.5
#   item = log(item / min, base) + 0.5
def normalize_to_levels(matrix, max_level, type='line'):
    [[min, _, _], [max, _, _]] = find_min_max(matrix)
    b = math.pow(max / min, -max_level)  # for log type

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                # it's already 0
                pass
            else:
                if type == 'line':
                    matrix[i][j] = (matrix[i][j] - min) / (max - min) * max_level + 0.5
                else:
                    matrix[i][j] = math.log(matrix[i][j] / min, b) + 0.5
    return matrix


def find_min_max(matrix, more_than=-float("inf")):
    matr_min = [float("inf"), -1, -1]
    matr_max = [-float("inf"), -1, -1]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                # skip diagonal
                continue
            if more_than < matrix[i][j] < matr_min[0]:
                matr_min = [matrix[i][j], i, j]
            if matrix[i][j] > matr_max[0]:
                matr_max = [matrix[i][j], i, j]
    return [matr_min, matr_max]


def divide_matrix(matrix, m):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] /= m


def find_average_of_less_b(matrix, b):
    sum = 0
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] <= b:
                sum += matrix[i][j]
                count += 1
    return [sum / (count + 1.0E-100), count]


def set_to(matrix, target_value, src_from_value, src_to_value):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                # skip diagonal
                continue
            if src_from_value <= matrix[i][j] <= src_to_value:
                matrix[i][j] = target_value


def average_error(m1, m2):
    sum1 = 0
    sum2 = 0
    sum = 0
    count = 0
    for i in range(len(m1)):
        for j in range(len(m1[i])):
            sum += abs(m1[i][j] - m2[i][j])
            sum1 += m1[i][j]
            sum2 += m2[i][j]
            count += 1
    return [sum / (count + 1.0E-100), sum / max(sum1, sum2)]


# Makes all triangles isosceles
def join_triangles(matrix, target_value):
    joined_count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                continue
            for j2 in range(len(matrix[i]) - j):
                # Let
                # matrix[i, j] = dist(a, b)
                # matrix[i, j2] = dist(a, c)
                # matrix[j, j2] = dist(a, c)
                #
                # Then set a 3rd triangle edge
                # if dist(a, b) == dist(a, c) == target_value:
                #     if dist(b, c) <= target_value:
                #         #it was merged at previous step, triangle is already isosceles
                #     else
                #         dist(b, c) = target_value
                if i == j2 or j == j2:
                    continue
                if matrix[i][j] == target_value and matrix[i][j2] == target_value:
                    if matrix[j][j2] > target_value:
                        joined_count += 1
                        matrix[j][j2] = target_value
                        matrix[j2][j] = target_value
    return joined_count


def get_cluster_mapping(matrix, target_value):
    row_to_cluster = {}
    cluster_to_row = []
    for i in range(len(matrix)):
        if i not in row_to_cluster:
            cluster_index = len(cluster_to_row)
            row_to_cluster[i] = cluster_index
            cluster_to_row.append([i])
            for j in range(len(matrix[i]) - i - 1):
                if matrix[i][j + i + 1] <= target_value:
                    row_to_cluster[j + i + 1] = cluster_index
                    cluster_to_row[cluster_index].append(j + i + 1)
    return [cluster_to_row, row_to_cluster]


def cluster_distances(matrix, clusters):
    def two_cluster_distance(c1, c2):
        sum = 0
        for i in range(len(c1)):
            for j in range(len(c2)):
                sum += matrix[c1[i]][c2[j]]
        return sum / (len(c1) * len(c2))

    res = [[0 if i == j else two_cluster_distance(clusters[i], clusters[j]) for j in range(len(clusters))] for i in
           range(len(clusters))]
    return res


def cluster_merge_error(matrix, clusters, target_distance):
    def two_cluster_distance(c1, c2):
        sum = 0
        for i in range(len(c1)):
            for j in range(len(c2)):
                sum += matrix[c1[i]][c2[j]]
        return (target_distance + 0.5) * (len(c1) * len(c2)) - sum

    res = [[0 if i == j else two_cluster_distance(clusters[i], clusters[j]) for j in range(len(clusters))] for i in
           range(len(clusters))]
    return res


def merge_two_clusters(matrix, clusters, target_distance, row, column):
    for i in clusters[row]:
        for j in clusters[column]:
            if i == j:
                # skip diagonal
                continue
            matrix[i][j] = target_distance
            matrix[j][i] = target_distance
    # TODO: set average distance?
