def generate_output_file(solver, filename: str = "output_maze.txt"):

    hex_lines = []
    for row in solver.grid:
        line = "".join(f"{cell:X}" for cell in row)
        hex_lines.append(line)

    entry_str = f"{solver.start[0]},{solver.start[1]}"
    exit_str = f"{solver.end[0]},{solver.end[1]}"

    path = solver.solve(silent=True)
    path_str = "".join(path)

    with open(filename, 'w') as f:
        for line in hex_lines:
            f.write(line + "\n")
        f.write("\n")
        f.write(entry_str + "\n")
        f.write(exit_str + "\n")
        f.write(path_str + "\n")
