import random

import numpy as np

import matplotlib.pyplot as plt
import fat_tree
from tqdm import tqdm


def simulate_response_time(n_servers):
    exec_times = np.random.exponential(expected_job_time_s / n_servers, n_servers)
    exec_times += fixed_job_time_s

    main_server = np.random.randint(0, n_servers)
    n_closest_servers = tree.n_closest(main_server, n_servers)
    for i, server in enumerate(n_closest_servers):
        avg_throughput = tree.avg_throughput(main_server, server, n_servers + 1)

        outbound_data_size = input_file_size_gb / n_servers * overhead
        outbound_time = outbound_data_size / avg_throughput

        return_size = np.random.uniform(0, 2 * output_file_size_gb / n_servers) * overhead
        return_time = return_size / avg_throughput

        exec_times[i] += outbound_time + return_time

    return np.max(exec_times)


if __name__ == "__main__":

    N = 10000
    n = 64
    tau_s = 0.000005
    capacity_gbit = 10
    expected_job_time_s = 8 * 3600
    fixed_job_time_s = 30
    input_file_size_gb = 4000
    output_file_size_gb = 4000
    overhead = 1 + 48 / 1500

    baseline = np.random.exponential(expected_job_time_s) + fixed_job_time_s

    tree = fat_tree.FatTree(n, tau_s, capacity_gbit)
    response_times = []

    servers = range(1, N + 1, 10)

    for n_servers in tqdm(servers):
        response_time = np.mean([simulate_response_time(n_servers) for _ in range(10)])
        response_times.append(response_time)

    plt.plot(servers, np.array(response_times) / baseline)
    plt.xlabel("Number of Servers")
    plt.ylabel("Response Time")
    plt.title("Normalised Response Time")
    plt.show()