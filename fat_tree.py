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
        self.main_server = None
        self.n = n
        self.n_aggregate_servers = n // 2
        self.n_edge_servers = n // 2
        self.tau = tau
        self.capacity = capacity

        self.n_servers = (n ** 3 // 4)
        self.n_servers_per_pod = self.n_servers // n
        pod_servers = np.arange(0, self.n_servers_per_pod, dtype=np.uint16)

        self.all_servers = np.tile(np.array(pod_servers, dtype=np.uint16), (n, 1))
        self.all_servers = self.all_servers.reshape(
            (n, self.n_servers_per_pod // self.n_edge_servers, self.n_edge_servers))

        broadcast_array = np.array([self.n_servers_per_pod * i for i in range(n)], dtype=np.uint16)
        broadcast_array = broadcast_array.reshape((n, 1, 1))

        self.all_servers += broadcast_array
        self.all_servers_flat = self.all_servers.flatten()
        self.n_hops_cache = np.ones(self.n_servers) * -1
        self.avg_throughput_cache = np.ones(self.n_servers) * -1
        self.round_trip_time_cache = np.ones(self.n_servers) * -1

    def set_main_server(self, server):
        self.main_server = server

    def get_n_hops(self, server):
        """Gets the number of hops between the main server and server.

        :arg
        server - the server.

        :return
        an integer that is the number hops.
        """
        return self.n_hops_cache[server]

    def in_same_pod(self, server):
        """Checks whether two servers are in the same pod in a fat-tree.

        :arg
        i - the first server.
        j - the second server.

        :return
        True if servers i and j are in the same pod, False otherwise.
        """
        main_pod_number = self.main_server // self.n_servers_per_pod
        server_pod_number = server // self.n_servers_per_pod

        return main_pod_number == server_pod_number

    def avg_throughput(self, server, servers):
        """Calculates the average throughput between the main server and server.

        :arg
        i - the first server.
        j - the second server.

        :return
        the average throughput in Gbit/s.
        """
        if self.avg_throughput_cache[server] != -1:
            return self.avg_throughput_cache[server]

        throughput = self.capacity \
                     * (1 / self.round_trip_time(server)) \
                     / sum([1 / self.round_trip_time(server) for server in servers])

        self.avg_throughput_cache[server] = throughput
        return throughput

    def round_trip_time(self, server):
        """Calculates the round trip time between two servers.

        :arg
        i - the first server.
        j - the second server.

        :return
        the round trip time between two servers in microseconds.
        """
        if self.round_trip_time_cache[server] != -1:
            return self.round_trip_time_cache[server]

        time = 2 * self.tau * self.get_n_hops(server)
        self.round_trip_time_cache[server] = time
        return time


    def n_closest(self, server: int, n_closest: int):
        """Finds the n closest servers in terms of number of hops.

        :arg
        server - the server from which to find the closest neighbours from.
        """

        pod_number = server // self.n_servers_per_pod
        edge_number = server % self.n_servers_per_pod // self.n_edge_servers

        # get all servers from the pod and more
        if n_closest > self.n_servers_per_pod:
            # pick the pod
            # get leftovers
            # distribute over or below
            pod_servers = self.all_servers[pod_number].flatten()
            edge_servers = self.all_servers[pod_number, edge_number]
            start, end = pod_servers[0], pod_servers[self.n_servers_per_pod - 1]

            n_remaining_servers = n_closest - self.n_servers_per_pod + 1

            below = min(start, n_remaining_servers)
            above = n_remaining_servers - below
            closest_servers = self.all_servers_flat[start - below:end + above + 1]
            closest_servers = closest_servers[closest_servers != server]
            self._set_hop_cache(closest_servers, 6)
            self._set_hop_cache(pod_servers, 4)
            self._set_hop_cache(edge_servers, 2)
            return closest_servers

        # get all servers from the edge switch and more
        if n_closest > self.n_edge_servers:
            edge_servers = self.all_servers[pod_number, edge_number]
            pod_servers = self.all_servers[pod_number].flatten()
            pod_start, pod_end = pod_servers[0], pod_servers[self.n_servers_per_pod - 1]

            start, end = edge_servers[0], edge_servers[self.n_edge_servers - 1]

            n_remaining_servers = n_closest - self.n_edge_servers + 1
            # restrict to servers in the same pod
            # find the start of the pod
            # find how much space we have before
            below = min(start - pod_start, n_remaining_servers)
            above = n_remaining_servers - below
            closest_servers = self.all_servers_flat[start - below: end + above + 1]
            closest_servers = closest_servers[closest_servers != server]
            self._set_hop_cache(closest_servers, 4)
            self._set_hop_cache(edge_servers, 2)
            return closest_servers

        # get from a single edge
        edge_servers = self.all_servers[pod_number, edge_number]

        edge_start, edge_end = edge_servers[0], edge_servers[self.n_edge_servers - 1]

        below = min(server - edge_start, n_closest)
        above = n_closest - below

        closest_servers = np.array([i for i in range(server - below, server + above + 1) if i != server])
        closest_servers = closest_servers[closest_servers != server]
        self._set_hop_cache(closest_servers, 2)
        return closest_servers

    def _set_hop_cache(self, servers, hops):
        self.n_hops_cache[servers] = hops

    def _set_avg_throughput_cache(self, servers, throughput):
        for s in servers:
            self.avg_throughput_cache[s] = throughput

    def _calc_avg_throughput(self, server, servers):
        throughput = self.capacity \
                     * (1 / self.round_trip_time(server)) \
                     / sum([1 / self.round_trip_time(server) for server in servers])

        return throughput
