import os

import numpy as np
from tqdm import tqdm

import fat_tree
from plot import plot_response_time
from response_time import simulate_fat_tree_response_time, TopologySimulation

if __name__ == "__main__":

    if not os.path.exists('img'):
        os.makedirs('img')

    N = 10000
    n = 64
    tau_s = 0.000005
    capacity_gbit = 10
    expected_job_time_s = 8 * 3600
    fixed_job_time_s = 30
    input_file_size_gb = 4000
    output_file_size_gb = 4000
    overhead = 1 + 48 / 1500
    n_sims = 100

    baseline = expected_job_time_s + fixed_job_time_s
    tree = fat_tree.FatTree(n, tau_s, capacity_gbit)

    fat_tree_response_times = []
    servers = range(1, N + 1, 10)
    for n_servers in tqdm(servers):
        sim = TopologySimulation(n_servers, tau_s, capacity_gbit, expected_job_time_s, fixed_job_time_s, input_file_size_gb,
                                 output_file_size_gb, overhead)

        response_time = np.mean([simulate_fat_tree_response_time(sim, tree) for _ in range(n_sims)])
        fat_tree_response_times.append(response_time)

    fat_tree_response_times = np.array(fat_tree_response_times)
    optimal_servers = [servers[np.argmin(fat_tree_response_times)]]

    fig, _ = plot_response_time(servers, [fat_tree_response_times / baseline], ["Fat Tree"],optimal_servers)

    fig.savefig("img/response_time.eps", format="eps")
