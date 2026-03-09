class PuzzleState:
    def __init__(self, tiles, size, goal_pos, parent=None, g=0, heuristic_fn=None):
        self.tiles = tiles
        self.size = size
        self.parent = parent
        self.g = g
        self.h = heuristic_fn(self, goal_pos) if heuristic_fn else 0
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
        return hash(self.tiles)

    def __lt__(self, other):
        return self.f < other.f

    def get_neighbors(self, goal_pos, heuristic_fn):
        neighbors = []
        zero_idx = self.tiles.index(0)
        x, y = divmod(zero_idx, self.size)

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                swap_idx = nx * self.size + ny
                new_tiles = list(self.tiles)
                new_tiles[zero_idx], new_tiles[swap_idx] = new_tiles[swap_idx], new_tiles[zero_idx]
                neighbors.append(PuzzleState(
                    tuple(new_tiles), self.size, goal_pos,
                    parent=self, g=self.g + 1,
                    heuristic_fn=heuristic_fn
                ))
        return neighbors

    def print_board(self):
        for i in range(self.size):
            print(" ".join(str(x) for x in self.tiles[i*self.size:(i+1)*self.size]))
        print()

    def reconstruct_path(self):
        path = []
        state = self
        while state:
            path.append(state)
            state = state.parent
        path.reverse()
        return path