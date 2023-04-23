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
    fig, ax = plt.subplots(1)

    for t_c, label in zip(time_complexity, labels):
        ax.plot(t_c.n_nodes, t_c.times, label=label)

    ax.set(title=title, ylabel="Time in s", xlabel="Number of nodes in graph")
    ax.legend()
    return fig, ax


def plot_connectivity_prob(connectivity_prob: list[connectivity.Connectivity], labels: [str], title: str, xlabel: str):
    """Plots the connectivity.

    :arg
    connectivity_prob - a list of Connectivity named tuples.
    labels - a list of labels.
    title - the title of the plot.
    """
    fig, ax = plt.subplots(1)

    for connec, label in zip(connectivity_prob, labels):
        ax.plot(connec.x, connec.probs, label=label)

    ax.set(title=title, xlabel=xlabel, ylabel="Connectivity Probability")
    if len(connectivity_prob) > 1:
        ax.legend()

    return fig, ax


def plot_response_time(servers, response_times):
    """Plots the expected response time."""
    fig, ax = plt.subplots(1)

    ax.plot(servers, response_times)
    ax.set(title="Normalised Response Time", xlabel="response time", ylabel="number of servers")

    return fig, ax