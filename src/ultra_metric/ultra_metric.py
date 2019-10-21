import copy


class UltraMetricParams:
    def __init__(self, b):
        assert b > 1
        self.b = b


# Gets matrix NxN and returns matrix NxN
# The returned matrix is the ultra metric matrix
def get_ultra_metric(src_matrix, ultra_metric_params):

    matrix = copy.deepcopy(src_matrix)
    min_non_zero = find_min_non_zero(matrix)
    divide_matrix(matrix, min_non_zero)
    [M, count_of_less] = find_average_of_less_b(matrix, ultra_metric_params.b)
    if count_of_less == 0:
        # TODO: what to do?
        pass

    divide_matrix(matrix, M)
    set_to(matrix, 1, 0, ultra_metric_params.b / M) # set to 1 for all items in (0; b]

    #divide_matrix(matrix, 1.0 / (M * min_non_zero))

    return matrix


def find_min_non_zero(matrix):
    min = matrix[1][0]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i != j and matrix[i][j] < min:
                min = matrix[i][j]
    return min


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

