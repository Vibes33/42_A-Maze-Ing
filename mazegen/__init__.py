"""mazegen — A reusable maze generator and solver package.

Quick start:
    from mazegen import MazeGenerator, MazeSolver

    gen = MazeGenerator(width=20, height=15)
    grid = gen.generate(perfect=True, pattern_42=True, seed=4242)

    solver = MazeSolver("config.txt")
    path = solver.solve()
"""

from .generator import MazeGenerator
from .solver import MazeSolver
from .affichage import print_maze, print_maze_path, entry_exit_to_coords
from .map2 import generate_output_file

__all__ = [
    "MazeGenerator",
    "MazeSolver",
    "print_maze",
    "print_maze_path",
    "entry_exit_to_coords",
    "generate_output_file",
]
