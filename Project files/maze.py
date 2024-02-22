import numpy as np
import random
import matplotlib.pyplot as plt

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

def generateMultiple(num_mazes, maze_size):
    mazes = [generateMaze(maze_size, maze_size) for _ in range(num_mazes)]
    return mazes

# https://matplotlib.org/stable/
def visualize_maze(maze):
    plt.imshow(maze, cmap='binary', origin='lower')
    plt.colorbar()
    plt.show()

# https://numpy.org/doc/stable/reference/generated/numpy.savetxt.html
def save_maze_to_file(maze, filename):
    np.savetxt(filename, maze, fmt='%d', delimiter=',')

# Generate 50 grid world environments with unique start and end points
num_mazes = 1  # Number of mazes to generate
maze_size = 10  # Size of the maze 
mazes_with_start_end = generateMultiple(num_mazes, maze_size)

# Visualize and save the first maze with start and end points
visualize_maze(mazes_with_start_end[0][0])
save_maze_to_file(mazes_with_start_end[0][0], 'maze0.txt')

# Visualize and save the second maze with start and end points, and so on...
for i, (maze, _, _) in enumerate(mazes_with_start_end[1:], start=1):
    visualize_maze(maze)
    save_maze_to_file(maze, f'maze{i}.txt')
