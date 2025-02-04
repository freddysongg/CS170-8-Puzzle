"""
    Purpose: Define the puzzle logic -> state representation, moves, goal test
"""


class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def goal_test(self, state):
        return state == self.goal_state

    def find_blank_tile(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == 0:
                    return i, j

    def is_valid(self, row, col):
        # We have to make sure that the move is within the 3x3 grid, no out of bound moves
        return 0 <= row < 3 and 0 <= col < 3

    def swap(self, state, row, col, new_row, new_col):
        # Make a copy to prevent modifying original states since lists are mutable
        temp = [row[:] for row in state]
        # Make the swap
        temp[row][col], temp[new_row][new_col] = (
            temp[new_row][new_col],
            temp[row][col],
        )
        return temp

    def get_children(self, state):
        row, col = self.find_blank_tile(state)

        valid_moves = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1),
        }

        children = []

        for action, (new_row, new_col) in valid_moves.items():
            if self.is_valid(new_row, new_col):
                # Make new state by swapping the blank with the target position
                temp = self.swap(state, row, col, new_row, new_col)
                children.append(
                    (temp, action)
                )  # If th emove is valid, add the new state and action to the successors

        return children

    def find_pos(self, state, tile):
        for i in range(3):
            for j in range(3):
                if state[i][j] == tile:
                    return (i, j)
        return None

    def calculate_misplaced_tile_heuristic(self, state):
        count = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != self.goal_state[i][j] and state[i][j] != 0:
                    count += 1
        return count

    def calculate_manhattan_distance_heuristic(self, state):
        dist = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    goal_pos = self.find_pos(self.goal_state, state[i][j])
                    dist += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return dist
