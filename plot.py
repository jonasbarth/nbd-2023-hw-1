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


def plot_response_time(servers, response_times: [np.array], labels: [str],optimal_servers):
    """Plots the expected response time."""
    fig, ax = plt.subplots(1)

    for response_time, label, optimal_server in zip(response_times, labels, optimal_servers):
        ax.plot(servers, response_time, label=label)
        ax.axvline(x=optimal_server, ls="--", label="Optimal Servers")
        ax.text(x=optimal_server * 0.90, y=np.max(response_times), s=optimal_server)

    ax.set(title="Normalised Response Time", ylabel="Response Time", xlabel="Number of Servers")
    ax.legend()

    return fig, ax

def plot_job_running_cost(servers,costs):
    """Creates a figure for the running cost."""
    fig, ax = plt.subplots(1)

    ax.plot(servers, costs)
    ax.set(title="Normalised Job Running Cost", ylabel="running cost", xlabel="number of servers")

    return fig, ax

def plot_job_running_cost_t(servers, costs, labels, opt_n):

    fig, ax = plt.subplots(1)
    for cost, label, optimal in zip(costs, labels, opt_n):
        ax.plot(servers, cost, label=label)
        ax.axvline(x=optimal, ls="--", label="Optimal Servers")
        ax.text(x=optimal+100, y=np.max(costs), s=optimal)
    ax.set(title="Normalised Job Running Cost", ylabel="Job Running Cost", xlabel="Number of Servers")
    ax.legend()
    return fig, ax