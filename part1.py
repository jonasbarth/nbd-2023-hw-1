"""Script for creating plots for part 1 of the assigment."""
import complexity
import connectivity
import graphs
import plot
import numpy as np

if __name__ == "__main__":

    # create complexity plots
    lap_complex = complexity.TimeComplexity(connec=connectivity.check_laplacian,
                                            create_graph=graphs.create_regular_graph)
    irred_complex = complexity.TimeComplexity(connec=connectivity.check_irreducibility,
                                              create_graph=graphs.create_regular_graph)
    bfs_complex = complexity.TimeComplexity(connec=connectivity.check_bfs, create_graph=graphs.create_regular_graph)

    n_exec = 100
    start_k = 3
    end_k = 100

    lap_complex.time(n_exec, start_k, end_k)
    irred_complex.time(n_exec, start_k, end_k)
    bfs_complex.time(n_exec, start_k, end_k)

    fig, ax = plot.plot_time_complexity(time_complexity=[irred_complex, lap_complex, bfs_complex],
                                        labels=["Irreducibility", "Laplacian", "BFS"],
                                        title="Connectivity Algorithm Complexity")
    fig.savefig("connectivity_complexity.eps", format="eps")


    # create connectivity probability plots

    r_connec1 = connectivity.r_random_connectivity(range(10, 101), 2, 10)
    r_connec2 = connectivity.r_random_connectivity(range(10, 101), 8, 10)

    fig, _ = plot.plot_connectivity_prob([r_connec1, r_connec2], ["r = 2", "r = 8"], "R-Random Graph Connectivity",
                                       "Number of Nodes")

    fig.savefig("r-random_graph_connectivity.eps", format="eps")

    er_connec = connectivity.er_connectivity(100, np.linspace(0.01, 1, 100), 10)
    fig, _ = plot.plot_connectivity_prob([er_connec], [""], "Erdos-Renyi Graph Connectivity",
                                          "p")

    fig.savefig("er-graph_connectivity.eps", format="eps")



