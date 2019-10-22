import copy
import math


class UltraMetricParams:
    def __init__(self, level_count):
        assert level_count >= 1
        self.level_count = level_count


# Gets matrix NxN and returns matrix NxN
# The returned matrix is the ultra metric matrix
def get_ultra_metric(src_matrix, ultra_metric_params):
    matrix = copy.deepcopy(src_matrix)
    normalize_to_levels(matrix, ultra_metric_params.level_count)

    target_value = 0
    while True:
        target_value += 1
        [src_min, src_max] = find_min_max(matrix, more_than=target_value - 1)
        if src_max <= target_value:
            break

        set_to(matrix, target_value, target_value + 0.5, target_value + 1.0)  # set to 1 for all items in (0.5; 1]

        joined_count = join_triangles(matrix, target_value)
        [clusters, row_to_cluster] = get_cluster_mapping(matrix, target_value)
        cluster_matrix = cluster_distances(matrix, clusters)

        [cluster_min, cluster_max] = find_min_max(cluster_matrix)
        if cluster_min >= target_value + 0.5:
            # everything merged
            pass
        else:
            # TODO: this is hack, replace with min error
            set_to(matrix, target_value, target_value, target_value + 0.5)  # set to 1 for all items in (1.0; 1.5]
            pass

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
    [min, max] = find_min_max(matrix)
    b = math.pow(max / min, -level_count)  # for log type

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if type == 'line':
                matrix[i][j] = (matrix[i][j] - min) / (max - min) * level_count + 0.5
            else:
                matrix[i][j] = math.log(matrix[i][j] / min, b) + 0.5
    return matrix


def find_min_max(matrix, more_than=0):
    min = 1.0E+300
    max = -1.0E+300
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - i - 1):
            if more_than < matrix[i][j] < min:
                min = matrix[i][j]
            if matrix[i][j] > max:
                max = matrix[i][j]
    return [min, max]


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
    return [sum / (count + 1.0E-10), count]


def set_to(matrix, target_value, src_from_value, src_to_value):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > src_from_value and matrix[i][j] <= src_to_value:
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
    return [sum / (count + 1.0E-10), sum / max(sum1, sum2)]


def join_triangles(matrix, target_value):
    joined_count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for j2 in range(len(matrix[i]) - j - 1):
                if matrix[i][j] == target_value and matrix[i][j2] == target_value:
                    if matrix[j][j2] != target_value:
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
                if matrix[i][j + i + 1] == target_value:
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

    res = [[1 if i == j else two_cluster_distance(clusters[i], clusters[j]) for j in range(len(clusters))] for i in
           range(len(clusters))]
    return res
