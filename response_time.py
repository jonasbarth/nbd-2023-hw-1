import random

import numpy as np

import matplotlib.pyplot as plt
import fat_tree
from tqdm import tqdm

if __name__ == "__main__":

    N = 1000
    n = 64
    tau = 0.000005
    capacity_gbit = 10 / 8
    expected_job_time_s = 8 * 3600
    fixed_job_time = 30
    input_file_size_gb = 4000
    output_file_size_gb = 4000
    overhead_multiplier = 1 + 48 / 1500

    tree = fat_tree.FatTree(n, tau, capacity_gbit)
    response_times = []

    for n_servers in tqdm(range(1, N + 1)):
        exec_times = np.random.exponential(expected_job_time_s / n_servers, n_servers)
        exec_times += fixed_job_time

        servers = list(range(n_servers + 1))
        main_server = random.choice(servers)
        servers.remove(main_server)

        for i, server in enumerate(servers):

            n_hops = tree.get_n_hops(main_server, server)
            avg_throughput = tree.avg_throughput(main_server, server, n_servers + 1)

            outbound_data_size = input_file_size_gb / n_servers * overhead_multiplier
            outbound_time = outbound_data_size / avg_throughput

            return_size = np.random.uniform(0, 2 * output_file_size_gb / n_servers) * overhead_multiplier
            return_time = return_size / avg_throughput

            exec_times[i] += outbound_time + return_time

        response_times.append(np.max(exec_times))

    plt.plot(np.arange(N), response_times)
    plt.show()