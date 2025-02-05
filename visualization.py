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


def compare_algorithms(algo):
    nodes_expanded = []
    max_queue_size = []
    solution_depth = []

    fig, ax = plt.subplots(figsize=(12, 8))

    bar_width = 0.25

    r1 = range(len(algo))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Plot metrics
    ax.bar(r1, nodes_expanded, width=bar_width, label="Nodes Expanded")
    ax.bar(r2, max_queue_size, width=bar_width, label="Max Queue Size")
    ax.bar(r3, solution_depth, width=bar_width, label="Solution Depth")

    # Add labels and title
    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Count")
    ax.set_title("Algorithm Performance Comparison")
    ax.set_xticks([r + bar_width for r in range(len(algo))])
    ax.set_xticklabels(algo, rotation=45)
    ax.legend()

    # Add the value labels on top of bars
    for i in range(len(algo)):
        ax.text(
            r1[i], nodes_expanded[i], str(nodes_expanded[i]), ha="center", va="bottom"
        )
        ax.text(
            r2[i], max_queue_size[i], str(max_queue_size[i]), ha="center", va="bottom"
        )
        ax.text(
            r3[i], solution_depth[i], str(solution_depth[i]), ha="center", va="bottom"
        )

    plt.tight_layout()
    plt.savefig("algorithm_comparison.png")
    plt.show()


def plot_depth_vs_nodes(ucs_data, misplaced_data, manhattan_data):
    plt.figure(figsize=(10, 6))
    max_depth = max(
        max(ucs_data.keys(), default=0),
        max(misplaced_data.keys(), default=0),
        max(manhattan_data.keys(), default=0),
    )

    depths = list(range(max_depth + 1))

    ucs_counts = [ucs_data.get(d, 0) for d in depths]
    misplaced_counts = [misplaced_data.get(d, 0) for d in depths]
    manhattan_counts = [manhattan_data.get(d, 0) for d in depths]

    plt.plot(depths, ucs_counts, label="Uniform Cost Search", marker="o")
    plt.plot(depths, misplaced_counts, label="A* (Misplaced Tile)", marker="s")
    plt.plot(depths, manhattan_counts, label="A* (Manhattan)", marker="^")

    plt.xlabel("Solution Depth")
    plt.ylabel("Nodes Expanded at Depth")
    plt.title("Nodes Expanded vs. Solution Depth for Each Algorithm")
    plt.legend()
    plt.grid(True)
    plt.xticks(depths)
    plt.savefig("node_expansion_vs_solution_depth.png")
    plt.show()
