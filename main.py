"""
    CS170 Project 1 - Eight Puzzle
    Freddy Song
    
    Requirements:
        - Uniform Cost Search
        - A* with the Misplaced Tile heuristic
        - A* with the Manhattan Distance heuristic
        
        This is all my work, excluding template or example code, which I reference in Dr. Keogh's example project report and project slides.
        
        Reused work: 
        - Prompting, I followed the example project prompting
    Purpose: Entry point for running the program with user input or default puzzle.
"""

from puzzle import Puzzle
from search import (
    generic_search,
    uniform_cost_search,
    a_star_misplaced,
    a_star_manhattan,
)
from test.test_cases import test_cases
from visualization import (
    plot_metrics,
    plot_time_vs_depth,
    plot_nodes_vs_depth,
    plot_max_queue_vs_depth,
)


def make_puzzle():
    """
    Function that converts user input into a puzzle state.
    Returns None if the input is invalid.
    """
    print("\nEnter your puzzle, using 0 to represent the blank space.")
    print(
        "Please enter a valid 8-puzzle configuration, delimiting numbers with spaces."
    )
    print("Press RETURN only after finishing each row.\n")

    puzzle = []
    for i in range(3):
        row = list(map(int, input(f"Enter row {i + 1}: ").split()))
        if len(row) != 3:
            raise Exception("Each row must contain exactly 3 numbers.")
        puzzle.append(row)

        # Make sure that the puzzle contains numbers 0 to 8 by flatenning the puzzle
        flattened = [num for row in puzzle for num in row]
        if sorted(flattened) != list(range(9)):
            raise Exception(
                "The puzzle must include all numbers from 0 to 8 with no duplicates."
            )

        return puzzle


def test():
    """
    Function that runs the test cases and visualizes the results.
    """
    algorithms = [
        ("A* Manhattan", a_star_manhattan),
        ("A* Misplaced Tile", a_star_misplaced),
        ("Uniform Cost Search", uniform_cost_search),
    ]

    results = {
        "A* Manhattan": {"depths": [], "times": [], "nodes": [], "queue": []},
        "A* Misplaced Tile": {"depths": [], "times": [], "nodes": [], "queue": []},
        "Uniform Cost Search": {"depths": [], "times": [], "nodes": [], "queue": []},
    }

    # Loop through each test case
    for test_case in test_cases:
        initial_state = test_case["initial_state"]
        expected_depth = test_case["depth"]
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        puzzle = Puzzle(initial_state, goal_state)

        # Loop through each algorithm
        for algo_name, algo in algorithms:
            result, depth_data, metrics = generic_search(puzzle, algo)

            if result is None:
                print(f"No solution found for {algo_name} on depth {expected_depth}")
                continue

            results[algo_name]["depths"].append(expected_depth)
            results[algo_name]["times"].append(metrics["time"])
            results[algo_name]["nodes"].append(metrics["expanded_nodes"])
            results[algo_name]["queue"].append(metrics["max_queue_size"])

    # Plot data
    plot_time_vs_depth(results)
    plot_nodes_vs_depth(results)
    plot_max_queue_vs_depth(results)


def main():
    print("Welcome to my 8-Puzzle Solver!")
    print(
        "Type '1' to use the default puzzle,'2' to create your own, or '3' to run the experiments."
    )

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            # Default puzzle
            initial_state = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]
        elif choice == 2:
            # Custom puzzle
            initial_state = make_puzzle()
            if initial_state is None:
                print("Failed to input a valid puzzle. Exiting.")
                return
        elif choice == 3:
            # Run test cases of depth 0-24
            test()
            return
        else:
            print("Invalid choice! Please enter '1' or '2'.")
            return
    except ValueError:
        print("Invalid input! Please enter '1' or '2'.")
        return

    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    puzzle = Puzzle(initial_state, goal_state)

    print("\nSelect algorithm:")
    print("(1) Uniform Cost Search")
    print("(2) A* with Misplaced Tile Heuristic")
    print("(3) A* with Manhattan Distance Heuristic")

    choice = int(input("Please enter your choice: "))
    if choice == 1:
        # Use Uniform Cost Search
        result, depth, ucs_metrics = generic_search(puzzle, uniform_cost_search)
    elif choice == 2:
        # Use A* with Misplaced Tile Heuristic
        result, depth, misplaced_metrics = generic_search(puzzle, a_star_misplaced)
    elif choice == 3:
        # Use A* with Manhattan Distance Heuristic
        result, depth, manhattan_metrics = generic_search(puzzle, a_star_manhattan)
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")
        return

    # Metrics for data visualization
    metrics = {
        "solution_depth": 0,
        "expanded_nodes": 0,
        "max_queue_size": 0,
        "execution_time": 0,
    }

    if result is None:
        print("No solution found.")
    else:
        print("\nGoal state!")

        metrics["solution_depth"] = len(result.get_soln()) - 1
        metrics["expanded_nodes"] = result.expanded_nodes
        metrics["max_queue_size"] = result.max_queue_size

        print(f"The solution depth was {metrics['solution_depth']}")
        print(f"Number of nodes expanded: {metrics['expanded_nodes']}")
        print(f"Max queue size: {metrics['max_queue_size']}")
        print("\nSolution Path:")
        for state, action, g, h in result.get_soln():
            print(f"The best state to expand with a g(n) = {g} and h(n) = {h} is...")
            for row in state:
                print(row)
            print()

        # Visualize the metrics (optional)
        algo = ""
        if choice == 1:
            algo = "Uniform Cost Search"
        elif choice == 2:
            algo = "A* with Misplaced Tile Heuristic"
        elif choice == 3:
            algo = "A* with Manhattan Distance Heuristic"

        # plot_metrics(metrics, algo)


if __name__ == "__main__":
    main()
