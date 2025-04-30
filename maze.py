from draw import Line, Point
import time
import random

class Cell():
    lines = []

    def __init__(self, x1, y1, x2, y2, window=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._window = window
        self._visited = False
        # left right top bottom
        self.walls = [True, True, True, True]

    def draw(self):
        if self._window is None:
            return
        if self.walls[0]:
            self._window.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)))
        else:
            self._window.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), fill_color="white")
        if self.walls[1]:
            self._window.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)))
        else:
            self._window.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), fill_color="white")
        if self.walls[2]:
            self._window.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)))
        else:
            self._window.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), fill_color="white")
        if self.walls[3]:
            self._window.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)))
        else:
            self._window.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), fill_color="white")

    def draw_move(self, move_to, undo=False):
        if self._window is None:
            return
        half = abs(self._x1 - self._x2) // 2
        line_x = self._x1 + half
        line_y = self._y1 + half
        half_to = abs(move_to._x1 - move_to._x2) // 2
        move_to_x = move_to._x1 + half_to
        move_to_y = move_to._y1 + half_to
        color = "red" if undo else "gray"
        line = Line(Point(line_x, line_y), Point(move_to_x, move_to_y))
        Cell.lines.append(line)
        self._window.draw_line(line, fill_color=color)

class Maze():
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, window=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._window = window
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        cells = []
        for i in range(self._num_rows):
            row = []
            for j in range(self._num_cols):
                x1 = self._x1 + j * self._cell_size_x
                y1 = self._y1 + i * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cell = Cell(x1, y1, x2, y2, self._window)
                cell.draw()
                row.append(cell)
            cells.append(row)
        self._cells = cells

    def _animate(self):
        if self._window is None:
            return
        self._window.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        if len(self._cells) == 0 or len(self._cells[0]) == 0:
            return
        top_left = self._cells[0][0]
        top_left.walls[2] = False
        bottom_right = self._cells[-1][-1]
        bottom_right.walls[3] = False
        top_left.draw()
        bottom_right.draw()

    def _break_walls_r(self, i, j):
        if i < 0 or i >= self._num_rows or j < 0 or j >= self._num_cols:
            return
        cell = self._cells[i][j]
        cell._visited = True
        while True:
            to_visit = []
            left = self._cells[i][j - 1] if j > 0 else None
            right = self._cells[i][j + 1] if j < self._num_cols - 1 else None
            up = self._cells[i - 1][j] if i > 0 else None
            down = self._cells[i + 1][j] if i < self._num_rows - 1 else None
            adjacent = [left, right, up, down]
            for adj in adjacent:
                if adj is not None and not adj._visited:
                    to_visit.append(adj)
            if len(to_visit) == 0:
                cell.draw()
                return
            next = random.choice(to_visit)
            if next == left:
                cell.walls[0] = False
                next.walls[1] = False
                self._break_walls_r(i, j - 1)
            elif next == right:
                cell.walls[1] = False
                next.walls[0] = False
                self._break_walls_r(i, j + 1)
            elif next == up:
                cell.walls[2] = False
                next.walls[3] = False
                self._break_walls_r(i - 1, j)
            elif next == down:
                cell.walls[3] = False
                next.walls[2] = False
                self._break_walls_r(i + 1, j)
            cell.draw()
            next.draw()

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def solve(self, method="dfs"):
        if method == "dfs":
            start = time.perf_counter()
            self._solve_dfs_r(0, 0)
            stop = time.perf_counter()
            print(f"DFS took {stop - start:.2f} seconds")
        elif method == "bfs":
            start = time.perf_counter()
            self._solve_bfs()
            stop = time.perf_counter()
            print(f"BFS took {stop - start:.2f} seconds")
        elif method == "astar":
            start = time.perf_counter()
            self._solve_a_star()
            stop = time.perf_counter()
            print(f"A* took {stop - start:.2f} seconds")

    def _solve_dfs_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell._visited = True
        if cell == self._cells[-1][-1]:
            return True
        adjacent = []
        left = self._cells[i][j - 1] if j > 0 else None
        right = self._cells[i][j + 1] if j < self._num_cols - 1 else None
        up = self._cells[i - 1][j] if i > 0 else None
        down = self._cells[i + 1][j] if i < self._num_rows - 1 else None
        if down is not None and not down._visited and not cell.walls[3]:
            adjacent.append((i + 1, j))
        if right is not None and not right._visited and not cell.walls[1]:
            adjacent.append((i, j + 1))
        if left is not None and not left._visited and not cell.walls[0]:
            adjacent.append((i, j - 1))
        if up is not None and not up._visited and not cell.walls[2]:
            adjacent.append((i - 1, j))
        if len(adjacent) == 0:
            return False
        for next in adjacent:
            cell.draw_move(self._cells[next[0]][next[1]])
            if self._solve_dfs_r(next[0], next[1]):
                return True
            cell.draw_move(self._cells[next[0]][next[1]], undo=True)
        return False
    
    def _solve_bfs(self):
        q = []
        cell = self._cells[0][0]
        cell._visited = True
        q.append((0, 0))
        while len(q) > 0:
            self._animate()
            ind = q.pop(0)
            i, j = ind[0], ind[1]
            cell = self._cells[i][j]
            cell._visited = True
            if cell == self._cells[-1][-1]:
                return True
            adjacent = []
            left = self._cells[i][j - 1] if j > 0 else None
            right = self._cells[i][j + 1] if j < self._num_cols - 1 else None
            up = self._cells[i - 1][j] if i > 0 else None
            down = self._cells[i + 1][j] if i < self._num_rows - 1 else None
            if down is not None and not down._visited and down not in q and not cell.walls[3]:
                adjacent.append((i + 1, j))
            if right is not None and not right._visited and right not in q and not cell.walls[1]:
                adjacent.append((i, j + 1))
            if left is not None and not left._visited and left not in q and not cell.walls[0]:
                adjacent.append((i, j - 1))
            if up is not None and not up._visited and left not in q and not cell.walls[2]:
                adjacent.append((i - 1, j))
            if len(adjacent) == 0:
                continue
            for next in adjacent:
                cell.draw_move(self._cells[next[0]][next[1]])
                q.append(next)
        return False
    
    def _solve_a_star(self):
        q = []
        cell = self._cells[0][0]
        cell._visited = True
        cell_h = abs(self._cells[-1][-1]._x1 - cell._x1) + abs(self._cells[-1][-1]._y1 - cell._y1)
        q.append((0, 0, 0, cell_h, None))
        while len(q) > 0:
            self._animate()
            q.sort(key=lambda x: x[2] + x[3])
            ind = q.pop(0)
            i, j = ind[0], ind[1]
            cell = self._cells[i][j]
            cell._visited = True
            if cell == self._cells[-1][-1]:
                return True
            if ind[4] is not None:
                cell.draw_move(ind[4])
            adjacent = []
            left = self._cells[i][j - 1] if j > 0 else None
            right = self._cells[i][j + 1] if j < self._num_cols - 1 else None
            up = self._cells[i - 1][j] if i > 0 else None
            down = self._cells[i + 1][j] if i < self._num_rows - 1 else None
            if down is not None and not down._visited and down not in q and not cell.walls[3]:
                adjacent.append((i + 1, j))
            if right is not None and not right._visited and right not in q and not cell.walls[1]:
                adjacent.append((i, j + 1))
            if left is not None and not left._visited and left not in q and not cell.walls[0]:
                adjacent.append((i, j - 1))
            if up is not None and not up._visited and left not in q and not cell.walls[2]:
                adjacent.append((i - 1, j))
            if len(adjacent) == 0:
                continue
            for next in adjacent:
                g = ind[2] + 1
                h = abs(self._cells[-1][-1]._x1 - self._cells[next[0]][next[1]]._x1) + abs(self._cells[-1][-1]._y1 - self._cells[next[0]][next[1]]._y1)
                q.append((next[0], next[1], g, h, cell))
        return False

    
    def reset(self):
        self._reset_cells_visited()
        for line in Cell.lines:
            self._window.draw_line(line, fill_color="white")
            
        
        
# know AWS, kubernetes, containers

        