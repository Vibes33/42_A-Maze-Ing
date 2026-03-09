import random
from rich import print as rprint

COLORS = [
    "green", "yellow", "blue", "magenta", "cyan"
]


def entry_exit_to_coords(filename):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("ENTRY"):
                entry = line.split("ENTRY=")[1]
            elif line.startswith("EXIT"):
                exit = line.split("EXIT=")[1]
    return entry, exit


def print_maze(grid, shuffle_colors=False, entry=None, exit=None):
    print(f"Entry: {entry}, Exit: {exit}")
    height = len(grid)
    width = len(grid[0])

    def random_color():
        if shuffle_colors:
            return random.choice(COLORS)
        else:
            return "white"

    # ligne du haut
    top_line = ""
    color = random_color()
    for x in range(width):
        top_line += f"[{color}]█[/{color}]"
        if grid[0][x] & 1:
            top_line += f"[{color}]█[/{color}]"
    top_line += f"[{color}]█[/{color}]"
    rprint(top_line)

# ligne du centre West et East
    for y in range(height):
        est_west = ""
        for x in range(width):
            cell = grid[y][x]
            if cell & 8:
                est_west += f"[{color}]█[/{color}]"
            else:
                est_west += " "
            if (x, y) == entry:
                est_west += "[green]█[/green]"
            elif (x, y) == exit:
                est_west += "[red]█[/red]"
            elif cell == 15:
                est_west += "[white]█[/white]"
            else:
                est_west += " "
        if grid[y][width - 1] & 2:
            est_west += f"[{color}]█[/{color}]"
        else:
            est_west += " "
        rprint(est_west)

# Sud
        sud = ""
        for x in range(width):
            cell = grid[y][x]
            if cell == 15:
                sud += f"[{color}]█[/{color}]"
            else:
                sud += f"[{color}]█[/{color}]"
            if cell & 4:
                sud += f"[{color}]█[/{color}]"
            else:
                sud += " "
        sud += f"[{color}]█[/{color}]"
        rprint(sud)


def print_maze_path(solver_grid, path, entry, exit):
    import copy
    grid = copy.deepcopy(solver_grid)

    x, y = entry

    for move in path:
        if move == 'N':
            y -= 1
        elif move == 'S':
            y += 1
        elif move == 'E':
            x += 1
        elif move == 'W':
            x -= 1
        grid[y][x] |= 16

    height = len(grid)
    width = len(grid[0])

    # Ligne du haut
    rprint("[white]█[/white]" * (width * 2 + 1))

    for y in range(height):
        row = ""
        for x in range(width):
            cell = grid[y][x]
            row += "[white]█[/white]" if (cell & 8) else " "
            if (x, y) == entry:
                row += "[green]█[/green]"
            elif (x, y) == exit:
                row += "[red]█[/red]"
            elif cell & 16:
                row += "[yellow]·[/yellow]"
            elif cell == 15:
                row += "[white]█[/white]"
            else:
                row += " "
        row += "[white]█[/white]" if (grid[y][width-1] & 2) else " "
        rprint(row)

        sud = ""
        for x in range(width):
            cell = grid[y][x]
            sud += "[white]█[/white]"
            sud += "[white]█[/white]" if (cell & 4) else " "
        sud += "[white]█[/white]"
        rprint(sud)
