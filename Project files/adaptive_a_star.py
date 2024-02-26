def adaptive_a_star(maze, break_ties_smaller_g=True):
    start = None
    end = None
    expanded_nodes = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i, j] == 2:
                start = (i, j)
            elif maze[i, j] == 3:
                end = (i, j)

    pq = PriorityQueue()
    pq.put((0, start))
    visited = set()
    parent = {}
    g = {start: 0}
    h = {
        start: abs(start[0] - end[0]) + abs(start[1] - end[1])
    }  # Initial heuristic estimate

    while not pq.empty():
        current_cost, current_node = pq.get()
        expanded_nodes += 1
        if current_node == end:
            path = []
            while current_node in parent:
                path.insert(0, current_node)
                current_node = parent[current_node]
            path.insert(0, start)
            return path, expanded_nodes

        visited.add(current_node)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = current_node[0] + dr, current_node[1] + dc
            if (
                0 <= nr < len(maze)
                and 0 <= nc < len(maze[0])
                and maze[nr, nc] != 1
                and (nr, nc) not in visited
            ):
                new_cost = g[current_node] + 1
                if (nr, nc) not in g or new_cost < g[(nr, nc)]:
                    g[(nr, nc)] = new_cost
                    h[(nr, nc)] = abs(nr - end[0]) + abs(nc - end[1])  # Update heuristic
                    priority = new_cost + h[(nr, nc)]  # Using updated heuristic
                    if break_ties_smaller_g:
                        pq.put((priority, (nr, nc)))
                    else:
                        pq.put((100 * (new_cost + h[(nr, nc)]) - g[(nr, nc)], (nr, nc)))  # Use diff priority for larger g values
                    parent[(nr, nc)] = current_node

    return None, expanded_nodes


def calc():
    maze, _, _ = generateMaze(10, 10)

    path_adaptive_1, expanded_nodes = adaptive_a_star(maze, break_ties_smaller_g=True)
    print("Path found using Adaptive A* (rxc format):", path_adaptive_1)
    print("Number of expanded nodes", expanded_nodes)

    path_adaptive_2, expanded_nodes = adaptive_a_star(maze, break_ties_smaller_g=False)
    print("Path found using Adaptive A* (rxc format):", path_adaptive_2)
    print("Number of expanded nodes", expanded_nodes)

    if path_adaptive_1:
        plt.imshow(maze, cmap="binary", origin="lower")
        for node in path_adaptive_1:
            plt.plot(node[1], node[0], "ro")
        plt.colorbar()
        plt.title("Path found using Adaptive A*")
        plt.show()
    else:
        print("No path found using Adaptive A*.")

    if path_adaptive_2:
        plt.imshow(maze, cmap="binary", origin="lower")
        for node in path_adaptive_2:
            plt.plot(node[1], node[0], "ro")
        plt.colorbar()
        plt.title("Path found using Adaptive A*")
        plt.show()
    else:
        print("No path found using Adaptive A*.")

if __name__ == "__main__":
    calc()
