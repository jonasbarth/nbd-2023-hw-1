
import complexity
import graphs
import connectivity
import plot
import numpy as np
import matplotlib.pyplot as plt
def test_complexity():
    irred_complex = complexity.TimeComplexity(connec=connectivity.check_irreducibility)

    times = irred_complex.time(graphs.create_regular_graph, 10, 3, 100)
    print(times)


def test_plot():
    lap_complex = complexity.TimeComplexity(connec=connectivity.check_laplacian, create_graph=graphs.create_regular_graph)
    irred_complex = complexity.TimeComplexity(connec=connectivity.check_irreducibility, create_graph=graphs.create_regular_graph)
    bfs_complex = complexity.TimeComplexity(connec=connectivity.check_bfs, create_graph=graphs.create_regular_graph)

    lap_complex.time(10, 3, 100)
    irred_complex.time(10, 3, 100)
    bfs_complex.time(10, 3, 100)

    plot.plot_time_complexity([irred_complex, lap_complex, bfs_complex], ["Irreducibility", "Laplacian", "BFS"])


def test_plot_prob():
    #er_connec = connectivity.er_connectivity(100, np.linspace(0.01, 1, 100), 10)
    r_connec1 = connectivity.r_random_connectivity(range(10, 101), 2, 1)
    r_connec2 = connectivity.r_random_connectivity(range(10, 101), 8, 1)

    f, a = plot.plot_connectivity_prob([r_connec1, r_connec2], ["r = 2", "r = 8"], "R-Random Graph Connectivity", "Number of Nodes")

    plt.savefig

