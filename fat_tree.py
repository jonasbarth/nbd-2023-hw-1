"""Module for a Fat Tree data centre topology structure."""


class FatTree:
    """A FatTree."""

    def __init__(self, n, tau, capacity):
        """creates the FatTree object.

        :arg
        n - the number of ports in a server in the fat-tree.
        N - the number of servers in the fat-tree.
        tau - trip time between two nodes in the server in micro-seconds.
        capacity - the capacity of links in the fat-tree in Gbit/s.
        """
        self.n = n
        self.n_aggregate_servers = n / 2
        self.n_edge_servers = n / 2
        self.tau = tau
        self.capacity = capacity

        self.n_hops_cache = {}
        self.avg_throughput_cache = {}
        self.round_trip_time_cache = {}

    def get_n_hops(self, i, j):
        """Gets the number of hops between two nodes.

        :arg
        i - the first server.
        j - the second server.

        :return
        an integer that is the number hops.
        """
        if (i, j) in self.n_hops_cache:
            return self.n_hops_cache[(i, j)]

        if not self.in_same_pod(i, j):
            self.n_hops_cache[(i ,j)] = 6
            return 6

        if self.share_edge_server(i, j):
            self.n_hops_cache[(i, j)] = 2
            return 2

        self.n_hops_cache[(i, j)] = 3
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

    def avg_throughput(self, i, j, n_servers):
        """Calculates the average throughput between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the average throughput in Gbit/s.
        """
        if (i, j) in self.avg_throughput_cache:
            return self.avg_throughput_cache[(i, j)]

        throughput = self.capacity \
            * (1 / self.round_trip_time(i, j)) \
            / sum([self.round_trip_time(i, k) for k in range(1, n_servers + 1)])

        self.avg_throughput_cache[(i, j)] = throughput
        return throughput

    def round_trip_time(self, i, j):
        """Calculates the round trip time between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the round trip time between two servers in microseconds.
        """
        if (i, j) in self.round_trip_time_cache:
            return self.round_trip_time_cache[(i, j)]

        time = 2 * self.tau * self.get_n_hops(i, j)
        self.round_trip_time_cache[(i, j)] = time
        return time
