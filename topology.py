"""Module for data centre topologies."""
from abc import abstractmethod
import random
import numpy as np


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
    def n_closest(self, server, n_closest):
        """Finds the n closest servers in terms of number of hops.

        :arg
        server - main server to start the research
        n_closest - the number of closest servers to find.

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


class Jellyfish(Topology):

    def __init__(self, n, tau, capacity):
        super().__init__(n, tau, capacity)
        self.r = n // 2  # number of neighbors
        self.S = n ** 2  # number of switches
        self.switches = {i: [] for i in
                         range(self.S)}  # initialize as a dictionary: key is the index, the values are the neighbor
        self.servers = (n ** 3) // 4  # number of servers
        self.server_connections = {}  # server connections to switches
        self.build_structure()
        self.add_servers()

    def build_structure(self):

        """
        |CONSTRUCTION PROCEDURE PART 1|

        1. Create a list of switches with free ports

        2. Until there are free ports:

                a. choice 2 random switch from the list;
                b. if they are not connected and they are not the same switch:

                        -connect them adding them to the list of neighbor;

                c. if one of them reach the maximum number of neighbor r:

                        -remove from the list of switches with free ports
        """
        switches_with_free_ports = list(range(self.S))  # indexes of switches with free port

        while switches_with_free_ports != []:

            switch1 = random.choice(switches_with_free_ports)  # random choices
            switch2 = random.choice(switches_with_free_ports)

            if switch1 != switch2 and switch1 not in self.switches[
                switch2]:  # check if they are the same or already connected

                self.switches[switch1].append(switch2)  # connect them
                self.switches[switch2].append(switch1)

                if len(self.switches[switch1]) == self.r:  # check maximum number of neighbor

                    switches_with_free_ports.remove(switch1)  # no more free ports

                if len(self.switches[switch2]) == self.r:
                    switches_with_free_ports.remove(switch2)

        """
        |CONSTRUCTION PROCEDURE PART 2|

        1. Check if a switch has >= 2 free ports left, say (p1,p2)

        2. Choose a random link (x,y)

        3. Remove the link

        4. Replace the link with (p1,x) and (p2,x)

        """

        for i in range(self.S):  # iterate over the switches

            if len(self.switches[i]) <= self.r - 2:  # check for >= 2 free ports

                # choose random link
                x = random.choice(list(self.switches.keys()))  # choose one random switch
                y = random.choice(self.switches[x])  # choose one random link

                # remove link
                self.switches[x].remove(y)  # remove y from the neighbor of x
                self.switches[y].remove(x)  # remove x from the neighbor of y

                p1, p2 = i  # set p1,p2 as two port of the switch

                # add the new link
                self.switches[p1].append(x)
                self.switches[x].append(p1)
                self.switches[p2].append(y)
                self.switches[y].append(p2)

    def add_servers(self):
        server_index = 0
        # Iterate over all switches
        for switch_index in range(self.S):
            # Calculate the number of free ports on the current switch
            free_ports = self.n - len(self.switches[switch_index])
            # Connect a number of servers equal to the number of free ports to the current switch
            for _ in range(free_ports):
                if server_index < self.servers:
                    self.server_connections[server_index] = switch_index
                    server_index += 1

    def n_closest(self, server, n_closest):
        # Initialize a set to keep track of visited servers
        visited = set()
        # Initialize a queue with the starting server
        queue = [server]
        # Initialize an array to store the nearest servers
        nearest_servers = []
        # While the queue is not empty and we haven't found enough nearest servers
        while queue and len(nearest_servers) < n_closest:
            # Pop the first server from the queue
            current_server = queue.pop(0)
            # If the current server has not been visited yet
            if current_server not in visited:
                # Add it to the visited set
                visited.add(current_server)
                # Add it to the nearest servers array
                nearest_servers.append(current_server)
                # Find the switch that the current server is connected to
                switch = self.server_connections[current_server]
                # Iterate over all neighboring switches of the current switch
                for neighbor_switch in self.switches[switch]:
                    # Iterate over all servers
                    for neighbor_server in self.server_connections:
                        # If a server is connected to the neighboring switch
                        if self.server_connections[neighbor_server] == neighbor_switch:
                            # Add it to the queue to be explored later
                            queue.append(neighbor_server)
        # Return a numpy array containing the nearest servers in terms of hops
        return np.array(nearest_servers[:n_closest])

    def avg_throughput(self, server):



        pass

