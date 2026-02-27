from Algo import MazeSolver
from affichage import print_maze, entry_exit_to_coords, print_maze_path
import sys


def main():
    try:
        solver = MazeSolver()
        print("Labyrinthe généré et chargé avec succès.")
        print(f"-> Dimensions : {solver.width} x {solver.height}")
        print(f"-> Mode Perfect : {solver.is_perfect}")
        print(f"-> Départ : {solver.start}")
        print(f"-> Arrivée : {solver.end}")

    except Exception as e:
        print(f"Erreur critique lors de l'init : {e}")
        return

    # Vérification de la validité
    print("\nVérification de la validité (Check Validity)...")
    is_valid = solver.validity_checker()

    print(f"    -> Valide : {is_valid}")
    if is_valid:
        print("    -> Status : Chemin trouvé (+ Unicité respectée si demandé).")
    else:
        print("    -> Status : Labyrinthe invalide.")

    # Affichage terminal du labyrinthe
    print("\nAffichage terminal du labyrinthe :\n")
    entry, exit = entry_exit_to_coords("config.txt")
    entry = tuple(map(int, entry.split(",")))
    exit = tuple(map(int, exit.split(",")))
    print_maze(solver.grid, shuffle_colors=False, entry=entry, exit=exit)
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
            main()
        elif choice == '2':
            print("\nShow/Hide path from entry to exit")
            print(show)
            if show:
                show = False
                path = solver.solve(show)
                print_maze_path(solver.grid, path=path, entry=entry, exit=exit)
            elif not show:
                show = True
                path = solver.solve(show)
                print_maze(solver.grid,
                           shuffle_colors=False, entry=entry, exit=exit)
        elif choice == '3':
            print("\nRotate maze colors")
            print_maze(solver.grid, shuffle_colors=True,
                       entry=entry, exit=exit)
            if not show:
                show = True
            elif show:
                show = True
        elif choice == '4':
            print("\nExit")
            sys.exit(0)


if __name__ == "__main__":
    main()
