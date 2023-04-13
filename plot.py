"""Module for plotting."""

import numpy as np
import matplotlib.pyplot as plt


def plot_connectivity_complexity(k: np.array, time: np.array, title: str):
    """Plots the time as a function of the number nodes in a graph.

    :arg
    k - the np.array to be plotted on the x-axis.
    time - the np.array to be plotted on the y-axis.

    :return
    None
    """
    plt.plot(k, time)
    plt.title(title)
    plt.ylabel("Time in s")
    plt.xlabel("Number of nodes in graph")
    plt.show()
