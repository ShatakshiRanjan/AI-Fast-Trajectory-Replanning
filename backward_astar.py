from queue import PriorityQueue

def backward_astar(maze, break_ties_smaller_g=True):
    # Find the start (value 2) and end (value 3) positions in the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 2:
                start = (i, j)
            elif maze[i][j] == 3:
                end = (i, j)
    
    # Initialize the priority queue with the end node
    pq = PriorityQueue()
    pq.put((0, end))
    visited = set()
    parent = {}
    g = {end: 0}  # g value for end node is 0

    while not pq.empty():
        current_cost, current_node = pq.get()
        if current_node == start:  # Check if we have reached the start
            path = []
            while current_node in parent:  # Backtrack to construct the path
                path.append(current_node)
                current_node = parent[current_node]
            path.append(end)  # Add the end node
            return path[::-1]  # Reverse the path

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

# Example maze representation
# 0 - open cell
# 1 - obstacle
# 2 - start
# 3 - end

maze_example = [
    [0, 0, 0, 2],
    [0, 1, 1, 0],
    [0, 1, 3, 0],
    [0, 0, 0, 0]
]

path = backward_astar(maze_example)
