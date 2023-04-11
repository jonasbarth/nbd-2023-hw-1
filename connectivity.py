"""Module for checking graph connectivity.

A graph is said to be connected if there is a path between any two nodes in the graph.
"""
import networkx as nx
import numpy as np


def check_irreducibility(graph: nx.graph):
    n = graph.number_of_nodes()
    adj = nx.to_numpy_array(graph)
    powers = np.arange(start=1, stop=n, step=1)

    matrix_sum = np.identity(n)
    for power in powers:
        matrix_sum = np.add(matrix_sum, np.linalg.matrix_power(adj, power))

    return np.all(matrix_sum > 0)


def check_laplacian(graph: nx.graph):
    pass


def check_bfs(graph: nx.graph):
    pass
