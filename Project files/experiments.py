import matplotlib.pyplot as plt
import numpy as np
from adaptive_a_star import adaptive_a_star
from astar import a_star
from backward_astar import backward_astar
from maze import generateMaze


def calcAStar(maze):
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


def calcBAStar(maze):
    # Run backward A* with ties broken in favor of larger g-values

    path_larger_g_a, expanded_nodes_a = a_star(maze, break_ties_smaller_g=False)

    print(
        "Repeated A* path found with ties broken for larger g-values:", path_larger_g_a
    )
    print("Repeated A* - number of expanded nodes", expanded_nodes_a)

    path_larger_g_b, expanded_nodes_b = backward_astar(maze, break_ties_smaller_g=False)

    print(
        "Backward A* path found with ties broken for larger g-values:", path_larger_g_b
    )
    print("Backward A* - number of expanded nodes", expanded_nodes_b)

    return path_larger_g_a, path_larger_g_b, expanded_nodes_a, expanded_nodes_b


def calcAAStar(maze):
    # Run Adaptive A* with ties broken in favor of larger g-values

    path_larger_g_a, expanded_nodes_a = a_star(maze, break_ties_smaller_g=False)

    print(
        "Repeated A* path found with ties broken for larger g-values:", path_larger_g_a
    )
    print("Repeated A* - number of expanded nodes", expanded_nodes_a)

    path_larger_g_d, expanded_nodes_d = adaptive_a_star(
        maze, break_ties_smaller_g=False
    )

    print(
        "Adaptive A* path found with ties broken for larger g-values:", path_larger_g_a
    )
    print("Adaptive A* - number of expanded nodes", expanded_nodes_d)

    return path_larger_g_a, path_larger_g_d, expanded_nodes_a, expanded_nodes_d


mazes = []
for i in range(0, 50):  # 50 mazes
    maze, _, _ = generateMaze(101, 101)
    mazes.append(maze)


def testAstar():  # returns mean # expanded nodes for g smaller and for g greater
    gs_sum = 0
    gg_sum = 0
    plt.rcParams.update({"axes.titlesize": "medium"})
    fig_height = 6 * len(mazes)
    fig, ax = plt.subplots(len(mazes), 2, figsize=(10, fig_height))
    for i in range(0, len(mazes)):
        gs_exp_nodes, gg_exp_nodes, path_smaller_g, path_larger_g = calcAStar(mazes[i])

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
    plt.savefig("astar.png")
    return gs_sum / len(mazes), gg_sum / len(mazes)


def testBackwardAstar():
    gg_sum_a = 0
    gg_sum_b = 0
    plt.rcParams.update({"axes.titlesize": "medium"})
    fig_height = 6 * len(mazes)
    fig, ax = plt.subplots(len(mazes), 2, figsize=(10, fig_height))
    for i in range(0, len(mazes)):
        path_larger_g_a, path_larger_g_b, expanded_nodes_a, expanded_nodes_b = (
            calcBAStar(mazes[i])
        )
        if path_larger_g_a and path_larger_g_b:
            #
            ax[i, 0].set_title("Forward A* path with ties broken for larger g-values")
            im = ax[i, 0].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_larger_g_a:
                ax[i, 0].plot(node[1], node[0], "ro")
            fig.colorbar(im, ax=ax[i, 0], orientation="vertical")

            ax[i, 1].set_title("Backward A* path with ties broken for larger g-values")
            im2 = ax[i, 1].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_larger_g_b:
                ax[i, 1].plot(node[1], node[0], "ro")
            fig.colorbar(im2, ax=ax[i, 1], orientation="vertical")

        else:
            print("No path found for at least one version of A*.")

        gg_sum_a += expanded_nodes_a
        gg_sum_b += expanded_nodes_b

    fig.tight_layout()
    plt.savefig("backward_a_star.png")
    return gg_sum_a / len(mazes), gg_sum_b / len(mazes)


def testAdaptiveAstar():
    gg_sum_a = 0
    gg_sum_d = 0
    plt.rcParams.update({"axes.titlesize": "medium"})
    fig_height = 6 * len(mazes)
    fig, ax = plt.subplots(len(mazes), 2, figsize=(10, fig_height))
    for i in range(0, len(mazes)):
        path_larger_g_a, path_larger_g_d, expanded_nodes_a, expanded_nodes_d = (
            calcAAStar(mazes[i])
        )
        if path_larger_g_a and path_larger_g_d:
            ax[i, 0].set_title("Forward A* path with ties broken for larger g-values")
            im = ax[i, 0].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_larger_g_a:
                ax[i, 0].plot(node[1], node[0], "ro")
            fig.colorbar(im, ax=ax[i, 0], orientation="vertical")

            ax[i, 1].set_title("Adaptive A* path with ties broken for larger g-values")
            im2 = ax[i, 1].imshow(mazes[i], cmap="binary", origin="lower")
            for node in path_larger_g_d:
                ax[i, 1].plot(node[1], node[0], "ro")
            fig.colorbar(im2, ax=ax[i, 1], orientation="vertical")

        else:
            print("No path found for at least one version of A*.")

        gg_sum_a += expanded_nodes_a
        gg_sum_d += expanded_nodes_d

    fig.tight_layout()
    plt.savefig("adaptive_a_star.png")
    return gg_sum_a / len(mazes), gg_sum_d / len(mazes)


if __name__ == "__main__":
    gs_avg, gg_avg = testAstar()
    print("G smaller average expanded nodes: ", gs_avg)
    print("G larger average expanded nodes: ", gg_avg)
    a_avg, b_avg = testBackwardAstar()
    print("A star average expanded nodes: ", a_avg)
    print("Backward A star average expanded nodes: ", b_avg)
    a_avg, d_avg = testAdaptiveAstar()
    print("A star average expanded nodes: ", a_avg)
    print("Adaptive A star average expanded nodes: ", d_avg)
