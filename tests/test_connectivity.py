import networkx as nx
import numpy as np

import connectivity


def test_that_graph_irreducible():
    m = np.array([[1, 0], [1, 1]])
    g = nx.from_numpy_array(m)

    assert connectivity.check_irreducibility(g)


def test_that_graph_reducible():
    m = np.array([[1, 0], [0, 1]])
    g = nx.from_numpy_array(m)

    assert not connectivity.check_irreducibility(g)


def test_laplacian_not_connected():
    m = np.array([[1, 0], [0, 1]])
    g = nx.from_numpy_array(m)

    assert not connectivity.check_laplacian(g)

def test_laplacian_connected():
    m = np.array([[1, 1], [1, 1]])
    g = nx.from_numpy_array(m)

    assert connectivity.check_laplacian(g)