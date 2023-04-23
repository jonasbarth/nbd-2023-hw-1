import numpy as np

from fat_tree import FatTree


def simulate_response_time(n_servers, expected_job_time_s, fixed_job_time_s, input_file_size_gb, output_file_size_gb,
                           overhead, tree: FatTree):
    outbound_data_size_gb = input_file_size_gb / n_servers * overhead

    edge_servers = tree.get_n_free_edge_servers(n_servers)
    pod_servers = tree.get_n_free_pod_servers(n_servers)
    core_servers = tree.get_n_free_core_servers(n_servers)

    edge_exec_times_s = np.random.exponential(expected_job_time_s / n_servers, edge_servers) + fixed_job_time_s
    pod_exec_times_s = np.random.exponential(expected_job_time_s / n_servers, pod_servers) + fixed_job_time_s
    core_exec_times_s = np.random.exponential(expected_job_time_s / n_servers, core_servers) + fixed_job_time_s

    edge_return_size_gb = np.random.uniform(0, 2 * output_file_size_gb / n_servers, size=edge_servers) * overhead
    pod_return_size_gb = np.random.uniform(0, 2 * output_file_size_gb / n_servers, size=pod_servers) * overhead
    core_return_size_gb = np.random.uniform(0, 2 * output_file_size_gb / n_servers, size=core_servers) * overhead

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

    for i in range(edge_servers):
        edge_return_time_s = edge_return_size_gb[i] / edge_throughput
        edge_exec_times_s[i] += edge_return_time_s + edge_outbound_time_s

    for i in range(pod_servers):
        pod_return_time_s = pod_return_size_gb[i] / pod_throughput
        pod_exec_times_s[i] += pod_return_time_s + pod_outbound_time_s

    for i in range(core_servers):
        rest_return_time_s = core_return_size_gb[i] / core_throughput
        core_exec_times_s[i] += rest_return_time_s + core_outbound_time_s

    return np.max(np.hstack((edge_exec_times_s, pod_exec_times_s, core_exec_times_s)))


def calc_round_trip_time(tau, n_hops):
    return 2 * tau * n_hops


def calc_avg_throughput(capacity, round_trip_time, network_throughput):
    return capacity * (1 / round_trip_time) / network_throughput


def calc_execution_time(n_servers, expected_job_time_s, fixed_job_time_s, round_trip_time, outbound_time):
    exec_times = np.random.exponential(expected_job_time_s / n_servers, n_servers)
    exec_times += fixed_job_time_s


