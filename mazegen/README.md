# 🏰 A-Maze-Ing

A maze generator and solver written in Python. Generates mazes with a "42" pattern carved at the center, solves them using BFS, and displays them in the terminal with color support.

---

## 📁 Project Structure

```
├── mazegen/                  # Reusable pip-installable package
│   ├── __init__.py           # Package exports
│   ├── generator.py          # MazeGenerator class (DFS recursive backtracker)
│   ├── solver.py             # MazeSolver class (BFS solver + validity checker)
│   ├── affichage.py          # Terminal display functions (rich colors)
│   └── map2.py               # Output file generator (hex grid + solution)
├── a_maze_ing.py             # Main entry point — interactive CLI menu
├── pyproject.toml            # Package build configuration
├── config.txt                # Maze configuration file
├── Makefile                  # Build automation
└── README.md
```

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

## 📦 Building the `mazegen` package

### Build from source
```bash
python3 -m pip install --upgrade build
python3 -m build
```
This generates `dist/mazegen-1.0.0-py3-none-any.whl` and `dist/mazegen-1.0.0.tar.gz`.

Or simply:
```bash
make build
```

### Install the package
```bash
pip install dist/mazegen-1.0.0-py3-none-any.whl
```
Or:
```bash
make install-pkg
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

## 🔧 Using `mazegen` as a reusable module

`mazegen` is a pip-installable package that can be imported in any Python project.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage — Generate a maze

```python
from mazegen import MazeGenerator

# Instantiate with width and height
gen = MazeGenerator(width=20, height=15)

# Generate a perfect maze (no loops) with the "42" pattern
grid = gen.generate(perfect=True, pattern_42=True)
```

### Custom parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `width` | `int` | — | Maze width in cells (min 10 for pattern_42) |
| `height` | `int` | — | Maze height in cells (min 10 for pattern_42) |
| `perfect` | `bool` | `True` | `True` = unique path (no loops), `False` = multiple paths |
| `pattern_42` | `bool` | `False` | Carve the "42" pattern at the center of the maze |
| `seed` | `int` | `None` | Seed for reproducible generation |

### Accessing the generated structure

```python
from mazegen import MazeGenerator

gen = MazeGenerator(20, 15)
grid = gen.generate(perfect=True, pattern_42=True, seed=4242)

# grid is a 2D list of ints (bitmask: N=1, E=2, S=4, W=8)
# 15 = all walls closed, 0 = all walls open
print(grid[0][0])  # Cell value at (0,0)

# Access pattern cells (set of (x,y) tuples)
print(gen.pattern_cells)
```

### Accessing a solution

```python
from mazegen import MazeSolver

solver = MazeSolver("config.txt")
path = solver.solve()  # Returns list of directions: ['S', 'E', 'E', 'S', ...]
print("".join(path))   # e.g. "SEESSWWSSE..."
```

### Full example

```python
from mazegen import MazeGenerator, MazeSolver

# 1. Generate
gen = MazeGenerator(width=20, height=15)
grid = gen.generate(perfect=False, pattern_42=True, seed=42)

# 2. Solve (via config file)
solver = MazeSolver("config.txt")
path = solver.solve(silent=True)
print(f"Solution: {''.join(path)}")
print(f"Path length: {len(path)} steps")

# 3. Check validity
is_valid = solver.validity_checker()
print(f"Maze valid: {is_valid}")
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
