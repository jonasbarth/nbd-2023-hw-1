import random
import numpy as np
import matplotlib.pyplot as plt
import fat_tree
from tqdm import tqdm
from response_time import simulate_response_time

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

    baseline = expected_job_time_s + fixed_job_time_s

    tree = fat_tree.FatTree(n, tau_s, capacity_gbit)
    response_times = []

    servers = range(1, N + 1, 100)

    for n_servers in tqdm(servers):
        response_time = np.mean([simulate_response_time(n_servers, expected_job_time_s, fixed_job_time_s, tree, input_file_size_gb, output_file_size_gb, overhead) for _ in range(10)])
        response_times.append(response_time)

    plt.plot(servers, np.array(response_times) / baseline)
    plt.xlabel("Number of Servers")
    plt.ylabel("Response Time")
    plt.title("Normalised Response Time")
    plt.show()
