# There are multiple clusterings of the same trees
# (e.g. clusterings with different parameters - is_reducing, param_a, g_weight, average/complete algorithms)
#
# Find branches which are similar in all these clusterings
#
# Example 1
# A and B are in the tree with 2 branches only in all clusterings
#
# Example 2
# A, B and C are in the tree with 3 branches only in all clusterings,
#   but sometimes tree is a (A,B),C , i.e.: d(A,B) < d(A,C) = d(B,C)
#   sometimes tree is a (A,C),B
#
# Example 3 - fuzzy
# 1st clustering: A and B are in the same tree with 2 branches
# 2nd clustering: A and B are in the same tree with 2 branches
# 3rd clustering: (A,C),B


def clustering_to_branches(clustering):
    res = {}  # {frozenset(branch1): 1.0, frozenset(branch2): 1.0, ...}
    full_cluster = []
    for i in range(len(clustering)):  # add single items, not presented in clustering
        full_cluster.append(frozenset({i}))

    for [item1_index, item2_index, dist, total_items] in clustering:
        # noinspection PyUnresolvedReferences
        # it's an index, not item
        new_set = full_cluster[item1_index].intersection(full_cluster[item2_index])
        full_cluster.append(new_set)
        res[new_set] = 1.0
    return res


def common_part(b1, b2):
    union = b1.union(b2)
    intersection = frozenset(b1.intersection(b2))
    return intersection, len(intersection) / len(union)


def find_similar_branches(clusterings):
    common_branches = clustering_to_branches(clusterings[0])
    for i in range(1, len(clusterings)):
        cur_branches = clustering_to_branches(clusterings[i])

        res = {}  # intersection => similarity
        for (common_branch, common_similarity) in common_branches.items():
            for cur_branch in cur_branches:
                intersection, similarity = common_part(common_branch, cur_branch)
                similarity *= common_similarity
                if similarity == 0:
                    continue
                existing_similarity = res.get(intersection)
                if existing_similarity is None:
                    res[intersection] = similarity
                else:
                    if similarity > existing_similarity:
                        res[intersection] = similarity
        common_branches = res

    return common_branches
