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

    def _get_edge_servers(self, server, n, pod_number):

        edge_number = server % self.n_servers_per_pod // self.n_edge_servers
        edge_servers = self.all_servers[pod_number, edge_number]
        edge_servers = np.delete(edge_servers, np.argwhere(edge_servers == server))

        edge_server_throughput = self._calc_avg_throughput(edge_servers[0], edge_servers)
        self._set_avg_throughput_cache(edge_servers, edge_server_throughput)
        self._set_hop_cache(edge_servers, 2)
        n_edge_servers = min(n, edge_servers.shape[0])

        return edge_servers[0:n_edge_servers], n_edge_servers

    def _get_pod_servers(self, pod_number, edge_servers, n_pod_servers):
        pod_servers = self.all_servers[pod_number].flatten()
        pod_servers = pod_servers[~np.isin(pod_servers, edge_servers)]
        pod_servers = pod_servers[0:n_pod_servers]

        pod_server_throughput = self._calc_avg_throughput(pod_servers[0], pod_servers)
        self._set_avg_throughput_cache(pod_servers, pod_server_throughput)
        self._set_hop_cache(pod_servers, 4)

        return pod_servers

    def n_closest(self, server: int, n_closest: int):
        """Finds the n closest servers in terms of number of hops.

        :arg
        server - the server from which to find the closest neighbours from.
        """
        pod_number = server // self.n_servers_per_pod

        # get the edge switch
        edge_number = server % self.n_servers_per_pod // self.n_edge_servers

        n_edge_servers = min(n_closest, self.n_edge_servers - 1)

        # pick only edge servers
        edge_servers = self.all_servers[pod_number, edge_number][:n_edge_servers + 1]

        start, end = edge_servers[0], edge_servers[n_edge_servers]

        if n_closest - n_edge_servers == 0:
            return np.array([i for i in range(start, end + 1) if i != server], dtype=np.unit16)
        # get the start server

        pod_number = server // self.n_servers_per_pod

        remaining_servers = n_closest - n_edge_servers

        n_pod_servers = min(remaining_servers, self.n_servers_per_pod - 1)

        pod_servers = self.all_servers[pod_number].flatten()[:n_pod_servers + 1]




        closest_servers = np.ones(n_closest, dtype=np.uint16)

        edge_servers, n_edge_servers = self._get_edge_servers(server, n_closest, pod_number)

        closest_servers[0:n_edge_servers] = edge_servers[0:n_edge_servers]

        if n_closest <= n_edge_servers:
            return closest_servers[0:n_edge_servers]

        n_remaining_servers = n_closest - n_edge_servers

        # either the entire pod, or a fraction of it
        n_pod_servers = np.min((n_remaining_servers, self.n_servers_per_pod - n_edge_servers))
        pod_servers = self._get_pod_servers(pod_number, edge_servers, n_pod_servers)
        n_remaining_servers = n_closest - n_edge_servers - n_pod_servers

        closest_servers[n_edge_servers:n_edge_servers + n_pod_servers] = n_pod_servers

        if n_remaining_servers == 0:
            return closest_servers[0:n_edge_servers + n_pod_servers]

        remaining_servers = self.all_servers.flatten()
        remaining_servers = remaining_servers[~np.isin(remaining_servers, edge_servers)]
        remaining_servers = remaining_servers[~np.isin(remaining_servers, server)]
        remaining_servers = remaining_servers[~np.isin(remaining_servers, pod_servers)]

        rest_servers = remaining_servers[0:n_remaining_servers]

        remaining_server_throughput = self._calc_avg_throughput(remaining_servers[0], remaining_servers)
        self._set_avg_throughput_cache(remaining_servers, remaining_server_throughput)
        self._set_hop_cache(rest_servers, 6)

        closest_servers[n_edge_servers + n_pod_servers:n_edge_servers + n_pod_servers + n_remaining_servers] = rest_servers

        return closest_servers[0:n_edge_servers + n_pod_servers + n_remaining_servers]

    def _set_hop_cache(self, servers, hops):
        for s in servers:
            self.n_hops_cache[s] = hops

    def _set_avg_throughput_cache(self, servers, throughput):
        for s in servers:
            self.avg_throughput_cache[s] = throughput

    def _calc_avg_throughput(self, server, servers):
        throughput = self.capacity \
                     * (1 / self.round_trip_time(server)) \
                     / sum([1 / self.round_trip_time(server) for server in servers])

        return throughput

    def t(self):
        # get the pod
        pass
        """
        pod_number = server // self.n_servers_per_pod

        # get the edge switch
        edge_number = server % self.n_servers_per_pod // self.n_edge_servers

        # get the start server
        start_idx = self.all_servers[pod_number, edge_number][0]

        # get the end server
        end_edge_server = min(n_closest, self.n_edge_servers)
        end_idx = self.all_servers[pod_number, edge_number][end_edge_server]

        n_closest -= end_edge_server - start_idx
        if n_closest == 0:
            return self.all_servers.flatten()[start_idx:end_idx]
        """