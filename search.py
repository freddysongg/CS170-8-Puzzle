""" 
    Purpose: Implement the search algorithms + heuristics
"""

from collections import defaultdict
from queue import PriorityQueue
from node import Node


def generic_search(puzzle, algorithm):
    """
    General search algorithm that expands nodes based on the algorithm the user selected.
    """
    expanded_nodes = 0
    max_queue_size = 1
    depth = defaultdict(int)

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
    
    explored = set()
    explored.add(tuple(map(tuple, puzzle.initial_state)))

    while True:
        # if EMPTY(nodes) then return "failure"
        if nodes.empty():
            return None, depth

        # node = REMOVE-FRONT(nodes)
        _, node = nodes.get()
        expanded_nodes += 1
        
        # For data tracking
        current_depth = node.path_cost
        depth[current_depth] += 1

        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        if puzzle.goal_test(node.state):
            node.update_metrics(expanded_nodes, max_queue_size)
            return node, depth
        
        # Track the maximum queue size
        current_queue_size = nodes.qsize()
        if current_queue_size > max_queue_size:
            max_queue_size = current_queue_size

        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS))
        for successor_state, action in puzzle.get_children(node.state):
            state = tuple(map(tuple, successor_state))

            if state not in explored:
                explored.add(state)
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
    heuristic_cost = puzzle.calculate_manhattan_distance_heuristic(child.state)
    total_cost = child.path_cost + heuristic_cost
    pQueue.put((total_cost, child))
    return pQueue
