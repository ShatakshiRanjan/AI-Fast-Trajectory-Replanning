from queue import PriorityQueue

import matplotlib.pyplot as plt
import numpy as np
from maze import generateMaze

def backward_astar(maze, break_ties_smaller_g=True):
    end = None
    start = None

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                start = (i, j)
            elif maze[i][j] == 3:
                end = (i, j)
    
    pq = PriorityQueue()
    pq.put((0, end))
    visited = set()
    parent = {}
    g = {end: 0}  # g value for end node is 0

    while not pq.empty():
        current_cost, current_node = pq.get()
        if current_node == start: 
            path = []
            while current_node in parent:  # backtracking
                path.append(current_node)
                current_node = parent[current_node]
            path.insert(0, end)
          #  path.append(end)  
            return path
          #  return path[::-1]  

        visited.add(current_node)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = current_node[0] + dr, current_node[1] + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != 1 and (nr, nc) not in visited:
                new_cost = g[current_node] + 1
                if (nr, nc) not in g or new_cost < g[(nr, nc)]:
                    g[(nr, nc)] = new_cost
                    priority = new_cost + abs(nr - start[0]) + abs(nc - start[1])
                    if not break_ties_smaller_g:
                        priority = 100 * new_cost - g[(nr, nc)]  # Modify priority for larger g-values
                    pq.put((priority, (nr, nc)))
                    parent[(nr, nc)] = current_node

    return None


def calc():
    # Generate maze using generateMaze from the maze module
    maze, _, _ = generateMaze(10, 10)  # Adjust the maze size as needed

    # Run backward A* with ties broken in favor of smaller g-values
    path_smaller_g = a_star(maze, break_ties_smaller_g=True)
    print("Path found with ties broken for smaller g-values:", path_smaller_g)

    # Run backward A* with ties broken in favor of larger g-values
    path_larger_g = a_star(maze, break_ties_smaller_g=False)
    print("Path found with ties broken for larger g-values:", path_larger_g)

    if path_smaller_g and path_larger_g:
        # Visualize the maze with both paths
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title("Path with ties broken for smaller g-values")
        plt.imshow(maze, cmap='binary', origin='lower')
        for node in path_smaller_g:
            plt.plot(node[1], node[0], 'ro')  # Plotting the path
        plt.colorbar()

        plt.subplot(1, 2, 2)
        plt.title("Path with ties broken for larger g-values")
        plt.imshow(maze, cmap='binary', origin='lower')
        for node in path_larger_g:
            plt.plot(node[1], node[0], 'ro')  # Plotting the path
        plt.colorbar()

        plt.tight_layout()
        plt.show()
    else:
        print("No path found for at least one version of A*.")

if __name__ == "__main__":
    calc()
