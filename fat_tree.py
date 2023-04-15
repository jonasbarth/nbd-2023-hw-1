"""Module for a Fat Tree data centre topology structure."""


class FatTree:
    """A FatTree."""

    def __init__(self, n, N, tau):
        """creates the FatTree object.

        :arg
        n - the number of ports in a server in the fat-tree.
        N - the number of servers in the fat-tree.
        tau - trip time between two nodes in the server in micro-seconds.
        """
        self.n = n
        self.n_servers = N
        self.n_aggregate_servers = n / 2
        self.n_edge_servers = n / 2
        self.tau = tau

    def get_n_hops(self, i, j):
        """Gets the number of hops between two nodes.

        :arg
        i - the first server.
        j - the second server.

        :return
        an integer that is the number hops.
        """
        if not self.in_same_pod(i, j):
            return 6

        if self.share_edge_server(i, j):
            return 2

        return 3

    def in_same_pod(self, i, j):
        """Checks whether two servers are in the same pod in a fat-tree.

        :arg
        i - the first server.
        j - the second server.

        :return
        True if servers i and j are in the same pod, False otherwise.
        """
        return (i % self.n) - (j % self.n) == 0

    def share_edge_server(self, i, j):
        """Checks whether two servers share the same edge server in a fat-tree.

        Assumes that servers are ordered sequentially from 1 to N.

        :arg
        i - the first server.
        j - the second server.

        :return
        True if the servers i and j are in the same pod and if they share an edge server, False otherwise.
        """
        return self.in_same_pod(i, j) and abs(i - j) == 1 and max(i, j) % 2 == 0

    def avg_throughput(self, i, j, capacity):
        """Calculates the average throughput between two servers.

        :arg
        i - the first server.
        j - the second server.
        capacity - the capacity of a network link in Gbit/s.

        :return
        the average throughput in Gbit/s.
        """
        return capacity \
            * (1 / self.round_trip_time(i, j)) \
            / sum([self.round_trip_time(i, k) for k in range(1, self.n_servers + 1)])

    def round_trip_time(self, i, j):
        """Calculates the round trip time between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the round trip time between two servers in microseconds.
        """
        return 2 * self.tau * self.get_n_hops(i, j)
