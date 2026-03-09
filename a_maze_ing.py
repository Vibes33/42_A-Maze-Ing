from Algo import MazeSolver
from affichage import print_maze, entry_exit_to_coords, print_maze_path
import sys


def main(config_file: str) -> None:
    try:
        solver = MazeSolver(config_file)
        print("Maze generate successfully generated")
        print(f"-> Dimensions : {solver.width} x {solver.height}")
        print(f"-> Perfect Mode: {solver.is_perfect}")
        print(f"-> Start : {solver.start}")
        print(f"-> End : {solver.end}")

    except Exception as e:
        print(f"critical error during INIT: {e}")
        return

    # validity check
    print("\n(Check Validity)...")
    is_valid = solver.validity_checker()

    print(f"    -> Valide : {is_valid}")
    if is_valid:
        print("    -> Status : Path find ")
    else:
        print("    -> Status : Invalid Maze")

    # Maze
    print("\nMaze display:\n")
    entry, exit_pos = entry_exit_to_coords(config_file)
    entry = tuple(map(int, entry.split(",")))
    exit_pos = tuple(map(int, exit_pos.split(",")))
    print_maze(solver.grid, shuffle_colors=False, entry=entry, exit=exit_pos)
    choice = 0
    show = True
    path = solver.solve(show)

    while choice != '4':
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Exit")
        choice = input("\nChoice (1-4): ")
        if choice == '1':
            print("\nRe-generate a new maze")
            main(config_file)
        elif choice == '2':
            print("\nShow/Hide path from entry to exit")
            if show:
                show = False
                path = solver.solve(show)
                print_maze_path(solver.grid, path=path,
                                entry=entry, exit=exit_pos)
            else:
                show = True
                path = solver.solve(show)
                print_maze(solver.grid,
                           shuffle_colors=False, entry=entry, exit=exit_pos)
        elif choice == '3':
            print("\nRotate maze colors")
            print_maze(solver.grid, shuffle_colors=True,
                       entry=entry, exit=exit_pos)
        elif choice == '4':
            print("\nExit")
            sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        print("Example: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    try:
        main(sys.argv[1])
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting A-Maze-ing. Goodbye!")
        sys.exit(0)
