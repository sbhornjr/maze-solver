from window import Window
from draw import Line, Point
from maze import Cell, Maze
import sys

def main():
    method = "comp"
    num_rows = 20
    num_cols = 20
    if len(sys.argv) > 1:
        method = sys.argv[1]
    if len(sys.argv) > 3:
        num_rows = int(sys.argv[2])
        num_cols = int(sys.argv[3])
    window = Window(num_cols * 20 + 20, num_rows * 20 + 20)
    maze = Maze(10, 10, num_rows, num_cols, 20, 20, window)
    if method == "comp":
        maze.solve(method="dfs")
        maze.reset()
        maze.solve(method="bfs")
        maze.reset()
        maze.solve(method="astar")
    else:
        maze.solve(method=method)
    window.wait_for_close()

main()