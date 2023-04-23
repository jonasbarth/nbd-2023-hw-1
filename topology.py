"""Module for data centre topologies."""
from abc import abstractmethod


class Topology:
    """Represents a data centre topology."""

    def __init__(self, n, tau, capacity):
        self.main_server = None
        self.n = n
        self.n_servers = (n ** 3) // 4
        self.tau = tau
        self.capacity = capacity

    def set_main_server(self, server):
        """Sets the main server.

        :arg
        server - the main server of the topology.
        """
        self.main_server = server

    @abstractmethod
    def n_closest(self, n):
        """Finds the n closest servers in terms of number of hops.

        :arg
        n - the number of closest servers to find.

        :return
        a numpy array of the n closest servers to the main server.
        """
        pass

    @abstractmethod
    def avg_throughput(self, server):
        """Calculates the average throughput between the main server and the provided server.

        :arg
        i - the first server.
        j - the second server.

        :return
        the average throughput in Gbit/s.
        """
        pass
