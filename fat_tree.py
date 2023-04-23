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
        self.main_server = None
        self.n = n
        self.n_aggregate_servers = n // 2
        self.n_edge_servers = n // 2
        self.tau = tau
        self.capacity = capacity

        self.n_servers = (n ** 3 // 4)
        self.n_servers_per_pod = self.n_servers // n

    def get_n_free_edge_servers(self, n_servers):
        return min(self.n_edge_servers - 1, n_servers)

    def get_n_free_pod_servers(self, n_servers):
        edge_servers = self.get_n_free_edge_servers(n_servers)
        return min(self.n_servers_per_pod - 1 - edge_servers, n_servers - edge_servers)

    def get_n_free_core_servers(self, n_servers):
        edge_servers = self.get_n_free_edge_servers(n_servers)
        pod_servers = self.get_n_free_pod_servers(n_servers)
        return min(self.n_servers - 1 - edge_servers - pod_servers, n_servers - edge_servers - pod_servers)