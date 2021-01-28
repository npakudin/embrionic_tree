import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster import hierarchy

from src.multiple_trees.matrix_diff import corrcoef


def draw_plot(clustered_trees, names, plot_name, filename):
    plt.rcParams["figure.figsize"] = (12.5, 8)
    plt.rcParams["figure.dpi"] = 80
    fig = plt.figure()

    ax1 = fig.add_axes((0.18, 0.10, 0.79, 0.88))
    #ax1.set_title(plot_name)
    ax1.set_xlabel("Distance")

    hierarchy.dendrogram(clustered_trees,
                         labels=np.array([x.replace('_', ' ') for x in names], np.str),
                         #labels=np.array([x for x in names], np.str),
                         link_color_func=lambda k: "black",
                         orientation='right', count_sort='ascending', distance_sort='ascending')
    fig.savefig(filename)
    plt.close(fig)
    # plt.show()


def corr_clustered_trees(clustered_trees, names, src_matr):
    n = len(names)
    matr = []
    for i in range(n):
        matr.append([])
        for j in range(i):
            matr[i].append(0)

    clusters = []
    for i in range(n):
        clusters.append([i])

    for i, item in enumerate(clustered_trees):
        cluster = clusters[int(item[0])] + clusters[int(item[1])]
        clusters.append(cluster)

    for item in clustered_trees:
        c1 = clusters[int(item[0])]
        c2 = clusters[int(item[1])]
        for i in c1:
            for j in c2:
                row = max(int(i), int(j))
                col = min(int(i), int(j))
                matr[row][col] = float(item[2])

    corr = corrcoef(matr, src_matr)
    # print_matrix(matr, f"clustered matr", names, corr, with_headers=True)
    return corr
