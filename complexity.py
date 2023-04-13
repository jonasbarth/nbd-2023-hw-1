"""Module for measuring and plotting complexity of graph connectivity algorithms."""

import timeit

import networkx as nx
import numpy as np


class TimeComplexity:
    """A class for measuring the time complexity of a graph connectivity algorithm."""

    def __init__(self, connec, create_graph):
        self.times = np.array([])
        self.n_nodes = np.array([])
        self.connec = connec
        self.create_graph = create_graph

    def _time_connectivity(self, n_exec: int, graph: nx.graph):
        """Times a connectivity function.

        :arg
        connec - a function from the connectivity module.
        n_exec - the number of executions.
        graph - an nx.graph to run the connectivity function on.

        :return
        the average execution time over n_exec executions.
        """
        return timeit.timeit(lambda: self.connec(graph), number=n_exec) / n_exec

    def time_connectivity_multiple(self, n_exec: int, start_k: int, end_k: int):
        """Times the connectivity function multiple times for graphs of different sizes.

        :arg
        create_graph - a function for creating a graph.
        n_exec - the number of executions for each single connectivity timing.
        start_k - the number of nodes in the first graph.
        end_k - the number of nodes in the last graph.

        :return
        (np.array, np.array) - a tuple where the first array is the number of nodes at each iteration and the second array
        is the time the execution took in seconds.
        """
        n_nodes = np.array([k for k in range(start_k, end_k + 1)])
        times = np.zeros((len(n_nodes)))

        for i, k in enumerate(n_nodes):
            graph = self.create_graph(k, 2)
            exec_time = self._time_connectivity(n_exec, graph)

            times[i] = exec_time

        self.n_nodes = n_nodes
        self.times = times
