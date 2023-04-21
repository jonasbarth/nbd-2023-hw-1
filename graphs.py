"""Module for creating graphs."""

import networkx as nx

def create_er_graph(k, p):
    """Creates an Erdos-Renyi random graph.

    :arg
    k - the number of nodes in the graph.
    p - the probability that any vertex pair is connected.

    :return
    an nx.graph with k nodes.
    """
    return nx.erdos_renyi_graph(k, p)

def create_regular_graph(k, node_degree):
    """Creates a random regular graph.

    :arg
    k - the number of nodes in the graph.
    deg - the degree of each node in the graph.

    :return
    an nx.graph with k nodes.
    """
    return nx.random_regular_graph(node_degree, k)