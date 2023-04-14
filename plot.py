"""Module for plotting."""

import numpy as np
import matplotlib.pyplot as plt
import complexity
import connectivity


def plot_time_complexity(time_complexity: list[complexity.TimeComplexity], labels: [str], title: str):
    """Plots the time as a function of the number nodes in a graph.

    :arg
    k - the np.array to be plotted on the x-axis.
    time - the np.array to be plotted on the y-axis.

    :return
    None
    """
    for t_c, label in zip(time_complexity, labels):
        plt.plot(t_c.n_nodes, t_c.times, label=label)

    plt.title("Connectivity Algorithm Complexity")
    plt.ylabel("Time in s")
    plt.xlabel("Number of nodes in graph")
    plt.legend()
    plt.show()


def plot_connectivity_prob(connectivity_prob: list[connectivity.Connectivity], labels: [str], title: str, xlabel: str):
    """Plots the connectivity.

    :arg
    connectivity_prob - a list of Connectivity named tuples.
    labels - a list of labels.
    title - the title of the plot.
    """
    for connec, label in zip(connectivity_prob, labels):
        plt.plot(connec.x, connec.probs, label=label)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Connectivity Probability")
    if len(connectivity_prob) > 1:
        plt.legend()

    plt.show()
