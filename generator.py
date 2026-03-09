import random
from typing import List, Tuple, Set


class MazeGenerator:
    """Standalone maze generator using Recursive Backtracker (DFS).

    Generates a 2D grid where each cell is a bitmask representing walls:
        NORTH=1, EAST=2, SOUTH=4, WEST=8 (15 = all walls closed).

    Usage:
        gen = MazeGenerator(width=20, height=15)
        grid = gen.generate(perfect=True, pattern_42=True)
        # grid[y][x] -> int bitmask of cell walls
        # gen.pattern_cells -> set of (x,y) tuples for the '42' pattern

    Parameters:
        width (int): Number of columns.
        height (int): Number of rows.
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    OPPOSITE = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST:  WEST,
        WEST:  EAST
    }

    def __init__(self, width: int, height: int):
        """Initialize the generator with given dimensions.

        Args:
            width: Maze width in cells (min 10 for pattern_42).
            height: Maze height in cells (min 10 for pattern_42).
        """
        self.width = width
        self.height = height
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def generate(self, perfect: bool = True,
                 pattern_42: bool = False) -> List[List[int]]:
        """Generate a maze and return the 2D grid.

        Args:
            perfect: If True, generates a perfect maze (unique path,
                     no loops). If False, ~5%% of extra walls are removed.
            pattern_42: If True, carves a '42' pattern at the center.

        Returns:
            A 2D list of ints (grid[y][x]) where each int is a wall bitmask.
        """
        self.grid = [[15 for _ in range(self.width)]
                     for _ in range(self.height)]
        self.pattern_cells = set()
        if pattern_42:
            self._apply_pattern_42()
        start_x, start_y = 0, 0
        while (start_x, start_y) in self.pattern_cells:
            stack = [(start_x, start_y)]
            visited = set()
            visited.add((start_x, start_y))
            visited.update(self.pattern_cells)
        while stack:
            cx, cy = stack[-1]
            neighbors = []

            potential_moves = [
                (0, -1, self.NORTH),
                (1,  0, self.EAST),
                (0,  1, self.SOUTH),
                (-1, 0, self.WEST)
            ]

            for dx, dy, direction in potential_moves:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = random.choice(neighbors)
                self.grid[cy][cx] &= ~direction
                self.grid[ny][nx] &= ~self.OPPOSITE[direction]

                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        if not perfect:
            self._make_imperfect()

        return self.grid

    def _apply_pattern_42(self):
        if self.width < 10 or self.height < 10:
            print("[Grille trop petite pour le pattern 42 "
                  "(min 10x10). Ignoré.")
            return

        pattern = [
            # 4
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 2), (2, 3), (2, 4),

            # 2
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2

        for dx, dy in pattern:
            px, py = offset_x + dx, offset_y + dy
            if 0 <= px < self.width and 0 <= py < self.height:
                self.pattern_cells.add((px, py))
                self.grid[py][px] = 15

    def _make_imperfect(self):
        """Casse des murs aléatoirement pour créer des boucles"""
        limit = int((self.width * self.height) * 0.05)
        count = 0

        while count < limit:
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)

            direction = random.choice([self.NORTH, self.EAST,
                                       self.SOUTH, self.WEST])

            dx, dy = 0, 0
            if direction == self.NORTH:
                dy = -1
            elif direction == self.EAST:
                dx = 1
            elif direction == self.SOUTH:
                dy = 1
            elif direction == self.WEST:
                dx = -1

            nx, ny = rx + dx, ry + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (self.grid[ry][rx] & direction) != 0:
                    self.grid[ry][rx] &= ~direction
                    self.grid[ny][nx] &= ~self.OPPOSITE[direction]
                    count += 1
