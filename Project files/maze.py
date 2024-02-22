import numpy as np
import random

def generateMaze(num_rows, num_cols):
    maze = np.zeros((num_rows, num_cols), dtype=int)
    visited = set()
    stack = []

    def checkValid(row, col):
        return 0 <= row < num_rows and 0 <= col < num_cols

    def unvisited(row, col):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if checkValid(nr, nc) and (nr, nc) not in visited:
                neighbors.append((nr, nc))
        return neighbors

    def mark(row, col):
        if random.random() < 0.3:
            maze[row, col] = 1  # Blocked
        else:
            maze[row, col] = 0  # Unblocked

    def backtrack():
        while stack:
            row, col = stack.pop()
            unvisited_neighbors = unvisited(row, col)
            if unvisited_neighbors:
                return unvisited_neighbors[0]
        return None

    # Choose a random start point (avoiding edges)
    start_row = random.randint(1, num_rows - 2)
    start_col = random.randint(1, num_cols - 2)
    stack.append((start_row, start_col))

    # Choose a random end point (avoiding edges and start point)
    end_row, end_col = start_row, start_col
    while (end_row, end_col) == (start_row, start_col):
        end_row = random.randint(1, num_rows - 2)
        end_col = random.randint(1, num_cols - 2)

    visited.add((start_row, start_col))
    visited.add((end_row, end_col))

    while stack:
        row, col = stack[-1]
        visited.add((row, col))

        unvisited_neighbors = unvisited(row, col)
        if unvisited_neighbors:
            next_row, next_col = unvisited_neighbors[random.randint(0, len(unvisited_neighbors) - 1)]
            visited.add((next_row, next_col))
            stack.append((next_row, next_col))
            mark(next_row, next_col)
        else:
            next_cell = backtrack()
            if next_cell:
                stack.append(next_cell)
            else:
                break  # No unvisited cells left

    # Set the start and end points in the maze
    maze[start_row, start_col] = 2  # Start point
    maze[end_row, end_col] = 3      # End point

    return maze, (start_row, start_col), (end_row, end_col)
