import random
from typing import List, Tuple, Set

class MazeGenerator:
    # Constantes Bitmask
    NORTH = 1
    EAST  = 2
    SOUTH = 4
    WEST  = 8

    # Table de correspondance pour ouvrir le mur opposé
    OPPOSITE = {
        NORTH: SOUTH,
        SOUTH: NORTH,
        EAST:  WEST,
        WEST:  EAST
    }

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # On initialise tout à 15
        self.grid = [[15 for _ in range(width)] for _ in range(height)]
        self.pattern_cells: Set[Tuple[int, int]] = set()

    def generate(self, perfect: bool = True, pattern_42: bool = False) -> List[List[int]]:
        # 1. Réinitialisation
        self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]

        # 2. Gestion du Motif "42"
        self.pattern_cells = set()
        if pattern_42:
            self._apply_pattern_42()

        # 3. Initialisation du DFS
        start_x, start_y = 0, 0
        while (start_x, start_y) in self.pattern_cells:
             start_x += 1 # On cherche un coin libre basique

        stack = [(start_x, start_y)]
        visited = set()
        visited.add((start_x, start_y))

        # On ajoute les cases du pattern à 'visited'
        visited.update(self.pattern_cells)

        # 4. Boucle Principale (Recursive Backtracker)
        while stack:
            cx, cy = stack[-1] # On regarde le sommet de la pile (Current)

            # Recherche des voisins valides (Dans la grille + Pas visités)
            # Tuple: (nx, ny, direction)
            neighbors = []

            potential_moves = [
                (0, -1, self.NORTH),
                (1,  0, self.EAST),
                (0,  1, self.SOUTH),
                (-1, 0, self.WEST)
            ]

            for dx, dy, direction in potential_moves:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, direction))

            if neighbors:
                #Si on a des voisins, on en choisit un au hasard
                nx, ny, direction = random.choice(neighbors)

                # On casse les murs
                # On enlève le bit 'direction' de la case courante
                self.grid[cy][cx] &= ~direction
                # On enlève le bit 'opposé' de la case voisine
                self.grid[ny][nx] &= ~self.OPPOSITE[direction]

                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                #Cul-de-sac : On backtrack (revient en arrière)
                stack.pop()

        # 7. Si imparfait, on casse quelques murs supplémentaires
        if not perfect:
            self._make_imperfect()

        return self.grid

    def _apply_pattern_42(self):
        if self.width < 10 or self.height < 10:
            print("[Grille trop petite pour le pattern 42 (min 10x10). Ignoré.")
            return

        # Motif 42 (coordonnées relatives x,y).
        # Zone de 7 de large (0..6) et 5 de haut (0..4)
        pattern = [
            # 4
            (0,0), (0,1), (0,2),        # Barre gauche haut
            (1,2),                       # Barre milieu
            (2,0), (2,1), (2,2), (2,3), (2,4), # Barre droite toute hauteur

            # Espace colonne 3 vide

            # 2
            (4,0), (5,0), (6,0),        # Haut
            (6,1),                       # Droite haut
            (4,2), (5,2), (6,2),        # Milieu
            (4,3),                       # Gauche bas
            (4,4), (5,4), (6,4)         # Bas
        ]

        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2

        for dx, dy in pattern:
            px, py = offset_x + dx, offset_y + dy
            if 0 <= px < self.width and 0 <= py < self.height:
                self.pattern_cells.add((px, py))
                self.grid[py][px] = 15 # Mur plein

    def _make_imperfect(self):
        """Casse des murs aléatoirement pour créer des boucles"""
        # On casse environ 5% du nombre total de cases
        limit = int((self.width * self.height) * 0.05)
        count = 0
  
        while count < limit:
            rx = random.randint(0, self.width - 1)
            ry = random.randint(0, self.height - 1)

            # On choisit un mur au pif (N, E, S, W)
            direction = random.choice([self.NORTH, self.EAST, self.SOUTH, self.WEST])
            
            dx, dy = 0, 0
            if direction == self.NORTH: dy = -1
            elif direction == self.EAST: dx = 1
            elif direction == self.SOUTH: dy = 1
            elif direction == self.WEST: dx = -1
            
            nx, ny = rx + dx, ry + dy
            
            # Si le voisin est dans la grille
            if 0 <= nx < self.width and 0 <= ny < self.height:
                # Et que le mur existe encore (Bitmask & Direction != 0)
                if (self.grid[ry][rx] & direction) != 0:
                    # On casse
                    self.grid[ry][rx] &= ~direction
                    self.grid[ny][nx] &= ~self.OPPOSITE[direction]
                    count += 1
