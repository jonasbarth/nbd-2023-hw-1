import random

import numpy as np

import matplotlib.pyplot as plt
import fat_tree
from tqdm import tqdm


def simulate_response_time(n_servers, expected_job_time_s, fixed_job_time_s, topology, input_file_size_gb, output_file_size_gb, overhead):
    exec_times = np.random.exponential(expected_job_time_s / n_servers, n_servers)
    exec_times += fixed_job_time_s

    outbound_data_size = input_file_size_gb / n_servers * overhead
    return_data_sizes = np.random.uniform(0, 2 * output_file_size_gb / n_servers, size=n_servers) * overhead

    main_server = np.random.randint(0, n_servers)
    topology.set_main_server(main_server)
    n_closest_servers = topology.n_closest(main_server, n_servers)
    for i, server in enumerate(n_closest_servers):
        avg_throughput = topology.avg_throughput(server, n_closest_servers) / 8

        outbound_time = outbound_data_size / avg_throughput

        return_time = return_data_sizes[i] / avg_throughput

        exec_times[i] += outbound_time + return_time

    return np.max(exec_times)
