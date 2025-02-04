""" 
    Purpose: Implement the search algorithms + heuristics
"""

from queue import PriorityQueue
from node import Node


def generic_search(puzzle, algorithm):
    """
    General search algorithm that expands nodes based on the given queueing function.

    Args:
        problem (Puzzle): The puzzle problem instance.
        queueing_function (function): The function that determines node expansion order.

    Returns:
        Node or str: The goal node if a solution is found, or "failure" otherwise.
    """

    if algorithm == a_star_misplaced:
        heuristic_cost = puzzle.calculate_misplaced_tile_heuristic(puzzle.initial_state)
    elif algorithm == a_star_manhattan:
        heuristic_cost = puzzle.calculate_manhattan_distance_heuristic(
            puzzle.initial_state
        )
    else:
        heuristic_cost = 0  # For UCS

    # MAKE-QUEUE(MAKE-NODE(problem.INITIAL-STATE))
    initial_node = Node(
        state=puzzle.initial_state, path_cost=0, heuristic_cost=heuristic_cost
    )
    nodes = PriorityQueue()
    nodes.put((initial_node.total_cost(), initial_node))

    while True:
        # if EMPTY(nodes) then return "failure"
        if nodes.empty():
            return None

        # node = REMOVE-FRONT(nodes)
        _, node = nodes.get()
        expanded_nodes += 1

        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        if puzzle.goal_test(node.state):
            return node

        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        for successor_state, action in puzzle.get_children(node.state):
            if algorithm == a_star_misplaced:
                child_heuristic = puzzle.calculate_misplaced_tile_heuristic(
                    successor_state
                )
            elif algorithm == a_star_manhattan:
                child_heuristic = puzzle.calculate_manhattan_distance_heuristic(
                    successor_state
                )
            else:
                child_heuristic = 0  # UCS has no heuristic

            child = Node(
                state=successor_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + 1,
                heuristic_cost=child_heuristic,
            )

            # Add child node to queue using the user selected strategy
            nodes = algorithm(nodes, child, puzzle)


def uniform_cost_search(pQueue, child, puzzle=None):
    # Priority is assigned as g(n)
    pQueue.put((child.path_cost, child))
    return pQueue


def a_star_misplaced(pQueue, child, puzzle=None):
    # Calculate heuristic cost using misplaced tile heuristic
    priority = child.total_cost()
    pQueue.put((priority, child))
    return pQueue


def a_star_manhattan(pQueue, child, puzzle):
    # Calculate heuristic cost using Manhattan distance heuristic
    heuristic_cost = puzzle.manhattan_distance_heuristic(child.state)
    total_cost = child.path_cost + heuristic_cost
    pQueue.put((total_cost, child))
    return pQueue
