"""Module for a Fat Tree data centre topology structure."""
import numpy as np

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
        self.n_aggregate_servers = n // 2
        self.n_edge_servers = n // 2
        self.tau = tau
        self.capacity = capacity

        self.n_servers = (n ** 3 // 4)
        self.n_servers_per_pod = self.n_servers // n
        pod_servers = np.arange(0, self.n_servers_per_pod, dtype=np.int32)

        self.all_servers = np.tile(np.array(pod_servers), (n, 1))
        self.all_servers = self.all_servers.reshape((n, self.n_servers_per_pod // self.n_edge_servers, self.n_edge_servers))

        broadcast_array = np.array([self.n_servers_per_pod * i for i in range(n)])
        broadcast_array = broadcast_array.reshape((n, 1, 1))

        self.all_servers += broadcast_array

        self.n_hops_cache = np.ones(self.n_servers) * -1
        self.avg_throughput_cache = np.ones(self.n_servers) * -1
        self.round_trip_time_cache = np.ones(self.n_servers) * -1

    def get_n_hops(self, i, j):
        """Gets the number of hops between two nodes.

        :arg
        i - the first server.
        j - the second server.

        :return
        an integer that is the number hops.
        """
        return self.n_hops_cache[j]

    def in_same_pod(self, i, j):
        """Checks whether two servers are in the same pod in a fat-tree.

        :arg
        i - the first server.
        j - the second server.

        :return
        True if servers i and j are in the same pod, False otherwise.
        """
        i_pod_number = i // self.n_servers_per_pod
        j_pod_number = j // self.n_servers_per_pod

        return i_pod_number == j_pod_number

    def share_edge_server(self, i, j):
        """Checks whether two servers share the same edge server in a fat-tree.

        Assumes that servers are ordered sequentially from 1 to N.

        :arg
        i - the first server.
        j - the second server.

        :return
        True if the servers i and j are in the same pod and if they share an edge server, False otherwise.
        """
        i_edge_number = i // self.n_edge_servers
        j_edge_number = j // self.n_edge_servers

        return self.in_same_pod(i, j) and i_edge_number == j_edge_number

    def avg_throughput(self, i, j, n_servers):
        """Calculates the average throughput between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the average throughput in Gbit/s.
        """
        if self.avg_throughput_cache[j] != -1:
            return self.avg_throughput_cache[j]

        throughput = self.capacity \
            * (1 / self.round_trip_time(i, j)) \
            / sum([1 / self.round_trip_time(i, k) for k in range(n_servers)])

        self.avg_throughput_cache[j] = throughput
        return throughput

    def round_trip_time(self, i, j):
        """Calculates the round trip time between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the round trip time between two servers in microseconds.
        """
        if self.round_trip_time_cache[j] != -1:
            return self.round_trip_time_cache[j]

        time = 2 * self.tau * self.get_n_hops(i, j)
        self.round_trip_time_cache[j] = time
        return time

    def n_closest(self, server, n_closest):
        """Finds the n closest servers in terms of number of hops.

        :arg
        server - the server from which to find the closest neighbours from.
        """

        pod_number = server // self.n_servers_per_pod
        edge_number = server % self.n_edge_servers
        edge_servers = self.all_servers[pod_number, edge_number]
        edge_servers = np.delete(edge_servers, np.argwhere(edge_servers == server))

        self._set_hop_cache(edge_servers, 2)
        n_edge_servers = edge_servers.shape[0]

        if n_closest <= n_edge_servers:
            return edge_servers[0:n_closest]

        n_remaining_servers = n_closest - n_edge_servers

        # either the entire pod, or a fraction of it
        n_pod_servers = np.min((n_remaining_servers, self.n_servers_per_pod - n_edge_servers))
        pod_servers = self.all_servers[pod_number].flatten()
        pod_servers = pod_servers[~np.isin(pod_servers, edge_servers)]
        pod_servers = pod_servers[0:n_pod_servers]

        self._set_hop_cache(pod_servers, 3)
        n_remaining_servers = n_closest - n_edge_servers - n_pod_servers

        if n_remaining_servers == 0:
            return np.hstack((edge_servers, pod_servers))

        remaining_servers = self.all_servers.flatten()
        remaining_servers = remaining_servers[~np.isin(remaining_servers, edge_servers)]
        remaining_servers = remaining_servers[~np.isin(remaining_servers, server)]
        remaining_servers = remaining_servers[~np.isin(remaining_servers, pod_servers)]

        rest_servers = remaining_servers[0:n_remaining_servers]

        self._set_hop_cache(rest_servers, 6)

        return np.hstack((edge_servers, pod_servers, rest_servers))

    def _set_hop_cache(self, servers, hops):
        for s in servers:
            self.n_hops_cache[s] = hops
