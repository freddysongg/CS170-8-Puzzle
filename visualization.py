"""
    Purpose: Implement the matplotlib data visualization graphs
"""

import matplotlib.pyplot as plt


def plot_metrics(data, algo):
    expanded_nodes = data["expanded_nodes"]
    max_queue_size = data["max_queue_size"]
    solution_depth = data["solution_depth"]

    fig, ax = plt.subplots(figsize=(10, 6))

    metrics = ["Nodes Expanded", "Max Queue Size", "Solution Depth"]
    values = [expanded_nodes, max_queue_size, solution_depth]

    bars = ax.bar(metrics, values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
        )

    ax.set_title(f"Search Metrics - {algo}")
    ax.set_ylabel("Count")
    ax.set_xlabel("Metric")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(f"{algo}_metrics.png")
    plt.show()


def plot_time_vs_depth(results):
    plt.figure(figsize=(10, 6))
    for algo_name, data in results.items():
        depths = data["depths"]
        times = data["times"]
        s_pairs = sorted(zip(depths, times))
        s_depths, s_times = zip(*s_pairs)
        plt.plot(s_depths, s_times, label=algo_name, marker="o")
    plt.xlabel("Solution Depth")
    plt.ylabel("Time (seconds)")
    plt.title("Time vs. Solution Depth by Algorithm")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_vs_depth.png")
    plt.show()


def plot_nodes_vs_depth(results):
    plt.figure(figsize=(10, 6))
    for algo_name, data in results.items():
        depths = data["depths"]
        nodes = data["nodes"]
        s_pairs = sorted(zip(depths, nodes))
        s_depths, s_nodes = zip(*s_pairs)
        plt.plot(s_depths, s_nodes, label=algo_name, marker="o")
    plt.xlabel("Solution Depth")
    plt.ylabel("Nodes Expanded")
    plt.title("Nodes Expanded vs. Solution Depth by Algorithm")
    plt.legend()
    plt.grid(True)
    plt.savefig("nodes_vs_depth.png")
    plt.show()


def plot_max_queue_vs_depth(results):
    plt.figure(figsize=(10, 6))
    for algo_name, data in results.items():
        depths = data["depths"]
        queue = data["queue"]
        s_pairs = sorted(zip(depths, queue))
        s_depths, s_queue = zip(*s_pairs)
        plt.plot(s_depths, s_queue, label=algo_name, marker="o")
    plt.xlabel("Solution Depth")
    plt.ylabel("Max Queue Size")
    plt.title("Max Queue Size (# of nodes) vs. Solution Depth by Algorithm")
    plt.legend()
    plt.grid(True)
    plt.savefig("max_queue_size_vs_depth.png")
    plt.show()
