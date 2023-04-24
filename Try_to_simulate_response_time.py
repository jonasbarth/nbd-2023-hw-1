import random
import numpy as np
import matplotlib.pyplot as plt
import topology
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


    tree = topology.Jellyfish(n, tau_s, capacity_gbit)

    tree.build_structure()
    tree.add_servers()

