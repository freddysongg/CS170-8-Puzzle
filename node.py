"""
    Purpose: Define the Node class for representing search tree nodes
"""


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic_cost = heuristic_cost
        self.expanded_nodes = 0
        self.max_queue_size = 0

    def update_metrics(self, expanded_nodes, max_queue_size):
        self.expanded_nodes = expanded_nodes
        self.max_queue_size = max_queue_size

    def total_cost(self):
        # f(n) = g(n) + h(n)
        return self.path_cost + self.heuristic_cost

    def get_soln(self):
        path = []
        current = self
        # Tuple made of (state, action, path_cost, heuristic_cost)
        while current:
            path.append(
                (
                    current.state,
                    current.action,
                    current.path_cost,
                    current.heuristic_cost,
                )
            )
            current = current.parent
        # Reverse to get the path from start to goal
        return path[::-1]

    def __lt__(self, other):
        return self.total_cost() < other.total_cost()

    def __eq__(self, other):
        return self.total_cost() == other.total_cost()
