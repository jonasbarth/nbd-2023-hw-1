from collections import namedtuple

import numpy as np

from fat_tree import FatTree

TopologySimulation = namedtuple("TopologySimulation", "n_servers, tau_s, capacity_gbit, expected_job_time_s, "
                                                      "fixed_job_time_s, input_file_size_gb, output_file_size_gb, "
                                                      "overhead")



def simulate_fat_tree_response_time(sim: TopologySimulation, tree: FatTree):
    """Simulates a response time for the Fat Tree topology."""
    outbound_data_size_gb = sim.input_file_size_gb / sim.n_servers * sim.overhead

    edge_servers = tree.get_n_free_edge_servers(sim.n_servers)
    pod_servers = tree.get_n_free_pod_servers(sim.n_servers)
    core_servers = tree.get_n_free_core_servers(sim.n_servers)

    edge_exec_times_s = np.random.exponential(sim.expected_job_time_s / sim.n_servers, edge_servers) + sim.fixed_job_time_s
    pod_exec_times_s = np.random.exponential(sim.expected_job_time_s / sim.n_servers, pod_servers) + sim.fixed_job_time_s
    core_exec_times_s = np.random.exponential(sim.expected_job_time_s / sim.n_servers, core_servers) + sim.fixed_job_time_s

    edge_return_size_gb = np.random.uniform(0, 2 * sim.output_file_size_gb / sim.n_servers, size=edge_servers) * sim.overhead
    pod_return_size_gb = np.random.uniform(0, 2 * sim.output_file_size_gb / sim.n_servers, size=pod_servers) * sim.overhead
    core_return_size_gb = np.random.uniform(0, 2 * sim.output_file_size_gb / sim.n_servers, size=core_servers) * sim.overhead

    edge_round_trip_time_s = 2 * tree.tau * 2
    pod_round_trip_time_s = 2 * tree.tau * 4
    core_round_trip_time_s = 2 * tree.tau * 6

    network_throughput = sum(
        [(1 / edge_round_trip_time_s) * edge_servers, (1 / pod_round_trip_time_s) * pod_servers,
         (1 / core_round_trip_time_s) * core_servers])

    edge_throughput = calc_avg_throughput(tree.capacity, edge_round_trip_time_s, network_throughput)
    pod_throughput = calc_avg_throughput(tree.capacity, pod_round_trip_time_s, network_throughput)
    core_throughput = calc_avg_throughput(tree.capacity, core_round_trip_time_s, network_throughput)

    edge_outbound_time_s = outbound_data_size_gb / edge_throughput
    pod_outbound_time_s = outbound_data_size_gb / pod_throughput
    core_outbound_time_s = outbound_data_size_gb / core_throughput

    edge_return_times_s = edge_return_size_gb / edge_throughput
    edge_exec_times_s += edge_return_times_s + edge_outbound_time_s

    pod_return_time_s = pod_return_size_gb / pod_throughput
    pod_exec_times_s += pod_return_time_s + pod_outbound_time_s

    rest_return_time_s = core_return_size_gb / core_throughput
    core_exec_times_s += rest_return_time_s + core_outbound_time_s

    return np.max(np.hstack((edge_exec_times_s, pod_exec_times_s, core_exec_times_s)))


def calc_round_trip_time(tau, n_hops):
    return 2 * tau * n_hops


def calc_avg_throughput(capacity, round_trip_time, network_throughput):
    return capacity * (1 / round_trip_time) / network_throughput
