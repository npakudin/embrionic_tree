import copy
import math


class UltraMetricParams:
    def __init__(self, level_count):
        assert level_count >= 1
        self.level_count = level_count


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


# Gets matrix NxN and returns matrix NxN
# The returned matrix is the ultra metric matrix
def get_ultra_metric(src_matrix, ultra_metric_params):
    matrix = copy.deepcopy(src_matrix)
    normalize_to_levels(matrix, ultra_metric_params.level_count)

    print_matrix(src_matrix, "src_matrix")
    print_matrix(matrix, "normalized")

    target_value = 0
    while True:
        target_value += 1
        [_, [src_max, _, _]] = find_min_max(matrix, more_than=target_value - 1)
        if src_max <= target_value:
            break

        set_to(matrix, target_value, target_value - 0.5, target_value)  # set to 1 for all items in [0.5; 1]
        print_matrix(matrix, "set_to")

        while True:
            joined_count = join_triangles(matrix, target_value)
            [clusters, row_to_cluster] = get_cluster_mapping(matrix, target_value)
            #cluster_matrix = cluster_distances(matrix, clusters)
            merge_error_matrix = cluster_merge_error(matrix, clusters, target_value)

            print_clusters(clusters, row_to_cluster)

            [[error_min, error_min_i, error_min_j], _] = find_min_max(merge_error_matrix)
            if error_min_i == -1 or error_min < 0:
                # everything is merged
                break
            else:
                # merge clusters i and j
                print(f"merge clusters {error_min_i} and {error_min_j}")
                merge_clusters(matrix, clusters, target_value, error_min_i, error_min_j)

                #set_to(matrix, target_value, target_value, target_value + 0.5)  # set to 1 for all items in (1.0; 1.5]

            print_matrix(matrix, "merged")

    # divide_matrix(matrix, 1.0 / (M * min_non_zero))

    return matrix


# For both
#   min -> 0.5
#   max -> level_count + 0.5
#
# For 'log':
#   log(max, base) - log(min, base) = level_count
#   log(max/min, base) = level_count
#   max/min = base^level_count
#   base = math.pow(max/min, -level_count)
#
# So formula for item is:
#   item = log(item, base) - log(min, base) + 0.5
#   item = log(item / min, base) + 0.5
def normalize_to_levels(matrix, level_count, type='line'):
    [[min, _, _], [max, _, _]] = find_min_max(matrix)
    b = math.pow(max / min, -level_count)  # for log type

    print(f"min: {min}")

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == j:
                # it's already 0
                pass
            else:
                if type == 'line':
                    matrix[i][j] = (matrix[i][j] - min) / (max - min) * level_count + 0.5
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


def merge_clusters(matrix, clusters, target_distance, row, column):
    for i in clusters[row]:
        for j in clusters[column]:
            if i == j:
                # skip diagonal
                continue
            matrix[i][j] = target_distance
            matrix[j][i] = target_distance


# 0  \
# 1 - 1  \
# 2  \      8
# 3 - 3 /

matr = [
    [0, 1, 8, 8],
    [1, 0, 8, 8],
    [8, 8, 0, 2],
    [8, 8, 2, 0],
]
um = get_ultra_metric(matr, UltraMetricParams(level_count=2))
print_matrix(um, "ultra_metric")
