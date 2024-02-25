# from astar import calc

import matplotlib.pyplot as plt
import numpy as np
from astar import a_star
from maze import generateMaze


def calc(maze):
    # Generate maze using generateMaze from the maze module

    # Run A* with ties broken in favor of smaller g-values
    path_smaller_g, gs_expanded_nodes = a_star(maze, break_ties_smaller_g=True)
    print(
        "Path found with ties broken for smaller g-values (rxc format):",
        path_smaller_g,
    )
    print("Number of expanded nodes", gs_expanded_nodes)

    # Run A* with ties broken in favor of larger g-values
    path_larger_g, gg_expanded_nodes = a_star(maze, break_ties_smaller_g=False)
    print(
        "Path found with ties broken for larger g-values (rxc format):",
        path_larger_g,
    )
    print("Number of expanded nodes", gg_expanded_nodes)

    return gs_expanded_nodes, gg_expanded_nodes, path_smaller_g, path_larger_g


mazes = []
for i in range(0, 50):  # 10 mazes
    maze, _, _ = generateMaze(5, 5)
    mazes.append(maze)


def testAstar():  # returns mean # expanded nodes for g smaller and for g greater
    gs_sum = 0
    gg_sum = 0
    plt.rcParams.update({"axes.titlesize": "medium"})
    fig_height = 6 * len(mazes)
    fig, ax = plt.subplots(len(mazes), 2, figsize=(10, fig_height))
    for i in range(0, len(mazes)):  # two mazes
        gs_exp_nodes, gg_exp_nodes, path_smaller_g, path_larger_g = calc(mazes[i])

        if path_smaller_g and path_larger_g:

            ax[i, 0].set_title("Path with ties broken for smaller g-values")
            im = ax[i, 0].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_smaller_g:
                ax[i, 0].plot(node[1], node[0], "ro")
            fig.colorbar(im, ax=ax[i, 0], orientation="vertical")

            ax[i, 1].set_title("Path with ties broken for larger g-values")
            im2 = ax[i, 1].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_larger_g:
                ax[i, 1].plot(node[1], node[0], "ro")
            fig.colorbar(im2, ax=ax[i, 1], orientation="vertical")

        else:
            print("No path found for at least one version of A*.")

        gs_sum += gs_exp_nodes
        gg_sum += gg_exp_nodes

    fig.tight_layout()
    plt.show()
    return gs_sum / len(mazes), gg_sum / len(mazes)


if __name__ == "__main__":
    gs_avg, gg_avg = testAstar()
    print("G smaller average expanded nodes: ", gs_avg)
    print("G larger average expanded nodes: ", gg_avg)
