class PuzzleState:
    def __init__(self, board, parent=None, g=0):
        self.board = board           # état actuel du puzzle
        self.parent = parent         # parent dans l’arbre des états
        self.g = g                   # coût depuis l’état initial
        self.h = self.manhattan()    # heuristique
        self.f = self.g + self.h     # coût total estimé (A*)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def manhattan(self):
        """Calcule la distance de Manhattan pour l’état actuel"""
        n = len(self.board)
        total = 0
        for i in range(n):
            for j in range(n):
                value = self.board[i][j]
                if value != 0:  # ignorer le vide
                    # position finale (ligne, colonne)
                    goal_i, goal_j = divmod(value - 1, n)
                    total += abs(i - goal_i) + abs(j - goal_j)
        return total

    def get_neighbors(self):
        """Génère tous les états voisins en déplaçant la case vide"""
        neighbors = []
        n = len(self.board)

        # trouver la position du 0 (case vide)
        for i in range(n):
            for j in range(n):
                if self.board[i][j] == 0:
                    x, y = i, j

        directions = [(-1,0),(1,0),(0,-1),(0,1)]  # haut, bas, gauche, droite
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                # copier le board pour ne pas modifier l’original
                new_board = [row[:] for row in self.board]
                # échanger la case vide avec la case cible
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                # créer le nouvel état et l’ajouter aux voisins
                neighbors.append(PuzzleState(new_board, parent=self, g=self.g + 1))

        return neighbors

    def print_board(self):
        """Affiche joliment le board (optionnel)"""
        for row in self.board:
            print(" ".join(str(x) for x in row))
        print()