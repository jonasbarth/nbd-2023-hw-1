"""Module for checking graph connectivity.

A graph is said to be connected if there is a path between any two nodes in the graph.
"""
import networkx as nx
import numpy as np
import random

def check_irreducibility(graph: nx.graph):
    """Checks connectivity of graph with reducibility of the graph's adjacency matrix.

    The adjacency matrix is irreducible if: I + A + A^2 + ... + A^n-1 > 0.

    :arg
    graph - a nx.graph to be checked.

    :return
    True if the graph's adjacency matrix is irreducible, false if not.
    """
    n = graph.number_of_nodes()
    adj = nx.to_numpy_array(graph)
    powers = np.arange(start=1, stop=n, step=1)

    matrix_sum = np.identity(n)
    for power in powers:
        matrix_sum = np.add(matrix_sum, np.linalg.matrix_power(adj, power))

    return np.all(matrix_sum > 0)


def check_laplacian(graph: nx.graph):
    """Checks connectivity of graph with a Laplacian matrix.

    The graph is considered connected if the 2nd smallest eigenvalue of the graph's Laplacian matrix is positive.

    :arg
    graph - a nx.graph to be checked.

    :return
    True if the graph 2nd smallest eigenvalue of the graph's Laplacian matrix is positive, false otherwise.
    """
    eigenvalues = np.sort(nx.laplacian_spectrum(graph))

    return eigenvalues[1] > 0


def check_bfs(graph: nx.graph):
    """Checks connectivity of graph with BFS.

    A graph is considered connected if the BFS traversal reaches all nodes, from any other node.

    :arg
    graph - an nx.graph to be checked.

    :return
    True if the BFS traversal reaches all nodes, False otherwise.
    """
    for start_node in graph.nodes():
        bfs_edges = nx.bfs_tree(graph, start_node).edges()
        if len(bfs_edges) != len(graph.edges()):
            return False

    return True
