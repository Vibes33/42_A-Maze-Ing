# 🏰 A-Maze-Ing

A maze generator and solver written in Python. Generates mazes with a "42" pattern carved at the center, solves them using BFS, and displays them in the terminal with color support.

---

## 📁 Project Structure

| File | Description |
|---|---|
| `a_maze_ing.py` | Main entry point — interactive CLI menu |
| `generator.py` | `MazeGenerator` class — standalone maze generation module |
| `Algo.py` | `MazeSolver` class — BFS solver + validity checker |
| `affichage.py` | Terminal display functions (uses `rich` for colors) |
| `map2.py` | Output file generator (hex grid + solution) |
| `config.txt` | Configuration file (dimensions, entry, exit, mode) |
| `Makefile` | Build automation (install, run, debug, clean, lint) |

---

## 🚀 Quick Start

### Install dependencies
```bash
make install
```

### Run the program
```bash
make run
```
Or manually:
```bash
python3 a_maze_ing.py config.txt
```

### Debug mode (pdb)
```bash
make debug
```

### Clean caches
```bash
make clean
```

### Lint
```bash
make lint          # flake8 + mypy
make lint-strict   # flake8 + mypy --strict
```

---

## ⚙️ Configuration (`config.txt`)

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
PERFECT=True
```

| Key | Description |
|---|---|
| `WIDTH` | Maze width (min 10) |
| `HEIGHT` | Maze height (min 10) |
| `ENTRY` | Start coordinates `x,y` |
| `EXIT` | End coordinates `x,y` |
| `PERFECT` | `True` = no loops (unique path), `False` = loops allowed |

---

## 🔧 Using `MazeGenerator` as a standalone module

`MazeGenerator` is a self-contained class in `generator.py` that can be imported in any project.

### Basic usage

```python
from generator import MazeGenerator

# Instantiate with width and height
gen = MazeGenerator(width=20, height=15)

# Generate a perfect maze (no loops) with the "42" pattern
grid = gen.generate(perfect=True, pattern_42=True)
```

### Custom parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Maze width in cells |
| `height` | `int` | — | Maze height in cells |
| `perfect` | `bool` | `True` | `True` = unique path (no loops), `False` = multiple paths |
| `pattern_42` | `bool` | `False` | Carve the "42" pattern at the center of the maze |

### Accessing the generated structure

```python
gen = MazeGenerator(20, 15)
grid = gen.generate(perfect=True, pattern_42=True)

# grid is a 2D list of ints (bitmask: N=1, E=2, S=4, W=8)
# 15 = all walls closed, 0 = all walls open
print(grid[0][0])  # Cell value at (0,0)

# Access pattern cells (set of (x,y) tuples)
print(gen.pattern_cells)
```

### Accessing a solution

```python
from generator import MazeGenerator
from Algo import MazeSolver

solver = MazeSolver("config.txt")
path = solver.solve()  # Returns list of directions: ['S', 'E', 'E', 'S', ...]
print("".join(path))   # e.g. "SEESSWWSSE..."
```

---

## 🧠 How it works

1. **Generation** — Uses Recursive Backtracker (DFS) to carve a perfect maze. The "42" pattern is reserved as walls before generation starts.
2. **Imperfect mode** — If `PERFECT=False`, ~5% of walls are randomly removed to create loops.
3. **Solving** — BFS (Breadth-First Search) finds the shortest path from entry to exit.
4. **Validation** — Checks grid size, entry/exit positions, path existence, and loop detection (for perfect mode).
5. **Display** — Terminal rendering with `rich` for colored output (entry=green, exit=red, path=yellow).

---

## 📦 Dependencies

- Python 3.10+
- [rich](https://github.com/Textualize/rich) — Terminal colors
- [flake8](https://flake8.pycqa.org/) — Linting (dev)
- [mypy](https://mypy-lang.org/) — Type checking (dev)
