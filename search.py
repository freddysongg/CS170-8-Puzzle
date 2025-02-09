""" 
    Purpose: Implement the search algorithms + heuristics
"""

import time
from collections import defaultdict
from queue import PriorityQueue
from node import Node


TIMEOUT = int(600)  # 10 minutes


def generic_search(puzzle, algorithm, timeout=TIMEOUT):
    """ 
        Generic search function that takes in a puzzle and an algorithm
        Returns the solution node, depth, and metrics
        
        Note: this function looks more complex from psuedocode but it's because I added in metrics logging/updating for data visualization
    """
    start = time.time()
    expanded_nodes = 0
    max_queue_size = 1
    depth = defaultdict(int)

    # Define heuristic cost
    heuristic_cost = 0
    if algorithm == a_star_misplaced:
        heuristic_cost = puzzle.calculate_misplaced_tile_heuristic(puzzle.initial_state)
    elif algorithm == a_star_manhattan:
        heuristic_cost = puzzle.calculate_manhattan_distance_heuristic(
            puzzle.initial_state
        )

    # Initialize the priority queue with the initial state
    initial_node = Node(
        state=puzzle.initial_state, path_cost=0, heuristic_cost=heuristic_cost
    )
    nodes = PriorityQueue()
    nodes.put((initial_node.total_cost(), initial_node))

    while not nodes.empty():
        # Check for timeout: if timed out, return None
        if time.time() - start > timeout:
            metrics = {
                "expanded_nodes": expanded_nodes,
                "max_queue_size": max_queue_size,
                "time": timeout,
                "timed_out": True,
            }
            return None, depth, metrics

        _, node = nodes.get()
        expanded_nodes += 1

        current_depth = node.path_cost
        depth[current_depth] += 1

        # Check if goal state is reached - if so, return the solution node 
        if puzzle.goal_test(node.state):
            metrics = {
                "expanded_nodes": expanded_nodes,
                "max_queue_size": max_queue_size,
                "time": time.time() - start,
                "timed_out": False,
            }
            node.update_metrics(expanded_nodes, max_queue_size)
            return node, depth, metrics

        # Update max queue size for data visualization
        current_queue_size = nodes.qsize()
        if current_queue_size > max_queue_size:
            max_queue_size = current_queue_size

        for successor_state, action in puzzle.get_children(node.state):
            # Calculate heuristic cost for child node
            if algorithm == a_star_misplaced:
                # A* with Misplaced Tile Heuristic
                child_heuristic = puzzle.calculate_misplaced_tile_heuristic(
                    successor_state
                )
            elif algorithm == a_star_manhattan:
                # A* with Manhattan Distance Heuristic
                child_heuristic = puzzle.calculate_manhattan_distance_heuristic(
                    successor_state
                )
            else:
                # Uniform Cost Search
                child_heuristic = 0

            # Create child node
            child = Node(
                state=successor_state,
                parent=node,
                action=action,
                path_cost=node.path_cost + 1,
                heuristic_cost=child_heuristic,
            )

            nodes = algorithm(nodes, child, puzzle)

    metrics = {
        "expanded_nodes": expanded_nodes,
        "max_queue_size": max_queue_size,
        "time": time.time() - start,
        "timed_out": False,
    }
    return None, depth, metrics


def uniform_cost_search(pQueue, child, puzzle=None):
    """ 
        Uniform Cost Search algorithm
        Returns the priority queue with the child node added and no heuristic cost
    """
    # Priority is assigned as g(n)
    pQueue.put((child.path_cost, child))
    return pQueue


def a_star_misplaced(pQueue, child, puzzle=None):
    """ 
        A* with Misplaced Tile Heuristic algorithm
        Returns the priority queue with the child node added and heuristic cost using the Misplaced Tile Heuristic
    """
    # Calculate heuristic cost using misplaced tile heuristic
    heuristic_cost = puzzle.calculate_misplaced_tile_heuristic(child.state)
    total_cost = child.path_cost + heuristic_cost
    pQueue.put((total_cost, child))
    return pQueue


def a_star_manhattan(pQueue, child, puzzle):
    """ 
        A* with Manhattan Distance Heuristic algorithm
        Returns the priority queue with the child node added and heuristic cost using the Manhattan Distance Heuristic
    """
    # Calculate heuristic cost using Manhattan distance heuristic
    heuristic_cost = puzzle.calculate_manhattan_distance_heuristic(child.state)
    total_cost = child.path_cost + heuristic_cost
    pQueue.put((total_cost, child))
    return pQueue
