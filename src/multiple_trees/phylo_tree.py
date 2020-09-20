import networkx as nx


def cut(distance_matrix, names):
    G = nx.Graph()
    for row_index, row in enumerate(distance_matrix):
        for col_index, item in enumerate(row):
            if (col_index < row_index):
                # G.add_edge(names[row_index], names[col_index], weight=item)
                G.add_edge(names[row_index], names[col_index], weight=item)
    return nx.stoer_wagner(G)


def sub_matrix(distance_matrix, names, part):
    sub_matr = []
    sub_names = []
    # print(f"len(distance_matrix):{len(distance_matrix)}, names: {names}, part: {part}")
    for row_index, row in enumerate(part):
        sub_matr.append([])
        sub_names.append(names[part[row_index]])
        for col_index, item in enumerate(part):
            sub_matr[row_index].append(distance_matrix[part[row_index]][part[col_index]])
    return (sub_matr, sub_names)


class PhyloTree:
    def __init__(self, distance_matrix, names):
        assert len(distance_matrix) > 0
        if len(distance_matrix) == 1:
            self.index = distance_matrix[0][0]
            self.name = names[0]
            self.l = None
            self.r = None
        else:
            self.name = '*'
            self.cut_value, (part1, part2) = cut(distance_matrix, list(range(0, len(distance_matrix))))

            print(f"cut_value/count: {self.cut_value / len(distance_matrix)}, part1: {part1}, part2: {part2}")

            sub_matr1, sub_names1 = sub_matrix(distance_matrix, names, part1)
            self.l = PhyloTree(sub_matr1, sub_names1)
            sub_matr2, sub_names2 = sub_matrix(distance_matrix, names, part2)
            self.r = PhyloTree(sub_matr2, sub_names2)

    def to_str(self, level):
        res = ""
        pad = "\n" + ("  " * level)
        res += pad + "name: " + str(self.name)
        if not (self.l.is_none()):
            res += pad + "l: " + self.l.to_str(level + 1)
        if not (self.r.is_none()):
            res += pad + "r: " + self.r.to_str(level + 1)
        return res

    def __str__(self):
        return self.to_str(0)

# phyloTree = PhyloTree(distance_matrix, list(range(0, len(distance_matrix))))

# cut_value, partition = cut(distance_matrix, list(range(0, len(distance_matrix))))
# print(f"cut_value: {cut_value}, partition: {partition}")
