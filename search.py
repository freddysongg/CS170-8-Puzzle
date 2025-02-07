""" 
    Purpose: Implement the search algorithms + heuristics
"""

import time
from collections import defaultdict
from queue import PriorityQueue
from node import Node


TIMEOUT = int(600)  # 10 minutes


def generic_search(puzzle, algorithm, timeout=TIMEOUT):
    start = time.time()
    expanded_nodes = 0
    max_queue_size = 1
    depth = defaultdict(int)

    heuristic_cost = 0
    if algorithm == a_star_misplaced:
        heuristic_cost = puzzle.calculate_misplaced_tile_heuristic(puzzle.initial_state)
    elif algorithm == a_star_manhattan:
        heuristic_cost = puzzle.calculate_manhattan_distance_heuristic(
            puzzle.initial_state
        )

    initial_node = Node(
        state=puzzle.initial_state, path_cost=0, heuristic_cost=heuristic_cost
    )
    nodes = PriorityQueue()
    nodes.put((initial_node.total_cost(), initial_node))

    while not nodes.empty():
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

        if puzzle.goal_test(node.state):
            metrics = {
                "expanded_nodes": expanded_nodes,
                "max_queue_size": max_queue_size,
                "time": time.time() - start,
                "timed_out": False,
            }
            node.update_metrics(expanded_nodes, max_queue_size)
            return node, depth, metrics

        current_queue_size = nodes.qsize()
        if current_queue_size > max_queue_size:
            max_queue_size = current_queue_size

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
                child_heuristic = 0

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
