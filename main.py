"""
    CS170 Project 1 - Eight Puzzle
    Freddy Song
    
    Requirements:
        - Uniform Cost Search
        - A* with the Misplaced Tile heuristic
        - A* with the Manhattan Distance heuristic
        
        This is all my work, excluding template or example code.
        
    Purpose: Entry point for running the program with user input or default puzzle.
"""

from puzzle import Puzzle
from search import (
    generic_search,
    uniform_cost_search,
    a_star_misplaced,
    a_star_manhattan,
)


def make_puzzle():
    print("\nEnter your puzzle, using 0 to represent the blank space.")
    print(
        "Please enter a valid 8-puzzle configuration, delimiting numbers with spaces."
    )
    print("Press RETURN only after finishing each row.\n")

    puzzle = []
    # Collect each row of the puzzle
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


def main():
    print("Welcome to my 8-Puzzle Solver!")
    print("Type '1' to use the default puzzle, or '2' to create your own.")

    try:
        choice = int(input("Enter your choice: "))
        if choice == 1:
            # Default puzzle
            initial_state = [[5, 2, 8], [4, 1, 7], [0, 3, 6]]
        elif choice == 2:
            # Custom puzzle
            initial_state = make_puzzle()
            if initial_state is None:
                print("Failed to input a valid puzzle. Exiting.")
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
        result, data = generic_search(puzzle, uniform_cost_search)
    elif choice == 2:
        # Use A* with Misplaced Tile Heuristic
        result, data = generic_search(puzzle, a_star_misplaced)
    elif choice == 3:
        # Use A* with Manhattan Distance Heuristic
        result, data = generic_search(puzzle, a_star_manhattan)
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")
        return

    if result is None:
        print("No solution found.")
    else:
        print("\nGoal state!")


if __name__ == "__main__":
    main()
