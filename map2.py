def generate_output_file(solver, filename: str = "output_maze.txt"):

    # 1. Grille hex avec sauts de ligne par rangée
    hex_lines = []
    for row in solver.grid:
        line = "".join(f"{cell:X}" for cell in row)
        hex_lines.append(line)

    # 2. Entrée / Sortie
    entry_str = f"{solver.start[0]},{solver.start[1]}"
    exit_str = f"{solver.end[0]},{solver.end[1]}"

    # 3. Solution
    path = solver.solve(silent=True)
    path_str = "".join(path)

    # 4. Écriture du fichier
    with open(filename, 'w') as f:
        for line in hex_lines:
            f.write(line + "\n")
        f.write("\n")
        f.write(entry_str + "\n")
        f.write(exit_str + "\n")
        f.write(path_str + "\n")


