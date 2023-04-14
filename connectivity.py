"""Module for checking graph connectivity.

A graph is said to be connected if there is a path between any two nodes in the graph.
"""
from collections import namedtuple

import networkx as nx
import numpy as np

import graph


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

    bfs_edges = nx.bfs_tree(graph, list(graph)[0]).edges()
    return len(bfs_edges) == len(graph.nodes) - 1


Connectivity = namedtuple("Connectivity", "x probs")


def er_connectivity(n_nodes: int, edge_probs, repeats: int):
    """Calculates the probability of connectivity of an ER graph as a function of the probability of edge connections.

    :arg
    n_nodes - the number of nodes in the ER graph.
    edge_probs - an iterable of probabilities of edge connections.
    repeats - number of repetitions for each value in the edge_probs.

    :return
    a Connectivity namedtuple with the edge_probs as the x value and the connection probability as the probs.
    """
    connected_probs = []
    for p in edge_probs:
        connected = 0
        for _ in range(repeats):
            er_graph = graph.create_er_graph(n_nodes, p=p)
            if check_bfs(er_graph):
                connected += 1

        connected_probs.append(connected / repeats)

    return Connectivity(np.array(edge_probs), np.array(connected_probs))


def r_random_connectivity(n_nodes, node_degree, repeats):
    """Calculates the probability of connectivity of an ER graph as a function of the probability of edge connections.

    :arg
    n_nodes - the number of nodes in the r-random graph.
    node_degree - the degree of every node in the graph.
    repeats - number of repetitions for each value in n_nodes.

    :return
    a Connectivity namedtuple with the n_nodes as the x value and the connection probability as the probs.
    """
    connected_probs = []

    for k in n_nodes:
        connected = 0
        for _ in range(repeats):
            er_graph = graph.create_regular_graph(k, r=node_degree)
            if check_bfs(er_graph):
                connected += 1

        connected_probs.append(connected / repeats)

    return Connectivity(np.array(n_nodes), np.array(connected_probs))
