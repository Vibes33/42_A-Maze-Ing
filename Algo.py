import sys
from collections import deque
from generator import MazeGenerator


class MazeSolver:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, config_file: str = "config.txt"):
        self.config: dict[str, str] = self._load_config(config_file)

        try:
            self.width = int(self.config["WIDTH"])
            self.height = int(self.config["HEIGHT"])
            self.start = self._parse_coords(self.config["ENTRY"])
            self.end = self._parse_coords(self.config["EXIT"])
            self.is_perfect = self.config.get("PERFECT",
                                              "False").lower() == "true"
        except KeyError as e:
            print(f"missing key {e} in {config_file}")
            sys.exit(1)
        except ValueError as e:
            print(f"Value error({e})")
            sys.exit(1)

        self.seed = None
        if "SEED" in self.config:
            try:
                self.seed = int(self.config["SEED"])
                print(f"-> Seed : {self.seed}")
            except ValueError:
                print(f"[Config] Warning: invalid SEED "
                      f"'{self.config['SEED']}', ignored.")
                self.seed = None
        else:
            print("-> Seed : NONE (Random Maze)")

        gen = MazeGenerator(self.width, self.height)
        self.grid = gen.generate(perfect=self.is_perfect,
                                 pattern_42=True, seed=self.seed)
        self.pattern_cells = gen.pattern_cells

    def _load_config(self, filepath: str) -> dict[str, str]:
        config = {}
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()

                    if not line or line.startswith('#'):
                        continue

                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
                    else:
                        print(f"[Config] Warning: line {line_num} "
                              f"ignored (no '='): {line}")

        except FileNotFoundError:
            print(f"[Config] critical error: file '{filepath}' not found.")
            sys.exit(1)

        return config

    def _parse_coords(self, coord_str: str) -> tuple[int, int]:
        try:
            x, y = coord_str.split(',')
            return (int(x.strip()), int(y.strip()))
        except ValueError:
            print(f"coordinate format: '{coord_str}' instead of ('x,y')")
            sys.exit(1)

    def solve(self, silent: bool = False) -> list[str]:
        if not silent:
            print(f"path research {self.start} to {self.end}...")

        queue = deque([self.start])
        visited = {self.start}

        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        found = False
        while queue:
            cx, cy = queue.popleft()

            if (cx, cy) == self.end:
                found = True
                break

            cell_value = self.grid[cy][cx]

            moves = [
                (0, -1, self.NORTH, 'N'),
                (1,  0, self.EAST,  'E'),
                (0,  1, self.SOUTH, 'S'),
                (-1, 0, self.WEST,  'W')
            ]
            for dx, dy, direction, char in moves:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not (cell_value & direction) and (nx,
                                                         ny) not in visited:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = ((cx, cy), char)
                        queue.append((nx, ny))

        if not found:
            if not silent:
                print("no path found")
            return []
        path = []
        cur = self.end

        while cur != self.start:
            prev_coord, direction_char = parent[cur]
            path.append(direction_char)
            cur = prev_coord

        path.reverse()
        return path

    def validity_checker(self) -> bool:
        if self.width < 10 or self.height < 10:
            return False

        sx, sy = self.start
        ex, ey = self.end

        # need to be in grid
        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return False
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            return False

        # 1 exit one entry
        if self.start == self.end:
            return False

        # exit / entry != patern
        if self.pattern_cells:
            if self.start in self.pattern_cells:
                return False
            if self.end in self.pattern_cells:
                return False

        # one path
        shortest_path = self.solve(silent=True)
        if not shortest_path:
            return False

        # PERFECT=False
        if not self.is_perfect:
            return True

        # PERFECT=True
        if self._has_loops():
            return False

        return True

    def _has_loops(self) -> bool:
        visited = set()
        stack = [(self.start, None)]

        while stack:
            current, parent = stack.pop()

            if current in visited:
                return True
            visited.add(current)
            cx, cy = current
            cell_value = self.grid[cy][cx]

            moves = [
                (0, -1, self.NORTH), (1, 0, self.EAST),
                (0, 1, self.SOUTH), (-1, 0, self.WEST)
            ]

            for dx, dy, direction in moves:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # no walls
                    if not (cell_value & direction):
                        # not directly in parent
                        if (nx, ny) != parent:
                            stack.append(((nx, ny), current))

        return False
