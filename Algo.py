import sys
from collections import deque
from generator import MazeGenerator


class MazeSolver:
    NORTH = 1
    EAST  = 2
    SOUTH = 4
    WEST  = 8

    def __init__(self, config_file: str = "config.txt"):
        self.config: dict[str, str] = self._load_config(config_file)
        
        try:
            self.width = int(self.config["WIDTH"])
            self.height = int(self.config["HEIGHT"])
            self.start = self._parse_coords(self.config["ENTRY"])
            self.end = self._parse_coords(self.config["EXIT"])
            self.is_perfect = self.config.get("PERFECT", "False").lower() == "true"
        except KeyError as e:
            print(f"Erreur Configuration: Clé manquante {e} dans {config_file}")
            sys.exit(1)
        except ValueError as e:
            print(f"Erreur Configuration: Valeur invalide ({e})")
            sys.exit(1)

        gen = MazeGenerator(self.width, self.height)
        self.grid = gen.generate(perfect=self.is_perfect, pattern_42=True)
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
                        print(f"[Config] Warning: Ligne {line_num} ignorée (pas de '='): {line}")
                        
        except FileNotFoundError:
            print(f"[Config] Erreur Critique: Fichier '{filepath}' introuvable.")
            sys.exit(1)

        return config

    def _parse_coords(self, coord_str: str) -> tuple[int, int]:
        try:
            x, y = coord_str.split(',')
            return (int(x.strip()), int(y.strip()))
        except ValueError:
            print(f"Erreur format coordonnées: '{coord_str}' (attendu: 'x,y')")
            sys.exit(1)

    def solve(self, silent: bool = False) -> list[str]:
        if not silent:
            print(f"Recherche du chemin de {self.start} vers {self.end}...")
        

        queue = deque([self.start])
        visited = {self.start}
        

        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}


        found = False

        #boucle princiale 
        while queue:
            cx, cy = queue.popleft()


            if (cx, cy) == self.end:
                found = True
                break


            cell_value = self.grid[cy][cx]
            
            # mouvements possibles / directions associées
            moves = [
                (0, -1, self.NORTH, 'N'),
                (1,  0, self.EAST,  'E'),
                (0,  1, self.SOUTH, 'S'),
                (-1, 0, self.WEST,  'W')
            ]
            #On explore les voisins en fonction des murs ouverts
            for dx, dy, direction, char in moves:
                nx, ny = cx + dx, cy + dy

                #on vérifie qu'on ne sors pas de la grille 
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    #Bitwise check pour savoir si un mur est ouvert ou pas 
                    if not (cell_value & direction) and (nx, ny) not in visited:
                        visited.add((nx, ny)) #MAJ des variables de visite
                        parent[(nx, ny)] = ((cx, cy), char)
                        queue.append((nx, ny))
        

        if not found:
            if not silent:
                print("Aucun chemin trouvé.")
            return []
        #on reconstruit le chemin a partir de la fin 
        path = []
        cur = self.end

        while cur != self.start:
            prev_coord, direction_char = parent[cur]
            path.append(direction_char)
            cur = prev_coord

        path.reverse()
        return path

    def validity_checker(self) -> bool:
        # Taille suffisante pour le pattern "42" (+1 marge sécu = min 10x10)
        if self.width < 10 or self.height < 10:
            return False

        # Vérification Entrée/Sortie
        sx, sy = self.start
        ex, ey = self.end
        
        # Doivent être dans la grille
        if not (0 <= sx < self.width and 0 <= sy < self.height):
            return False
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            return False
            
        # Doivent être différentes (1 entrée, 1 sortie distinctes)
        if self.start == self.end:
            return False

        # Entrée/Sortie != pattern
        if self.pattern_cells:
            if self.start in self.pattern_cells:
                return False
            if self.end in self.pattern_cells:
                return False

        # 1. Au moins un chemin
        shortest_path = self.solve(silent=True)
        if not shortest_path:
            return False

        # 2. PERFECT=False
        if not self.is_perfect:
            return True

        # 3. PERFECT=True
        if self._has_loops():
            return False
        
        return True

    def _has_loops(self) -> bool:
        visited = set()
        stack = [(self.start, None)] # (current_node, parent_node)

        while stack:
            current, parent = stack.pop()
            
            if current in visited:
                #si on retombe sur une case visité
                return True
            
            visited.add(current)
            cx, cy = current
            cell_value = self.grid[cy][cx]

            #voisins
            moves = [
                (0, -1, self.NORTH), (1, 0, self.EAST), 
                (0, 1, self.SOUTH), (-1, 0, self.WEST)
            ]

            for dx, dy, direction in moves:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    #pas de mur
                    if not (cell_value & direction):
                        #pas immédiatement chez le parent
                        if (nx, ny) != parent:
                            stack.append(((nx, ny), current))
        
        return False


