"""
    Purpose: Define the puzzle logic -> state representation, moves, goal test
"""

class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        
    def goal_test(self, state):
        return state == self.goal_state
    
    def calculate_misplaced_tile_heuristic(self, state):
        count=0
        for i in range(3):
            for j in range(3):
                if state[i][j] != self.goal_state[i][j] and state[i][j] != 0:
                    count +=1
        return count
    
    def calculate_manhattan_distance_heuristic(self, state):
        dist = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    goal_pos = self.find_tile_position(self.goal_state, state[i][j])
                    dist += abs(i - goal_pos[0]) + abs(j - goal_pos[1])
        return dist
