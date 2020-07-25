import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from src.compare_trees.global_params import GlobalParams
from src.diff_with_systematic.matrix_diff import MatrixDiff, print_matrix, make_experiment_array, to_full_matrix, \
    corrcoef
import scipy.spatial.distance as ssd

from src.ultra_metric.ultra_metric import get_ultra_metric, UltraMetricParams


def draw_plot(clustered_trees, names, plot_name, filename):
    plt.rcParams["figure.figsize"] = (12.5, 8)
    plt.rcParams["figure.dpi"] = 80
    fig = plt.figure()

    ax1 = fig.add_axes((0.13, 0.1, 0.84, 0.85))
    ax1.set_title(plot_name)
    ax1.set_xlabel("distance, Minarskys")

    hierarchy.dendrogram(clustered_trees,
                         #labels=np.array([x.split('_')[0] + ' ' + x.split('_')[1][:5] for x in names], np.str),
                         labels=np.array([x for x in names], np.str),
                         orientation='right', count_sort='ascending', distance_sort='ascending')
    fig.savefig(filename)
    plt.close(fig)
    #plt.show()


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
    #print_matrix(matr, f"clustered matr", names, corr, with_headers=True)
    return corr